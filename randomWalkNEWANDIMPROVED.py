def main():

    ## modules for random number generation, angle of walk generation, and graph generation
    import random as rd
    import numpy as np
    import math as mt
    import turtle as tr

    timestep = float(input("What is the resolution(in seconds) of your simulation(float)?"))
    simlen = int(input("please enter the length of your simulation in seconds"))

    class Mouse:
        def __init__(self, xpos, ypos):
            self.ypos = ypos ## total y position
            self.xpos = xpos ## total x position
            self.dx = [0] ## Instantaneous change in x position
            self.dy = [0] ## Instantaneous change in x position
        def posupdate(self): ## update the position of the mouse
            self.xpos += self.dx
            self.ypos += self.dy
            return self.xpos, self.ypos

    def genangle(): ## generate an angle in radians
        instangle= rd.randint(0,359)
        instrad = (instangle/180)*mt.pi
        return instrad

    newangle = genangle()
    print(newangle)





main()