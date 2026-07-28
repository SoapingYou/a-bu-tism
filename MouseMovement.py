# The user specifies the length of the simulation and the decimal place accuracy of the mouse's movements. 
#outputs (x,y) coordinates, speed, and vector distance from the starting position at each time step
#with an 80% chance of moving in the same direction as the previous step and a 20% chance of moving in a random direction

import random as rd
import turtle as tr
import math as m

#variables for the simulation

timeStep = 1

#prompt user for simulation parameters
simlen = int(input("What is the length you would like to run your simulation for?"))
decimals = int(input("What is the decimal place accuracy of the mouse's movements?"))

#tracking simulation over timestep
currentTime = [0]*simlen
deltaXPos = [0.0]*simlen
deltaYPos = [0.0]*simlen
deltaHyp = [0.0]*simlen
instRadians = [0.0]*simlen
instDegrees = [0.0]*simlen
chance = [0]*simlen

#quadrant counters for analysis 
q1 = [0]*simlen
q2 = [0]*simlen
q3 = [0]*simlen
q4 = [0]*simlen

##Turtle Setup:
graph = tr.Screen()
graph.setup(width=1000,height=1000)

mouse = tr.Turtle()
mouse.shape("circle")
mouse.speed(0)
mouse.color("green")
mouse.shapesize(0.5)   # Make the dot smaller
mouse.pensize(3)


for i in range (1,simlen):
    currentTime[i] = i * timeStep

    preXCord = sum(deltaXPos)
    preYCord = sum(deltaYPos)

#random displacement components scaled by factor for accuracy
    deltaXPos[i] = rd.randint(-100*decimals,100*decimals)/decimals
    deltaYPos[i] = rd.randint(-100*decimals, 100*decimals) / decimals
#calculating step speed and displacement magnitude
    deltaHyp[i] = m.sqrt((deltaYPos[i]*deltaYPos[i])+(deltaXPos[i]*deltaXPos[i]))
# 80% chance of moving in the same direction as the previous step, 20% chance of moving in a random direction
    chance[i] = rd.randint(0,100)
    if chance[i]/100 <= 80/100:
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
#computing the instantaneous angle of movement 
    instRadians[i] = m.atan2(deltaYPos[i], deltaXPos[i])
    if instRadians[i] < 0.0:
        instRadians[i] = (2*m.pi)+instRadians[i]
    instDegrees[i] = (instRadians[i]*(180/m.pi))
    if instDegrees[i] < 0:
        instDegrees[i] = instDegrees[i] + 360
#calclate cumulative distance from starting position
    xCord = sum(deltaXPos)
    yCord = sum(deltaYPos)
#make sure the mouse stays within the bounds of the screen
    xCord = max(-500, min(500,xCord))
    yCord = max(-500, min(500,yCord))
#if mouse reaches the edge of the screen, it will bounce back in the opposite direction
    if xCord == 500:
        deltaXPos[i] = -abs(deltaXPos[i])
        xCord = xCord+deltaXPos[i]
    if xCord == -500:
        deltaXPos[i] = abs(deltaXPos[i])
        xCord = xCord+abs(deltaXPos[i])
    if yCord == 500:
        deltaYPos[i] = -abs(deltaYPos[i])
        yCord = yCord+deltaYPos[i]
    if yCord == -500:
        deltaYPos[i] = abs(deltaYPos[i])
        yCord = yCord+abs(deltaYPos[i])
#draw the mouse's movement on the screen
    mouse.goto(xCord, yCord)
    mouse.dot(10,"blue")
#output the mouse's position and speed at each timestep
totalDistance = sum(deltaHyp)
vectorFromStart = m.sqrt((yCord*yCord)+(xCord*xCord))
print(vectorFromStart,"is the vector distance from the starting position")
print("This is a list of the x coordinate at each time step:", deltaXPos)
print("This is a list of the y coordinate at each time step:", deltaYPos)
print("This is how fast the mouse moved each timestep, of course in cm/s:",deltaHyp)

tr.done()

#NEW CODE
#NEW CODE
#NEW CODE
#NEW CODE
#NEW CODE
#NEW CODE
#NEW CODE
#NEW CODE
#NEW CODE
#NEW CODE
#NEW CODE
#NEW CODE

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
