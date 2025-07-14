import serial
import time

def send_command(ser, cmd):
    """Sends a command to the Velmex VP9000 and reads the response."""
    full_cmd = cmd + '\r'
    ser.write(full_cmd.encode())
    time.sleep(0.1)
    response = ser.read_all().decode(errors='ignore').strip()
    return response

def move_to(ser, x, y):
    """Moves the stage to the specified (x, y) coordinates."""
    try:
        x = float(x)
        y = float(y)
        cmd_x = f'X+{x:.2f}'
        cmd_y = f'Y+{y:.2f}'
        
        response_x = send_command(ser, cmd_x)
        response_y = send_command(ser, cmd_y)
        send_command(ser, 'G')  # Execute queued moves

        print(f"Sent: {cmd_x}, Response: {response_x}")
        print(f"Sent: {cmd_y}, Response: {response_y}")

    except ValueError:
        print("Invalid coordinates. Please enter numeric values.")

def move_home(ser):
    """Moves the stage to the home position (0, 0)."""
    try:
        response_home_x = send_command(ser, 'HX:')
        time.sleep(5)
        response_home_y = send_command(ser, 'HY:')
        time.sleep(5)
        print(f"Sent: HX:, Response: {response_home_x}")
        print(f"Sent: HY:, Response: {response_home_y}")
    except Exception as e:
        print(f"Error during homing: {e}")

def main():
    port = 'COM3'  # or '/dev/ttyUSB0' on Linux
    baud_rate = 9600

    with serial.Serial(port, baud_rate, timeout=1) as ser:
        send_command(ser, 'Z')  # Clear errors/alarms
        move_home(ser)
        move_to(ser, 1000, 2000)

if __name__ == "__main__":
    main()
