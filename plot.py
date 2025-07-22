import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots()
ax.set_xlim(-80, 80)
ax.set_ylim(-80, 80)
ax.set_title("Hodoscope Position")
ax.set_xlabel("X [mm]")
ax.set_ylabel("Y [mm]")
ax.grid(True)
# Forbidden region box: from -40 to +65 in both x and y
forbidden_box = patches.Rectangle(
    (-40, -40),       # Bottom-left corner
    80,              # Width: 65 - (-40)
    80,              # Height: 65 - (-40)
    linewidth=1.5,
    edgecolor='red',
    facecolor='none',
    linestyle='--',
    label='Forbidden Zone'
)
ax.add_patch(forbidden_box)
prev_x, prev_y = 0, 0  # Start position

dot, = ax.plot([0], [0], 'ro') # Red dot for current position
# Create the rectangle box centered at (3,0) with width=4, height=4
box_size = 38.4
box = patches.Rectangle((0 - box_size/2, 0 - box_size/2), box_size, box_size,
                        linewidth=1, edgecolor='red', facecolor='none')
ax.add_patch(box)
position_label = ax.text(0.02, 0.95, '', transform=ax.transAxes,
                         fontsize=10, verticalalignment='top',
                         bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
dot.set_data([0], [0])
black_dots = []

plt.ion()
plt.show()

def update_dot(x, y):
    '''Update the position of the dot and add a black dot trail.'''
    global prev_x, prev_y,black_dots, box
    print(f"Updating dot to ({x}, {y})")
    # Add black dot trail
    black_dot, = ax.plot(prev_x, prev_y, 'ko')
    black_dots.append(black_dot)
    # Update dot position
    dot.set_data([x], [y])
    # Move the green box to be centered at (x, y)
    box.set_xy((x - box_size/2, y - box_size/2))
    # Update the position label
    position_label.set_text(f"Position: ({x:.1f} mm, {y:.1f} mm)")
    # Update previous position
    prev_x, prev_y = x, y
    # Redraw the plot
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.01)
    # Remove oldest if more than 4
    if len(black_dots) > 2:
        old_dot = black_dots.pop(0)
        old_dot.remove()
    
    return prev_x, prev_y

def update_dot_rel(dx, dy):
    '''Update the position of the dot relatively and add a black dot trail.'''
    global prev_x, prev_y
    new_x = prev_x + dx
    new_y = prev_y + dy
    return update_dot(new_x, new_y)

def reset_plot():
    global prev_x, prev_y, dot, black_dots, box, ax

    prev_x, prev_y = 0, 0

    # Clear the current axes
    ax.cla()
    ax.set_xlim(-80, 80)
    ax.set_ylim(-80, 80)
    ax.set_title("Hodoscope Position")
    ax.set_xlabel("X [mm]")
    ax.set_ylabel("Y [mm]")
    ax.grid(True)
    # Forbidden region box
    forbidden_box = patches.Rectangle(
        (-40, -40),       # Bottom-left corner
        80,              # Width: 
        80,              # Height: 
        linewidth=1.5,
        edgecolor='red',
        facecolor='none',
        linestyle='--',
        label='Forbidden Zone'
    )
    ax.add_patch(forbidden_box)
    # Reset main red dot and box
    dot, = ax.plot([prev_x], [prev_y], 'ro')

    box = patches.Rectangle((prev_x - box_size/2, prev_y - box_size/2), box_size, box_size,
                            linewidth=1, edgecolor='red', facecolor='none')
    ax.add_patch(box)
    # Update previous position
    position_label.set_text(f"Position: ({prev_x:.1f} mm, {prev_y:.1f} mm)")
    # Clear black dot trail
    for d in black_dots:
        try:
            d.remove()
        except:
            pass
    black_dots.clear()

    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.01)
    print("Plot reset to initial position (0,0)")

def set_plot_limits(xmin, xmax, ymin, ymax):
    """Update the forbidden zone to match the stage's full range."""
    width = xmax - xmin
    height = ymax - ymin
    forbidden_box.set_xy((xmin, ymin))
    forbidden_box.set_width(width)
    forbidden_box.set_height(height)
    ax.figure.canvas.draw()

if __name__ == "__main__":
    reset_plot()
    update_dot(5, 5)
    update_dot(10, 10)
    update_dot(15, 15)
    update_dot(18, 18)
    update_dot(19, 19)
    plt.ioff()
    plt.show()