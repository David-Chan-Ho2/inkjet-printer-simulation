import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches

# Constants
DISTANCE = 3E-3         # 3 mm
CAPACITOR_LENGTH = 1E-3 * 1e3 # 1 mm
VELOCITY = 20           # m/s

# Derived values
travel_time = DISTANCE / VELOCITY
frames = 100
time_values = np.linspace(0, travel_time, frames)

# Setup figure
fig, ax = plt.subplots()
ax.set_xlim(0, DISTANCE * 1e3)
ax.set_ylim(-1, 1)
ax.set_xlabel("Horizontal Distance (mm)")
ax.set_title("Droplet Motion")

capacitorTop = patches.Rectangle((1.25, 0.5), CAPACITOR_LENGTH, 0.25,
                                 color='red', alpha=0.4, label='Top Plate')
ax.add_patch(capacitorTop)

capacitorBottom = patches.Rectangle((1.25, -0.75), CAPACITOR_LENGTH, 0.25,
                                    color='lightblue', alpha=0.4, label='Bottom Plate')
ax.add_patch(capacitorBottom)

# Moving dot (red)
(dot,) = ax.plot([], [], 'ro', markersize=10, label='Droplet')

# Line trail (blue)
(line,) = ax.plot([], [], 'b-', lw=2, label='Trail')

# Static elements
ax.axhline(0, color='gray', linestyle='--')
ax.legend()

# Timer text
timer_text = ax.text(0.8 * DISTANCE * 1e3, 0.6, '', fontsize=12, color='black')

# Initialize animation
def init():
    dot.set_data([], [])
    line.set_data([], [])
    timer_text.set_text('')
    return dot, line, timer_text

# Update animation
def update(frame):
    # X position in mm
    x = np.linspace(0, (DISTANCE * 1e3) * (frame / frames), max(1, frame))

    y = np.zeros_like(x)
    
    # Update the trail and the dot
    line.set_data(x, y)
    dot.set_data([x[-1]], [0])
    
    # Update timer
    t_ms = time_values[frame] * 1e3
    timer_text.set_text(f"Time: {t_ms:.2f} ms")
    
    return dot, line, timer_text

# Animate
ani = FuncAnimation(
    fig, update, frames=frames,
    init_func=init, blit=True,
    interval=50, repeat=False
)

plt.show()
