import turtle as tr

class TurtlePlotter:
    def __init__(self):
        pass
    def turtlebit(self, accessiblespeed, accessiblexlist,accessibleylist):
        simlen = len(accessiblespeed)
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
