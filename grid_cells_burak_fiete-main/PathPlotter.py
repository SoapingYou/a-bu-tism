import numpy as np
import matplotlib.pyplot as plt

class PathPlotter:
    def __init__(self):
        pass
    
    def paths(self,paths:np.ndarray, colors=[], labels=[]):
        """
        plots all paths in their colors
        :param np.ndarray paths: ((x,y)) 3d numpy array. k x n x 2, where k is # of path
                                    k is number of paths, xi, yi is coords
        :param list colors: list of colors (matplotlib compliant or hex code)
        """

        for i in range(len(paths)):
            plt.plot(paths[i][:,0], paths[i][:,1], color=colors[i], label=labels[i])
        plt.legend()
        plt.show()