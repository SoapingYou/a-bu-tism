# Written by Sophie Yu. Finished 2:51 AM. Mistakes may have been made. 

from NewRandomWalk import main as NewRandomWalk
from grid_cells import Module
from phases_to_location import phasesToLocation1DProgressive

import numpy as np


class RunTrial:
    def __init__(self, NUM_OF_MODS=10, NUM_SPATIAL_PHASES=20, NUM_NEURONS_P_PHASE=20, 
                 speed_noise_amplitude = 0.05, headdir_noise_amplitude=0.025):
        self.NUM_MODULES = NUM_OF_MODS
        self.NUM_SPATIAL_PHASES = NUM_SPATIAL_PHASES
        self.NUM_NEURONS_P_PHASE = NUM_NEURONS_P_PHASE

        self.ts = 0.001  # in seconds, timestep
        self.simlen = 1000  # of timesteps, simulation length

        self.speed = np.zeros(1)  # cm / s
        self.head_dir = np.zeros(1)  # radians
        self.final_og_position = np.zeros(2)  # cm
        self.speed_noise_amplitude = speed_noise_amplitude
        self.headdir_noise_amplitude = headdir_noise_amplitude

    # arbitrary numbers, adjust till it looks right ;) . OR replace w a better func, idrc
    # ? make gaussian
    def hex_basis_to_cart(self, u, v):
        x = u + 0.5 * v
        y = np.sqrt(3) / 2 * v
        return x, y

    def assembly_grid_cells(self, spacing_min=25, scaling=1.65):
        ''' generate grid cell structure of NUM_MODULES modules,
        each with 20 spatial phases, 20 neurons per phase'''
        self.s_is = [spacing_min * (scaling ** i) for i in range(self.NUM_MODULES)]
        self.modules = [Module(spacing=self.s_is[i], speed_noise_amplitude=self.speed_noise_amplitude
                               , dir_noise_amplitude=self.headdir_noise_amplitude)
                        for i in range(self.NUM_MODULES)]
        # for module in self.modules:
        #     module.add_cells(self.NUM_SPATIAL_PHASES,self.NUM_SPATIAL_PHASES)

    def get_random_walk(self):
        _outputs = NewRandomWalk()
        self.speed = np.array(_outputs[0])
        self.head_dir = np.array(_outputs[1])
        self.ts = _outputs[2]
        self.simlen = _outputs[3]
        self.final_og_position = _outputs[4]

    def run_trial(self, error_freq: int = -1):
        """
        Simulates the grid cell phases changing by velocity of the mouse

        :param int error_freq: 
            -1 if you just want to call get_location() at the end.
            otherwise frequency per time step that get_location() 
            is called to determine time-based error. 
            will call get_location() at end no matter what.
            e.g., 1 for calling get_location every timestep. 
        """
        if(error_freq == -1): self.simulated_locations=np.zeros((1,3))
        else: self.simulated_locations=np.zeros((int(np.floor(self.simlen/error_freq)), 3))
        for t in range(self.simlen):
            # simulate velocity (with error).
            t_speed = self.speed[t]
            t_headdir = self.head_dir[t]

            # update phase
            for i in range(self.NUM_MODULES):
                self.modules[i].update(t_speed, t_headdir, self.ts)

            #see current sim location & error
            if(error_freq != -1 and t % error_freq==0):
                self.simulated_locations[int(t/error_freq)][0] = t
                self.simulated_locations[int(t/error_freq)][1:] = self.get_location()

        self.final_simulated_position = self.get_location()
        return self.final_simulated_position

    def get_location(self):
        phases = np.array([self.modules[i].phase for i in range(self.NUM_MODULES)])
        data_x = np.zeros((self.NUM_MODULES, 2))
        data_x[:, 0] = self.s_is
        data_x[:, 1] = phases[:, 0]
        x_trig_dist = phasesToLocation1DProgressive(data_x)

        data_y = np.zeros((self.NUM_MODULES, 2))
        data_y[:, 0] = self.s_is
        data_y[:, 1] = phases[:, 1]
        y_trig_dist = phasesToLocation1DProgressive(data_y)
        return self.hex_basis_to_cart(x_trig_dist, y_trig_dist)
    