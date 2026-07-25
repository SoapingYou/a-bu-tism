import numpy as np


class Module:
    """
    |    Represents grid cell module. Phase differs between cells.
    |    Access the i-th grid cell using list notation: module[i]
    |    Note that triangular y-axis is pi/3 CCW from x-axis!

        :param float spacing: spatial scale in mm; distance between each lattice point.
        :param float orientation: rotation of grid in radians.
        :param float base_prob: lowest possible probability of each grid cell firing [0.0, 1.0].
        :param float max_prob: highest possible_probability of each grid cell firing [0.0, 1.0].
        :param float threshold: minimum normalized grid activity required for firing [0.0, 1.0).
            Values below threshold are set to zero, and remaining activity is rescaled 0 to 1.
    """

    def __init__(self, spacing=50.0, orientation=0.0, base_prob=0.0, max_prob=1.0, threshold=0.0):
        self.grid_cells = []  # list of all grid cells in this module
        self.spacing = spacing
        self.orientation = orientation
        self.base_prob = base_prob
        self.max_prob = max_prob
        self.threshold = threshold

        # some constants that will be helpful for computation later
        self.phase_scale = self.spacing / (2 * np.pi)  # used to convert from rad to rect dist
        wavelength = self.spacing / 2 * np.sqrt(3)
        scale = 2 * np.pi / wavelength

        # wave directions (rotated 2pi/3 from each other)
        angles = self.orientation + np.pi / 2 + np.array([0, 2 / 3 * np.pi, 4 / 3 * np.pi])
        self.wave_vectors = scale * np.stack((np.cos(angles), np.sin(angles)), axis=1)  # (3, 2)

    def add_cell(self, phase_x=0, phase_y=0) -> int:
        """
            Adds one grid cell to the module, appending to grid_cells list.

            :param float phase_x: phase shifted along triangular x-axis in rad (pos direction).
            :param float phase_y: phase shifted along triangular y-axis in rad (pos direction).

            :return: index of the added cell
            :rtype int:
        """
        self.grid_cells.append(FiringField(module=self, phase_x=phase_x, phase_y=phase_y))
        return len(self) - 1

    def add_cells(self, num_x=1, num_y=1) -> tuple[int, int]:  # if anyone has better names here, please change LOL
        """
        |    Adds num_x * num_y grid cells to the module, appending to grid_cells list.
        |    Phases are evenly spaced from 0 to 2pi.

            :param int num_x: number of different phases along triangular x-axis.
            :param int num_y: number of different phases along triangular y-axis.

            :return: tuple containing the starting and ending indices of the newly added cells.
            :rtype tuple:
        """
        for x in range(num_x):
            for y in range(num_y):
                self.grid_cells.append(FiringField(module=self,
                                                   phase_x=x * 2 * np.pi / num_x,
                                                   phase_y=y * 2 * np.pi / num_y))
        return len(self) - num_x * num_y, len(self) - 1

    def __getitem__(self, index):
        return self.grid_cells[index]

    def __len__(self):
        return len(self.grid_cells)


class FiringField:
    """
        Represents a grid cell's firing field in a triangular lattice.

        :param Module module: the module of which the grid cell belongs to
        :param float phase_x: phase shifted along triangular x-axis in rad (pos direction).
        :param float phase_y: phase shifted along triangular y-axis in rad (pos direction).
    """

    def __init__(self, module: Module, phase_x=0.0, phase_y=0.0):
        self.module = module
        self.phase_x = phase_x
        self.phase_y = phase_y

        self._phase_x_rect = self.module.phase_scale * phase_x + self.module.phase_scale * phase_y / 2
        self._phase_y_rect = self.module.phase_scale * phase_y * np.sqrt(3) / 2

    def probability(self, x: float, y: float) -> float:
        """
            Gives the probability of firing when organism is at rectangular coordinate point (x,y).

            :param float x: position along rectangular x-axis.
            :param float y: position along rectangular y-axis.

            :return: probability of grid cell firing at rectangular coordinates (x, y).
            :rtype float:
        """
        # shift due to phase
        pos = np.array([x - self._phase_x_rect,
                        y - self._phase_y_rect])

        # normalize activity on 0.0 to 1.0 scale
        normalized_activity = (np.cos(self.module.wave_vectors @ pos).sum() + 1.5) / 4.5

        # apply threshold (remove activity below threshold and normalize the rest)
        threshold_field = np.maximum(0.0, normalized_activity - self.module.threshold) / (1 - self.module.threshold)

        return self.module.base_prob + (self.module.max_prob - self.module.base_prob) * threshold_field
