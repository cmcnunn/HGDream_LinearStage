import serial
import time
from connection import ser

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
        if cmd.startswith('I'):
            ser.write(b'R')
            time.sleep(0.05)
        
        response = b""
        timeout = time.time() + 5
        while b'^' not in response and time.time() < timeout:
            response += ser.read(1)
        return response.decode(errors='ignore').strip()
    except serial.SerialException as e:
        print(f"Serial error: {e}")
        return None
    
def convert_cm_to_steps(cm, steps_per_cm=50):
    """Convert centimeters to motor steps."""
    return int(cm * steps_per_cm)

def move_to(ser, x_cm, y_cm):
    """Move stage to absolute position given in centimeters."""
    try:
        x_steps = convert_cm_to_steps(int(x_cm))
        y_steps = convert_cm_to_steps(int(y_cm))
        cmd_x = f'IA1M{x_steps}'  # Absolute move motor 1 (X)
        cmd_y = f'IA3M{y_steps}'  # Absolute move motor 2 (Y)
        resp_x = send_command(ser, cmd_x)
        time.sleep(1)  # Small delay between commands
        resp_y = send_command(ser, cmd_y)
        time.sleep(0.5)  # Optional wait after commands
        return resp_x, resp_y
    except Exception as e:
        print(f"Error in move_to: {e}")
        return None, None

def rel_move_to(ser, x_cm, y_cm):
    """Move stage relative to current position given in centimeters."""
    try:
        x_steps = convert_cm_to_steps(int(x_cm))
        y_steps = convert_cm_to_steps(int(y_cm))
        cmd_x = f'I1M{x_steps}'  # Relative move motor 1 (X)
        cmd_y = f'I3M{y_steps}'  # Relative move motor 2 (Y)
        resp_x = send_command(ser, cmd_x)
        time.sleep(1)  # Small delay between commands
        resp_y = send_command(ser, cmd_y)
        time.sleep(0.5)  # Optional wait after commands
        return resp_x, resp_y
    except Exception as e:
        print(f"Error in rel_move_to: {e}")
        return None, None
    
def move_home(ser):
    """Home the stage."""
    try:
        resp_x = send_command(ser, 'I1M-0')  # Home motor 1 (X)
        time.sleep(1)  # Small delay between commands
        resp_y = send_command(ser, 'I2M-0')  # Home motor 2 (Y)
        time.sleep(0.5)  # Optional wait after commands
        return resp_x, resp_y
    except Exception as e:
        print(f"Error in move_home: {e}")
        return None, None
    
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