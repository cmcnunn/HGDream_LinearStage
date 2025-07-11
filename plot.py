import matplotlib.pyplot as plt

# Initial setup
fig, ax = plt.subplots()
dot, = ax.plot([0], [0], 'ro')  # red dot for current position
ax.set_xlim(-100, 100)
ax.set_ylim(-100, 100)
ax.set_title("Dot Position")
ax.set_xlabel("X")
ax.set_ylabel("Y")

# Store previous position
prev_x, prev_y = 0, 0

plt.ion()  # Interactive mode on
plt.show()

def update_dot(x, y):
    global prev_x, prev_y

    # Plot old position as black dot
    ax.plot(prev_x, prev_y, 'ko')  # small black dot at old position

    # Draw vector (arrow) from old to new
    dx = x - prev_x
    dy = y - prev_y
    ax.arrow(prev_x, prev_y, dx, dy, head_width=3, head_length=6, fc='blue', ec='blue', length_includes_head=True)

    # Update current dot
    dot.set_data([x], [y])

    # Redraw everything
    plt.draw()
    plt.pause(0.01)

    # Update stored position
    prev_x, prev_y = x, y
