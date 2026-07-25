import random as rd
import turtle as tr
import math as m

timeStep = 1
simlen = int(input("What is the length you would like to run your simulation for?"))
decimals = int(input("What is the decimal place accuracy of the mouse's movements?"))
currentTime = [0]*simlen
deltaXPos = [0.0]*simlen
deltaYPos = [0.0]*simlen
deltaHyp = [0.0]*simlen
instRadians = [0.0]*simlen
instDegrees = [0.0]*simlen
chance = [0]*simlen
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

    deltaXPos[i] = rd.randint(-100*decimals,100*decimals)/decimals
    deltaYPos[i] = rd.randint(-100*decimals, 100*decimals) / decimals
    deltaHyp[i] = m.sqrt((deltaYPos[i]*deltaYPos[i])+(deltaXPos[i]*deltaXPos[i]))

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

    instRadians[i] = m.atan2(deltaYPos[i], deltaXPos[i])
    if instRadians[i] < 0.0:
        instRadians[i] = (2*m.pi)+instRadians[i]
    instDegrees[i] = (instRadians[i]*(180/m.pi))
    if instDegrees[i] < 0:
        instDegrees[i] = instDegrees[i] + 360

    xCord = sum(deltaXPos)
    yCord = sum(deltaYPos)
    xCord = max(-500, min(500,xCord))
    yCord = max(-500, min(500,yCord))

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

    mouse.goto(xCord, yCord)
    mouse.dot(10,"blue")

totalDistance = sum(deltaHyp)
vectorFromStart = m.sqrt((yCord*yCord)+(xCord*xCord))
print(vectorFromStart,"is the vector distance from the starting position")
print("This is a list of the x coordinate at each time step:", deltaXPos)
print("This is a list of the y coordinate at each time step:", deltaYPos)
print("This is how fast the mouse moved each timestep, of course in cm/s:",deltaHyp)

tr.done()
