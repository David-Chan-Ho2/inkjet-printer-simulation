from math import sqrt

def calc_capacitor_voltage(electric_field, vel_y):
    return electric_field * vel_y

def calc_velocity_vertical(accel_y, time):
    return accel_y * time

def calc_accel_vertical(charge, electric_field, distance):
    return charge * electric_field / distance

def calc_distance(vel_x, time):
    return vel_x * time

def calc_velocity_magnitude(vel_x, vel_y):
    return sqrt(vel_x ** 2 + vel_y ** 2)
