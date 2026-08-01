import numpy as np


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
