# Written by Sophie Yu. Finished 2:51 AM. Mistakes may have been made. 

from NewRandomWalk import main as NewRandomWalk
from grid_cells import Module
from phases_to_location import phasesToLocation1DProgressive

import numpy as np


class RunTrial:
    def __init__(self, NUM_OF_MODS=10, NUM_SPATIAL_PHASES=20, NUM_NEURONS_P_PHASE=20,
                 speed_noise_amplitude=0.05, headdir_noise_amplitude=0.025,
                 speed_tau=2.0, dir_tau=1.0,
                 ts=0.001, simlen=20000, deltahead=2.4,
                 spacing_min=25, scaling=1.75, seed=67):
        self.NUM_MODULES = NUM_OF_MODS
        self.NUM_SPATIAL_PHASES = NUM_SPATIAL_PHASES
        self.NUM_NEURONS_P_PHASE = NUM_NEURONS_P_PHASE

        self.ts = ts  # in seconds, timestep
        self.simlen = simlen  # of timesteps, simulation length
        self.deltahead = deltahead  # in degrees

        self.speed = np.zeros(1)  # cm / s
        self.head_dir = np.zeros(1)  # radians
        self.final_og_position = np.zeros(2)  # cm

        '''
            documentation for below from grid_cells.py:

            speed_noise_amplitude: noise strength for fractional speed error. Default 0.05
            dir_noise_amplitude: noise strength for radian head direction error. Default 0.025
            speed_tau: relaxation constant for speed OU process. Default 2.0
            dir_tau: relaxation constant for head direction OU process. Default 1.0
        '''
        self.speed_noise_amplitude = speed_noise_amplitude
        self.dir_noise_amplitude = headdir_noise_amplitude
        self.speed_tau = speed_tau  # s
        self.dir_tau = dir_tau  # s

        self.spacing_min = spacing_min  # cm, grid cell assembly
        self.scaling = scaling  # ratio, grid cell assembly

        self.seed = seed

        self.x_trig_dist = 0.0
        self.y_trig_dist = 0.0

        self.rng = np.random.default_rng(seed)

    # arbitrary numbers, adjust till it looks right ;) . OR replace w a better func, idrc
    # ? make gaussian
    def hex_basis_to_cart(self, u, v):
        x = u + 0.5 * v
        y = np.sqrt(3) / 2 * v
        return x, y

    def assembly_grid_cells(self):
        ''' generate grid cell structure of NUM_MODULES modules,
        each with 20 spatial phases, 20 neurons per phase'''
        self.s_is = [self.spacing_min * (self.scaling ** i) for i in range(self.NUM_MODULES)]
        self.modules = [Module(spacing=self.s_is[i]) for i in range(self.NUM_MODULES)]
        # for module in self.modules:
        #     module.add_cells(self.NUM_SPATIAL_PHASES,self.NUM_SPATIAL_PHASES)

    def get_random_walk(self):  # figure out a better way to structure ts </3
        _outputs = NewRandomWalk(user_input=False, plot_turtle=False,
                                 timestep=self.ts, simlen=self.simlen, deltaheading=self.deltahead,
                                 seed=self.seed)
        self.speed = np.array(_outputs[0])
        self.head_dir = np.array(_outputs[1])
        self.og_position_x = _outputs[2]
        self.og_position_y = _outputs[3]

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
        speed_noise = 0.0
        dir_noise = 0.0

        if (error_freq == -1):
            self.simulated_locations = np.zeros((1, 3))
        else:
            _len_for_sim_locations = int(np.floor(self.simlen / error_freq))
            if ((self.simlen - 1) % error_freq != 0): _len_for_sim_locations += 1
            self.simulated_locations = np.zeros((_len_for_sim_locations, 3))

        for t in range(self.simlen):
            # simulate velocity (with error).
            speed_noise += self.OU_increment(speed_noise, self.speed_tau, self.speed_noise_amplitude, self.ts)
            dir_noise += self.OU_increment(dir_noise, self.dir_tau, self.dir_noise_amplitude, self.ts)

            t_speed = max(0.0, self.speed[t] * (1 + speed_noise))
            t_headdir = self.head_dir[t] + dir_noise

            # update phase
            for i in range(self.NUM_MODULES):
                self.modules[i].update(t_speed, t_headdir, self.ts)

            # see current sim location & error
            if ((error_freq != -1 and t % error_freq == 0)):
                self.simulated_locations[int(t / error_freq)][0] = t
                self.simulated_locations[int(t / error_freq)][1:] = self.get_location()
            elif (t == self.simlen - 1):
                self.simulated_locations[-1][0] = t
                self.simulated_locations[-1][1:] = self.get_location()

        self.final_simulated_position = self.get_location()
        return self.final_simulated_position

    def get_location(self):
        phases = np.array([self.modules[i].phase for i in range(self.NUM_MODULES)])
        data_x = np.zeros((self.NUM_MODULES, 2))
        data_x[:, 0] = self.s_is
        data_x[:, 1] = phases[:, 0]
        self.x_trig_dist = phasesToLocation1DProgressive(data_x, self.x_trig_dist)

        data_y = np.zeros((self.NUM_MODULES, 2))
        data_y[:, 0] = self.s_is
        data_y[:, 1] = phases[:, 1]
        self.y_trig_dist = phasesToLocation1DProgressive(data_y, self.y_trig_dist)
        return self.hex_basis_to_cart(self.x_trig_dist, self.y_trig_dist)

    def OU_increment(self, noise, tau, amp, dt):
        """
            Update OU process.

            :param float noise: current process value.
            :param float tau: relaxation time in seconds.
            :param float amp: scale of noise.
            :param float dt: time step length in seconds.
            :return update for OU process:
            :rtype float:
        """
        return -noise * dt / tau + self.rng.normal(loc=0.0, scale=amp * np.sqrt(dt))
