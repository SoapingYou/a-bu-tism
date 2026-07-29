def main():
    ## modules for random number generation, angle of walk generation, and graph generation
    import random as rd
    import math as mt

    ##setting parameters of simulation
    timestep = float(input("What is the resolution(in seconds) of your simulation(float)?"))
    simlen = int(input("please enter the length of your simulation in seconds"))*int((1/timestep))
    deltaheading = float(input(
        """
    what is the number of degrees the mouse can turn in one timestep
    (about 2.4 degrees for ms, assuming it takes the mouse 75 ms to do 180)"""))

    ## setting up empty lists to fill with accessible variables
    accessiblespeed = [0.0]*simlen
    accessiblehead = [0.0]*simlen
    accessiblexlist = [0.0]*simlen
    accessibleylist = [0.0]*simlen

    ## generating a small turn in the animal's head direction
    def gensmallangle():
        instangle = rd.randint(-180, 180)
        instrad = (instangle / 180) * mt.pi        ## generate an angle in radians
        smallinstrad = (instrad / 360) * ((deltaheading * 1000) * timestep)  ## generate a small angle for how much
        ##the mouse can turn in one timestep based on real mice turning at about 2.4 degrees per millisecond
        return smallinstrad

    def genspeed():
        instspeed = rd.randint(-1000, 1000) * timestep
        return instspeed

    class Mouse:
        def __init__(self, xpos, ypos, headdirection, speed):
            self.ypos = ypos  ## total y position
            self.xpos = xpos  ## total x position
            self.headdirection = headdirection  ## direction the mouse is facing, between 0-2pi
            self.speed = speed  ## speed of the mouse

        def posupdate(self):  ## update the position of the mouse
            self.dx = self.speed *timestep * mt.cos(self.headdirection) ##take the angle and make x out of it using current speed as hypotenuse, controlling for timestep
            self.dy = self.speed * timestep * mt.sin(self.headdirection)## take the angle and make y out of it using current speed as hypotenuse, controlling for timestep
            self.xpos += self.dx
            self.ypos += self.dy
            return self.ypos, self.xpos

        def headupdate(self): ## update head with small random angle
            self.headdirection += gensmallangle()
            return self.headdirection

        def speedupdate(self): ## update speed with random added/subtracted speed, max speed = 1000
            self.speed += genspeed()
            if self.speed < 0:
                self.speed = 0
            self.speed = min(self.speed, 1000)
            return self.speed

    kaelyn = Mouse(0,0,0,0) ## kaelyn asked for it to be named after her :)
    ##it's her bday today on the 29th!!!

    def simloop():##loop all class functions
        for i in range (0,simlen):
            kaelyn.speedupdate()
            kaelyn.headupdate()
            kaelyn.posupdate()

##create index-able lists
            accessiblespeed[i] = kaelyn.speed
            accessiblehead[i] = kaelyn.headdirection
            accessiblexlist[i] = kaelyn.xpos
            accessibleylist[i] = kaelyn.ypos

    def turtlebit(): ## individual turle section, can be removed if needed
        import turtle as tr

        screen = tr.Screen() ##screen setup
        screen.setup(width=1200, height=1200)
        screen.setworldcoordinates(-1200, -1200, 1200, 1200)

        mouse = tr.Turtle() ##mouse setup
        mouse.pensize(2)
        mouse.color("purple")
        mouse.dot(5, "blue")
        screen.tracer(0)

        for i in range(0, simlen): ## world borders
            if accessiblexlist[i] > 1000:
                accessiblexlist[i] = 1000
            if accessiblexlist[i] < -1000:
                accessiblexlist[i] = -1000
            if accessibleylist[i] > 1000:
                accessibleylist[i] = 1000
            if accessibleylist[i] < -1000:
                accessibleylist[i] = -1000

            mouse.goto(accessiblexlist[i], accessibleylist[i]) ## update mouse position with new position
        screen.update()

        tr.done()

    simloop() ## run all functions, print lists of all data and the total distance from home
    turtlebit()
    print(accessiblespeed)
    print(accessiblehead)
    print(accessiblexlist)
    print(accessibleylist)
    totalhomedist = mt.sqrt((accessiblexlist[simlen-1]**2) + (accessibleylist[simlen-1]**2))
    print("the mouse moved this far:", totalhomedist)


main()
