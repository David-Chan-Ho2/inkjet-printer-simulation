import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import Normalize
import matplotlib.ticker as ticker
from helpers import *
from constants import *

DROPLET_VELOCITY *= 2
R = DROPLET_DIAMETER / 2
m = DROPLET_DENSITY * (4/3) * np.pi * R**3 
q_over_m_abs = abs(DROPLET_CHARGE) / m

L_gun_to_cap = TOTAL_DISTANCE - CAPACITOR_LENGTH - CAPACITOR_DISTANCE
W = CAPACITOR_WIDTH
D = TOTAL_DISTANCE
Vx = DROPLET_VELOCITY

T_flight_capacitor = CAPACITOR_LENGTH / Vx
T_interval = T_flight_capacitor
N_dots_total = int(PAPER_HEIGHT * PRINTER_RESOLUTION) 

T_total_flight = D / Vx 
MAX_DROPS_IN_FLIGHT = int(np.ceil(T_total_flight / T_interval)) 

paper_height_m = PAPER_HEIGHT * INCHES_2_METERS 
y_full_max_deflection = paper_height_m / 2
N_dots_paper = N_dots_total

K_deflect = (1.0 / q_over_m_abs) * (W * Vx**2) / (CAPACITOR_LENGTH * (CAPACITOR_LENGTH/2 + CAPACITOR_DISTANCE))

y_positions = np.linspace(-y_full_max_deflection, y_full_max_deflection, N_dots_paper)
animation_indices = np.linspace(0, N_dots_paper - 1, N_dots_total, dtype=int)
y_positions_visible = y_positions[animation_indices] 

V_required_full = y_positions * K_deflect * np.sign(DROPLET_CHARGE)

V_max_practical = np.max(np.abs(V_required_full)) 

FRAMES_PER_DOT_INTERVAL = 2
T_last_fire = (N_dots_total - 1) * T_interval
T_last_land = T_last_fire + T_total_flight
GLOBAL_TIME_STEP = T_interval / FRAMES_PER_DOT_INTERVAL
TOTAL_ANIMATION_FRAMES = int(np.ceil(T_last_land / GLOBAL_TIME_STEP))
ANIMATION_SPEED_FACTOR = 50000 

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8))  

ax1.set_xlim(-0.5e-3, D + 0.5e-3)
ax1.set_ylim(-y_full_max_deflection, y_full_max_deflection)
ax1.xaxis.set_major_formatter(ticker.FuncFormatter(mm_formatter))
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(mm_formatter))
ax1.set_title('Simulation')
ax1.set_xlabel('Horizontal Distance (mm)')
ax1.set_ylabel('Vertical Position (mm)')
ax1.grid(True, linestyle=':', alpha=0.6)

ax2.set_ylim(-y_full_max_deflection, y_full_max_deflection)
ax2.xaxis.set_major_formatter(ticker.FuncFormatter(mm_formatter))
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(mm_formatter))
ax2.set_title('Paper - Hit Positions')
ax2.set_ylabel('Vertical Position (mm)')
ax2.grid(True, linestyle=':', alpha=0.6)

init_gun(ax1)

init_capacitor(ax1, L_gun_to_cap)

ax1.axvline(x=D, color='blue', linestyle='--', linewidth=2, label='Paper Target')
ax1.legend(loc='upper right')
    
norm = Normalize(vmin=np.min(V_required_full), vmax=np.max(V_required_full))

all_flying_droplets = ax1.scatter([], [], s=30, zorder=5, label='Flying Droplets')
saved_dots_flight, = ax1.plot([], [], 'o', color='black', markersize=6, alpha=1.0, label='Landed Dots')

paper_dots, = ax2.plot([], [], 'o', color='red', markersize=4, alpha=0.7, label='Hit Positions')

time_text = ax1.text(0.02, 0.98, '', transform=ax1.transAxes)
droplet_index_text = ax1.text(0.02, 0.94, '', transform=ax1.transAxes)
hit_info_text = ax1.text(0.02, 0.02, '', color='red', fontsize=10, 
                        ha='left', va='bottom', transform=ax1.transAxes)

paper_progress_text = ax2.text(0.02, 0.98, '', transform=ax2.transAxes, fontsize=12)

hit_positions_y = []

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
    saved_dots_flight.set_data([], [])
    paper_dots.set_data([], [])
    time_text.set_text('')
    droplet_index_text.set_text('')
    hit_info_text.set_text('')
    paper_progress_text.set_text('Paper Hits: 0')
    return all_flying_droplets, saved_dots_flight, paper_dots, time_text, droplet_index_text, hit_info_text, paper_progress_text

def animate(frame):
    global hit_positions_y
    
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
                
                hit_x = np.append(saved_dots_flight.get_xdata(), D)
                hit_y = np.append(saved_dots_flight.get_ydata(), y_target)
                saved_dots_flight.set_data(hit_x, hit_y)
                
                hit_positions_y.append(y_target)
                paper_dots.set_data(np.zeros(len(hit_positions_y)), hit_positions_y)
                
                hit_info_text.set_text(f'LAST HIT: Y={y_target*1000:.2f} mm')
                paper_progress_text.set_text(f'Paper Hits: {len(hit_positions_y)}')
                
            elif hit_check_index % 50 == 0: 
                 hit_info_text.set_text(f'Dot {hit_check_index} landed (not plotted)')
            else:
                hit_info_text.set_text('')
    else:
        if t_global >= T_last_land:
            hit_info_text.set_text(f'SIMULATION COMPLETE. Total Time: {T_last_land*1000:.3f} ms')
            paper_progress_text.set_text(f'Paper Hits: {len(hit_positions_y)} (COMPLETE)')
        elif t_global < T_total_flight:
            hit_info_text.set_text('')

    if current_firing_index < N_dots_total:
        V_current_firing = V_required_full[current_firing_index]
        dot_index_in_sequence = current_firing_index + 1
    else:
        V_current_firing = V_required_full[N_dots_total - 1]
        dot_index_in_sequence = N_dots_total
        
    time_text.set_text(f'Draw Time: {t_global*1000:.3f} ms')
    droplet_index_text.set_text(f'Dot Fired: {dot_index_in_sequence} / {N_dots_total}')

    return all_flying_droplets, saved_dots_flight, paper_dots, time_text, droplet_index_text, hit_info_text, paper_progress_text

interval_ms = (GLOBAL_TIME_STEP * 1000) / ANIMATION_SPEED_FACTOR

print(f"Total theoretical simulation time: {T_last_land*1000:.3f} ms")
print(f"Total animation frames: {TOTAL_ANIMATION_FRAMES}")

ani = animation.FuncAnimation(
    fig, animate, init_func=init, 
    frames=TOTAL_ANIMATION_FRAMES, 
    interval=interval_ms, 
    blit=True,
    repeat=False
)

plt.tight_layout()
plt.show()
