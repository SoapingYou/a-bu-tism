from RunTrial import RunTrial

import numpy as np

def euclidean_pos_error(sim_vec: np.ndarray, true_vec: np.ndarray):
    x_error = sim_vec[0] - true_vec[1]
    y_error = sim_vec[1] - sim_vec[1]
    return np.sqrt(np.square(x_error) + np.square(y_error))

def baseline(trial_num=10):
    error = 0
    for trial_num in range(trial_num):
        simulator = RunTrial()
        simulator.assembly_grid_cells()
        simulator.get_random_walk(debug=False)
        simulator.run_trial(error_freq = -1)
        og = simulator.final_og_position
        sim = simulator.final_simulated_position
        err = euclidean_pos_error(sim_vec=sim, true_vec=og)
        print(sim)
        print(og)
        print(err)

baseline(1)
        


    