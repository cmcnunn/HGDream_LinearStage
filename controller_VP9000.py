import serial
import time
from connection import ser

def zero_to(ser):
    """Zero the stage position."""
    try:
        print("Zeroing stage...")

        resp_x = send_command(ser, 'I1M-0', clear_first=True)  # Zero motor 1
        resp_y = send_command(ser, 'I2M0', clear_first=True)  # Zero motor 2

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

        resp_x = send_command(ser, 'IA1M13016')  # Set motor 1 to center position
        resp_y = send_command(ser, 'IA2M-13016')  # Set motor 2 to center position

        time.sleep(1)
    
        ser.write(b'R\r') #Run
        time.sleep(1)

        print(f"Zeroed motor 1: {resp_x}")
        print(f"Zeroed motor 2: {resp_y}")

        ser.write(b'N\r') #Erase Position 
        print("Erased position")
        time.sleep(1)

        ser.write(b'Q\r') #Turn motor offline 
        print("Turned motors offline")
        time.sleep(1)

        ser.write(b'F\r') #Turn motor online
        print("Turned motors online")
        time.sleep(1)
        
        ser.write(b'C\r') #Clear queued commands
        time.sleep(1)

        print("ZEROING COMPLETE...Stage should be at (0,0)")

    except serial.SerialException as e:
        print(f"Serial error during zeroing: {e}")

def send_command(ser, cmd, wait_for_ready=True, clear_first=False):
    try:
        # Online mode
        ser.write(b'F\r')
        time.sleep(0.05)

        # Stop and clear queue before motion
        if clear_first or cmd.startswith('I'):
            ser.write(b'K\r')  # Kill any current motion
            time.sleep(0.05)

            ser.write(b'C\r')   # Clear queued commands
            time.sleep(0.05)
            ser.reset_input_buffer()

        # Send command
        full_cmd = cmd + '\r'
        ser.write(full_cmd.encode())
        time.sleep(0.05)

        # Send R if it's motion
        if cmd.startswith('I'):
            ser.write(b'R\r')
            time.sleep(0.05)

        if wait_for_ready:
            response = b""
            timeout = time.time() + 15  # 15 seconds timeout
            while b'^' not in response and time.time() < timeout:
                response += ser.read(1)

            if time.time() >= timeout:
                print("Timeout waiting for motor response, assuming motor is stuck.")
                motor_stuck(ser)

            if b'^' not in response:
                raise TimeoutError("Did not receive the expected '^' character within timeout.")

            return response.decode(errors='ignore').strip()

        else:
            return ser.read_all().decode(errors='ignore').strip()

    except serial.SerialException as e:
        print(f"Serial error: {e}")
        return None

def convert_mm_to_steps(mm, steps_per_mm=400):
    """Convert millimeters to motor steps."""
    try:
        int(mm * steps_per_mm)
        return int(mm * steps_per_mm)
    except ValueError:
        print("Invalid input for convert_mm_to_steps: mm must be a number.")
        return None

def convert_steps_to_mm(steps, steps_per_mm=400):
    """Convert motor steps to millimeters."""
    try:
        return steps / steps_per_mm
    except ValueError:
        print("Invalid input for convert_steps_to_mm: steps must be a number.")
        return None

def move_to(ser, x_mm, y_mm):
    """Move stage to absolute position given in steps."""
    try:
        x_steps = convert_mm_to_steps(int(x_mm))
        y_steps = convert_mm_to_steps(int(y_mm))

        cmd_x = f'IA1M{x_steps}'  # Absolute move motor 1 (X)

        if y_steps >= 0: #flip y direction because motor is inverted
            cmd_y = f'IA2M-{y_steps}'
        else:
            cmd_y = f'IA2M{abs(y_steps)}'

        resp_x = send_command(ser, cmd_x)
        resp_y = send_command(ser, cmd_y)

        # Optionally wait a bit after commands
        time.sleep(0.1)

        print(f"Sent: {cmd_x}, Response: {resp_x}")
        print(f"Sent: {cmd_y}, Response: {resp_y}")

    except ValueError:
        print("Invalid steps, must be integers.")

def rel_move_to(ser, x_mm, y_mm):
    """Move stage relative to current position by given steps."""
    try:
        x_steps = convert_mm_to_steps(int(x_mm)) 
        y_steps = convert_mm_to_steps(int(y_mm))

        cmd_x = f'I1M{x_steps}'  # Relative move motor 1 (X)
        if y_steps >= 0: #flip y direction because motor is inverted
            cmd_y = f'IA2M-{y_steps}'
        else:
            cmd_y = f'IA2M{abs(y_steps)}'


        resp_x = send_command(ser, cmd_x)
        resp_y = send_command(ser, cmd_y)

        # Optionally wait a bit after commands
        time.sleep(1)

        print(f"Sent: {cmd_x}, Response: {resp_x}")
        print(f"Sent: {cmd_y}, Response: {resp_y}")

    except ValueError:
        print("Invalid steps, must be integers.")

def move_home(ser):
    """Home motors 1 and 2 by indexing to position 0."""
    resp_x = send_command(ser, 'IA1M0')  # Home motor 1
    resp_y = send_command(ser, 'IA2M0')  # Home motor 2

    print(f"Sent: IA1M0, Response: {resp_x}")
    print(f"Sent: IA2M0, Response: {resp_y}")


def motor_stuck(ser):
    '''Motor is stuck: Stop all motion and clear queue'''
    ser.write(b'K\r')  # Kill any current motion
    time.sleep(0.05)
    ser.write(b'C\r')   # Clear queued commands
    time.sleep(2)

    #reset to zero
    ser.write(b'IA1M-0\r') # Move stage to negative limit
    time.sleep(1)
    zero_to(ser)

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
        return int(response) * -1 # Invert Y direction
    except ValueError:
        print(f"Failed to parse Y position: {repr(response)}")
        return None
    
def get_mid_position(xres_min, xres_max, yres_min, yres_max):
    x_mid = int((xres_min + xres_max) / 2)
    y_mid = int((yres_min + yres_max) / 2)
    return x_mid, y_mid

def main():
    
    try:
        with ser:
            send_command(ser, 'Z')  # Zero stage (optional, depends on your setup)
            move_home(ser)
            move_to(ser, 1000, 2000)
    except serial.SerialException as e:
        print(f"Serial error: {e}")

if __name__ == "__main__":
    main()
