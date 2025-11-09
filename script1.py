import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.ticker as ticker
from constants import TOTAL_DISTANCE, DROPLET_VELOCITY, CAPACITOR_WIDTH
from calculations import L_gun_to_cap 
from helpers import init_capacitor, mm_formatter 

t_travel = TOTAL_DISTANCE / DROPLET_VELOCITY
frames = 100
time_values = np.linspace(0, t_travel, frames)

# Setup Figure
fig, ax = plt.subplots()

# Set X-axis limit in METERS
ax.set_xlim(0, TOTAL_DISTANCE * 1.1)

# Set Y-axis limit based on CAPACITOR_WIDTH (in METERS) 
y_limit_m = (CAPACITOR_WIDTH  / 2) * 2.0 
ax.set_ylim(-y_limit_m, y_limit_m)

# Use the mm_formatter helper to display axis labels in mm
ax.xaxis.set_major_formatter(ticker.FuncFormatter(mm_formatter))
ax.yaxis.set_major_formatter(ticker.FuncFormatter(mm_formatter))

ax.set_xlabel("Horizontal Distance (mm)")
ax.set_ylabel("Vertical Position (mm)") 
ax.set_title("Droplet Motion")
ax.grid(True, linestyle=':', alpha=0.6) 

# Draw Capacitor Plates
init_capacitor(ax, L_gun_to_cap)

ax.axvline(x=TOTAL_DISTANCE, color='blue', linestyle='--', linewidth=2, label='Paper Target')

# Moving dot
(dot,) = ax.plot([], [], 'ko', markersize=10, label='Droplet')

ax.legend(loc='upper right')

# Timer text 
timer_text = ax.text(0.7 * TOTAL_DISTANCE, -y_limit_m * 0.9, '', fontsize=12, color='black')


# Animation Functions

def init():
    dot.set_data([], [])
    timer_text.set_text('')
    return dot, timer_text

def update(frame):
    # Get current time
    t_current = time_values[frame]
    
    # Generate array of X positions (trail)
    # The dot's X position is determined by its constant velocity
    x_current = DROPLET_VELOCITY * np.linspace(0, t_current, max(2, frame))

    # Update the dot (at the end of the trail)
    dot.set_data([x_current[-1]], [0])

    # Update timer (convert to ms)
    t_ms = t_current * 1000
    timer_text.set_text(f"Time: {t_ms:.2f} ms")

    return dot, timer_text

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
# ani.save('q1.mp4', writer='ffmpeg', fps=50) 

plt.show()