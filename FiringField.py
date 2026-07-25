import numpy as np


class FiringField:
    """
        Represents a grid cell's firing field in a triangular grid.

        Attributes:
            spacing (float): spatial scale in mm; distance between each lattice point.
            phase_x (float): phase shifted along triangular x-axis in rad (pos direction).
            phase_y (float): phase shifted along triangular y-axis in rad (pos direction).
            orientation (float): radians rotated.
            base_prob (float): lowest possible probability of firing (0.0 to 1.0).
            max_prob (float): highest possible_probability of firing (0.0 to 1.0).
            threshold (float):

        Notes:
            The triangular y-axis, by definition, is rotated pi/3 counterclockwise from the x-axis!
    """

    def __init__(self, spacing=1.0, phase_x=0.0, phase_y=0.0, orientation=0.0, base_prob=0.0, max_prob=1.0, threshold=0.0):
        self.spacing = spacing
        self.phase_x = phase_x
        self.phase_y = phase_y
        self.orientation = orientation
        self.base_prob = base_prob
        self.max_prob = max_prob
        self.threshold = threshold

        self._phase_x_rect = self.spacing / (2 * np.pi) * phase_x + self.spacing / (2 * np.pi) * phase_y / 2
        self._phase_y_rect = self.spacing / (2 * np.pi) * phase_y * np.sqrt(3) / 2

        wave_sep = self.spacing / 2 * np.sqrt(3)
        self._scale = 2 * np.pi / wave_sep

        # wave directions (rotated 2pi/3 from each other)
        angles = self.orientation + np.pi / 2 + np.array([0, 2 / 3 * np.pi, 4 / 3 * np.pi])
        self.wave_vectors = self._scale * np.stack((np.cos(angles), np.sin(angles)), axis=1)  # (3, 2)

    def probability(self, x: float, y: float) -> float:
        """
        Gives the probability of firing when organism is at rectangular coordinate point (x,y).

        Parameters:
            x (float): position along x-axis.
            y (float): position along y-axis.

        Returns:
            float: probability of grid cell firing at rectangular coordinates (x, y)
        """
        # shift due to phase
        pos = np.array([x - self._phase_x_rect,
                        y - self._phase_y_rect])

        normalized_activity = (np.cos(self.wave_vectors @ pos).sum() + 1.5) / 4.5

        threshold_firing_field = np.maximum(0.0, normalized_activity - self.threshold) / (1 - self.threshold)

        return self.base_prob + (self.max_prob - self.base_prob) * threshold_firing_field  # expected rate
