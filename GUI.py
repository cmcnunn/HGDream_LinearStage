import tkinter as tk
from plot import update_dot
from plot import reset_plot
import controller

#input display
def show_move():
    user_input = f"({x_input.get()}, {y_input.get()})"
    label.config(text=f"Moving to {user_input}")

#when click display input 
def on_click_move():
    show_move()
    update_dot(float(x_input.get()), float(y_input.get()))

#when home button is clicked, reset dot position
def on_click_home():
    user_input = "(0, 0)"
    label.config(text=f"Moving to {user_input}")
    update_dot(0, 0)

#creates the GUI window    
root = tk.Tk()
root.title("Linear Stage Control")
root.geometry("250x150")

# Label showing output
label = tk.Label(root, text="Welcome")
label.place(x=20, y=25)  

# Y input field
y_input = tk.Entry(root, width=5)
y_input.place(x=100, y=50)

# X input field
x_input = tk.Entry(root, width=5)
x_input.place(x=50, y=50)

# Move button
move_button = tk.Button(root, text="Move", command=on_click_move)
move_button.place(x=100, y=100)

# Home button 
home_button = tk.Button(root, text="Home", command=on_click_home)
home_button.place(x=50, y=100)

# Reset button
reset_button = tk.Button(root, text="Reset", command=reset_plot)
reset_button.place(x=150, y=100)

# Start the GUI event loop
root.mainloop()
