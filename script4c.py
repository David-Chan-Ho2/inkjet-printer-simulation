import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import Normalize
import matplotlib.ticker as ticker
from helpers import *
from constants import *

DROPLET_DIAMETER *= 10

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

# Correct deflection constant calculation
distance_after_cap = CAPACITOR_DISTANCE
L_cap = CAPACITOR_LENGTH
K_deflect_correct = (m * W * Vx**2) / (abs(DROPLET_CHARGE) * (L_cap**2/2 + L_cap*distance_after_cap))

y_positions = np.linspace(-y_full_max_deflection, y_full_max_deflection, N_dots_paper)
animation_indices = np.linspace(0, N_dots_paper - 1, N_dots_total, dtype=int)

V_required_full = y_positions * K_deflect_correct * np.sign(DROPLET_CHARGE)

V_max_practical = np.max(np.abs(V_required_full)) 

print("=== CAPACITOR PLATE CONSTRAINTS ===")
print(f"Capacitor width (plate separation): {W*1000:.2f} mm")
print(f"Max allowed vertical displacement inside capacitor: ±{W/2*1000:.2f} mm")

FRAMES_PER_DOT_INTERVAL = 2
T_last_fire = (N_dots_total - 1) * T_interval
T_last_land = T_last_fire + T_total_flight
GLOBAL_TIME_STEP = T_interval / FRAMES_PER_DOT_INTERVAL
TOTAL_ANIMATION_FRAMES = int(np.ceil(T_last_land / GLOBAL_TIME_STEP))
ANIMATION_SPEED_FACTOR = 50000 

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8))  

# Left plot: Simulation
ax1.set_xlim(-0.5e-3, D + 0.5e-3)
ax1.set_ylim(-W/2 * 1.5, W/2 * 1.5)  # Zoom in to see capacitor region better
ax1.xaxis.set_major_formatter(ticker.FuncFormatter(mm_formatter))
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(mm_formatter))
ax1.set_title('Droplet Simulation')
ax1.set_xlabel('Horizontal Distance (mm)')
ax1.set_ylabel('Vertical Position (mm)')
ax1.grid(True, linestyle=':', alpha=0.6)

# Highlight capacitor region and plates
capacitor_x_start = L_gun_to_cap
capacitor_x_end = L_gun_to_cap + CAPACITOR_LENGTH

# Draw capacitor plates
ax1.axhline(y=W/2, xmin=capacitor_x_start/D, xmax=capacitor_x_end/D, 
           color='red', linewidth=3, linestyle='-', label='Capacitor Plates')
ax1.axhline(y=-W/2, xmin=capacitor_x_start/D, xmax=capacitor_x_end/D, 
           color='red', linewidth=3, linestyle='-')
ax1.axvspan(capacitor_x_start, capacitor_x_end, alpha=0.1, color='red', 
           label='Capacitor Region')

# Right plot: Voltage Profile
ax2.set_title('Applied Voltage Profile')
ax2.set_xlabel('Time (ms)')
ax2.set_ylabel('Voltage (V)')
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)

# Set voltage plot limits
V_min_actual = np.min(V_required_full)
V_max_actual = np.max(V_required_full)
V_range = V_max_actual - V_min_actual
V_min_plot = V_min_actual - 0.1 * V_range
V_max_plot = V_max_actual + 0.1 * V_range
ax2.set_ylim(V_min_plot, V_max_plot)
ax2.set_xlim(0, T_last_land * 1000)

init_gun(ax1)
ax1.axvline(x=D, color='blue', linestyle='--', linewidth=2, label='Paper Target')
ax1.legend(loc='upper right')
    
norm = Normalize(vmin=np.min(V_required_full), vmax=np.max(V_required_full))

# Create simulation plot elements
all_flying_droplets = ax1.scatter([], [], s=30, zorder=5, label='Flying Droplets')
failed_droplets = ax1.scatter([], [], s=40, marker='x', color='red', zorder=6, 
                             label='Failed (Hit Plate)')
saved_dots_flight, = ax1.plot([], [], 'o', color='green', markersize=6, alpha=1.0, 
                             label='Successfully Landed')

# Create voltage plot elements
voltage_line, = ax2.plot([], [], 'b-', linewidth=2, label='Applied Voltage')
voltage_dot, = ax2.plot([], [], 'ro', markersize=6, alpha=0.8, label='Current Voltage')
current_voltage_text = ax2.text(0.02, 0.98, '', transform=ax2.transAxes, fontsize=10,
                               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# Time markers for voltage plot
ax2.axvline(x=0, color='green', linestyle='--', alpha=0.5, label='Start')
ax2.axvline(x=T_last_land*1000, color='red', linestyle='--', alpha=0.5, label='End')
ax2.legend(loc='upper right')

time_text = ax1.text(0.02, 0.98, '', transform=ax1.transAxes,
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
droplet_index_text = ax1.text(0.02, 0.94, '', transform=ax1.transAxes,
                             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# Statistics
success_stats_text = ax1.text(0.02, 0.78, 'Success: 0\nFailed: 0', transform=ax1.transAxes,
                             fontsize=10, bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

# Data structures to track droplet status
class DropletStatus:
    def __init__(self):
        self.successful_droplets = []  # Indices of droplets that made it
        self.failed_droplets = []      # Indices of droplets that hit plates
        self.droplet_positions = {}    # Store positions for animation
        self.droplet_voltages = {}     # Store voltages for animation
        self.droplet_status = {}       # Track status: 'flying', 'failed', 'landed'
        self.failure_positions = []    # Store where droplets failed
        
droplet_status = DropletStatus()
hit_positions_y = []
voltage_time_data = []
voltage_value_data = []

def calculate_position(idx, t_flight):
    V = V_required_full[idx] 
    a_y = (DROPLET_CHARGE / m) * (V / W)
    x = Vx * t_flight
    
    if x <= L_gun_to_cap:
        y = 0.0
        status = 'before_capacitor'
    elif x <= L_gun_to_cap + CAPACITOR_LENGTH:
        t_inside = t_flight - (L_gun_to_cap / Vx)
        y = 0.5 * a_y * t_inside**2
        status = 'inside_capacitor'
    else:
        t_inside = CAPACITOR_LENGTH / Vx
        t_outside = t_flight - (L_gun_to_cap + CAPACITOR_LENGTH) / Vx
        V_y_exit = a_y * t_inside
        y_exit = 0.5 * a_y * t_inside**2
        y = y_exit + V_y_exit * t_outside
        status = 'after_capacitor'
        
    return x, y, V, status

def check_capacitor_clearance(x, y, status):
    """Check if droplet clears capacitor plates"""
    capacitor_x_start = L_gun_to_cap
    capacitor_x_end = L_gun_to_cap + CAPACITOR_LENGTH
    
    # If droplet is inside capacitor region
    if capacitor_x_start <= x <= capacitor_x_end:
        # Check if it hits the plates (±W/2)
        if abs(y) >= W/2:
            return False  # Hits plate
    return True  # Clears capacitor

def init():
    # Initialize simulation plot
    all_flying_droplets.set_offsets(np.empty((0, 2)))
    failed_droplets.set_offsets(np.empty((0, 2)))
    saved_dots_flight.set_data([], [])
    
    # Initialize voltage plot
    voltage_line.set_data([], [])
    voltage_dot.set_data([], [])
    
    time_text.set_text('')
    droplet_index_text.set_text('')
    current_voltage_text.set_text('Voltage: 0.00 V')
    success_stats_text.set_text('Success: 0\nFailed: 0')
    
    # Reset droplet status
    droplet_status.successful_droplets = []
    droplet_status.failed_droplets = []
    droplet_status.droplet_positions = {}
    droplet_status.droplet_voltages = {}
    droplet_status.droplet_status = {}
    droplet_status.failure_positions = []
    
    return (all_flying_droplets, failed_droplets, saved_dots_flight, 
            voltage_line, voltage_dot, time_text, droplet_index_text, current_voltage_text, success_stats_text)

def animate(frame):
    global hit_positions_y, voltage_time_data, voltage_value_data
    
    t_global = frame * GLOBAL_TIME_STEP 
    current_firing_index = int(t_global // T_interval)
    num_fired = current_firing_index + 1
    
    # Update voltage profile
    if current_firing_index < N_dots_total:
        V_current = V_required_full[current_firing_index]
        t_current = current_firing_index * T_interval
        
        if t_global >= t_current and len(voltage_time_data) <= current_firing_index:
            voltage_time_data.append(t_current * 1000)
            voltage_value_data.append(V_current)
    
    # Update voltage plot
    if voltage_time_data:
        voltage_line.set_data(voltage_time_data, voltage_value_data)
        
        if current_firing_index < len(voltage_time_data):
            voltage_dot.set_data(
                [voltage_time_data[current_firing_index]], 
                [voltage_value_data[current_firing_index]]
            )
            current_voltage_text.set_text(f'Voltage: {voltage_value_data[current_firing_index]:.2f} V')
    
    # Track flying and failed droplets
    flying_positions = []
    flying_voltages = []
    failed_positions = []
    
    start_dot_index = max(0, current_firing_index - MAX_DROPS_IN_FLIGHT + 1)
    end_dot_index = min(num_fired, N_dots_total)

    for i in range(start_dot_index, end_dot_index):
        # Skip if droplet already failed
        if i in droplet_status.failed_droplets:
            continue
            
        t_fire_time = i * T_interval
        t_since_fire = t_global - t_fire_time
        
        if 0 <= t_since_fire < T_total_flight:
            x, y, V, status = calculate_position(i, t_since_fire)
            
            # Check if droplet clears capacitor plates
            if check_capacitor_clearance(x, y, status):
                # Store position for tracking
                droplet_status.droplet_positions[i] = (x, y)
                droplet_status.droplet_voltages[i] = V
                droplet_status.droplet_status[i] = 'flying'
                
                if i in animation_indices:
                    flying_positions.append([x, y])
                    flying_voltages.append(V)
            else:
                # Droplet hit capacitor plate
                if i not in droplet_status.failed_droplets:
                    droplet_status.failed_droplets.append(i)
                    droplet_status.failure_positions.append((x, y))
                    droplet_status.droplet_status[i] = 'failed'
                    
                    if i in animation_indices:
                        failed_positions.append([x, y])
                
                # Remove from flying positions if it was there
                droplet_status.droplet_positions.pop(i, None)
                droplet_status.droplet_voltages.pop(i, None)
    
    # Update flying droplets display
    if flying_positions:
        flying_positions = np.array(flying_positions)
        all_flying_droplets.set_offsets(flying_positions)
        colors = plt.cm.coolwarm(norm(flying_voltages))
        all_flying_droplets.set_color(colors)
    else:
        all_flying_droplets.set_offsets(np.empty((0, 2)))
    
    # Update failed droplets display
    if failed_positions:
        failed_droplets.set_offsets(np.array(failed_positions))
    else:
        failed_droplets.set_offsets(np.empty((0, 2)))
    
    # Check for successful landings
    hit_check_index = int(np.floor((t_global - T_total_flight) / T_interval))
    
    if hit_check_index >= 0 and hit_check_index < N_dots_total:
        t_prev_global = (frame - 1) * GLOBAL_TIME_STEP
        prev_hit_check_index = int(np.floor((t_prev_global - T_total_flight) / T_interval))
        
        if hit_check_index != prev_hit_check_index:
            # Only process if droplet wasn't already failed
            if (hit_check_index not in droplet_status.failed_droplets and 
                hit_check_index in animation_indices):
                
                y_target = y_positions[hit_check_index]
                
                # Mark as successful
                if hit_check_index not in droplet_status.successful_droplets:
                    droplet_status.successful_droplets.append(hit_check_index)
                    droplet_status.droplet_status[hit_check_index] = 'landed'
                
                # Add to landed dots display
                hit_x = np.append(saved_dots_flight.get_xdata(), D)
                hit_y = np.append(saved_dots_flight.get_ydata(), y_target)
                saved_dots_flight.set_data(hit_x, hit_y)
                
                hit_positions_y.append(y_target)
             
    
    # Update statistics
    success_count = len(droplet_status.successful_droplets)
    failed_count = len(droplet_status.failed_droplets)
    success_stats_text.set_text(f'Success: {success_count}\nFailed: {failed_count}')
    
    # Update time and index display
    if current_firing_index < N_dots_total:
        dot_index_in_sequence = current_firing_index + 1
    else:
        dot_index_in_sequence = N_dots_total
        
    time_text.set_text(f'Time: {t_global*1000:.3f} ms')
    droplet_index_text.set_text(f'Dot: {dot_index_in_sequence}/{N_dots_total}')
    
    # Show completion message
    if t_global >= T_last_land:
        total_failed = len(droplet_status.failed_droplets)
        total_success = len(droplet_status.successful_droplets)
    
    return (all_flying_droplets, failed_droplets, saved_dots_flight, 
            voltage_line, voltage_dot, time_text, droplet_index_text)

interval_ms = (GLOBAL_TIME_STEP * 1000) / ANIMATION_SPEED_FACTOR

print(f"\n=== ANIMATION PARAMETERS ===")
print(f"Total simulation time: {T_last_land*1000:.3f} ms")
print(f"Number of dots: {N_dots_total}")
print(f"Droplets will be removed if they exceed ±{W/2*1000:.2f} mm in capacitor")

# Pre-calculate voltage profile
time_points = np.arange(0, N_dots_total) * T_interval * 1000
voltage_profile = V_required_full[:N_dots_total]
ax2.plot(time_points, voltage_profile, 'k--', alpha=0.3, linewidth=1, label='Complete Profile')

ani = animation.FuncAnimation(
    fig, animate, init_func=init, 
    frames=TOTAL_ANIMATION_FRAMES, 
    interval=interval_ms, 
    blit=False,  # Changed to False for better performance with multiple artists
    repeat=False
)

plt.tight_layout()
plt.show()

# Final statistics
print(f"\n=== FINAL STATISTICS ===")
print(f"Total droplets fired: {N_dots_total}")
print(f"Droplets that would hit capacitor plates: {len(droplet_status.failed_droplets)}")
print(f"Droplets that would successfully reach paper: {len(droplet_status.successful_droplets)}")

# Check which positions fail
if droplet_status.failed_droplets:
    print("\nDroplets that hit plates (indices):")
    for idx in droplet_status.failed_droplets[:10]:  # Show first 10
        y_target = y_positions[idx]
        V_applied = V_required_full[idx]
        print(f"  Index {idx}: y_target={y_target*1000:.2f} mm, V={V_applied:.2f} V")
    if len(droplet_status.failed_droplets) > 10:
        print(f"  ... and {len(droplet_status.failed_droplets)-10} more")