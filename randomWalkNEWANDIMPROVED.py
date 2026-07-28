def main():

    ## modules for random number generation, angle of walk generation, and graph generation
    import random as rd
    import numpy as np
    import math as mt
    import turtle as tr

    timestep = float(input("What is the resolution(in seconds) of your simulation(float)?"))
    simlen = int(input("please enter the length of your simulation in seconds"))
    deltaheading = int(input(
    """what is the number of degrees the mouse can turn in one timestep
    (about 0.1 degrees, assuming it takes the mouse a second to turn around)"""))

    class Mouse:
        def __init__(self, xpos, ypos, headdirection, speed):
            self.ypos = ypos ## total y position
            self.xpos = xpos ## total x position
            self.dx = [0] ## Instantaneous change in x position
            self.dy = [0] ## Instantaneous change in x position
            self.headdirection = headdirection ## direction the mouse is facing
            self.speed = speed ## speed of the mouse

        def posupdate(self): ## update the position of the mouse
            self.xpos += self.dx
            self.ypos += self.dy
            return self.xpos, self.ypos

        def headupdate(self):
            self.headdirection += gensmallangle()


    def genangle(): ## generate an angle in radians
        instangle= rd.randint(0,359)
        instrad = (instangle/180)*mt.pi
        return instrad
    
    def gensmallangle(): ## generate an angle in radians
        smallinstrad = (genangle()/360)*((2.4*1000)*timestep)## generate a small angle for how much 
        ##the mouse can turn in one timestep based on real mice turning at about 2.4 degrees per millisecond
        return smallinstrad

    newangle = gensmallangle()
    print(newangle)





main()
main()
