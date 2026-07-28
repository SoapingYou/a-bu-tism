# The user specifies the length of the simulation and the decimal place accuracy of the mouse's movements. 
#outputs (x,y) coordinates, speed, and vector distance from the starting position at each time step
#with an 80% chance of moving in the same direction as the previous step and a 20% chance of moving in a random direction
def main():

    import random as rd
    import turtle as tr
    import torch

    interval = float(input("Enter the length of each timestep, in seconds. float. "))
    timeStep = 1
    simlen = int(input("What is the length you would like to run your simulation for in seconds? int."))

    # Tracking simulation over timestep
    deltaXPos = torch.zeros(simlen, dtype=torch.float32, requires_grad=True)
    deltaYPos = torch.zeros(simlen, dtype=torch.float32, requires_grad=True)
    deltaHyp = torch.zeros(simlen, dtype=torch.float32)
    instRadians = torch.zeros(simlen, dtype=torch.float32)
    instDegrees = torch.zeros(simlen, dtype=torch.float32)
    chance = torch.zeros(simlen, dtype=torch.int32)
    num_small_steps = simlen * int(1/interval)
    smallDX = torch.zeros(num_small_steps, dtype=torch.float32)
    smallDY = torch.zeros(num_small_steps, dtype=torch.float32)

    # Quadrant counters
    q1 = torch.zeros(simlen, dtype=torch.int32)
    q2 = torch.zeros(simlen, dtype=torch.int32)
    q3 = torch.zeros(simlen, dtype=torch.int32)
    q4 = torch.zeros(simlen, dtype=torch.int32)

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
    xCord = torch.tensor(0.0, dtype=torch.float32)
    yCord = torch.tensor(0.0, dtype=torch.float32)

    segments = int(1 / interval)

    for i in range(1, simlen):

        currentTime = i

        # Random displacement
        dx_val = torch.tensor(float(rd.randint(-100, 100) * timeStep), dtype=torch.float32)
        dy_val = torch.tensor(float(rd.randint(-100, 100) * timeStep), dtype=torch.float32)

        # Speed
        deltaXPos = deltaXPos.clone()
        deltaYPos = deltaYPos.clone()
        deltaXPos[i] = dx_val
        deltaYPos[i] = dy_val

        deltaHyp = deltaHyp.clone()
        deltaHyp[i] = torch.sqrt(deltaXPos[i]**2 + deltaYPos[i]**2)

        # 80% chance of continuing in previous direction
        chance[i] = rd.randint(0, 100)

        if chance[i] <= 80:
            prev_deg = instDegrees[i-1].item()
            if 0 <= prev_deg < 90:
                dx_val = torch.abs(dx_val)
                dy_val = torch.abs(dy_val)

            elif 90 <= prev_deg < 180:
                dx_val = -torch.abs(dx_val)
                dy_val = torch.abs(dy_val)

            elif 180 <= prev_deg < 270:
                dx_val = -torch.abs(dx_val)
                dy_val = -torch.abs(dy_val)

            elif 270 <= prev_deg < 360:
                dx_val = torch.abs(dx_val)
                dy_val = -torch.abs(dy_val)

            deltaXPos[i] = dx_val
            deltaYPos[i] = dy_val
            deltaHyp[i] = torch.sqrt(deltaXPos[i]**2 + deltaYPos[i]**2)

        # Compute angle
        instRadians = instRadians.clone()
        instDegrees = instDegrees.clone()
        instRadians[i] = torch.atan2(deltaYPos[i], deltaXPos[i])

        if instRadians[i] < 0:
            instRadians[i] += 2 * torch.pi

        instDegrees[i] = instRadians[i] * (180.0 / torch.pi)

        # Divide movement into smaller pieces
        # Note: These assignments overwrite the `smallDX` and `smallDY` tensors initialized earlier
        smallDX = deltaXPos[i] / segments
        smallDY = deltaYPos[i] / segments

        for j in range(segments):

            xCord = xCord + smallDX
            yCord = yCord + smallDY

            # Bounce off walls
            if xCord >= 500:
                xCord = torch.tensor(500.0, dtype=torch.float32)
                smallDX = -torch.abs(smallDX)

            elif xCord <= -500:
                xCord = torch.tensor(-500.0, dtype=torch.float32)
                smallDX = torch.abs(smallDX)

            if yCord >= 500:
                yCord = torch.tensor(500.0, dtype=torch.float32)
                smallDY = -torch.abs(smallDY)

            elif yCord <= -500:
                yCord = torch.tensor(-500.0, dtype=torch.float32)
                smallDY = torch.abs(smallDY)

            mouse.goto(xCord.item(), yCord.item())
            mouse.dot(10, "blue")
        tr.update()

    print("Simulation stopped at timestep:", currentTime)

    totalDistance = torch.sum(deltaHyp)
    vectorFromStart = torch.sqrt(xCord**2 + yCord**2)

    print(vectorFromStart.item(), "is the vector distance from the starting position")
    print("Total path length:", totalDistance.item())
    print("This is a list of the x displacement each timestep:", smallDX.item())
    print("This is a list of the y displacement each timestep:", smallDY.item())
    print("This is how fast the mouse moved each timestep:", deltaHyp.tolist())

    tr.done()

main()

