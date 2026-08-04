import numpy as np
import matplotlib.pyplot as plt
from Connectivity import Connectivity

class ContinuousAttractorNetwork:
    def __init__(self, n, spacing,
                 tau=0.01, dt = 0.001, 
                 a=1, gamma_scalar = 1.05, beta_scalar= 3.0, lambda_net=13, l=1, velocity_gain=0.10315, 
                 periodicity=True,
                 nonlinearity = "rect", center=0, init_bump_scaling_const=10):
        """
        activity
        connectivity
        preferred_vectors
        step()
        get_phase()"""
        self.n = n
        self.N = n*n
        self._radius = 10
        self.preferred_vectors, self.pos = self.make_grid() # 1d numpy arrays (N)
        self.activity = self.initialize_bump(center=center, scaling_constant=init_bump_scaling_const) #rectangular neural grid... but we are actually encoding TRIANGULAR LATTICE
        self.conn_obj = Connectivity(n, self.preferred_vectors, self.pos, spacing=spacing,
                                     a=a, gamma_scalar=gamma_scalar, beta_scalar=beta_scalar, lambda_net=lambda_net, l=l, velocity_gain=velocity_gain,
                                     nonlinearity=nonlinearity, periodicity=periodicity, 
                                     dt=dt, tau=tau)
        for _ in range(100):
            self.step(calc_phase=False)
        self.lambda_net = self.measure_lambda_net(self.activity,self.pos,self.n)
        self.phase_pos = self.init_phase_pos= self.unwrapped_pos = self.initialize_phase(_radius = self._radius) #triangular
        self.unwrapped_pos = self.unwrapped_pos.astype(float)

    def initialize_phase(self,_radius=7):
        i = int(self.n/2)
        j = int(self.n/2)
        activity2d = self.activity.reshape(self.n, self.n)

        cropped = activity2d[
            i-_radius:i+_radius,
            j-_radius:j+_radius
        ]

        # coordinates inside the crop
        di, dj = np.unravel_index(np.argmax(cropped), cropped.shape)

        # coordinates in the full grid
        I = i - _radius + di
        J = j - _radius + dj

        return np.array([I,J])
        
    def make_grid(self):
        """
        makes neural grid of cells --> represented in 2 np.ndarrays shape (N,2) and (N)
          - first np array tracks all of the neurons preferred unit vectors (0,60,120,180,240,300 deg)
                these neurons all are rando for that. 

                preferred_vectors[x*n + y] = (cartesian unit vector) = (cos(theta), sin(theta))
                where theta refers to preferred direction of neuron at TRIANGULAR lattic point (x,y)

          - second np array tracks activity 
                it's triangular, and it's a 1D array of length N...

                activity[x*n+y] = something in Amps, where (x,y) is the triangular lattice point of the neuron

          - third np array tracks the actual grid cell pos / phase in triangular lattice in CART coords
                it's grid cell pos / phase in triangular lattice in CART coords 

                pos[x*n+y] = cartesian coordinates of the triangular lattice point (x,y) in cm, 
                where (x,y) is the triangular lattice point of the neuron

        and the actual grid cell pos / phase is calculated by position in array
        """
        _direction_idx = np.zeros(self.N, dtype=int)
        idx = 0
        for i in range(self.n):
            for j in range(self.n):
                _direction_idx[idx] = 3 * (j % 2) + (i % 3) # tiles N in [[0,3],[1,4],[2,5]]
                idx += 1 # _direction_idx is kinda like [0,3,0,3...,1,4,1,4...2,5,2,5...0,3,0,3...etc]
        _preferred_directionality = np.full((self.N), np.pi/3)
        _preferred_directionality = _preferred_directionality*_direction_idx
        preferred_vectors = np.zeros((self.N, 2))
        preferred_vectors[:,0] = np.cos(_preferred_directionality)
        preferred_vectors[:,1] = np.sin(_preferred_directionality)

        pos = np.zeros((self.N,2))
        idx = 0
        for i in range(self.n):
            for j in range(self.n):
                pos[idx] = np.array([i + 0.5*j, (j*np.sqrt(3)/2)])
                idx+=1

        return preferred_vectors, pos

    def initialize_bump(self, center=0, scaling_constant=10):
        """
        initializes bump of activity at center neuron
        :param int center: index of neuron from 0 to N-1 to center bump on
                            if -1, will randomly select a neuron to center bump on
        """
        if center == -1:
            center = np.random.randint(self.N)

        distances = np.linalg.norm(
            self.pos - self.pos[center],
            axis=1
        )

        return np.exp(-distances/scaling_constant) # arbitrary beginning bump
    def measure_lambda_net(self, activity, pos, n):
        """
        more ai slop, find better way to calculate distances between peaks
        """
        activity_2d = activity.reshape((n, n))
        
        # find the global peak
        peak_idx = np.argmax(activity)
        peak_pos = pos[peak_idx]
        
        # find all local maxima (a neuron brighter than all its immediate lattice neighbors)
        local_maxima = []
        for i in range(n):
            for j in range(n):
                val = activity_2d[i, j]
                neighbors = [
                    activity_2d[(i-1) % n, j], activity_2d[(i+1) % n, j],
                    activity_2d[i, (j-1) % n], activity_2d[i, (j+1) % n],
                    activity_2d[(i-1) % n, (j-1) % n], activity_2d[(i+1) % n, (j+1) % n],
                ]
                if val > max(neighbors) and val > activity.max() * 0.3:
                    local_maxima.append(pos[i * n + j])
        
        local_maxima = np.array(local_maxima)
        
        # distance from the global peak to every other local max, take the smallest
        dists = np.linalg.norm(local_maxima - peak_pos, axis=1)
        dists = dists[dists > 1e-6]
        
        lambda_net_measured = dists.min()
        return lambda_net_measured

    def step(self, velocity: np.ndarray = np.zeros(2), calc_phase =True):
        """
        a step basically is 
        tau * dsi/dt + si = phi (sum(wij*sj) + bi) 
        phi is nonlinearity, currently its rect. 
        """
        self.activity = self.conn_obj.derive_new_activity(self.activity,velocity) # 1D array (N)
        if(calc_phase):
            self.update_phase()
                                                                            
    def update_phase(self):
        """
        claude generated. shame, i know, im sorry. 
        """
        r = self._radius
        i0, j0 = self.phase_pos          # last known center, in (i, j) lattice-index units

        row_idx = (np.arange(i0 - r, i0 + r) % self.n).astype(int)
        col_idx = (np.arange(j0 - r, j0 + r) % self.n).astype(int)

        activity_2d = self.activity.reshape((self.n, self.n))
        window = activity_2d[np.ix_(row_idx, col_idx)]     # shape (2r, 2r), correctly wrapped

        # --- circular mean over the window, instead of argmax ---
        # row_idx/col_idx aren't contiguous once wrapped, so we can't just do a
        # normal weighted average of them directly (e.g. indices [38,39,0,1] would
        # average to ~19.5, which is on the wrong side of the sheet entirely).
        # Standard fix: map each wrapped index to an angle around the sheet's
        # circumference, average on the unit circle, then map back to an index.
        two_pi = 2 * np.pi

        theta_i = row_idx * (two_pi / self.n)
        theta_j = col_idx * (two_pi / self.n)

        w = window                                   # (2r, 2r) activity weights
        w_row = w.sum(axis=1)                        # marginal weight per row index
        w_col = w.sum(axis=0)                         # marginal weight per col index

        # weighted circular mean, row axis
        sin_i = np.sum(w_row * np.sin(theta_i))
        cos_i = np.sum(w_row * np.cos(theta_i))
        mean_theta_i = np.arctan2(sin_i, cos_i) % two_pi

        # weighted circular mean, col axis
        sin_j = np.sum(w_col * np.sin(theta_j))
        cos_j = np.sum(w_col * np.cos(theta_j))
        mean_theta_j = np.arctan2(sin_j, cos_j) % two_pi

        # map angles back to continuous (non-integer) lattice-index coordinates
        new_i = mean_theta_i * (self.n / two_pi)
        new_j = mean_theta_j * (self.n / two_pi)

        # --- accumulate UNWRAPPED phase using minimum-image on the STEP only ---
        step_i = ((new_i - i0 + self.n / 2) % self.n) - self.n / 2
        step_j = ((new_j - j0 + self.n / 2) % self.n) - self.n / 2
        self.unwrapped_pos += np.array([step_i, step_j])

        self.phase_pos = np.array([new_i, new_j])

    def get_phase(self):
        self.phase_change = ((self.unwrapped_pos-self.init_phase_pos) % self.lambda_net) / self.lambda_net * 2 * np.pi
        return self.phase_change
    
    def plot_activity(self):
        plt.scatter(
            self.pos[:,0],
            self.pos[:,1],
            c=self.activity
        )
        plt.show()