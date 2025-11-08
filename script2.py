import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import Normalize
import matplotlib.ticker as ticker
from helpers import *
from constants import *
from calculations import *

# --- 3. Setup the Plot and Static Geometry ---
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlim(-0.5e-3, D + 0.5e-3)
ax.set_ylim(-y_min_max_visible, y_min_max_visible) 

ax.xaxis.set_major_formatter(ticker.FuncFormatter(mm_formatter))
ax.yaxis.set_major_formatter(ticker.FuncFormatter(mm_formatter))

ax.set_title(f'CIJ Simulation (Full Time: {N_dots_total} dots) | V_max={V_max_practical:.0f} V')
ax.set_xlabel('Horizontal Distance (mm)')
ax.set_ylabel('Vertical Position (mm)')
ax.grid(True, linestyle=':', alpha=0.6)

# Inkjet Droplet Gun
init_gun(ax)

# Capacitor Plates
init_capacitor(ax, L_gun_to_cap)

# Paper
ax.axvline(x=D, color='blue', linestyle='--', linewidth=2, label='Paper Target')

ax.legend(loc='upper right')
    
norm = Normalize(vmin=np.min(V_required_full), vmax=np.max(V_required_full))

# Initialize Plot Objects
all_flying_droplets = ax.scatter([], [], s=30, zorder=5, label='Flying Droplets')
saved_dots, = ax.plot([], [], 'o', color='black', markersize=6, alpha=1.0, label='Saved Dot')

time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
voltage_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)
droplet_index_text = ax.text(0.02, 0.85, '', transform=ax.transAxes)
hit_info_text = ax.text(0.02, 0.02, '', color='red', fontsize=10, 
                        ha='left', va='bottom', transform=ax.transAxes)

# --- 4. Animation Functions ---
def calculate_position(idx, t_flight):
    V = V_required_full[idx] 
    a_y = (DROPLET_CHARGE / m) * (V / W)
    x = Vx * t_flight
    
    if x <= L_gun_to_cap:
        y = 0.0
    elif x <= L_gun_to_cap + CAPACITOR_LENGTH:
        t_inside = t_flight - (L_gun_to_cap / Vx)
        y = 0.5 * a_y * t_inside**2
    else:
        t_inside = CAPACITOR_LENGTH / Vx
        t_outside = t_flight - (L_gun_to_cap + CAPACITOR_LENGTH) / Vx
        V_y_exit = a_y * t_inside
        y_exit = 0.5 * a_y * t_inside**2
        y = y_exit + V_y_exit * t_outside
        
    return x, y, V

def init():
    all_flying_droplets.set_offsets(np.empty((0, 2)))
    saved_dots.set_data([], [])
    time_text.set_text('')
    voltage_text.set_text('')
    droplet_index_text.set_text('')
    hit_info_text.set_text('')
    return all_flying_droplets, saved_dots, time_text, voltage_text, droplet_index_text, hit_info_text

def animate(frame):
    t_global = frame * GLOBAL_TIME_STEP 
    current_firing_index = int(t_global // T_interval)
    num_fired = current_firing_index + 1
    
    flying_positions = []
    flying_voltages = []

    start_dot_index = max(0, current_firing_index - MAX_DROPS_IN_FLIGHT + 1)
    end_dot_index = min(num_fired, N_dots_total)

    for i in range(start_dot_index, end_dot_index):
        t_fire_time = i * T_interval
        t_since_fire = t_global - t_fire_time
        
        if 0 <= t_since_fire < T_total_flight:
            x, y, V = calculate_position(i, t_since_fire)
            
            if i in animation_indices:
                flying_positions.append([x, y])
                flying_voltages.append(V)
            
        
    if flying_positions:
        flying_positions = np.array(flying_positions)
        all_flying_droplets.set_offsets(flying_positions)
        colors = plt.cm.coolwarm(norm(flying_voltages))
        all_flying_droplets.set_color(colors)
    else:
        all_flying_droplets.set_offsets(np.empty((0, 2)))


    hit_check_index = int(np.floor((t_global - T_total_flight) / T_interval))
    
    if hit_check_index >= 0 and hit_check_index < N_dots_total:
        t_prev_global = (frame - 1) * GLOBAL_TIME_STEP
        prev_hit_check_index = int(np.floor((t_prev_global - T_total_flight) / T_interval))
        
        if hit_check_index != prev_hit_check_index:
            
            if hit_check_index in animation_indices:
                y_target = y_positions[hit_check_index]
                
                hit_x = np.append(saved_dots.get_xdata(), D)
                hit_y = np.append(saved_dots.get_ydata(), y_target)
                saved_dots.set_data(hit_x, hit_y)
                
                hit_info_text.set_text(f'LAST HIT: Y={y_target*1000:.2f} mm')
            elif hit_check_index % 50 == 0: 
                 hit_info_text.set_text(f'Dot {hit_check_index} landed (not plotted)')
            else:
                hit_info_text.set_text('')
    else:
        if t_global >= T_last_land:
            hit_info_text.set_text(f'SIMULATION COMPLETE. Total Time: {T_last_land*1000:.3f} ms')
        elif t_global < T_total_flight:
            hit_info_text.set_text('')


    if current_firing_index < N_dots_total:
        V_current_firing = V_required_full[current_firing_index]
        dot_index_in_sequence = current_firing_index + 1
    else:
        V_current_firing = V_required_full[N_dots_total - 1]
        dot_index_in_sequence = N_dots_total
        
    time_text.set_text(f'Draw Time: {t_global*1000:.3f} ms')
    voltage_text.set_text(f'Applied Voltage $V$: {V_current_firing:.2f} V')
    droplet_index_text.set_text(f'Dot Fired: {dot_index_in_sequence} / {N_dots_total}')

    return all_flying_droplets, saved_dots, time_text, voltage_text, droplet_index_text, hit_info_text

# --- 5. Create and Display the Animation ---
ani = animation.FuncAnimation(
    fig, animate, init_func=init, 
    frames=TOTAL_ANIMATION_FRAMES, 
    interval=interval_ms, 
    blit=True,
    repeat=False
)

plt.show()