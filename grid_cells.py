import numpy as np
import os, sys


# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory to the Python path environment
sys.path.append(current_dir+"/networks")
from ContinuousAttractor import ContinuousAttractorNetwork


class Module:
    """
    |    Represents grid cell module.
    |    Currently simplified model where firing neuron's phase is chosen by diff eq.
    |    Note that triangular y-axis is pi/3 CCW from x-axis!

        :param float spacing: spatial scale in cm; distance between each lattice point.
            Default 50 cm.
    """

    def __init__(self, spacing=50.0):
        self.spacing = spacing  # s_i, cm

        # rad phases in triangular coord grid
        self.phase = np.zeros(2)  # [p_ix, p_iy]

        # displacements after noise for baseline results
        self.displacements = []

        # some constants that will be helpful for computation later
        self.dist_to_rad = 2 * np.pi / self.spacing
        self.transform = np.asarray([
            [1, -1 / np.sqrt(3)],
            [0, 2 / np.sqrt(3)]
        ], dtype=np.float64)

    def update(self, speed=0, head_dir=0, dt=0.001):
        """
        |    Update triangular phases [p_ix, p_iy] based on rectangular velocity.
        |    Adds error.

            :param float speed: speed in cm/s.
            :param float head_dir: head direction in radians.
            :param float dt: length of timestep in seconds.
        """
        cos = np.cos(head_dir)
        sin = np.sin(head_dir)
        displacement = [speed * cos * dt, speed * sin * dt]

        self.displacements.append(displacement)
        displacement = self.transform @ np.asarray(displacement)  # rect displacement -> triangular displacement
        self.phase += self.dist_to_rad * displacement
        self.phase %= 2 * np.pi

class GridCellModule:
    def __init__(self, spacing=50.0, orientation=0, n=20, K = 1): 
        """
        :param float spacing: spatial scale in cm; distance between each lattice point.

        :param float orientation: orientation of the grid cell module in radians.
                                there is nothing on orientation rn.

        :param int n: number of neurons in the grid cell module.

        :param float K: scaling factor for velocity gain to the spacing modules... 
                        you need to play around with this to get the right scaling factor.
                        K should be constant across modules. 
        """

        # NEED TO CALIBRATE K
        self.spacing = spacing  # s_i, cm
        """matthew bu write ur orientation shi"""
        self.orientation = orientation
        self.n=n
        velocity_gain = K / spacing
        self.can = ContinuousAttractorNetwork(n, tau=0.01, dt = 0.001, 
                                               a=1, gamma = 0.01863905325, beta= 0.01775147929, l=1, velocity_gain=velocity_gain, 
                                               periodicity=True,
                                               nonlinearity = "rect")
        # self.can = self.get_can() 

    def get_can(self, tau=0.01, dt = 0.001,  
                     a=1, gamma = 0.01863905325, beta= 0.01775147929, l=1, K=1,
                     nonlinearity = "rect", periodicity = True):
        """
        call manually after if you want to change parameters of can.
        """
        velocity_gain = K/self.spacing
        return ContinuousAttractorNetwork(n=self.n, tau=tau, dt=dt,
                                           a=a, gamma=gamma, beta=beta, l=l, velocity_gain=velocity_gain, 
                                           nonlinearity=nonlinearity, periodicity=periodicity)
    def firing_rates(self):
        self.can.get_firing_rates()
    def phase(self):
        self.can.get_phase()

gridcell_test = GridCellModule(spacing=50.0, orientation=0, n=20, K = 1)
gridcell_test.can.step(velocity=np.array([1.0, 0.0]))