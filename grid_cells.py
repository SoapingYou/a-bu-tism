import numpy as np
import matplotlib.pyplot as plt
import os, sys


# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add networks directory to the Python path environment
sys.path.append(current_dir+"/networks")

from networks.ContinuousAttractor import ContinuousAttractorNetwork


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
        velocity_gain = K / self.spacing
        self.can = ContinuousAttractorNetwork(n, tau=0.01, dt = 0.001, spacing=self.spacing,
                                               a=1, gamma_scalar = 1.05, beta_scalar=3.0, lambda_net=13, l=1, velocity_gain=velocity_gain, 
                                               periodicity=True,
                                               nonlinearity = "rect", init_bump_scaling_const=10,center=0)
        # self.can = self.get_can() 

    def get_can(self, tau=0.01, dt = 0.001,
                     a=1, gamma_scalar = 1.05, beta_scalar = 3.0, lambda_net=13, l=1, K=1,center=0,
                     nonlinearity = "rect", periodicity = True, init_bump_scaling_const=10,):
        """
        call manually after if you want to change parameters of can.
        """
        velocity_gain = K/self.spacing
        return ContinuousAttractorNetwork(n=self.n, spacing=self.spacing, tau=tau, dt=dt,
                                           a=a, gamma_scalar=gamma_scalar, beta_scalar=beta_scalar, lambda_net=lambda_net,l=l, velocity_gain=velocity_gain, 
                                           nonlinearity=nonlinearity, periodicity=periodicity, center=center,
                                           init_bump_scaling_const=init_bump_scaling_const)
    def firing_rates(self):
        #self.can.get_firing_rates()
        pass

    def get_phase(self):
        """
        runs phase decoder... 
        """
        return self.can.get_phase() #replace 0 with orientation of module

gridcell_test = GridCellModule(spacing=1.0, orientation=0, n=40, K = 1)
gridcell_test.can = gridcell_test.get_can(gamma_scalar=1.05, beta_scalar=3.,init_bump_scaling_const=10, lambda_net=13, K=1,center=0)
fig, axes = plt.subplots(1)

# test = [100, 200, 300]
# for i in range(3):
#     gridcell_test = GridCellModule(spacing=test[i], orientation=0, n=40, K = 1)
#     gridcell_test.can = gridcell_test.get_can(gamma_scalar=1.05, beta_scalar=3.0,init_bump_scaling_const=10, K=1,center=0, lambda_net=13)
#     for j in range(60):
#         gridcell_test.can.step(velocity=np.array([0,0]))
#     axes[i].scatter(
#                 gridcell_test.can.pos[:,0],
#                 gridcell_test.can.pos[:,1],
#                 c=gridcell_test.can.activity
#             )

# plt.show()
gridcell_test.can.plot_activity()