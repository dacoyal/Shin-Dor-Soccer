import math, copy, random
from cmu_112_graphics import *
#want to check wether we hit the left or right part of the player
#then decided of wether to go right or left
#check wether cx + app.r or cx - app.r hits the same x as the rectangle
def gameDimensions():
    width = 200
    height = 200
    radiusBall = 10
    cx, cy = radiusBall, radiusBall
    return width, height, radiusBall, cx , cy

def appStarted(app): 
    app.width, app.height, app.r, app.ballCx, app.ballCy = gameDimensions()
    #direction of the ball, - is up and left, positive is for down and right
    app.bdy = 0 #movement y of the ball 
    app.bdx = 2 #movement x of the ball 
    app.gravity = 2
    app.timerDelay = 60
    app.time = 0
    app.epsilon = 10**-3
    #coordinates of our rectangle person
    app.x0, app.y0, app.x1, app.y1 = (app.width//2 - app.r, app.height//8,
    app.width//2, app.height)
    doStep(app)

def doStep(app):
    app.bdy += app.gravity
    app.ballCy += app.bdy

    #once the ball reaches constant ground level make sure it does not bounce
    if app.ballCy == app.height - app.r:
        app.ballCy = app.height - app.r
        app.bdy = 0
        app.gravity = 0

    elif app.ballCy + app.r >= (app.height) and app.bdy > 0: 
        app.bdy = -app.bdy 
 
    elif app.ballCy <= app.r: 
        app.bdy = -app.bdy 
     
    app.ballCx += app.bdx

    #once the ball does not bounce anymore apply friction
    if app.gravity == 0 : 
        app.time += 1
        if abs(app.bdx) < 1 * 10**(-5): 
            app.bdx = 0
        if app.bdx != 0: 
            if app.bdx > 0:
                app.bdx -= 0.05
            else: 
                app.bdx += 0.05
    if app.ballCx >= app.width - app.r: 
        app.ballCx = app.width - app.r 
        app.bdx = -app.bdx

    elif app.ballCx <= app.r: 
        app.ballCx = app.r
        app.bdx = -app.bdx
    #check if the ball hits the player
    checkBallHitsPlayer(app)

def checkBallHitsPlayer(app): 
    #Same x position and ball is in y range of the person
    leftPosition = abs(abs(app.x0 - app.r) - app.ballCx)
    rightPosition = abs(abs(app.x1 + app.r) - app.ballCx)
    if (leftPosition <= app.epsilon and leftPosition >= 0
    or rightPosition <= app.epsilon and rightPosition >= 0): 
        if app.ballCy >= app.y0 and app.ballCy <= app.y1:
            app.bdx = -app.bdx
    
def timerFired(app): 
    doStep(app)

def keyPressed(app, event):
    if event.key == 'Left':
        app.x0 -= 5
        app.x1 -= 5

        #make sure the rectangle does not go over the ball
        if app.ballCx < app.x0 and app.x0 < app.ballCx + app.r: 
            app.x0 += 5 
            app.x1 += 5 
            app.bdx = -app.bdx

        #check for out of bounds
        if app.x0 < 0: 
            app.x0 +=5 
            app.x1 += 5
        checkBallHitsPlayer(app)

    elif event.key == 'Right':
        app.x0 += 5
        app.x1 += 5
        #make sure the rectangle does not go over the ball
        if app.ballCx > app.x1 and app.x1 > app.ballCx - app.r: 
            app.x0 -= 5
            app.x1 -= 5
            app.bdx = -app.bdx
        #check for out of bounds
        if app.x1 > app.width:
            app.x1 -= 5
            app.x0 -= 5
        checkBallHitsPlayer(app)
    
def redrawAll(app, canvas): 
    canvas.create_rectangle(0,0, app.width, app.height, fill = "black")
    canvas.create_oval(app.ballCx - app.r, app.ballCy - app.r, app.ballCx 
    + app.r, app.ballCy + app.r, fill = "cyan")
    canvas.create_rectangle(app.x0, app.y0, app.x1, app.y1, fill = 'purple')

def playBall(): 
    runApp(width = 200 , height = 200)

def main():
    playBall()

if __name__ == '__main__':
    main()