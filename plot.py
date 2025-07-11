import matplotlib.pyplot as plt

# Initial setup
fig, ax = plt.subplots()
dot, = ax.plot([0], [0], 'ro')
ax.set_xlim(-100, 100)
ax.set_ylim(-100, 100)
ax.set_title("Dot Position")
ax.set_xlabel("X")
ax.set_ylabel("Y")

prev_x, prev_y = 0, 0
plt.ion()
plt.show()

def update_dot(x, y):
    global prev_x, prev_y
    ax.plot(prev_x, prev_y, 'ko')  # leave a black trail
    ax.arrow(prev_x, prev_y, x - prev_x, y - prev_y,head_width=3, head_length=6, fc='blue', ec='blue', length_includes_head=True)
    dot.set_data([x], [y])
    plt.draw()
    plt.pause(0.01)
    prev_x, prev_y = x, y

def reset_plot():
    global prev_x, prev_y, dot
    prev_x, prev_y = 0, 0

    ax.cla()  # clear all objects

    # Rebuild axes and dot
    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)
    ax.set_title("Dot Position")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    dot, = ax.plot([0], [0], 'ro')  # recreate red dot at center

    plt.draw()
    plt.pause(0.01)
