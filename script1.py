from helpers import calc_time_droplet_2_paper
import constants
import numpy as np
import matplotlib.pyplot as plt


def run_script1():
    distance = constants.DROPLET_GUN_DISTANCE
    velocity = constants.DROPLET_VELOCITY

    time_droplet_2_paper = calc_time_droplet_2_paper(distance=distance, velocity=velocity)

    print(f"Time to reach paper: {time_droplet_2_paper:.2e}s") 

    t = np.linspace(0, time_droplet_2_paper, 100)
    x = velocity * t
    
    t_ms = t * 1e3
    x_ms = x * 1e3

    plt.plot(t_ms , x_ms)
    plt.xlabel("Time (ms)")
    plt.ylabel("Horizontal Position (mm)")
    plt.title("Droplet Motion without Voltage")
    plt.show()
    
if __name__ == "__main__":
    run_script1()
