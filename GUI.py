import tkinter as tk
from plot import update_dot,reset_plot, update_dot_rel,prev_x,prev_y
from controller_dummy import move_to,move_home,rel_move_to
import serial
import connection

# Create a separate window to get serial port input
# This window will block until the user provides input
serwindow = tk.Tk()
serwindow.title("Serial Port Input")
serwindow.geometry("400x200")
serlabel = tk.Label(serwindow, text="Enter Serial Port (e.g. COM6):")
serlabel.pack(pady=5)
serentry = tk.Entry(serwindow, width=5)
serentry.place(x=180, y=50)

def on_submit():
    '''Submit the serial port and close the window'''
    import connection
    SERIAL_PORT = serentry.get().strip()

    if SERIAL_PORT.lower() == 'dummy':
        connection.ser = 'Dummy'
        serwindow.destroy()
    else:
        try:
            connection.ser = serial.Serial(
                port=SERIAL_PORT,
                baudrate=9600,
                bytesize=serial.SEVENBITS,
                parity=serial.PARITY_EVEN,
                stopbits=serial.STOPBITS_TWO,
                timeout=1
            )
            serwindow.destroy()
        except Exception as e:
            serlabel.config(text=f"Connection failed: {e}")

submit_button = tk.Button(serwindow, text="Submit", command=on_submit)
submit_button.place(x=170, y=80)
serwindow.mainloop()

if connection.ser is None:
    print("No serial port provided. Exiting.")
    exit()

if connection.ser == 'Dummy':
    print("Using dummy controller. No actual movements will be made.")


def show_move():
    '''Show the move command'''
    check_input()
    user_input = f"({x_input.get()}, {y_input.get()})"
    label.config(text=f"Moving to {user_input}")

def on_click_move():
    '''Move to specified position'''
    x, y = check_input()
    label.config(text=f"Moving to ({x}, {y})")
    update_dot(x, y)
    move_to(connection.ser, x, y)

def on_click_relmove():
    '''Move relative to current position'''
    x_rel, y_rel = check_input()
    label.config(text=f"Moving by ({x_rel}, {y_rel})")
    update_dot_rel(x_rel, y_rel)
    rel_move_to(connection.ser, x_rel, y_rel)

def on_click_home():
    '''Home the stage and move to (0,0)'''
    user_input = "(3, 0)"
    label.config(text=f"Moving to {user_input}")
    reset_plot()
    update_dot(3, 0)    
    move_home(connection.ser)

def check_input():
    """Validate and return x and y input as integers."""
    try:
        x = int(x_input.get())
    except ValueError:
        x = 0
        x_input.delete(0, tk.END)
        x_input.insert(0, "0")

    try:
        y = int(y_input.get())
    except ValueError:
        y = 0
        y_input.delete(0, tk.END)
        y_input.insert(0, "0")

    return x, y

#creates the GUI window    
root = tk.Tk()
root.title("Linear Stage Control")
root.geometry("250x150")

# Label showing output
label = tk.Label(root, text="Welcome")
label.place(x=20, y=25)  

# X input field
x_label = tk.Label(root, text="X:")
x_label.place(x=60, y=50)
x_input = tk.Entry(root, width=5)
x_input.place(x=80, y=50)

# Y input field
y_label = tk.Label(root, text="Y:")
y_label.place(x=120, y=50)
y_input = tk.Entry(root, width=5)
y_input.place(x=140, y=50)

# Move button
move_button = tk.Button(root, text="Move", command=on_click_move)
move_button.place(x=75, y=100)

# Home button 
home_button = tk.Button(root, text="Home", command=on_click_home)
home_button.place(x=25, y=100)

# Relative motion 
rel_motion = tk.Button(root, text="Relative Motion", command=on_click_relmove)
rel_motion.place(x=125, y=100)
# Start the GUI event loop
root.mainloop()
