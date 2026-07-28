import numpy as np


class Module:
    """
    |    Represents grid cell module. Phase differs between cells.
    |    Access the i-th grid cell's properties using list notation: module[i]
    |    Note that triangular y-axis is pi/3 CCW from x-axis!

        :param float spacing: spatial scale in mm; distance between each lattice point.
        :param float orientation: rotation of grid in radians.
        :param float base_prob: lowest possible probability of each grid cell firing [0.0, 1.0].
        :param float max_prob: highest possible_probability of each grid cell firing [0.0, 1.0].
        :param float threshold: minimum normalized grid activity required for firing [0.0, 1.0).
            Values below threshold are set to zero, and remaining activity is rescaled 0 to 1.
    """

    def __init__(self, spacing=50.0, orientation=0.0, base_prob=0.0, max_prob=1.0, threshold=0.0):
        self.spacing = spacing  # s_i
        self.orientation = orientation
        self.base_prob = base_prob
        self.max_prob = max_prob
        self.threshold = threshold

        # phases in triangular coord grid, shape (N,)
        self._phase_x = np.empty(0, dtype=np.float64)
        self._phase_y = np.empty(0, dtype=np.float64)

        # cached phases in rect (x, y), shape (N, 2)
        self._phase_rect = np.empty((0, 2), dtype=np.float64)

        # some constants that will be helpful for computation later
        self.phase_scale = self.spacing / (2 * np.pi)  # used to convert from rad to rect dist
        wavelength = self.spacing / 2 * np.sqrt(3)
        scale = 2 * np.pi / wavelength

        # wave directions (rotated 2pi/3 from each other)
        angles = self.orientation + np.pi / 2 + np.array([0, 2 / 3 * np.pi, 4 / 3 * np.pi])
        wave_vectors = scale * np.stack((np.cos(angles), np.sin(angles)), axis=1)  # (3, 2)
        self._wave_vectors_T = wave_vectors.T

    def add_cell(self, phase_x=0.0, phase_y=0.0) -> int:
        """
            Adds one grid cell to the module.

            :param float phase_x: phase shifted along triangular x-axis in rad (pos direction).
            :param float phase_y: phase shifted along triangular y-axis in rad (pos direction).

            :return: index of added cell.
            :rtype int:
        """

        return self.add_cells_from_phase([phase_x], [phase_y])[0]

    def add_cells(self, num_x=1, num_y=1) -> tuple[int, int]:  # if anyone has better names here, please change LOL
        """
        |    Adds num_x * num_y grid cells to the module.
        |    Phases are evenly spaced from 0 to 2pi.

            :param int num_x: number of different phases along triangular x-axis.
            :param int num_y: number of different phases along triangular y-axis.

            :return: tuple containing the starting index (inclusive) and ending index (exclusive) of newly added cells.
            :rtype tuple:
        """

        phase_x = np.arange(num_x) * 2 * np.pi / num_x
        phase_y = np.arange(num_y) * 2 * np.pi / num_y
        grid_x, grid_y = np.meshgrid(phase_x, phase_y, indexing='ij')
        return self.add_cells_from_phase(grid_x.ravel(), grid_y.ravel())  # so that phase x and y per neuron match

    def add_cells_from_phase(self, phase_x, phase_y) -> tuple[int, int]:
        """
        |    Adds grid cells to the module with phases in phase_x and phase_y array-likes.

            :param phase_x: array-like of different phases along triangular x-axis.
            :param phase_y: array-like of different phases along triangular y-axis.

            :return: tuple containing the starting index (inclusive) and ending index (exclusive) of newly added cells.
            :rtype tuple:
        """

        # make sure things are in numpy arrays
        phase_x = np.asarray(np.atleast_1d(phase_x), dtype=np.float64)
        phase_y = np.asarray(np.atleast_1d(phase_y), dtype=np.float64)

        start = len(self)

        # add phases to lists
        self._phase_x = np.concatenate([self._phase_x, phase_x])
        self._phase_y = np.concatenate([self._phase_y, phase_y])

        # update cached rect phases
        rect_x = self.phase_scale * phase_x + self.phase_scale * phase_y / 2
        rect_y = self.phase_scale * phase_y * np.sqrt(3) / 2
        self._phase_rect = np.concatenate([self._phase_rect, np.stack([rect_x, rect_y], axis=1)], axis=0)

        end = len(self)
        return start, end

    def probabilities(self, positions: np.ndarray[np.float64]) -> np.ndarray[np.float64]:
        """
            Gives the probabilities of firing for all neurons when organism is positions in rectangular coordinates.

            :param np.ndarray[np.float64] positions: positions along rectangular axes given, shape (M, 2).

            :return: probabilities of grid cell firing at rectangular coordinates, shape (M, N).
            :rtype np.ndarray[np.float64]:
        """
        # shifts due to phase
        positions = np.asarray(positions, dtype=np.float64)
        if positions.ndim != 2 or positions.shape[1] != 2: raise ValueError("positions must be shape (M, 2)")
        relative_pos = positions[:, None, :] - self._phase_rect[None, :, :]  # (M, N, 2)

        # project onto the three wave vectors
        projections = relative_pos @ self._wave_vectors_T  # shape (M, N, 3)

        # normalize activity on 0.0 to 1.0 scale
        normalized_activity = (np.cos(projections).sum(axis=-1) + 1.5) / 4.5  # (M, N)

        # apply threshold (remove activity below threshold and normalize the rest)
        threshold_field = np.maximum(0.0, normalized_activity - self.threshold) / (1 - self.threshold)

        return self.base_prob + (self.max_prob - self.base_prob) * threshold_field

    def __getitem__(self, index):
        return {
            "phase_x": self._phase_x[index],
            "phase_y": self._phase_y[index],
            "phase_rect": self._phase_rect[index]
        }

    def __len__(self):
        return len(self._phase_x)
