import numpy as np

class Connectivity:
    def __init__(self, n, preferred_vectors: np.ndarray, pos, spacing,
                 a, gamma_scalar, beta_scalar, lambda_net,l, velocity_gain, nonlinearity, 
                 periodicity = True,   
                 dt = 0.001, tau=0.01):
        self.n = n
        self.N = n*n
        self.preferred_vectors = preferred_vectors # (N,2)
        self.periodicity = periodicity
        self.pos = pos
        self.spacing = spacing
        self.lambda_net = lambda_net

        self.gamma_scalar = gamma_scalar
        self.beta_scalar = beta_scalar

        self.a = a
        self.beta = self.beta_scalar / (self.lambda_net)**2
        self.gamma = self.gamma_scalar*self.beta
        self.l = l
        self.velocity_gain = velocity_gain

        self.nonlinearity = nonlinearity

        self.dt = dt
        self.tau = tau

        self.distances_sqrd = self.compute_distances_sqrd(self.pos)
        self.weights_ij = self.get_weights()

    def compute_distances_sqrd(self, pos:np.ndarray):
        """
        computes displacements between all neurons and their shifts
        takes in position vector of neurons (N,2) which is cartesian coordinates of triangular lattice points of neurons
        
        CHECK: pos has index of triangular lattice, but is cartesian coords, 
                preferred_vectors has index of triangular lattice, 
                but is cartesian unit vector of preferred direction of neuron

        distancessqrd = posi-posj-l*etheta (etheta is unit vector of preferred direction of neuron i)
        returns 3D array of displacements (N,N,2)
        """
        distances_sqrd = np.zeros((self.N, self.N))
        _shift_displacement = self.l * self.preferred_vectors
        delta = np.zeros((self.N,self.N,2))

        for i in range(self.N):
            for j in range(self.N):
                delta[i,j] = pos[i] - pos[j]

        delta -= _shift_displacement
        # wrap delta in triangular lattice. delta is currently in cartesian x,y difs
        i = delta[:,:,0] - delta[:,:,1]/np.sqrt(3)  # i is NxN
        j = 2*delta[:,:,1]/np.sqrt(3) # j is NxN

        i = i - np.round(i/self.n)*self.n 
        j = j - np.round(j/self.n)*self.n

        x = i+j/2 # x is NxN
        y=j*np.sqrt(3)/2 #y is NxN

        displacements = np.array([x,y]) # 2xNxN
        distances_sqrd = displacements[0]**2+displacements[1]**2 # NxN
        return distances_sqrd

    def get_weights(self):
        """
        returns 2D array of weights (N,N)
        Wij = ae^(-gamma * distancessqrd) - e^(-beta*distancessqrd)
        distancessqrd = xi-xj-l*etheta (etheta is unit vector of preferred direction of neuron i)
        """
        weights_ij = np.zeros((self.N, self.N))
        weights_ij = self.a * np.exp(-self.gamma * self.distances_sqrd) - np.exp(-self.beta * self.distances_sqrd)
        return weights_ij

    def get_biases(self, velocity:np.ndarray = np.zeros(2)):
        """
        returns 2D array of biases (N)
        Bi = A(xi) * (1 - etheta *velocity)
          (etheta is unit vector of preferred direction of neuron i)
          A(xi) = 1 if periodic, anddddddd idrc about the nonperiodic rn LMAO too complicated.
        """
        biases = np.zeros((self.N))
        for i in range(self.N):
            A = 1
            if(not self.periodicity):
                A = self.aperiodic_A() #rn it just returns 1, but later will be a function of xi
            # velocity = np.array([velocity[0] * self.dt, velocity[1] * self.dt])
            biases[i] = A * (1 + self.velocity_gain * np.dot(self.preferred_vectors[i], velocity))
        return biases
    

        
    def derive_new_activity(self, activity:np.ndarray, velocity:np.ndarray = np.zeros(2)):
        """
        returns 2D array of new activity (n,n)
        tau * dsi/dt + si = phi (sum(wij*sj) + bi) 
                phi is nonlinearity, currently its rect. 
        """
        weight_effects = self.weights_ij @ activity # 2D array (NxN), where
         # for each neuron i, it computes the sum of wij*sj for all j
        bias_effects = self.get_biases(velocity) # 1D array (N), where
         # for each neuron i, it computes the bias bi
        new_activity = weight_effects + bias_effects # 1D array (N),
        if(self.nonlinearity == "rect"):
            phi_output = np.maximum(0, new_activity)
        else: #if there is another nonlinearity func, add here
            phi_output = new_activity
        dsidt = (phi_output - activity) / self.tau
        activity_new = activity + dsidt * self.dt
        return activity_new
        
    def aperiodic_A(self):
        """
        has some ... equation for aperiodic A(xi) that I will implement later.
        """
        return 1