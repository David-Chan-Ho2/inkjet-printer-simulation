from helpers import Vector, calc_accel_vertical, calc_velocity_vertical, calc_sphere_volume, calc_mass, calc_electric_field, inches_2_meters, calc_time_droplet_2_paper
import constants
import matplotlib.pyplot as plt

def run_script1():
    voltage = 0
    accel = Vector()
    vel = Vector()
    
    electric_field = calc_electric_field(capacitor_voltage=voltage, width=constants.CAPACITOR_WIDTH)
    droplet_volume = calc_sphere_volume(diameter=constants.DROPLET_DIAMETER)
    droplet_mass = calc_mass(density=constants.DROPLET_DENSITY, volume=droplet_volume)
    accel.y = calc_accel_vertical(charge=constants.DROPLET_CHARGE, electric_field=electric_field, mass=droplet_mass)
    time_droplet_2_paper = calc_time_droplet_2_paper(constants.DROPLET_GUN_DISTANCE, constants.DROPLET_VELOCITY)
    print(f"{time_droplet_2_paper:.2e} s") 
    
    for x in range(10):
        vel.y = calc_velocity_vertical(accel_y=accel.y, time=x)
        print(vel.y)
        
    
if __name__ == "__main__":
    run_script1()