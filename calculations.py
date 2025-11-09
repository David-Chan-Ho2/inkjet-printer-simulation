import numpy as np
from constants import * 

# Droplet Kinematics
R = DROPLET_DIAMETER / 2
m = DROPLET_DENSITY * (4/3) * np.pi * R**3 
q_over_m_abs = abs(DROPLET_CHARGE) / m

# Geometric Parameters (Aliases)
W = CAPACITOR_WIDTH
D = TOTAL_DISTANCE
Vx = DROPLET_VELOCITY
L_gun_to_cap = D - CAPACITOR_LENGTH - CAPACITOR_DISTANCE

# Time and Firing Parameters (Based on Vx and geometry)
T_flight_capacitor = CAPACITOR_LENGTH / Vx
f_fire = 1.0 / T_flight_capacitor 
T_interval = T_flight_capacitor
N_dots_total = int(PAPER_HEIGHT * PRINTER_RESOLUTION) 

T_total_flight = D / Vx 
MAX_DROPS_IN_FLIGHT = int(np.ceil(T_total_flight / T_interval)) 

# Calculate the deflection constant (K_deflect)
K_deflect = (1.0 / q_over_m_abs) * (W * Vx**2) / (CAPACITOR_LENGTH * (CAPACITOR_LENGTH/2 + CAPACITOR_DISTANCE))

# Target Y-Positions
paper_height_m = PAPER_HEIGHT * INCHES_2_METERS 
y_full_max_deflection = paper_height_m / 2
N_dots_paper = N_dots_total
y_positions = np.linspace(-y_full_max_deflection, y_full_max_deflection, N_dots_paper)

# Required Voltage Array and Max Voltage
V_required_full = y_positions * K_deflect * np.sign(DROPLET_CHARGE)
V_max_practical = np.max(np.abs(V_required_full)) 

# Animation Parameters
animation_indices = np.linspace(0, N_dots_total - 1, N_dots_total, dtype=int)
y_positions_visible = y_positions[animation_indices] 

# Visual Scaling for Y-axis
y_min_max_visible = (W / 2) * 1.5 

# Final Animation Timing
T_last_fire = (N_dots_total - 1) * T_interval
T_last_land = T_last_fire + T_total_flight
GLOBAL_TIME_STEP = T_interval / FRAMES_PER_DOT_INTERVAL
TOTAL_ANIMATION_FRAMES = int(np.ceil(T_last_land / GLOBAL_TIME_STEP))
interval_ms = (GLOBAL_TIME_STEP * 1000) / ANIMATION_SPEED_FACTOR