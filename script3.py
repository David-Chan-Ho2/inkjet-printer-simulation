import numpy as np
import matplotlib.pyplot as plt
from constants import *

T = CAPACITOR_LENGTH / DROPLET_VELOCITY    # Time droplet spends inside capacitor (s)

# Number of droplets
N = 12

# Voltage applied for each droplet (example staircase pattern)
# Replace with zeros for drawing letter "I"
voltages = np.array([0, 4, 8, 4, 0, -4, -8, -4, 0, 4, 0, 0])

# -----------------------------
# Generate staircase timing
# -----------------------------
# Time boundaries between droplets
time_edges = np.arange(N + 1) * T

# -----------------------------
# Plotting
# -----------------------------
plt.figure(figsize=(8, 4))

for i in range(N):
    # Horizontal line for each droplet's voltage
    plt.hlines(voltages[i], time_edges[i], time_edges[i+1], linewidth=2)
    
    # Vertical transition line between steps (except last)
    if i < N - 1:
        plt.vlines(time_edges[i+1], voltages[i], voltages[i+1], linewidth=1)

plt.xlabel("Time (s)", fontsize=12)
plt.ylabel("Applied Voltage V(t)", fontsize=12)
plt.title("Staircase Voltage Profile (Per Droplet)", fontsize=14)
plt.grid(True, alpha=0.3)

plt.show()
