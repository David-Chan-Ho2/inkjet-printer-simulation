import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

# Parameters
V1_max = 10000  # 10 kV
V2_max = 7730   # 7.73 kV
droplets_vertical = 20  # Reduced for smoother animation
droplets_horizontal = 15

# Capacitor dimensions
L1a = 0.01  
L1b = 0.01 
W1 = 0.001 
W2 = 0.001 
L2 = 0.00125 

# Physical constants
v_x = 100  # m/s
q_over_m = 1.397e-4 * v_x**2  # From earlier calculation

# Create figure
fig = plt.figure(figsize=(16, 8))
ax1 = fig.add_subplot(121, projection='3d')  # 3D view
ax2 = fig.add_subplot(222)  # Voltage V1
ax3 = fig.add_subplot(224)  # Voltage V2

# Initialize storage for animation
trajectories = []
current_droplet = 0
plotted_droplets = []

# Capacitor positions in 3D space
cap1_z_start, cap1_z_end = 0, L1a
cap2_z_start, cap2_z_end = L1a, L1a + L1b
paper_z = L1a + L1b + L2

# Generate H shape coordinates
def generate_H_coordinates():
    # Left vertical
    x_left = np.full(droplets_vertical, -0.10795)
    y_left = np.linspace(-0.1397, 0.1397, droplets_vertical)
    
    # Horizontal bar
    x_bar = np.linspace(-0.10795, 0.10795, droplets_horizontal)
    y_bar = np.zeros(droplets_horizontal)
    
    # Right vertical
    x_right = np.full(droplets_vertical, 0.10795)
    y_right = np.linspace(0.1397, -0.1397, droplets_vertical)
    
    x_positions = np.concatenate([x_left, x_bar, x_right])
    y_positions = np.concatenate([y_left, y_bar, y_right])
    
    return x_positions, y_positions

target_x, target_y = generate_H_coordinates()

# Calculate required voltages for each target position
def calculate_voltages(target_x, target_y):
    # Simplified calculation - in reality would use the full deflection equations
    V1_required = (target_y / 0.1397) * V1_max
    V2_required = (target_x / 0.10795) * V2_max
    return V1_required, V2_required

V1_required, V2_required = calculate_voltages(target_x, target_y)

# Set up 3D plot
def setup_3d_plot():
    ax1.clear()
    
    # Draw capacitors
    # Capacitor 1 (vertical deflection - horizontal plates)
    cap1_x = [-W1/2, W1/2, W1/2, -W1/2, -W1/2]
    cap1_y = [-W1/2, -W1/2, W1/2, W1/2, -W1/2]
    cap1_z = [cap1_z_start, cap1_z_start, cap1_z_start, cap1_z_start, cap1_z_start]
    ax1.plot(cap1_x, cap1_y, cap1_z, 'b-', alpha=0.6, label='Capacitor 1')
    ax1.plot(cap1_x, cap1_y, [cap1_z_end]*5, 'b-', alpha=0.6)
    
    # Capacitor 2 (horizontal deflection - vertical plates)
    cap2_x = [-W2/2, W2/2, W2/2, -W2/2, -W2/2]
    cap2_y = [-0.005, -0.005, 0.005, 0.005, -0.005]  # Taller plates
    cap2_z = [cap2_z_start, cap2_z_start, cap2_z_start, cap2_z_start, cap2_z_start]
    ax1.plot(cap2_x, cap2_y, cap2_z, 'r-', alpha=0.6, label='Capacitor 2')
    ax1.plot(cap2_x, cap2_y, [cap2_z_end]*5, 'r-', alpha=0.6)
    
    # Draw paper
    paper_x = [-0.15, 0.15, 0.15, -0.15, -0.15]
    paper_y = [-0.2, -0.2, 0.2, 0.2, -0.2]
    ax1.plot(paper_x, paper_y, [paper_z]*5, 'g-', alpha=0.3, label='Paper')
    
    ax1.set_xlabel('X (m)')
    ax1.set_ylabel('Y (m)')
    ax1.set_zlabel('Z (m)')
    ax1.set_title('3D Droplet Motion - Drawing Letter "H"')
    ax1.legend()

# Set up voltage plots
def setup_voltage_plots():
    ax2.clear()
    ax3.clear()
    
    ax2.set_ylabel('V1 (kV)')
    ax2.set_title('Vertical Deflection Capacitor Voltage')
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(-12, 12)
    
    ax3.set_ylabel('V2 (kV)')
    ax3.set_xlabel('Droplet Number')
    ax3.set_title('Horizontal Deflection Capacitor Voltage')
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim(-9, 9)

# Calculate droplet trajectory
def calculate_trajectory(V1, V2, num_points=20):
    z_positions = np.linspace(0, paper_z, num_points)
    x_positions = []
    y_positions = []
    
    for z in z_positions:
        if z <= cap1_z_end:  # In capacitor 1
            t = z / v_x
            # Vertical acceleration in cap1
            a_y1 = (q_over_m * V1) / W1
            y = 0.5 * a_y1 * t**2
            x = 0
        elif z <= cap2_z_end:  # In capacitor 2
            t_cap1 = cap1_z_end / v_x
            a_y1 = (q_over_m * V1) / W1
            v_y_after_cap1 = a_y1 * t_cap1
            
            t_in_cap2 = (z - cap1_z_end) / v_x
            # Horizontal acceleration in cap2
            a_x2 = (q_over_m * V2) / W2
            x = 0.5 * a_x2 * t_in_cap2**2
            y = 0.5 * a_y1 * t_cap1**2 + v_y_after_cap1 * t_in_cap2
        else:  # After capacitors, drift to paper
            t_cap1 = cap1_z_end / v_x
            t_cap2 = (cap2_z_end - cap1_z_end) / v_x
            a_y1 = (q_over_m * V1) / W1
            a_x2 = (q_over_m * V2) / W2
            
            v_y_after_cap1 = a_y1 * t_cap1
            v_x_after_cap2 = a_x2 * t_cap2
            
            t_drift = (z - cap2_z_end) / v_x
            
            x = 0.5 * a_x2 * t_cap2**2 + v_x_after_cap2 * t_drift
            y = 0.5 * a_y1 * t_cap1**2 + v_y_after_cap1 * (t_cap2 + t_drift)
        
        x_positions.append(x)
        y_positions.append(y)
    
    return x_positions, y_positions, z_positions

# Animation function
def animate(frame):
    global current_droplet, plotted_droplets
    
    if current_droplet >= len(target_x):
        return
    
    setup_3d_plot()
    setup_voltage_plots()
    
    # Plot all previous droplets on paper
    for i, (x, y) in enumerate(plotted_droplets):
        ax1.scatter(x, y, paper_z, c='blue', s=10, alpha=0.6)
    
    # Calculate and plot current droplet trajectory
    V1 = V1_required[current_droplet]
    V2 = V2_required[current_droplet]
    
    x_traj, y_traj, z_traj = calculate_trajectory(V1, V2)
    ax1.plot(x_traj, y_traj, z_traj, 'k-', alpha=0.5, linewidth=1)
    ax1.scatter([x_traj[-1]], [y_traj[-1]], [paper_z], c='red', s=50)
    
    # Update voltage plots
    ax2.plot(range(current_droplet + 1), V1_required[:current_droplet + 1] / 1000, 'b-', linewidth=2)
    ax3.plot(range(current_droplet + 1), V2_required[:current_droplet + 1] / 1000, 'r-', linewidth=2)
    
    # Add current voltage values
    ax2.scatter([current_droplet], [V1/1000], c='blue', s=50, zorder=5)
    ax3.scatter([current_droplet], [V2/1000], c='red', s=50, zorder=5)
    
    # Store plotted droplet
    plotted_droplets.append((x_traj[-1], y_traj[-1]))
    
    current_droplet += 1
    
    # Add progress information
    ax1.text2D(0.02, 0.98, f'Droplet: {current_droplet}/{len(target_x)}', 
               transform=ax1.transAxes, fontsize=12,
               bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

# Create animation
print("Creating 3D animation...")
ani = FuncAnimation(fig, animate, frames=len(target_x), 
                   interval=50, repeat=False, blit=False)

# Save animation (optional)
ani.save('H_letter_animation.mp4', writer='ffmpeg', fps=20, dpi=100)

plt.tight_layout()
plt.show()

# Print animation summary
print(f"\nAnimation Summary:")
print(f"Total droplets in animation: {len(target_x)}")
print(f"Left vertical stroke: {droplets_vertical} droplets")
print(f"Horizontal bar: {droplets_horizontal} droplets") 
print(f"Right vertical stroke: {droplets_vertical} droplets")
print(f"Capacitor 1: {L1a*1000} mm long, ±{V1_max/1000} kV")
print(f"Capacitor 2: {L1b*1000} mm long, ±{V2_max/1000} kV")