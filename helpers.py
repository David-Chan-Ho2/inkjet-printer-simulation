from math import sqrt, pi
from dataclasses import dataclass
from matplotlib.patches import Rectangle 
from constants import GUN_X_START, GUN_Y_START, GUN_WIDTH, GUN_HEIGHT, TOTAL_DISTANCE, CAPACITOR_WIDTH, CAPACITOR_LENGTH 


# Visualization Setup Functions
def init_gun(ax):
    """Adds the static visual representation of the Inkjet Droplet Gun to the plot."""
    inkjet_gun = Rectangle((GUN_X_START, GUN_Y_START), GUN_WIDTH, GUN_HEIGHT, 
                       color='darkgray', fill=True, ec='black', lw=1, label='Inkjet Gun')
    ax.add_patch(inkjet_gun)

def init_capacitor(ax, L_gun_to_cap):
    """Draws the static capacitor plates and marker lines."""
    
    W = CAPACITOR_WIDTH # Use explicit variable for readability
    L = CAPACITOR_LENGTH
    
    # Capacitor Plates
    ax.plot([L_gun_to_cap, L_gun_to_cap + L], [W/2, W/2], 'k-', linewidth=4, label='Capacitor')
    ax.plot([L_gun_to_cap, L_gun_to_cap + L], [-W/2, -W/2], 'k-', linewidth=4)
    
    # Start and End Marker Lines
    ax.axvline(x=L_gun_to_cap, color='gray', linestyle=':', linewidth=1)
    ax.axvline(x=L_gun_to_cap + L, color='gray', linestyle=':', linewidth=1)


def init_paper(ax):
    ax.axvline(x=TOTAL_DISTANCE, color='blue', linestyle='--', linewidth=2, label='Paper Target')

#  Kinematics and Physics Calculation Functions 

def calc_sphere_volume(diameter):
    """Calculates the volume of a sphere given its diameter."""
    radius = diameter / 2
    return (4/3) * pi * (radius ** 3)

def calc_mass(density, volume):
    """Calculates mass given density and volume."""
    return density * volume

def calc_accel_vertical(charge, electric_field, mass):
    """Calculates vertical acceleration from electrostatic force (F=qE)."""
    return charge * electric_field / mass

def calc_velocity_vertical(accel_y, time):
    """Calculates vertical velocity (V = a*t)."""
    return accel_y * time

def calc_electric_field(capacitor_voltage, width):
    """Calculates electric field strength (E = V/d)."""
    return capacitor_voltage / width

def calc_capacitor_voltage(electric_field, width):
    """Calculates required voltage (V = E*d)."""
    return electric_field * width

# Time, Distance, and Formatting Utilities

def calc_distance(vel_x, time):
    """Calculates distance traveled (d = v*t)."""
    return vel_x * time

def calc_time_droplet_2_paper(distance, velocity):
    """Calculates time taken to travel a distance at constant velocity."""
    return distance / velocity

def mm_formatter(x, pos):
    """Formats axis labels from meters (m) to millimeters (mm)."""
    return f'{x*1000:.1f}' 

def convert_mm_to_int(mm):
    """Converts a value from millimeters (mm) to meters (m)."""
    return mm * 1E3


# Data Structures

@dataclass
class Vector:
    """A simple class for handling 2D vectors."""
    x: float = 0.0
    y: float = 0.0
    
    def magnitude(self):
        """Calculates the magnitude (length) of the vector."""
        return sqrt(self.x ** 2 + self.y ** 2)