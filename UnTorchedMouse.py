def main():

    import random as rd
    import turtle as tr
    import math as m

    interval = float(input("Enter the length of each timestep, in seconds. float. "))
    timeStep = 1
    simlen = int(input("What is the length you would like to run your simulation for in seconds? int."))

    # Tracking simulation over timestep
    deltaXPos = [0.0] * simlen
    deltaYPos = [0.0] * simlen
    deltaHyp = [0.0] * simlen
    instRadians = [0.0] * simlen
    instDegrees = [0.0] * simlen
    chance = [0] * simlen
    smallDX = [0.0] * simlen * int((1/interval))
    smallDY = [0.0] * simlen * int((1/interval))

    # Quadrant counters
    q1 = [0] * simlen
    q2 = [0] * simlen
    q3 = [0] * simlen
    q4 = [0] * simlen

    # Turtle setup
    graph = tr.Screen()
    graph.setup(width=1000, height=1000)

    mouse = tr.Turtle()
    mouse.shape("circle")
    mouse.speed(0)
    mouse.color("green")
    mouse.shapesize(0.5)
    mouse.pensize(3)

    tr.tracer(0)

    # Current position
    xCord = 0
    yCord = 0

    segments = int(1 / interval)

    for i in range(1, simlen):

        currentTime = i

        # Random displacement
        deltaXPos[i] = rd.randint(-100, 100) * timeStep
        deltaYPos[i] = rd.randint(-100, 100) * timeStep

        # Speed
        deltaHyp[i] = m.sqrt(deltaXPos[i]**2 + deltaYPos[i]**2)

        # 80% chance of continuing in previous direction
        chance[i] = rd.randint(0, 100)

        if chance[i] <= 80:
            if 0 <= instDegrees[i-1] < 90:
                deltaXPos[i] = abs(deltaXPos[i])
                deltaYPos[i] = abs(deltaYPos[i])

            elif 90 <= instDegrees[i-1] < 180:
                deltaXPos[i] = -abs(deltaXPos[i])
                deltaYPos[i] = abs(deltaYPos[i])

            elif 180 <= instDegrees[i-1] < 270:
                deltaXPos[i] = -abs(deltaXPos[i])
                deltaYPos[i] = -abs(deltaYPos[i])

            elif 270 <= instDegrees[i-1] < 360:
                deltaXPos[i] = abs(deltaXPos[i])
                deltaYPos[i] = -abs(deltaYPos[i])

        # Compute angle
        instRadians[i] = m.atan2(deltaYPos[i], deltaXPos[i])

        if instRadians[i] < 0:
            instRadians[i] += 2 * m.pi

        instDegrees[i] = m.degrees(instRadians[i])

        # Divide movement into smaller pieces
        smallDX = deltaXPos[i] / segments
        smallDY = deltaYPos[i] / segments

        for j in range(segments):

            xCord += smallDX
            yCord += smallDY

            # Bounce off walls
            if xCord >= 500:
                xCord = 500
                smallDX = -abs(smallDX)

            elif xCord <= -500:
                xCord = -500
                smallDX = abs(smallDX)

            if yCord >= 500:
                yCord = 500
                smallDY = -abs(smallDY)

            elif yCord <= -500:
                yCord = -500
                smallDY = abs(smallDY)

            mouse.goto(xCord, yCord)
            mouse.dot(10, "blue")
            print(xCord, yCord, smallDX, smallDY)
        tr.update()

    print("Simulation stopped at timestep:", currentTime)

    totalDistance = sum(deltaHyp)
    vectorFromStart = m.sqrt(xCord**2 + yCord**2)

    print(vectorFromStart, "is the vector distance from the starting position")
    print("Total path length:", totalDistance)
    print("This is a list of the x displacement each timestep:", smallDX)
    print("This is a list of the y displacement each timestep:", smallDY)
    print("This is how fast the mouse moved each timestep:", deltaHyp)

    tr.done()


main()