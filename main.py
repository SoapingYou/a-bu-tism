# Written by Sophie Yu. Finished 2:51 AM. Mistakes may have been made. 

from MouseMovement import main as pathMake
from grid_cells import Module 
from phases_to_location import phasesToLocation1D

import numpy as np

class RunSimulator:

    def __init__(self, NUM_OF_MODS=10, NUM_SPATIAL_PHASES=20, NUM_NEURONS_P_PHASE=20):
        self.NUM_MODULES = NUM_OF_MODS
        self.NUM_SPATIAL_PHASES = NUM_SPATIAL_PHASES
        self.NUM_NEURONS_P_PHASE = NUM_NEURONS_P_PHASE

        self.ts = 0.001 # in seconds, timestep
        self.length = 4 # in seconds, simulation length
        self.ticks = int(self.length/self.ts)

    #arbitrary numbers, adjust till it looks right ;) . OR replace w a better func, idrc
    # ? make gaussian
    def generate_error(self, k=0.1):
        return np.random()*k
    def hex_basis_to_cart(self, u, v):
        x = u + 0.5 * v
        y = np.sqrt(3) / 2 * v
        return x, y

    def assembly_grid_cells(self, spacing_min=25, scaling = 1.65):
        ''' generate grid cell structure of NUM_MODULES modules, 
        each with 20 spatial phases, 20 neurons per phase'''
        self.modules = [Module(spacing=spacing_min* (scaling** i)) for i in range(self.NUM_MODULES)]
        for module in self.modules:
            module.add_cells(self.NUM_SPATIAL_PHASES,self.NUM_SPATIAL_PHASES)

    def get_random_walk(self, debug = True):
        displacements_x, displacements_y = pathMake()

        if(debug==True):
        # check ts works yo
            print(displacements_x, displacements_y)

        # original velocities
        self.og_velocities = np.zeros((2,self.ticks))
        self.og_velocities[0,:] = np.array(displacements_x) / self.ts 
        self.og_velocities[1,:] = np.array(displacements_y) / self.ts

    def run_simulation(self):
        # current phase of all modulos --> OVERSIMPLIFICATION AS OF NOW
        phases = np.zeros((2,self.NUM_MODULES))

        for t in range(self.ticks):
            # simulate velocity (with error).
            t_velocity = np.zeros(2)
            t_velocity[0] = self.og_velocities[0,t] + self.generate_error()
            t_velocity[1] = self.og_velocities[1,t] + self.generate_error()

            # update phase
            for i in range(self.NUM_MODULES):
                module = self.modules[i]
                phases[:,i] = module.phases_from_veloctiy(t_velocity, phases[:,i])
        return self.get_location(phases)


    def get_location(self,phases):
        x_trig_dist = phasesToLocation1D(phases[0])
        y_trig_dist = phasesToLocation1D(phases[1])
        return self.hex_basis_to_cart(x_trig_dist,y_trig_dist)

        

simulator = RunSimulator()
simulator.assembly_grid_cells()
simulator.get_random_walk()
simulator.run_simulation()
simulated_location = simulator.get_location()




