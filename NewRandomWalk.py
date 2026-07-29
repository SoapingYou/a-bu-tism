def main():
    ## modules for random number generation, angle of walk generation, and graph generation
    import random as rd
    import math as mt

    ##setting parameters of simulation
    timestep = float(input("What is the resolution(in seconds) of your simulation(float, 0.001 recommended)?"))
    simlen = int(input("please enter the length of your simulation in seconds(int, 20-100 recommended)"))*int((1/timestep))
    deltaheading = float(input(
        """
    what is the number of degrees the mouse can turn in one timestep
    (about 2.4 degrees, assuming it takes the mouse 75 ms to do 180)"""))

    ## setting up empty lists to fill with accessible variables
    accessiblespeed = [0.0]*simlen
    accessiblehead = [0.0]*simlen
    accessiblexlist = [0.0]*simlen
    accessibleylist = [0.0]*simlen
    accessibledx = [0.0]*simlen
    accessibledy = [0.0]*simlen

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

        def headupdate(self):
            self.headdirection += gensmallangle()
            if self.xpos >= 1000:
                self.headdirection = mt.pi
            if self.xpos <= -1000:
                self.headdirection = 0
            if self.ypos >= 1000:
                self.headdirection = 3*mt.pi/2
            if self.ypos <= -1000:
                self.headdirection = mt.pi/2
            return self.headdirection

        def speedupdate(self):
            self.speed += genspeed()
            if self.speed < 0:
                self.speed = 0
            self.speed = min(self.speed, 100)
            return self.speed

    kaelyn = Mouse(0,0,0,0)

    def simloop():
        for i in range (0,simlen):
            kaelyn.speedupdate()
            kaelyn.posupdate()
            kaelyn.headupdate()


            accessiblespeed[i] = kaelyn.speed
            accessiblehead[i] = kaelyn.headdirection
            accessiblexlist[i] = kaelyn.xpos
            accessibleylist[i] = kaelyn.ypos
            accessibledx[i] = kaelyn.dx
            accessibledy[i] = kaelyn.dy

    def turtlebit():
        import turtle as tr

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

    simloop()
    turtlebit()
    ##print("this is the mouse's change each in x timestep:",accessibledx)
    ##print("this is the mouse's change in y each timestep:",accessibledy)
    print("this is the mouse's speed each timestep:", accessiblespeed)
    # print(accessiblespeed)
    # print(accessiblehead)
    print(accessiblexlist)
    print(accessibleylist)
    print(accessiblexlist[-1], accessibleylist[-1])
    totalhomedist = mt.sqrt((accessiblexlist[simlen-1]**2) + (accessibleylist[simlen-1]**2))
    print("the mouse moved this far:", totalhomedist)
    return accessiblexlist, accessibleylist, timestep, simlen
