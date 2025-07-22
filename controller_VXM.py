import serial
import time
from connection import ser

def zero_to(ser):
    """Zero the stage position."""
    try:
        resp_x = send_command(ser, 'I1M-0', clear_first=True)  # Send motor 1 to negative limit
        resp_y = send_command(ser, 'I2M0', clear_first=True)  # Send motor 2 to positive limit

        print('Moving to Limit')

        time.sleep(1)

        ser.write(b'N\r') #Erase Position
        print("Erased position")
        time.sleep(1)

        ser.write(b'Q\r') #Turn motor offline
        print("Turned motors offline")
        time.sleep(1)

        ser.write(b'F\r') #Turn motor online
        print("Turned motors online")
        time.sleep(1)


        resp_x = send_command(ser, 'IA1M13016')  # Zero motor 1
        resp_y = send_command(ser, 'IA2M13016')  # Zero motor 2

        time.sleep(1)

        print(f"Zeroed motor 1: {resp_x}")
        print(f"Zeroed motor 2: {resp_y}")

        ser.write(b'N') #Erase Position
        print("Erased position")
        time.sleep(1)
        
        ser.write(b'Q\r') #Turn motor offline
        print("Turned motors offline")
        time.sleep(1)

        ser.write(b'F\r') #Turn motor online
        print("Turned motors online")
        time.sleep(1)

        ser.write(b'C\r') #Clear queued commands
        print('Cleared Commands')
        time.sleep(1)

        print("ZEROING COMPLETE...Stage should be at (0,0)")

    except serial.SerialException as e:
        print(f"Serial error during zeroing: {e}")

    

def send_command(ser, cmd): 
    """Send a command to the serial port and return the response."""
    try:
        ser.write(b'F')  # Ensure online mode
        time.sleep(0.05)
        ser.write(b'C')   # Clear queued commands
        time.sleep(0.05)
        ser.write(b'R')
        time.sleep(0.05)
        ser.reset_input_buffer()
        full_cmd = cmd + '\r'
        ser.write(full_cmd.encode())
        time.sleep(0.05)

        if cmd.startswith('I'): #if indexing motor always R
            ser.write(b'R')
            time.sleep(0.05)
        
        response = b""
        timeout = time.time() + 15 # 15 seconds timeout
        while b'^' not in response and time.time() < timeout:
            response += ser.read(1)
        
        if time.time() >= timeout:
            print("Warning: Command response timeout. Assuming motor is stuck.")
            motor_stuck()

        if b'^' not in response:
            print("Warning: Did not receive expected termination character '^'.")

        return response.decode(errors='ignore').strip()
    
    except serial.SerialException as e:
        print(f"Serial error: {e}")
        return None
    
def convert_mm_to_steps(mm, steps_per_mm=400):
    """Convert millimeters to motor steps."""
    try: 
        x = int(mm * steps_per_mm)
        return x
    except ValueError: 
        print("Invalid input for convertmm_to_stpes: mm must be an integer")

def convert_steps_to_mm(steps, steps_per_mm=400):
    """Convert motor steps to millimeters."""
    try: 
        return int(steps / steps_per_mm)
    except ValueError: 
        print(f"Invalid input for convert_steps_to_mm: steps must be an integer divisable by {steps_per_mm}")

def move_to(ser, x_mm, y_mm):
    """Move stage to absolute position given in centimeters."""
    try:
        x_steps = convert_mm_to_steps(int(x_mm))
        y_steps = convert_mm_to_steps(int(y_mm))

        cmd_x = f'IA1M{x_steps}'  # Absolute move motor 1 (X)
        if y_steps >= 0:
            cmd_y = f'IA2M-{y_steps}' # Absolute move motor 2 (Y) negative for upward
        else:
            cmd_y = f'IA2M{abs(y_steps)}' # Absolute move motor 2 (Y) positive for downward

        resp_x = send_command(ser, cmd_x)
        time.sleep(1)  # Small delay between commands
        resp_y = send_command(ser, cmd_y)
        time.sleep(0.5)  # Optional wait after commands

        print(f"Sent: {cmd_x}, Response: {resp_x}")
        print(f"Sent: {cmd_y}, Response: {resp_y}")
    
    except ValueError: 
        print("Invalid input for move_to: x_mm and y_mm must be integers.")
        
    except Exception as e:
        print(f"Error in move_to: {e}")
        
def rel_move_to(ser, x_mm, y_mm):
    """Move stage relative to current position given in centimeters."""
    try:
        x_steps = convert_mm_to_steps(int(x_mm))
        y_steps = convert_mm_to_steps(int(y_mm)) 

        cmd_x = f'I1M{x_steps}'  # Relative move motor 1 (X)
        if y_steps >= 0: #flip y direction because motor is inverted
            cmd_y = f'IA2M-{y_steps}'
        else:
            cmd_y = f'IA2M{abs(y_steps)}'

        resp_x = send_command(ser, cmd_x)
        time.sleep(1)  # Small delay between commands
        resp_y = send_command(ser, cmd_y)
        time.sleep(0.5)  # Optional wait after commands
        
        print(f"Sent: {cmd_x}, Response: {resp_x}")
        print(f"Sent: {cmd_y}, Response: {resp_y}")
    
    except ValueError:
        print("Invalid input for rel_move_to: x_mm and y_mm must be integers.")
    except Exception as e:
        print(f"Error in rel_move_to: {e}")

def move_home(ser):
    """Home the stage."""
    try:
        resp_x = send_command(ser, 'IA1M0')  # Home motor 1 (X)
        time.sleep(1)  # Small delay between commands
        resp_y = send_command(ser, 'IA2M0')  # Home motor 2 (Y)

        print(f"Sent: IA1M0, Response: {resp_x}")
        print(f"Sent: IA2M0, Response: {resp_y}")

    except Exception as e:
        print(f"Error in move_home: {e}")
        return None, None
    
def motor_stuck():
    '''Motor is stuck: Stop all motion and clear queue '''
    print("Motor appears to be stuck. Stopping all motion and clearing command queue.")
    try:
        ser.write(b'K\r')  # Kill any current motion
        time.sleep(0.5)
        ser.write(b'C\r')  # Clear queued commands
        time.sleep(2)
        ser.write(b'IA1M-0\r') #Move Stage to Negative limit
        zero_to(ser)
    except serial.SerialException as e:
        print(f"Serial error while handling stuck motor: {e}")

def find_range(ser):
    print("Finding range...")

    ser.write(b'K\r')  # Kill any current motion
    time.sleep(0.5)
    send_command(ser, 'C')   # clear queue

    send_command(ser, 'I1M-0', clear_first=True)  # home X
    time.sleep(5)
    xres_min = convert_steps_to_mm(get_position_x(ser))

    send_command(ser, 'I1M0', clear_first=True)   # move to positive X
    time.sleep(5)
    xres_max = convert_steps_to_mm(get_position_x(ser))

    send_command(ser, 'I2M-0', clear_first=True)  # home Y
    time.sleep(5)
    yres_max = convert_steps_to_mm(get_position_y(ser))

    send_command(ser, 'I2M0', clear_first=True)   # move to positive Y
    time.sleep(5)
    yres_min = convert_steps_to_mm(get_position_y(ser))

    print(f"Range of X: {xres_min}, {xres_max}")
    print(f"Range of Y: {-1 * yres_min}, {-1 * yres_max}")

    move_home(ser)  # Return to home position

    return xres_min, xres_max, yres_min, yres_max


def get_position_x(ser):
    ser.write(b'X\r')
    time.sleep(0.05)
    response = ser.read_until(b'\r').decode().strip()
    try:
        return int(response)
    except ValueError:
        print(f"Failed to parse X position: {repr(response)}")
        return None

def get_position_y(ser):
    ser.write(b'Y\r')
    time.sleep(0.05)
    response = ser.read_until(b'\r').decode().strip()
    try:
        return int(response)
    except ValueError:
        print(f"Failed to parse Y position: {repr(response)}")
        return None
    
if __name__ == "__main__":
    # Example usage
    if ser is None:
        print("Serial port not connected.")
    else:
        print("Homing stage...")
        move_home(ser)
        print("Moving to (2, 3)...")
        move_to(ser, 2, 3)
        print("Moving relative by (-1, -1)...")
        rel_move_to(ser, -1, -1)
        print("Done.")