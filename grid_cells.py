import numpy as np


class Module:
    """
    |    Represents grid cell module.
    |    Currently simplified model where firing neuron's phase is chosen by diff eq.
    |    Note that triangular y-axis is pi/3 CCW from x-axis!

        :param float spacing: spatial scale in cm; distance between each lattice point.
            Default 50 cm.
        :param float speed_noise_amplitude: noise strength for fractional speed error. Default 0.0
        :param float dir_noise_amplitude: noise strength for radian head direction error. Default 0.0
        :param float speed_tau: relaxation constant for speed OU process. Default 1.0
        :param float dir_tau: relaxation constant for head direction OU process. Default 1.0
    """

    def __init__(self, spacing=50.0, speed_noise_amplitude=0.05, dir_noise_amplitude=0.025, speed_tau=2.0, dir_tau=1.0):
        self.spacing = spacing  # s_i, cm
        self.speed_noise_amplitude = speed_noise_amplitude
        self.dir_noise_amplitude = dir_noise_amplitude
        self.speed_tau = speed_tau  # s
        self.dir_tau = dir_tau  # s

        self.speed_noise = 0.0  # Ornstein Uhlenbeck process (error) for speed
        self.dir_noise = 0.0  # OU process for direction

        # rad phases in triangular coord grid
        self.phase = np.zeros(2)  # [p_ix, p_iy]

        # some constants that will be helpful for computation later
        self.dist_to_rad = 2 * np.pi / self.spacing
        self.transform = np.asarray([
            [1, -1 / np.sqrt(3)],
            [0,  2 / np.sqrt(3)]
        ], dtype=np.float64)

        self.rng = np.random.default_rng()

    def update(self, speed=0, head_dir=0, dt=0.001):
        """
        |    Update triangular phases [p_ix, p_iy] based on rectangular velocity.
        |    Adds error.

            :param float speed: speed in cm/s.
            :param float head_dir: head direction in radians.
            :param float dt: length of timestep in seconds.
        """

        self.speed_noise += self.OU_increment(self.speed_noise, self.speed_tau, self.speed_noise_amplitude, dt)
        self.dir_noise += self.OU_increment(self.dir_noise, self.dir_tau, self.dir_noise_amplitude, dt)

        # speeds and head directions with error
        speed_noisy = max(0.0, speed * (1 + self.speed_noise))
        dir_noisy = head_dir + self.dir_noise

        v_noisy = speed_noisy * np.array([
            np.cos(dir_noisy),
            np.sin(dir_noisy)
        ])

        displacement = v_noisy * dt
        displacement = self.transform @ displacement  # rect displacement -> triangular displacement
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
