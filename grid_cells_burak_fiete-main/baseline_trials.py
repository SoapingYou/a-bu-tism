from claudestuff import simulate_and_decode

import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Now you can import your module normally
from RunTrial import RunTrial

from PathPlotter import PathPlotter

import numpy as np

def OU_increment(noise, tau, amp, dt):
    """
        Update OU process.

        :param float noise: current process value.
        :param float tau: relaxation time in seconds.
        :param float amp: scale of noise.
        :param float dt: time step length in seconds.
        :return update for OU process:
        :rtype float:
    """
    rng = np.random.default_rng()
    return -noise * dt / tau + rng.normal(loc=0.0, scale=amp * np.sqrt(dt))

baseline_tnum = 10
sim = 20000

base_model_i = RunTrial()
# pos_pred_baseline = np.zeros((10000, 2))
base_model_i.assembly_grid_cells()
base_model_i.get_random_walk()
base_model_i.run_trial(error_freq=1)
pos_pred_baseline = base_model_i.simulated_locations[:,1:]

#get input velocity, but it has OU noise
speed=base_model_i.speed
head_dir=base_model_i.head_dir
speed_noise = 0
dir_noise = 0
speed_tau = 2.0
dir_tau = 1.0
bio_speed_amp=0.05
bio_dir_amp=0.025
dt = 0.001
input_v = np.zeros((sim,2))

for t in range(sim):
    speed_noise += OU_increment(speed_noise, speed_tau, bio_speed_amp, dt)
    dir_noise += OU_increment(dir_noise, dir_tau, bio_dir_amp, dt)
    t_speed = max(0.0, speed[t] * (1 + speed_noise))
    t_headdir = head_dir[t] + dir_noise
    input_v[t] = np.array([t_speed * np.cos(t_headdir), t_speed*np.sin(t_headdir)])
print(input_v)

can_result = simulate_and_decode(input_v=input_v,n=40)

plotter = PathPlotter()
path_temp = np.zeros((3, sim, 2) )
path_temp[0] = pos_pred_baseline
path_temp[1] = can_result["pos"]
path_temp[2] = np.array([base_model_i.og_position_x, base_model_i.og_position_y]).T
plotter.paths(path_temp, colors=['blue', 'red','black'], labels=['base','can','true'])