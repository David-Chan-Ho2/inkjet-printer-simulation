from helpers import calc_time_droplet_2_paper
import constants

def run_script1():
    distance = constants.DROPLET_GUN_DISTANCE
    velocity = constants.DROPLET_VELOCITY
    
    time_droplet_2_paper = calc_time_droplet_2_paper(distance=distance, velocity=velocity)
    
    print(f" {time_droplet_2_paper:.2e} s") 
    
if __name__ == "__main__":
    run_script1()