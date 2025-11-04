from math import sqrt, pi
from dataclasses import dataclass
import constants
    
def calc_capacitor_voltage(electric_field, vel_y):
    return electric_field * vel_y

def calc_electric_field(capacitor_voltage, width):
    return capacitor_voltage / width

def calc_velocity_vertical(accel_y, time):
    return accel_y * time

def calc_time_droplet_2_paper(distance, velocity):
    return distance / velocity

def calc_accel_vertical(charge, electric_field, mass):
    return charge * electric_field / mass

def calc_distance(vel_x, time):
    return vel_x * time

def calc_sphere_volume(diameter):
    radius = diameter / 2
    return (4/3) * pi * (radius ** 3)

def calc_mass(density, volume):
    return density * volume

def inches_2_meters(inches):
    return inches * constants.INCHES_2_METERS

def convert_mm_to_int(mm):
    return mm * 1E3

@dataclass
class Vector:
    x: float = 0.0
    y: float = 0.0
    
    def magnitude(self):
        return sqrt(self.x ** 2 + self.y ** 2)
    