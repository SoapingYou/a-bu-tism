# Written by Sophie Yu. Finished 2:51 AM. Mistakes may have been made. 

from NewRandomWalk import main as NewRandomWalk
from grid_cells import Module 
from phases_to_location import phasesToLocation1D

import numpy as np

class RunSimulator:
    def __init__(self, NUM_OF_MODS=10, NUM_SPATIAL_PHASES=20, NUM_NEURONS_P_PHASE=20):
        self.NUM_MODULES = NUM_OF_MODS
        self.NUM_SPATIAL_PHASES = NUM_SPATIAL_PHASES
        self.NUM_NEURONS_P_PHASE = NUM_NEURONS_P_PHASE

        self.ts = 0.001# in seconds, timestep
        self.length = 1000 # of timesteps, simulation length

#arbitrary numbers, adjust till it looks right ;) . OR replace w a better func, idrc
    def hex_basis_to_cart(self, u, v):
        x = u + 0.5 * v
        y = np.sqrt(3) / 2 * v
        return x, y

    def assembly_grid_cells(self, spacing_min=25, scaling = 1.65):
        ''' generate grid cell structure of NUM_MODULES modules, 
        each with 20 spatial phases, 20 neurons per phase'''
        self.s_is = [spacing_min * (scaling**i) for i in range(self.NUM_MODULES)]
        self.modules = [Module(spacing=self.s_is[i]) for i in range(self.NUM_MODULES)]
        # for module in self.modules:
        #     module.add_cells(self.NUM_SPATIAL_PHASES,self.NUM_SPATIAL_PHASES)

    def get_random_walk(self, debug = True):
        displacements = NewRandomWalk()
        displacements_x = np.array(displacements[0])
        displacements_y = np.array(displacements[1])
        self.ts = displacements[2]
        self.simlen = displacements[3]

        if(debug==True):
        # check ts works yo
            print(displacements[0], displacements[1])

        # original velocities
        self.og_velocities = np.zeros((2,self.simlen))
        self.og_velocities[0,:] = np.array(displacements_x) / self.ts 
        self.og_velocities[1,:] = np.array(displacements_y) / self.ts

    def run_simulation(self):
        # current phase of all modulos --> OVERSIMPLIFICATION AS OF NOW

        for t in range(self.simlen):
            # simulate velocity (with error).
            t_velocity = np.zeros(2)
            t_velocity[0] = self.og_velocities[0,t] 
            t_velocity[1] = self.og_velocities[1,t] 

            # update phase
            for i in range(self.NUM_MODULES):
                self.modules[i].update(t_velocity, self.ts)
        return self.get_location()


    def get_location(self):
        phases = np.array([self.modules[i].phase for i in range(self.NUM_MODULES)])
        data_x = np.zeros((self.NUM_MODULES,2))
        data_x[:,0] = self.s_is
        data_x[:,1] = phases[:,0]
        x_trig_dist = phasesToLocation1D(data_x)

        data_y = np.zeros((self.NUM_MODULES,2))
        data_y[:,0] = self.s_is
        data_y[:,1] = phases[:,1]
        y_trig_dist = phasesToLocation1D(data_y)
        return self.hex_basis_to_cart(x_trig_dist,y_trig_dist)

        

simulator = RunSimulator()
simulator.assembly_grid_cells()
simulator.get_random_walk(debug=False)
location = simulator.run_simulation()
print(location)