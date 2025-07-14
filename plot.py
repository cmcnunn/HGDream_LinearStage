import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots()
ax.set_xlim(-15, 15)
ax.set_ylim(-15, 15)
ax.set_title("Hodoscope Position")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.grid(True)

dot, = ax.plot([0], [0], 'ro')

# Create the rectangle box centered at (0,0) with width=4, height=4
box_size = 4
box = patches.Rectangle((-box_size/2, -box_size/2), box_size, box_size,
                        linewidth=1, edgecolor='green', facecolor='none')
ax.add_patch(box)

prev_x, prev_y = 0, 0
arrows = []
black_dots = []

plt.ion()
plt.show()

def update_dot(x, y):
    global prev_x, prev_y, arrows, black_dots, box

    # Add black dot trail
    black_dot, = ax.plot(prev_x, prev_y, 'ko')
    black_dots.append(black_dot)

    # Draw arrow from old to new
    arrow = ax.arrow(prev_x, prev_y, x - prev_x, y - prev_y,
                     head_width=1, head_length=2, fc='blue', ec='blue', length_includes_head=True)
    arrows.append(arrow)

    # Remove oldest if more than 4
    if len(arrows) > 4:
        old_arrow = arrows.pop(0)
        old_arrow.remove()
    if len(black_dots) > 4:
        old_dot = black_dots.pop(0)
        old_dot.remove()

    # Update dot position
    dot.set_data([x], [y])

    # Move the green box to be centered at (x, y)
    box.set_xy((x - box_size/2, y - box_size/2))

    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.01)

    prev_x, prev_y = x, y

def reset_plot():
    global prev_x, prev_y, dot, arrows, black_dots, box
    prev_x, prev_y = 0, 0

    ax.cla()

    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)
    ax.set_title("Dot Position")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)

    dot, = ax.plot([0], [0], 'ro')

    # Recreate the box centered at (0,0)
    box = patches.Rectangle((-box_size/2, -box_size/2), box_size, box_size,
                            linewidth=1, edgecolor='green', facecolor='none')
    ax.add_patch(box)

    # Clear arrows and dots lists
    for a in arrows:
        a.remove()
    for d in black_dots:
        d.remove()
    arrows.clear()
    black_dots.clear()

    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.01)
