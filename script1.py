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
D = TOTAL_DISTANCE

y_limit_m = (CAPACITOR_WIDTH  / 2) * 2.0 

fig, (ax_path, ax_hit) = plt.subplots(1, 2, figsize=(8, 8)) # 2 rows, 1 column

ax_path.set_xlim(0, D * 1.1)
ax_path.set_ylim(-y_limit_m, y_limit_m)

ax_path.xaxis.set_major_formatter(ticker.FuncFormatter(mm_formatter))
ax_path.yaxis.set_major_formatter(ticker.FuncFormatter(mm_formatter))

ax_path.set_title("Droplet Motion (Zoomed on Capacitor)")
ax_path.set_xlabel("Horizontal Distance (mm)")
ax_path.set_ylabel("Vertical Position (mm)") 
ax_path.grid(True, linestyle=':', alpha=0.6) 

init_capacitor(ax_path, L_gun_to_cap)
ax_path.axvline(x=D, color='blue', linestyle='--', linewidth=2, label='Paper Target')

(dot,) = ax_path.plot([], [], 'ko', markersize=10, label='Droplet')
ax_path.legend(loc='upper right')

timer_text = ax_path.text(0.7 * D, -y_limit_m * 0.9, '', fontsize=12, color='black')

ax_hit.set_ylim(-y_limit_m, y_limit_m)
ax_hit.set_xlim(-0.01, 0.01) 

ax_hit.set_title("Droplet Hit Location on Paper")
ax_hit.set_ylabel("Vertical Position (mm)") 
ax_hit.yaxis.set_major_formatter(ticker.FuncFormatter(mm_formatter))
ax_hit.grid(axis='y', linestyle=':', alpha=0.6)

ax_hit.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

(hit_dot,) = ax_hit.plot([], [], 'ro', markersize=15, label='Hit Location')

def init():
    dot.set_data([], [])
    timer_text.set_text('')
    hit_dot.set_data([], [])
    return dot, timer_text, hit_dot

def update(frame):
    t_current = time_values[frame]
    
    x_current = DROPLET_VELOCITY * np.linspace(0, t_current, max(2, frame))
    
    y_current = np.zeros_like(x_current)

    dot.set_data([x_current[-1]], [0])

    t_ms = t_current * 1000
    timer_text.set_text(f"Time: {t_ms:.2f} ms")

    if x_current[-1] >= D:
        hit_dot.set_data([0], [y_current[-1]]) 
    else:
        hit_dot.set_data([], [])

    return dot, timer_text, hit_dot

ani = FuncAnimation(
    fig, 
    update, 
    frames=frames,
    init_func=init, 
    blit=True,
    interval=50, 
    repeat=False
)

plt.tight_layout()
plt.show()