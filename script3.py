import numpy as np
import matplotlib.pyplot as plt
import math
from constants import *

V_MAX_SAFE = 3000                 

R = DROPLET_DIAMETER / 2
volume = (4/3)*math.pi*R**3
m = DROPLET_DENSITY * volume
q = DROPLET_CHARGE

W  = CAPACITOR_WIDTH
L1 = CAPACITOR_LENGTH
L2 = CAPACITOR_DISTANCE
Vx = DROPLET_VELOCITY

q_over_m_abs = abs(q) / m
K_deflect = (1.0 / q_over_m_abs) * (W * Vx**2) / (L1*(L1/2 + L2))

y_max = V_MAX_SAFE / K_deflect        
height_printable = 2 * y_max           

print("\n===== PRINTABLE SIZE RESULTS =====")
print(f"Maximum printable full height: {height_printable*1000:.3f} mm")

step_size = 0.085e-3      
N = int(height_printable / step_size)

y_positions = np.linspace(-y_max, y_max, N)

V_steps = y_positions * K_deflect * np.sign(q)

T = L1 / Vx
t_edges = np.arange(N+1) * T

plt.figure(figsize=(10,4))
plt.step(t_edges[:-1], V_steps, where='post')
plt.xlabel("Time (s)")
plt.ylabel("Voltage V(t) (Volts)")
plt.title("Staircase Voltage Profile for Printing Maximum Height 'I' (~6 mm tall)")
plt.grid(True)
plt.tight_layout()
plt.show()

print(f"Max required |V|: {np.max(np.abs(V_steps)):.1f} V (should be ~3000 V)")
print(f"Total number of droplets: {N}")
print(f"Time per droplet: {T*1e6:.2f} µs")
print(f"Total printing time: {N*T*1000:.3f} ms\n")
