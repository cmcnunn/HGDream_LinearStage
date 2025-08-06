import serial 
import time
from connection import ser 
from plot import set_plot_limits

def convert_mm_to_steps(mm, steps_per_mm=200):
    try:
        x = round(mm * steps_per_mm)
        return x
    except TypeError:
        print("\033[31mInvalid input for unit conversion.\033[0m")

def convert_steps_to_mm(steps, steps_per_mm=200):
    try:
        x = round(steps / steps_per_mm)
        return x
    except TypeError:
        print("\033[31mInvalid input for unit conversion.\033[0m")

def send_command(ser, cmd): 
    '''Send a command to the serial poort and return the responce. '''
    try: 
        ser.write(b'F') #Turn the motor online 
        time.sleep(1)
        ser.write(b'C') #Clear command que
        time.sleep(1)
        ser.write(b'R')
        ser.reset_input_buffer()

        full_cmd = cmd + '\r' #write command
        ser.write(full_cmd.encode()) #send command

        if cmd.startswith('I'): #if indexing moror always R
            ser.write(b'R') #runs indexing command 
            time.sleep(1)
    
        response = b""
        timeout = time.time() + 15 #15 seconds timeout
        while b'^' not in response and time.time() < timeout: 
            response += ser.read(1)

        if time.time() > timeout: 
            print("\033[31mWARNING: Command response timeout. Motor is stuck\033[0m")
            motor_stuck()
        
    except serial.SerialException as e: 
        print(f"\033[31mSerial error: {e}\033[0m")
        return None

def find_range(ser): 

    try:
        print("Finding range")

        send_command(ser, 'K') #kill all motion 
        time.sleep(1)

        send_command(ser, 'I1M-0') #get x lower limit
        time.sleep(1)
        xres_min = convert_steps_to_mm(get_position_x(ser))

        send_command(ser, "I2M0") #get y lower limit
        time.sleep(1)
        yres_min = convert_steps_to_mm(get_position_y(ser))

        send_command(ser, "I1M0") #get x upper limit 
        time.sleep(1)
        xres_max = convert_steps_to_mm(get_position_x(ser))

        send_command(ser, "I2M-0") #get y upper limit
        time.sleep(1)
        yres_max = convert_steps_to_mm(get_position_y(ser))


        midpoint_int = lambda a, b: round((a + b) / 2)

        x_mid = midpoint_int(xres_max, xres_min)
        y_mid = midpoint_int(yres_max, yres_min)

        xtot_d = xres_max - xres_min
        ytot_d = yres_max - yres_min

        x_max = xtot_d/2
        x_min = -1*x_max

        y_max = ytot_d/2
        y_min = -1*y_max

        print(f"Range X:{x_min}-{x_max} Y:{y_min},{y_max}")

        print(f"Midpoints: X:{x_mid}, Y:{y_mid}")

        return x_min, x_max, y_min, y_max, x_mid, y_mid
    
    except Exception as e: 
        return print(f"\033[31mERROR in find_range: {e}\033[0m")


def zero_to(ser, x_mid, y_mid):
    print(f"Now Zeroing to ({x_mid,y_mid})")
    try: 
        resp_x = send_command(ser, 'I1M-0')
        resp_y = send_command(ser, 'I2M0')

        print("Moving to Limit")

        time.sleep(1)

        ser.write(b'N\r')
        print('Erased Position')
        time.sleep(1)

        ser.write(b'Q\r')
        print("Turned motors offline")
        time.sleep(1)

        ser.write(b'F\r')
        print("Motor Online")
        time.sleep(1)

        move_to(ser,x_mid,y_mid) #move to midpoints

        time.sleep(1)

        print("Zeroed Motors")
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
        print(f"\033[31mSeral error during zeroing: {e}\033[0m")

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
        print("\033[31mInvalid input for move_to: x_mm and y_mm must be integers.\033[0m")
        
    except Exception as e:
        print(f"\033[31mError in move_to: {e}\033[0m")

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
        print("\033[31mInvalid input for rel_move_to: x_mm and y_mm must be integers.\033[0m")
    except Exception as e:
        print(f"\033[31mError in rel_move_to: {e}\033[0m")

def move_home(ser):
    """Home the stage."""
    try:
        resp_x = send_command(ser, 'IA1M0')  # Home motor 1 (X)
        time.sleep(1)  # Small delay between commands
        resp_y = send_command(ser, 'IA2M0')  # Home motor 2 (Y)

        print(f"Sent: IA1M0, Response: {resp_x}")
        print(f"Sent: IA2M0, Response: {resp_y}")

    except Exception as e:
        print(f"\033[31mError in move_home: {e}\033[0m")
        return None, None
    

import concurrent.futures

def motor_stuck(ser):
    '''Motor is stuck: Stop all motion and clear queue '''
    print("\033[32mMotor appears to be stuck. Stopping all motion and clearing command queue.\033[0m")
    try:
        ser.write(b'K\r')  # Kill motion
        time.sleep(0.5)
        ser.write(b'C\r')  # Clear queue
        time.sleep(2)
        ser.write(b'IA1M-0\r')  # Move to negative limit
        print("\033[31mResetting...\033[0m")

        def reset_and_find():
            xmin, xmax, ymin, ymax, midx, midy = find_range(ser)
            zero_to(ser, midx, midy)
            set_plot_limits(xmin, xmax, ymin, ymax)

        # Run with timeout
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(reset_and_find)
            try:
                future.result(timeout=30)  # seconds
            except concurrent.futures.TimeoutError:
                print("\033[31mCannot Reset. Please Close Window\033[0m")
                
                return

        return

    except Exception as e:
        print(f"\033[31mUnexpected error: {e}\033[0m")


def get_position_x(ser):
    ser.write(b'X\r')
    time.sleep(0.05)
    response = ser.read_until(b'\r').decode().strip()
    try:
        if response.startswith('^'):
            response = response[1:]  # Remove leading '^'
        return int(response)
    except ValueError:
        print(f"\033[31mFailed to parse X position: {repr(response)}\033[0m")
        return None

def get_position_y(ser):
    ser.write(b'Y\r')
    time.sleep(0.05)
    response = ser.read_until(b'\r').decode().strip()
    try:
        if response.startswith('^'):
            response = response[1:]  # Remove leading '^'
        return int(response)
    except ValueError:
        print(f"\033[31mFailed to parse Y position: {repr(response)}\033[0m")
        return None
