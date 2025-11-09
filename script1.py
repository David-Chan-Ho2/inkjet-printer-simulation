import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.ticker as ticker
from constants import TOTAL_DISTANCE, DROPLET_VELOCITY, CAPACITOR_WIDTH
from calculations import L_gun_to_cap 
from helpers import init_capacitor, mm_formatter 

# --- Derived Values ---
t_travel = TOTAL_DISTANCE / DROPLET_VELOCITY
frames = 100
time_values = np.linspace(0, t_travel, frames)
D = TOTAL_DISTANCE

# Set Y-axis limit based on CAPACITOR_WIDTH (in METERS) 
# We use this zoomed limit for both plots for consistency.
y_limit_m = (CAPACITOR_WIDTH  / 2) * 2.0 

# --- Setup Figure (Two Subplots) ---
fig, (ax_path, ax_hit) = plt.subplots(1, 2, figsize=(8, 8)) # 2 rows, 1 column

# === Plot 1: Droplet Path Simulation (ax_path) ===
ax_path.set_xlim(0, D * 1.1)
ax_path.set_ylim(-y_limit_m, y_limit_m)

ax_path.xaxis.set_major_formatter(ticker.FuncFormatter(mm_formatter))
ax_path.yaxis.set_major_formatter(ticker.FuncFormatter(mm_formatter))

ax_path.set_title("Droplet Motion (Zoomed on Capacitor)")
ax_path.set_xlabel("Horizontal Distance (mm)")
ax_path.set_ylabel("Vertical Position (mm)") 
ax_path.grid(True, linestyle=':', alpha=0.6) 

# Static Elements
init_capacitor(ax_path, L_gun_to_cap)
ax_path.axvline(x=D, color='blue', linestyle='--', linewidth=2, label='Paper Target')

# Moving dot and Text
(dot,) = ax_path.plot([], [], 'ko', markersize=10, label='Droplet')
ax_path.legend(loc='upper right')

timer_text = ax_path.text(0.7 * D, -y_limit_m * 0.9, '', fontsize=12, color='black')


# === Plot 2: Droplet Hit Location (ax_hit) ===
# Set Y-limits to match the path plot
ax_hit.set_ylim(-y_limit_m, y_limit_m)
# Set a tiny arbitrary X-range since the paper is just a line (we only care about Y)
ax_hit.set_xlim(-0.01, 0.01) 

ax_hit.set_title("Droplet Hit Location on Paper")
ax_hit.set_ylabel("Vertical Position (mm)") 
ax_hit.yaxis.set_major_formatter(ticker.FuncFormatter(mm_formatter))
ax_hit.grid(axis='y', linestyle=':', alpha=0.6)

# Hide X-axis entirely since it has no meaning in this 1D view
ax_hit.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

# Hit location dot
(hit_dot,) = ax_hit.plot([], [], 'ro', markersize=15, label='Hit Location')

# --- Animation Functions ---

def init():
    # Reset both plots
    dot.set_data([], [])
    timer_text.set_text('')
    hit_dot.set_data([], [])
    # MUST return all blitted objects
    return dot, timer_text, hit_dot

def update(frame):
    # Get current time
    t_current = time_values[frame]
    
    # X position
    x_current = DROPLET_VELOCITY * np.linspace(0, t_current, max(2, frame))
    
    # Y position (Undeflected, always 0)
    y_current = np.zeros_like(x_current)

    # 1. Update the Path Plot (ax_path)
    dot.set_data([x_current[-1]], [0])

    # Update timer (convert to ms)
    t_ms = t_current * 1000
    timer_text.set_text(f"Time: {t_ms:.2f} ms")

    # 2. Update the Hit Plot (ax_hit)
    if x_current[-1] >= D:
        # Droplet has reached the paper. Plot it at the current y-position (which is 0)
        # We use an arbitrary x=0 in the hit plot's coordinate system
        hit_dot.set_data([0], [y_current[-1]]) 
    else:
        # Hide the hit dot until the paper is reached
        hit_dot.set_data([], [])

    # MUST return all blitted objects
    return dot, timer_text, hit_dot

# --- Animate ---
ani = FuncAnimation(
    fig, 
    update, 
    frames=frames,
    init_func=init, 
    blit=True,
    interval=50, 
    repeat=False
)

# Use tight_layout to prevent subplots from overlapping
plt.tight_layout()
plt.show()