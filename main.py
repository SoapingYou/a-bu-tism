# Written by Sophie Yu. Finished 2:26 AM. Mistakes may have been made. 

from MouseMovement import main as pathMake
from grid_cells import Module 
from phases_to_location import phasesToLocation1D

import numpy as np

#arbitrary numbers, adjust till it looks right ;) . OR replace w a better func, idrc
def generate_error(k=0.1):
    return np.random()*k

NUM_OF_MODULOS = 10
SPATIAL_PHASES = 20
NEURONS_PER_PHASE = 20 # ts is NOT used yet lmao
 
# generate grid cell structure of NUM_OF_MODULOS modules, 
# each with 20 spatial phases, 20 neurons per phase
modules = [Module(spacing=25 * (1.65 ** i)) for i in range(NUM_OF_MODULOS)]
for module in modules:
    module.add_cells(SPATIAL_PHASES,SPATIAL_PHASES)

ts = 0.001 # in seconds, timestep
len = 4 # in seconds, simulation length
ticks = int(len/ts)
displacements_x, displacements_y = pathMake()
# check ts works yo
print(displacements_x, displacements_y)

# original velocities
og_velocities = np.zeros((2,ticks))
og_velocities[0,:] = np.array(displacements_x) / ts 
og_velocities[1,:] = np.array(displacements_y) / ts

# current phase of all modulos --> OVERSIMPLIFICATION AS OF NOW
phases = np.zeros((2,NUM_OF_MODULOS))

for t in range(ticks):
    # simulate velocity (with error).
    t_velocity = np.zeros(2)
    t_velocity[0] = og_velocities[0,t] + generate_error()
    t_velocity[1] = og_velocities[1,t] + generate_error()

    # update phase
    for i in range(NUM_OF_MODULOS):
        module = modules[i]
        phases[:,i] = module.phases_from_veloctiy(t_velocity, phases[:,i])

phasesToLocation1D(phases)

        



