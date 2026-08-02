import numpy as np
from Connectivity import Connectivity

class ContinuousAttractorNetwork:
    def __init__(self, n, 
                 tau=0.01, dt = 0.001, 
                 a=1, gamma = 0.01863905325, beta= 0.01775147929, l=1, velocity_gain=0.10315, 
                 periodicity=True,
                 nonlinearity = "rect"):
        """
        activity
        connectivity
        preferred_vectors
        step()
        get_phase()"""
        self.n = n
        self.N = n*n
        self.preferred_vectors, self.activity, self.pos = self.make_grid() # 1d numpy arrays (N)
        self.conn_obj = Connectivity(n, self.preferred_vectors, self.pos,
                                     a, gamma, beta, l, velocity_gain,
                                     nonlinearity, periodicity=periodicity, 
                                     dt=dt, tau=tau )
        
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
        rng = np.random.default_rng()
        _randos = rng.integers(0, 6, size=(self.N))
        _preferred_directionality = np.full((self.N), np.pi/3)
        _preferred_directionality = _preferred_directionality*_randos
        preferred_vectors = np.zeros((self.N, 2))
        preferred_vectors[:,0] = np.cos(_preferred_directionality)
        preferred_vectors[:,1] = np.sin(_preferred_directionality)

        self.activity = np.zeros(self.N) #rectangular neural grid... but we are actually encoding TRIANGULAR LATTICE
        self.pos = np.zeros((self.N, 2))
        for i in range(self.n):
            for j in range(self.n):
                self.pos[i*self.n+j,0] = i + 0.5*j
                self.pos[i*self.n+j,1] = np.sqrt(3)/2 * j

        return preferred_vectors, self.activity, self.pos

    def step(self, velocity: np.ndarray = np.zeros(2)):
        """
        a step basically is 
        tau * dsi/dt + si = phi (sum(wij*sj) + bi) 
        phi is nonlinearity, currently its rect. 
        """
        self.activity = self.conn_obj.derive_new_activity(self.activity,velocity) # 2D array (nxn)

    def get_phase(self):
        """
        runs phase decoder
        """
        return np.argmax(self.activity) 

    
