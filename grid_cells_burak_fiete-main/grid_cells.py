import numpy as np
import matplotlib.pyplot as plt


class Module:
    """
    |    Represents grid cell module.
    |    Currently simplified model where firing neuron's phase is chosen by diff eq.
    |    Note that triangular y-axis is pi/3 CCW from x-axis!

        :param float spacing: spatial scale in cm; distance between each lattice point.
            Default 50 cm.
    """

    def __init__(self, spacing=50.0, bio_noise=False, speed_tau=2.0, speed_amp=0.05, dir_tau=1.0, dir_amp=0.025):
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

        self.speed_noise = 0.0  # OU noise for speed
        self.dir_noise = 0.0  # OU noise for head dir

        self.speed_tau = speed_tau
        self.speed_amp = speed_amp
        self.dir_tau = dir_tau
        self.dir_amp = dir_amp

        self.bio_noise = bio_noise

        self.rng = np.random.default_rng()

    def update(self, speed=0, head_dir=0, dt=0.001):
        """
        |    Update triangular phases [p_ix, p_iy] based on rectangular velocity.
        |    Adds error.

            :param float speed: speed in cm/s.
            :param float head_dir: head direction in radians.
            :param float dt: length of timestep in seconds.
        """

        if self.bio_noise:
            self.speed_noise += self.OU_increment(self.speed_noise, self.speed_tau, self.speed_amp, dt)
            self.dir_noise += self.OU_increment(self.dir_noise, self.dir_tau, self.dir_amp, dt)

        cos = np.cos(head_dir + self.dir_noise)
        sin = np.sin(head_dir + self.dir_noise)
        displacement = [(speed + self.speed_noise) * cos * dt, (speed + self.speed_noise) * sin * dt]

        self.displacements.append(displacement)
        displacement = self.transform @ np.asarray(displacement)  # rect displacement -> triangular displacement
        self.phase += self.dist_to_rad * displacement
        self.phase %= 2 * np.pi

    def OU_increment(self, noise, tau, amp, dt):
        """
            Update OU process.

            :param float noise: current process value.
            :param float tau: relaxation time in seconds.
            :param float amp: scale of noise.
            :param float dt: time step length in seconds.
            :return update for OU process:
            :rtype float:
        """
        return -noise * dt / tau + self.rng.normal(loc=0.0, scale=amp * np.sqrt(dt))