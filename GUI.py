import tkinter as tk

root = tk.Tk()
root.title("My First GUI")
root.geometry("600x400")

label = tk.Label(root, text="Welcome")
label.place(x=0, y=100)  # use .place() instead of .pack() so we can move it

def move_label(x=0):
    if x <= 500:
        label.place(x=x, y=100)
        root.after(10, move_label, x+5)  # move 5 pixels every 10ms

def on_click():
    label.config(text="Moving...")
    move_label()

button = tk.Button(root, text="Move", command=on_click)
button.pack()

root.mainloop()
