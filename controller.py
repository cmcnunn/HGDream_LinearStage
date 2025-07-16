import serial
import time
from connection import ser

def send_command(ser, cmd, wait_for_ready=True):
    try:
        # Ensure we're in Online Mode
        ser.write(b'F')
        time.sleep(0.05)

        # Send command
        full_cmd = cmd + '\r'
        ser.write(full_cmd.encode())

        # If it's a motion command, send 'R'
        if cmd.startswith(('I', 'S', 'A')):
            time.sleep(0.05)
            ser.write(b'R\r')

        # Now wait for ready signal '^'
        if wait_for_ready:
            response = b""
            timeout = time.time() + 5  # wait up to 5 seconds
            while b'^' not in response and time.time() < timeout:
                response += ser.read(1)

            return response.decode(errors='ignore').strip()
        else:
            return ser.read_all().decode(errors='ignore').strip()

    except serial.SerialException as e:
        print(f"Serial error: {e}")
        return None


def move_to(ser, x_steps, y_steps):
    """Move stage to absolute position given in steps."""
    try:
        x_steps = int(x_steps)
        y_steps = int(y_steps)

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

def rel_move_to(ser, x_steps, y_steps):
    """Move stage relative to current position by given steps."""
    try:
        x_steps = int(x_steps)
        y_steps = int(y_steps)

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
    """Home motors 1 and 2 by indexing to negative limit."""
    resp_x = send_command(ser, 'I1M-0')  # Home motor 1
    resp_y = send_command(ser, 'I2M-0')  # Home motor 2

    print(f"Sent: I1M-0, Response: {resp_x}")
    print(f"Sent: I2M-0, Response: {resp_y}")

    # Wait enough time for homing to finish
    time.sleep(5)

    # Zero the motor positions after homing
    zero_x = send_command(ser, 'IA1M0')  # Zero motor 1
    zero_y = send_command(ser, 'IA2M0')  # Zero motor 2
    print(f"Zeroed motor 1: {zero_x}")
    print(f"Zeroed motor 2: {zero_y}")

def get_position_x(ser):
    '''Get current X position in steps.'''
    resp = send_command(ser, 'X')
    try:
        return int(resp)
    except ValueError:
        print(f"Failed to parse X position: {repr(resp)}")
        return None

def get_position_y(ser):
    '''Get current Y position in steps.'''
    resp = send_command(ser, 'Y')
    try:
        return int(resp)
    except ValueError:
        print(f"Failed to parse Y position: {repr(resp)}")
        return None

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
