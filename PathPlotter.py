import turtle as tr
import numpy as np
import matplotlib.pyplot as plt

class PathPlotter:
    def __init__(self):
        pass
    def turtlebit(self, accessiblexlist,accessibleylist, accessiblespeed=None):
        simlen = len(accessiblexlist)
        screen = tr.Screen()
        screen.setup(width=1200, height=1200)
        screen.setworldcoordinates(-1200, -1200, 1200, 1200)

        mouse = tr.Turtle()
        mouse.pensize(2)
        mouse.speed(0)
        mouse.dot(5, "blue")
        screen.tracer(0)

        for i in range(0, simlen):
            if 0 <= accessiblespeed[i] < 20:
                mouse.pencolor("blue")
            elif 20 <= accessiblespeed[i] < 40:
                mouse.pencolor("green")
            elif 40 <= accessiblespeed[i] < 60:
                mouse.pencolor("yellow")
            elif 60 <= accessiblespeed[i] < 80:
                mouse.pencolor("orange")
            else:
                mouse.pencolor("red")
            mouse.goto(accessiblexlist[i], accessibleylist[i])
        screen.update()

        tr.done()
    def paths(self,paths:np.ndarray, colors=[], labels=[]):
        """
        plots all paths in their colors
        :param np.ndarray paths: ((x,y)) 3d numpy array. k x n x 2, where k is # of path
                                    k is number of paths, xi, yi is coords
        :param list colors: list of colors (matplotlib compliant or hex code)
        """

        for i in range(paths.shape[0]):
            plt.plot(paths[i,:,0], paths[i,:,1], color=colors[i], label=labels[i])
        plt.legend()
        plt.show()


    def two_turtlebit(self, og_positions, sim_positions):
        simlen = len(og_positions)

        try:
            screen = tr.getscreen()
        except Exception:
            screen = tr.Screen()
        
        screen.setup(width=1200, height=1200)
        screen.setworldcoordinates(-1200, -1200, 1200, 1200)

        mouse = tr.Turtle()
        mouse.pensize(2)
        mouse.speed(0)
        mouse.dot(5, "blue")
        mouse.pencolor("red")

        screen.tracer(0)
        for i in range(0, simlen):
            mouse.goto(og_positions[i,0],og_positions[i,1])
            mouse.dot(2)
        screen.update()
        mouse.penup()
        mouse.home()
        mouse.pendown()
        mouse.dot(5,)
        mouse.pencolor("blue")
        for i in range(0, simlen):
            mouse.goto(sim_positions[i,0], sim_positions[i,1])
            mouse.dot(2)
        screen.update()
        tr.done()
