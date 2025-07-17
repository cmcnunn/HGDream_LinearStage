import serial
import time
from connection import ser

def zero_to(ser):
    """Zero the stage position."""
    try:
        resp_x = send_command(ser, 'IA1M13016', clear_first=True)  # Zero motor 1
        resp_y = send_command(ser, 'IA2M13016', clear_first=True)  # Zero motor 2

        ser.write(b'R\r') #Run
        time.sleep(1)
        
        print(f"Zeroed motor 1: {resp_x}")
        print(f"Zeroed motor 2: {resp_y}")

        ser.write(b'R\r') #Run
        time.sleep(1)

    except serial.SerialException as e:
        print(f"Serial error during zeroing: {e}")

def send_command(ser, cmd, wait_for_ready=True, clear_first=False):
    try:
        # Online mode
        ser.write(b'F\r')
        time.sleep(0.05)

        # Stop and clear queue before motion
        if clear_first or cmd.startswith('I'):
            ser.write(b'XQ\r')  # Kill any current motion
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
            timeout = time.time() + 5
            while b'^' not in response and time.time() < timeout:
                response += ser.read(1)
            return response.decode(errors='ignore').strip()
        else:
            return ser.read_all().decode(errors='ignore').strip()

    except serial.SerialException as e:
        print(f"Serial error: {e}")
        return None

def convert_mm_to_steps(mm, steps_per_mm=400):
    """Convert millimeters to motor steps."""
    return int(mm * steps_per_mm + 13016) # Offset for zeroing)

def move_to(ser, x_mm, y_mm):
    """Move stage to absolute position given in steps."""
    try:
        x_steps = convert_mm_to_steps(int(x_mm))
        y_steps = convert_mm_to_steps(int(y_mm))

        cmd_x = f'IA1M{x_steps}'  # Absolute move motor 1 (X)
        cmd_y = f'IA2M{y_steps}'  # Absolute move motor 2 (Y)

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
        x_steps = convert_mm_to_steps(int(x_mm)) - 13016
        y_steps = convert_mm_to_steps(int(y_mm)) - 13016

        cmd_x = f'I1M{x_steps}'  # Relative move motor 1 (X)
        cmd_y = f'I2M{y_steps}'  # Relative move motor 2 (Y)

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
    resp_x = send_command(ser, 'IA1M13016')  # Home motor 1
    resp_y = send_command(ser, 'IA2M13016')  # Home motor 2

    print(f"Sent: IA1M13016, Response: {resp_x}")
    print(f"Sent: IA2M13016, Response: {resp_y}")

    # Wait enough time for homing to finish
    time.sleep(5)


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
