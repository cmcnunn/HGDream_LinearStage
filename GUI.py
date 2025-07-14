import tkinter as tk
from plot import update_dot,reset_plot
from controller import move_to,move_home
import serial
from connection import ser

# Create a separate window to get serial port input
# This window will block until the user provides input
serwindow = tk.Tk()
serwindow.title("Serial Port Input")
serwindow.geometry("400x200")
serlabel = tk.Label(serwindow, text="Enter Serial Port & Baud number (e.g. COM3 and 9600):")
serlabel.pack(pady=5)
serentry = tk.Entry(serwindow, width=5)
serentry.place(x=150, y=50)
bauentry = tk.Entry(serwindow, width=5)
bauentry.place(x=200, y=50)

def on_submit():
    global ser
    SERIAL_PORT = serentry.get()
    BAUD_RATE = bauentry.get()
    if SERIAL_PORT and BAUD_RATE:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        serwindow.destroy()
    else:
        serlabel.config(text="Please enter a valid serial port.")

submit_button = tk.Button(serwindow, text="Submit", command=on_submit)
submit_button.place(x=170, y=80)
serwindow.mainloop()

if ser is None:
    print("No serial port provided. Exiting.")
    exit()

#input display
def show_move():
    user_input = f"({x_input.get()}, {y_input.get()})"
    label.config(text=f"Moving to {user_input}")

#when click display input 
def on_click_move():
    show_move()
    update_dot(float(x_input.get()), float(y_input.get()))
    move_to(ser.get(), x_input.get(), y_input.get())  # Initial call to set position

#when home button is clicked, reset dot position
def on_click_home():
    user_input = "(0, 0)"
    label.config(text=f"Moving to {user_input}")
    update_dot(0, 0)
    move_home(ser.get())

def on_click_reset():
    label.config(text="Resetting plot")
    reset_plot()
    update_dot(0, 0)
    move_home(ser.get())

#creates the GUI window    
root = tk.Tk()
root.title("Linear Stage Control")
root.geometry("250x150")

# Label showing output
label = tk.Label(root, text="Welcome")
label.place(x=20, y=25)  

# Serial port input field
ser_input = tk.Entry(root, width=5)
ser_input.place(x=20, y=50)

# X input field
x_input = tk.Entry(root, width=5)
x_input.place(x=80, y=50)

# Y input field
y_input = tk.Entry(root, width=5)
y_input.place(x=140, y=50)


# Move button
move_button = tk.Button(root, text="Move", command=on_click_move)
move_button.place(x=100, y=100)


# Home button 
home_button = tk.Button(root, text="Home", command=on_click_home)
home_button.place(x=50, y=100)


# Reset button
reset_button = tk.Button(root, text="Reset", command=on_click_reset)
reset_button.place(x=150, y=100)

# Start the GUI event loop
root.mainloop()
