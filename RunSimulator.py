from RunTrial import RunTrial
from PathPlotter import PathPlotter

import numpy as np
import matplotlib.pyplot as plt

class RunSimulator:
    def __init__(self):
        pass

    def distance_error(self, sim_vec: np.ndarray, true_vec: np.ndarray):
        """
        computes distance of 2 coordinate pairs
        
        :param np.ndarray (2,) sim_vec: simulated vector
        :param np.ndarray (2,) true_vec: true vector
        returns float distance
        rtype float
        """
        return np.linalg.norm(sim_vec-true_vec)
    def mean_error(self, sim_vec: np.ndarray, true_vec: np.ndarray):
        """
        computes distance of 2 sets of coord pairs (over time)
        and takes the mean of all those distances
        
        :param np.ndarray (n,2) sim_vec: simulated coords
        :param np.ndarray (n,2) true_vec: true coords
        rtype float
        """
        return np.mean(np.linalg.norm(sim_vec-true_vec, axis=1))

    def rmse(self, sim_vec: np.ndarray, true_vec: np.ndarray):
        """
        computes rmse of 2 sets of coord pairs (over time)
        
        :param np.ndarray (n,2) sim_vec: simulated coords
        :param np.ndarray (n,2) true_vec: true coords
        rtype float
        """
        return np.sqrt(np.mean(np.sum((sim_vec-true_vec)**2, axis=1)))
    def error_over_time(self, sim_vec: np.ndarray, true_vec: np.ndarray):
        """
        computes distance of 2 sets of coord pairs (over time)
        and takes the mean of all those distances
        
        :param np.ndarray (n,2) sim_vec: simulated coords
        :param np.ndarray (n,2) true_vec: true coords
        rtype np.ndarray (n)
        """
        return np.linalg.norm(sim_vec-true_vec, axis=1)

    def average_errors(self,errors):
        """
        takes average of errors 
        :param np.ndarray (n) errors: errors
        rtype float
        """
        return np.mean(errors)

    def baseline(self, trial_num=10, 
                speed_noise_amplitude=0.05, headdir_noise_amplitude=0.025,
                error_freq=-1, ts=0.001, sim=20000, deltahead=2.4):
        """
        runs simulation
        
        :param int trial_num:  # of trials ran
        :param float speed_noise_amplitude:  speed noise amplitude
        :param float headdir_noise_amplitude:  head direction noise amplitude
        :param int error_freq: frequency in simulation that get_location() is 
                                called to compare error over time.
        :param float ts:  time step
        :param int sim:  simulation length in timesteps
        :param deltahead: max head change angle in one timestep

        no rt, but makes all_final_drift, all_mean_error, all_rmse, and all_error_over_time available
        """
        self.all_final_drift = np.zeros(trial_num)
        self.all_mean_error = np.zeros(trial_num)
        self.all_rmse = np.zeros(trial_num)
        self.all_error_over_time = [] # trial_num x (floor(simlen/error_freq))
        
        for trial_num in range(trial_num):
            simulator = RunTrial(speed_noise_amplitude=speed_noise_amplitude,
                                headdir_noise_amplitude=headdir_noise_amplitude,
                                ts = ts, simlen = sim, deltahead=deltahead)
            simulator.assembly_grid_cells()
            simulator.get_random_walk()
            simulator.run_trial(error_freq = error_freq)

            # og positions: 50000 x 2 shape [[xt],[yt]]
            self.og_positions = np.array([simulator.og_position_x,simulator.og_position_y])
            self.og_positions = self.og_positions.T
            # simulated positions: floor(simlen / errorfreq) x 3 shape [[ti,xi,yi],...]
            self.sim_positions = simulator.simulated_locations

            # ending errors
            self.final_drift_i = self.distance_error(sim_vec=self.sim_positions[-1,1:], 
                                           true_vec=self.og_positions[-1,:])

            # errors over time
            self.trimmed_og_pos = self.og_positions[self.sim_positions[:,0].astype(int),:]
            self.trimmed_sim_pos = self.sim_positions[:,1:]
            self.mean_error_i = self.mean_error(self.trimmed_sim_pos, 
                                                self.trimmed_og_pos)
            self.rmse_i = self.rmse(self.trimmed_sim_pos, 
                                                self.trimmed_og_pos)
            self.error_over_time_i = self.error_over_time(self.trimmed_sim_pos, 
                                                self.trimmed_og_pos)

            # updating the error lists
            self.all_final_drift[trial_num] = self.final_drift_i
            self.all_mean_error[trial_num] = self.mean_error_i
            self.all_rmse[trial_num] = self.rmse_i
            self.all_error_over_time.append(self.error_over_time_i)

            print(self.og_positions[-1:,])
            print(self.sim_positions[-1,1:])


