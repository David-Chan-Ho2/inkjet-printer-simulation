import matplotlib.pyplot as plt
import numpy as np
from constants import TOTAL_DISTANCE, DROPLET_VELOCITY
from helpers import convert_mm_to_int

DISTANCE = convert_mm_to_int(TOTAL_DISTANCE) 

t_travel = DISTANCE / DROPLET_VELOCITY
frames = 100
time_values = np.linspace(0, t_travel, frames)

# Setup figure
fig, ax = plt.subplots()
ax.set_xlim(0, DISTANCE)
ax.set_ylim(-1, 1)
ax.set_xlabel("Horizontal Distance (mm)")
ax.set_title("Droplet Motion")
