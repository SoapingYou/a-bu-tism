import numpy as np
import matplotlib.pyplot as plt
from Connectivity import Connectivity

class ContinuousAttractorNetwork:
    def __init__(self, n, 
                 tau=0.01, dt = 0.001, 
                 a=1, gamma = 0.01863905325, beta= 0.01775147929, l=1, velocity_gain=0.10315, 
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
        self.preferred_vectors, self.pos = self.make_grid() # 1d numpy arrays (N)
        self.activity = self.initialize_bump(center=center, scaling_constant=init_bump_scaling_const) #rectangular neural grid... but we are actually encoding TRIANGULAR LATTICE
        self.conn_obj = Connectivity(n, self.preferred_vectors, self.pos,
                                     a, gamma, beta, l, velocity_gain,
                                     nonlinearity, periodicity=periodicity, 
                                     dt=dt, tau=tau)
        
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

    def step(self, velocity: np.ndarray = np.zeros(2)):
        """
        a step basically is 
        tau * dsi/dt + si = phi (sum(wij*sj) + bi) 
        phi is nonlinearity, currently its rect. 
        """
        self.activity = self.conn_obj.derive_new_activity(self.activity,velocity) # 1D array (N)

    def get_phase(self):
        """
        currently returns the RECTANGULAR phase of neuron with highest activity
        
        later will replace with weighted avg of positions of neurons by activity 
        rtype np.ndarray (2)
        """
        #replace with weighted average of positions of neurons weighted by their activity
        return self.pos[(np.argmax(self.activity))] / self.n * 2*np.pi
    def plot_activity(self):
        plt.scatter(
            self.pos[:,0],
            self.pos[:,1],
            c=self.activity
        )
        plt.show()