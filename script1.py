import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches
from constants import TOTAL_DISTANCE, CAPACITOR_LENGTH, DROPLET_VELOCITY
from helpers import convert_mm_to_int

# Constants
DISTANCE = convert_mm_to_int(TOTAL_DISTANCE)

CAPACITOR = {
    'LENGTH': convert_mm_to_int(CAPACITOR_LENGTH),
    'WIDTH': 0.25,
    'X': 1.25,
    'TOP': {
        'Y': 0.5
    },
    'BOTTOM': {
        'Y': -0.75
    },
}

# Derived values
t_travel = DISTANCE / DROPLET_VELOCITY
frames = 100
time_values = np.linspace(0, t_travel, frames)

# Setup figure
fig, ax = plt.subplots()
ax.set_xlim(0, DISTANCE)
ax.set_ylim(-1, 1)
ax.set_xlabel("Horizontal Distance (mm)")
ax.set_title("Droplet Motion")

def capacitor(y, color, label): 
    c = patches.Rectangle(
        (CAPACITOR['X'], y), 
        CAPACITOR['LENGTH'], 
        CAPACITOR['WIDTH'],
        color=color, 
        alpha=0.4, 
        label=label
    )
    ax.add_patch(c)

capacitor(y=CAPACITOR['TOP']['Y'], color='red', label='Top Plate')
capacitor(y=CAPACITOR['BOTTOM']['Y'], color='lightblue', label='Bottom Plate')

# Moving dot
(dot,) = ax.plot([], [], 'ko', markersize=10, label='Droplet')

# Line trail
(line,) = ax.plot([], [], 'k-', lw=2, label='Trail')

ax.legend()

# Timer text
timer_text = ax.text(0.7 * DISTANCE, -.9, '', fontsize=12, color='black')

# Initialize animation
def init():
    dot.set_data([], [])
    line.set_data([], [])
    timer_text.set_text('')
    return dot, line, timer_text

# Update animation
def update(frame):
    # X position in mm
    x = np.linspace(0, (DISTANCE) * (frame / frames), max(1, frame))
    y = np.zeros_like(x)

    # Update the trail and the dot
    line.set_data(x, y)
    dot.set_data([x[-1]], [0])

    # Update timer
    t_ms = convert_mm_to_int(time_values[frame])
    timer_text.set_text(f"Time: {t_ms:.2f} ms")

    return dot, line, timer_text

# Animate
ani = FuncAnimation(
    fig, 
    update, 
    frames=frames,
    init_func=init, 
    blit=True,
    interval=50, 
    repeat=False
)

plt.show()
