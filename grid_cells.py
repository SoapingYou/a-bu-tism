import numpy as np


class Module:
    """
    |    Represents grid cell module.
    |    Currently simplified model where firing neuron's phase is chosen by diff eq.
    |    Note that triangular y-axis is pi/3 CCW from x-axis!

        :param float spacing: spatial scale in cm; distance between each lattice point.
            Default 50 cm.
        :param float noise_amplitude: multiplier for error noise. At 1.0, error in distance
            per timestep is maximum 1 cm. Default 0.0
    """

    def __init__(self, spacing=50.0, noise_amplitude=0.0):
        self.spacing = spacing  # s_i
        self.noise_amplitude = noise_amplitude

        # rad phases in triangular coord grid
        self.phase = np.asarray([0.0, 0.0], dtype=np.float64)  # [p_ix, p_iy]

        # some constants that will be helpful for computation later
        self.dist_to_rad = 2 * np.pi / self.spacing
        self.transform = np.asarray([
            [1, -1 / np.sqrt(3)],
            [0,  2 / np.sqrt(3)]
        ], dtype=np.float64)

    def update(self, v=None, dt=0.001):
        """
        |    Update triangular phases [p_ix, p_iy] based on rectangular velocity v.
        |    Adds error.

            :param np.ndarray v: velocities [v_x, v_y] in cm/s.
            :param float dt: length of timestep in seconds.
        """
        if v is None: v = np.zeros(2, dtype=np.float64)

        displacement = (v * dt + self.error())  # velocities with error
        displacement = self.transform @ displacement  # rect velocity -> triangular velocity
        self.phase += self.dist_to_rad * displacement
        self.phase %= 2 * np.pi

    def error(self) -> np.ndarray:
        """
            Generate random error in distances traveled for update().

            :return: random error [e_x, e_y].
            :rtype np.ndarray:
        """
        theta = np.random.uniform(0, 2 * np.pi)
        radius = np.random.uniform()
        return np.asarray([np.cos(theta), np.sin(theta)], dtype=np.float64) * radius * self.noise_amplitude
