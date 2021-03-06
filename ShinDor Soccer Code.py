#####################################################################################
# 15-112:Fundamentals of Programming and Computer Science
# Carnegie Mellon University
# Final Project: ShinDor Soccer
# Code by: Alejandro Ruiz
# Graphics by: Daniela Ruiz
#####################################################################################


import pygame
import os
import math
import time
from pygame import mixer
import random
from datetime import datetime

#this will get the current hour and time of today

today = datetime.now()
hourToday = today.hour
minuteToday = today.minute
stadiumImg = None
#determine wether the background should be day or night
if hourToday >= 19 or hourToday < 6:
    #stadium made by Daniela Ruiz Gomez inspired from a stadium from the game "Head Soccer La Liga"
    stadiumImg = "Head Soccer Background Dani Edited.png"
else:
    #stadium made by Daniela Ruiz Gomez inspired from a stadium from the game "Head Soccer La Liga"
    stadiumImg ="Day Stadium Edited.png"

pygame.init()
#creates the screen, where 800 is width and 600 is the height
widthScreen = 1100    #800
heightScreen = 600  #600
clock = pygame.time.Clock()
screen = pygame.display.set_mode((widthScreen, heightScreen))
#Image made by Daniela Ruiz Gomez

#Tile and Icon of the window
pygame.display.set_caption("ShinDor Soccer")

#declare variables
# from: https://vectortoons.com/products/a-groovy-looking-nightclub-dance-floor-background
disco = pygame.image.load("disco.jpg")
#<div>Icons made by <a href="https://www.flaticon.com/authors/alfredo-hernandez" title="Alfredo Hernandez">Alfredo Hernandez</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
xImg = pygame.image.load("xbutton.png")

#pause image gotten from: https://www.clipartmax.com/download/m2i8Z5H7Z5G6Z5G6_389-free-vector-icons-red-pause-button-png/
pauseImg = pygame.image.load("Pause.png")

##Soccer gotten from: http://www.pngmart.com/image/592
soccerImg = pygame.image.load("Soccer.png")

#Doraemon gotten from: https://www.pngfind.com/mpng/hJohToh_free-download-doraemon-png-clipart-doraemon-doraemon-transparent/
guestPlayerImg = pygame.image.load("Doraemon Left.png")

#Shin Chan gotten from: https://www.seekpng.com/ipng/u2q8u2a9r5t4q8q8_shin-chan-shin-chan/
playerImg = pygame.image.load("Shin Chan Right.png")

#Goal Image gotten from: https://www.seekpng.com/idown/u2q8e6y3t4w7y3r5_soccer-goal-sprite-006-soccer-goal-sprite-sheet/
goalLeftImg = pygame.image.load("Goal Left Fixed.png")
goalRightImg = pygame.image.load("Goal Right Fixed.png")

#Up Icon made by Daniela Ruiz Gomez 
#png inside block from: https://www.pngwing.com/en/free-png-mralp
superJumpImg = pygame.image.load("Super Jump Dani Resized.png")

#Image made by Daniela Ruiz Gomez
runFastImg = pygame.image.load("Run Fast Dani Edited.png")

#https://www.pngitem.com/middle/iTJxi_3d-play-button-png-transparent-png/
playImg = pygame.image.load("Play.png")

#https://www.kindpng.com/downpng/obboRo_restart-button-being-more-experienced-team-leaders-so-delhi-logo-png-transparent/
restartImg = pygame.image.load("Restart.png")

#https://imgbin.com/download-png/7Ayuc7gZ
doramiImg = pygame.image.load("Dorami.png")

#jail from : https://www.tornado-studios.com/stock-3d-models/jail-cell-01
#nobita crying from Doraemon series
#image made by Daniela Ruiz Gomez
nobitaJail = pygame.image.load("Nobita Jail Resized.png")

goalHeight = 250
goalWidth = 127
time = 0


#Doraemon intro png gotten from: http://pluspng.com/png-83346.html
doraemonIntroImg = pygame.image.load("Doraemon Intro.png")

#Shin Chan intro png gotten from:https://www.uihere.com/free-cliparts/crayon-shin-chan-comedy-film-anime-youtube-crayon-1565529
shinChanIntroImg = pygame.image.load("Shin Chan Intro.png")

#Soccer Intro png gotten from: https://clipartpng.com/?855,soccer-ball-png-clipart
soccerIntroImg = pygame.image.load("Soccer Intro.png")

#readFile and writeFile from: https://www.cs.cmu.edu/~112/notes/notes-strings.html
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

#############################
#create classes for ball, players, buttons and pause
#############################
class Button(object):

    def __init__(self, x, y, width, height, fontButton, color1, colorButton, text, xCenterText, yCenterText, pressed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color1 = color1
        self.text = text
        self.font = fontButton
        self.colorButton = colorButton
        self.xCenter = xCenterText
        self.yCenter = yCenterText
        self.pressed = pressed
        self.saveColor1 = color1
        self.saveColorButton = colorButton

    #displayButton creates the button and displays it
    def displayButton(self, screen):
        textButton = self.font.render(self.text, True, self.color1)
        buttonRectangle = textButton.get_rect()
        buttonRectangle.center = (self.xCenter, self.yCenter)
        pygame.draw.rect(screen, self.colorButton, (self.x, self.y, self.width, self.height))
        screen.blit(textButton, buttonRectangle)

    #overButton changes the color of the button if we put our mouse over it, to improve the user experience
    def overButton(self, mouseCoordX, mouseCoordY):
        black = (0, 0, 0)
        yellow = (255, 255, 0)
        #now check that the mouseCoordX and mouseCoordY are in the range of the rectangle we drew
        if ((mouseCoordX >= self.x and mouseCoordX <= self.x + self.width) and 
        (mouseCoordY >= self.y and mouseCoordY <= self.y + self.height)):
            self.color1 = black
            self.colorButton = yellow
        else:
            self.color1 = self.saveColor1
            self.colorButton = self.saveColorButton

    #pressedButton checks to see if the mouseButton was pressed and if it is pressed it changes the color of the button back to its original color
    def pressedButton(self, mouseCoordX, mouseCoordY):
        #now check that the mouseCoordX and mouseCoordY are in the range of the rectangle we drew
        if ((mouseCoordX >= self.x and mouseCoordX <= self.x + self.width) and 
        (mouseCoordY >= self.y and mouseCoordY <= self.y + self.height)):
            self.color1 = self.saveColor1
            self.colorButton = self.saveColorButton
            self.pressed = True
        #check if the mouse coordinates are inside the button range. If it is the button has been pressed

class PauseGame(object):

    def __init__(self, width, height, x, y, pressed):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.pressed = pressed

    def pressedPause(self, mouseCoordX, mouseCoordY):
        if ((mouseCoordX >= self.x and mouseCoordX <= self.x + self.width) and 
        (mouseCoordY >= self.y and mouseCoordY <= self.y + self.height)):
            self.pressed = True


class Ball(object):

    def __init__(self, x, y, width, height, soccerBDX, soccerBDY, friction, gravity, airResistance):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.BDX = soccerBDX
        self.BDY = soccerBDY
        self.friction = friction
        self.gravity = gravity
        self.airResistance = airResistance
    
    #this function changes the value of the movement in change of y of the ball
    #to make it move like if it had gravity applied on it
    def applyGravity(self):
        if self.gravity != 0:
            self.BDY += self.gravity
            self.y += self.BDY
    
    def applyXMovement(self):
        self.x += self.BDX

        #this function checks for a collision with the ground and if so changes the
        #direction of the ball
    def checkForCollisionWithGround(self, heightScreen):
        bouncing_Sound = mixer.Sound("Bounce.mp3")
        #check if the ball is going more downwards than the "floor" of the screen
        if self.y + self.height >= heightScreen and self.BDY > 0:
            self.BDY *= -1
            self.BDY += self.airResistance
            self.y = heightScreen - self.width
            if self.BDX > 0:
                self.BDX -= self.friction
            elif self.BDX < 0:
                self.BDX += self.friction
            
            if abs(soccer.BDY) > 2:
                bouncing_Sound.play()
        #checks if the ball is barely bouncing
        #soccer.y + soccer.height > heightScreen + 3
        elif self.y + self.height > heightScreen:
            self.BDY = 0
            self.y == heightScreen - self.width
            self.gravity = 0

            ########################################
            #FRICTION
            ########################################
        if self.gravity == 0:

            if abs(self.BDX) < 10**-7:
                self.BDX = 0
            
            elif self.BDX > 0:
                self.BDX -= 0.002
        
            elif self.BDX < 0:
                self.BDX += 0.002
    
    def checkForAllowedXDirectionBall(self, widthScreen):
        #if the soccer goes out of bounds in the left side, flip the direction and ensure it is visible by relocating it inside the screen.
        if self.x <= 0:
            self.BDX *= -1
            self.x = 5

        #if the soccer goes out of bounds in the def checkForAllowed right side switch the x velocity and ensure that it is still visible
        elif soccer.x + soccer.width > widthScreen:
            soccer.BDX *= -1
            soccer.x = widthScreen - soccer.width

    def checkForCollisionPostofGoal(self, goalHeight, goalWidth, widthScreen, heightScreen):
        if ((self.y <= heightScreen - goalHeight - 25) and 
        ((self.x + self.width >= widthScreen - goalWidth - 3) or (self.x <= goalWidth + 3))):
            self.BDX *= -1
            if self.BDX < 0:
                self.x -= 5
            else:
                self.x += 5

    def checkFor1stPlayerGoal(self, player, widthScreen, heightScreen, goalWidth, goalHeight, guestPlayer):
        ###########################
        #Check for goal in the left
        ###########################

        if (self.x + self.width < goalWidth + 5) and self.y > heightScreen - goalHeight - 25:
            self.x = 0
            player.scoredGoal = True
            self.BDX = 0
            self.BDY = 0
            self.y = heightScreen//2 - 20
            self.x = widthScreen//2
            guestPlayer.x = goalWidth + guestPlayer.width/2
            guestPlayer.y = heightScreen - guestPlayer.height
            player.y = heightScreen - player.height
            player.x = widthScreen - playerWidth - goalWidth - 5
            guestPlayer.jumpHeight = guestPlayer.jumpHeightSecure
            player.jumpHeight = player.jumpHeightSecure
            player.jumping = False
            guestPlayer.jumping = False
            player.goalCount += 1
            goal_Sound = mixer.Sound("Goal Audio.mp3")
            
            if player.goalCount != 4:
                goal_Sound.play()

    
    def checkForGuestPlayerGoal(self, guestPlayer, widthScreen, heightScreen, goalWidth, goalHeight, player):
        ############################
        #Check for goal in the right
        ############################
        if self.x + self.width > (widthScreen - goalWidth + 1.5*self.width) and self.y > heightScreen - goalHeight - 25:
            self.x = widthScreen - self.width
            guestPlayer.scoredGoal = True
            guestPlayer.jumping = False
            player.jumping = False
            self.BDX = 0
            self.BDY = 0
            self.y = heightScreen//2 - 20
            self.x = widthScreen//2
            guestPlayer.goalCount += 1
            guestPlayer.x = goalWidth + 5
            guestPlayer.y = heightScreen - guestPlayer.height
            player.x = widthScreen - playerWidth - goalWidth - 5
            player.y = heightScreen - player.height
            guestPlayer.jumpHeight = guestPlayer.jumpHeightSecure
            player.jumpHeight = player.jumpHeightSecure
            goal_Sound = mixer.Sound("Goal Audio.mp3")

            if guestPlayer.goalCount != 4:
                goal_Sound.play()
    
    
    def checkForBallCollisionsAndGravity(self, heightScreen, widthScreen, epsilon):

        self.applyGravity() 
        self.applyXMovement()
        self.checkForCollisionWithGround(heightScreen)
        self.checkForAllowedXDirectionBall(widthScreen)

class SoccerPlayer(object):

    def __init__(self, width, height, x, y, BDY, jumping, jumpHeight, scoredGoal, goalCount, extraSpeed, collidedTimes, frozen, jumpHeightSecure, beenFreezed):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.BDY = BDY
        self.jumping = jumping
        self.jumpHeight = jumpHeight
        self.scoredGoal = scoredGoal
        self.goalCount = goalCount
        self.extraSpeed = extraSpeed
        self.collidedTimes = collidedTimes
        self.frozen = frozen
        self.jumpHeightSecure = jumpHeightSecure
        self.beenFreezed = beenFreezed

    def jump(self, soccer):
        #if the jumpHeight varible is greater than 0 this means the y coordinate of our player should be less positive so that it moves upwards
        #this is attempted to represent the physics equation : y = 1/2at^2
        self.jumping = True
        if self.jumpHeight > 0:
            self.y -= 1/2 * self.jumpHeight**2
            self.jumpHeight -= 1
            self.checkPlayerHittingBall(soccer, heightScreen, widthScreen)
            self.checkBallHitsMiddleHead(soccer, epsilon)

        #if our jumpHeight is negative our y coordinate of our player should be more positive so that it goes back to the floor

        elif self.jumpHeight >= -self.jumpHeightSecure and self.jumpHeight <= 0:
            self.y += 1/2 * (self.jumpHeight ** 2)
            self.jumpHeight -= 1
            self.checkPlayerHittingBall(soccer, heightScreen, widthScreen)
            self.checkBallHitsMiddleHead(soccer, epsilon)
        
        #if ourJumpHeight surpasses negative 10 we have reached ground and hence we stop jumping
        elif self.jumpHeight < -self.jumpHeightSecure:
            self.jumpHeight = self.jumpHeightSecure
            self.jumping = False
            self.checkPlayerHittingBall(soccer, heightScreen, widthScreen)
            self.checkBallHitsMiddleHead(soccer, epsilon)

    def checkPlayerHittingBall(self, soccer, heightScreen, widthScreen):
        collided = False
        #in pygame the x point is represented as the leftmost point

        #check if the ball hits the left side of the player
        self.checkBallHitsMiddleHead(soccer, epsilon)
        #first let us check if the ball is inside the body of our player and to the right
        if (not self.checkBallHitsMiddleHead(soccer, epsilon) and 
        (soccer.y >= self.y - 3) and 
        (soccer.y + soccer.width  <= self.y + self.width) and 
        (soccer.x > self.x + 2)  and
        (soccer.x + soccer.width < self.x + self.width) and 
        (abs(soccer.x - self.x)) > abs(soccer.x + soccer.width - self.x - self.width)):
            soccer.BDY *= -1
            collided = True

        #checks if it is inside the player's body and if it is to the left of it
        elif (not self.checkBallHitsMiddleHead(soccer, epsilon) and 
        (soccer.y >= self.y) and 
        (soccer.y + soccer.width  <= self.y + self.width) and 
        (soccer.x > self.x + 2)  and
        (soccer.x + soccer.width < self.x + self.width) and 
        (abs(soccer.x - self.x)) < abs(soccer.x + soccer.width - self.x - self.width)):
            # soccer.x = self.x - 5
            soccer.BDY = 10*math.sin(70)
            soccer.BDX = -10*math.cos(70)
            collided = True
            self.collidedTimes += 1

        #Im going to make it so if the player is jumping and the ball is hit by the player the ball goes upwards

        #checking if it collides in the left
        if( (self.jumping) and (soccer.y + soccer.height <= self.y + self.height) and
        (soccer.y >= self.y) and (soccer.x > self.x) and (soccer.x <= self.x + 5)):
            soccer.BDY = 10*math.sin(-70)
            soccer.BDX = -10*math.cos(70)
            collided = True
            self.collidedTimes += 1
    
        #if it collides in the right 
        elif ((self.jumping) and (soccer.y + soccer.height <= self.y + self.width - 5) and
        (soccer.y >= self.y) and (soccer.x + soccer.width <= self.x + self.width) and 
        (soccer.x + soccer.width >= self.x + self.width +5)): 
            soccer.BDY  = 10*math.sin(-70)
            soccer.BDX = 10*math.cos(70)
            collided = True
            self.collidedTimes += 1

        #This checks if the ball was hit with the upper half of the body
        if ((soccer.y >= self.y) and 
        (soccer.y <= self.y + self.height/2) and 
        (soccer.x + soccer.width >= self.x + 20) and 
        (soccer.x + soccer.width < self.x + self.width/2)):
            #if the player is jumping
            
            if self.jumping:
                soccer.BDY = 9*math.sin(-70)
                soccer.BDX = -10*math.cos(70) - 0.25
        
            elif soccer.BDY <0: #meaning the ball is moving upwards
                soccer.BDY = 8*math.sin(-70)
                soccer.BDX = -8*math.cos(70) - 0.25
                soccer.x -= 10

            elif soccer.BDY > 0:  #if the ball is moving downwards
                soccer.BDX *= -1
                soccer.BDX -= 1
                soccer.BDY = 5
                soccer.x -= 5
    
            collided = True
            self.collidedTimes += 1

        #this applies to the lower half of the left side of the player
        elif ((soccer.y >= self.y) and 
        (soccer.y <= self.y + self.height - 30)  and
        (soccer.x + soccer.width >= self.x + 20) and 
        (soccer.x + soccer.width < self.x + self.width/2)):
            #this first if statement applies for when the ball is not bouncing  
            if soccer.BDX == 0 and abs(soccer.BDY) < 2:
                soccer.BDX = -3
                soccer.applyXMovement()

            #this second if statement applies if the ball is bouncing
            elif soccer.BDX == 0 and soccer.gravity != 0:
                soccer.BDX = -0.25
            else:
                soccer.BDX *= -1
            soccer.x = player.x - 20

            collided = True
            self.collidedTimes += 1

        #check if the ball hits the right side of the player
        #first check for the upper half (head)

        if ((soccer.y >= self.y) and 
        (soccer.y <= self.y + self.height/2) and 
        (soccer.x >= self.x + self.width/2) and 
        (soccer.x <= self.x + self.width - 20)):
            #if the player is jumping then we apply the sin and cos as if a force was applied creating a physics-parabola effect
            if self.jumping:
                soccer.BDY = -10*math.sin(70)
                soccer.BDX = 10*math.cos(70) + 0.25

            elif soccer.BDY < 0:            #this means the soccer is moving upwards
                soccer.BDY = -10*math.sin(70)
                soccer.BDX = 8*math.cos(70) + 0.25
                soccer.x += 10

            elif soccer.BDY > 0 and soccer.y <= self.y + self.width/2:            #this checks if the ball is moving downwards
                soccer.BDX *= -1
                soccer.BDX += 2
                soccer.x += 10

            collided = True
            self.collidedTimes += 1

        elif ((soccer.y >= self.y) and 
        (soccer.y <= self.y + self.height) and
        (soccer.x >= self.x + self.width/2) and 
        (soccer.x <= self.x + self.width - 20)):
            #the first if statement checks if the ball is not bouncing
            if soccer.BDX == 0 and abs(soccer.BDY) < 2:
                soccer.BDX = 3
                soccer.applyXMovement()

            #this applies for when the ball is bouncing
            elif soccer.BDX == 0 and soccer.gravity != 0:
                soccer.BDX = 0.25

            else:
                soccer.BDX *= -1

            soccer.x = self.x + self.width - 10
            collided = True
            self.collidedTimes += 1

        return collided

    def checkBallHitsMiddleHead(self, soccer, epsilon):
        #if the ball hits the player directly in the middle (so like directly in head)

        if (self.jumping and abs(soccer.y + soccer.height >= self.y - 2) and 
        soccer.x >= self.x and soccer.x + soccer.width <= self.x + self.width - 3 
        and soccer.BDY > 0):
            soccer.BDY *= -1
            soccer.y -= 8
            self.collidedTimes += 1
            return True
        
        elif ( not self.jumping and 
        abs(soccer.y + soccer.height >= self.y - 2) and 
        soccer.x >= self.x and soccer.x + soccer.width <= self.x + self.width - 3 
        and soccer.BDY > 0):

            soccer.BDY *= -1
            self.collidedTimes += 1
            return True
        
        return False

    #check if the ball is not moving if so lift it up
    def checkBallNotMoving(self, otherPlayer, soccer, epsilon, heightScreen):
        if ((abs(soccer.BDY) < 2) and (abs(self.x - (soccer.x + soccer.width)) <= 5) and (abs(soccer.x  - (otherPlayer.x + otherPlayer.width)) <= 5) and 
        (abs(self.y + self.height - heightScreen) <= epsilon) and (abs(otherPlayer.y + otherPlayer.height - heightScreen) <= epsilon)):
            soccer.BDY = -3
            soccer.y = heightScreen//2

#We will make the collisions a little bit different for Doraemon since he has a wider head and different body than Shin Chan
class DoraemonPlayer(SoccerPlayer):
    #we can call the init function from our soccerPlayer class since it will take the same values
    def __init__(self, width, height, x, y, BDY, jumping, jumpHeight, scoredGoal, goalCount, extraSpeed, collidedTimes, frozen, jumpHeightSecure, beenFreezed):
        super().__init__(width, height, x, y, BDY, jumping, jumpHeight, scoredGoal, goalCount, extraSpeed, collidedTimes, frozen, jumpHeightSecure, beenFreezed)


    def checkPlayerHittingBall(self, soccer, heightScreen, widthScreen):
        #in pygame the x point is represented as the leftmost point
        collided = False
        #check if the ball hits the left side of the player
        self.checkBallHitsMiddleHead(soccer, epsilon)
        #first let us check if the ball is inside the body of our player and to the right
        if (not self.checkBallHitsMiddleHead(soccer, epsilon) and 
        (soccer.y >= self.y - 7) and 
        (soccer.y + soccer.width  <= self.y + self.width) and 
        (soccer.x > self.x + 2)  and
        (soccer.x + soccer.width < self.x + self.width) and 
        (abs(soccer.x - self.x)) > abs(soccer.x + soccer.width - self.x - self.width)):
            soccer.BDY *= -1
            collided = True
            self.collidedTimes += 1

        #checks if it is inside the player's body and if it is to the left of it
        elif (not self.checkBallHitsMiddleHead(soccer, epsilon) and 
        (soccer.y >= self.y + 10) and 
        (soccer.y + soccer.width  <= self.y + self.width) and 
        (soccer.x > self.x + 2)  and
        (soccer.x + soccer.width < self.x + self.width) and 
        (abs(soccer.x - self.x)) < abs(soccer.x + soccer.width - self.x - self.width)):
            soccer.BDY = 9.5*math.sin(70)
            soccer.BDX = -7*math.cos(70) - 0.25
            collided = True
            self.collidedTimes += 1

        #Im going to make it so if the player is jumping and the ball is hit by the player the ball goes upwards

        #checking if it collides in the left
        if( (self.jumping) and (soccer.y + soccer.height <= self.y + self.height) and
        (soccer.y >= self.y) and (soccer.x > self.x) and (soccer.x <= self.x + 5)):
            soccer.BDY = 11*math.sin(-70)
            soccer.BDX = -9*math.cos(70) - 0.25
            collided = True
            self.collidedTimes += 1

        #if it collides in the right 
        elif ((self.jumping) and (soccer.y + soccer.height <= self.y + self.width - 5) and
        (soccer.y >= self.y) and (soccer.x + soccer.width <= self.x + self.width - 3) and
        (soccer.x + soccer.width >= self.x + self.width + 5)): 
            soccer.BDY  = 10*math.sin(-70)
            soccer.BDX = 8*math.cos(70) + 0.25
            collided = True
            self.collidedTimes += 1

        #This checks if the ball was hit with the upper half of the body and
        if ((soccer.y >= self.y - 15 ) and 
        (soccer.y <= self.y + self.height/2) and 
        (soccer.x + soccer.width >= self.x - 10) and 
        (soccer.x + soccer.width <= self.x + self.width/2)):
            #if the player is jumping
            if self.jumping:
                soccer.BDY = 11*math.sin(-70)
                soccer.BDX = -9*math.cos(70) - 0.25

            elif soccer.BDY <0: #meaning the ball is moving upwards
                soccer.BDY = 11*math.sin(-70)
                soccer.BDX = -9*math.cos(70) - 1
                soccer.x -= 10
               
            elif soccer.BDY > 0:  #if the ball is moving downwards
                if soccer.BDX == 0:
                    soccer.BDX = -2
                    soccer.applyXMovement()

                elif soccer.BDX > 0:
                    soccer.BDX *= -1
                    soccer.applyXMovement()

                elif soccer.BDX < 0 :
                    soccer.BDX -= 0.5
                    soccer.applyXMovement()

                # soccer.x = self.x - 30
                soccer.applyGravity()
                    
            collided = True
            self.collidedTimes += 1
    

        #this applies to the lower half of the left side of the player
        elif ((soccer.y >= self.y) and 
        (soccer.y <= self.y + self.height)  and 
        (soccer.x + soccer.width >= self.x + 20) and 
        (soccer.x + soccer.width < self.x + self.width/2 )):
            #this first if statement applies for when the ball is not bouncing
            if soccer.BDX == 0 and abs(soccer.BDY) < 2:
                soccer.BDX = -3
                soccer.applyXMovement()
    
            #this second if statement applies if the ball is bouncing
            elif soccer.BDX == 0 and soccer.gravity != 0:
                soccer.BDX = -0.25
                # soccer.x = self.x - 20
                
            else:
                soccer.BDX *= -1

            soccer.x = self.x - 10
            collided = True
            self.collidedTimes += 1

        #check if the ball hits the right side of the player
        #first check for the upper half (head)

        if ((soccer.y >= self.y - 15) and 
        (soccer.y <= self.y + self.height/2) and 
        (soccer.x >= self.x + self.width/2) and 
        (soccer.x <= self.x + self.width - 5)):
            #if the player is jumping then we apply the sin and cos as if a force was applied creating a physics-parabola effect
            if self.jumping:
                soccer.BDY = -10*math.sin(70)
                soccer.BDX = 9*math.cos(70) + 0.25

            elif soccer.BDY < 0:            #this means the soccer is moving upwards
                soccer.BDY = -10*math.sin(70)
                soccer.BDX = 9*math.cos(70)
                soccer.x += 10
                
            elif soccer.BDY > 0 and soccer.y <= self.y + self.width/2:            #this checks if the ball is moving downwards
                soccer.BDX *= -1
                soccer.BDX += 2
                soccer.x += 10

            collided = True
            self.collidedTimes +=1 
            
        #lower half of right side of the player
        elif ((soccer.y >= self.y) and 
        (soccer.y <= self.y + self.height) and
        (soccer.x >= self.x + self.width/2) and 
        (soccer.x <= self.x + self.width - 20)):
            #the first if statement checks if the ball is not bouncing
            if soccer.BDX == 0 and abs(soccer.BDY) < 2:
                soccer.BDX = 3
                soccer.applyXMovement()
                
            #this applies for when the ball is bouncing
            elif soccer.BDX == 0 and soccer.gravity != 0:
                soccer.BDX = 0.25

            else:
                soccer.BDX *= -1

            soccer.x = self.x + self.width - 10
            collided = True
            self.collidedTimes += 1

        return collided


    def checkBallHitsMiddleHead(self, soccer, epsilon):
        #if the ball hits the player directly in the middle (so like directly in head)
        #doraemon has a bigger head so we need to change this
        if self.jumping and (
        ((soccer.y + soccer.height >= self.y - 100) and (soccer.x >= self.x) and
        (soccer.x + soccer.width <= self.x + self.width - 3)) and soccer.BDY > 0):
            soccer.BDY *= -1
            soccer.y -= 7
            self.collidedTimes += 1
            return True

        elif ( not self.jumping and
        ((soccer.y + soccer.height >= self.y - 3) and (soccer.x >= self.x) and
        (soccer.x + soccer.width <= self.x + self.width - 3)) and soccer.BDY > 0):
            soccer.BDY *= -1.1
            self.collidedTimes += 1

            return True
        return False

#do the collisions for Dorami
class DoramiPlayer(SoccerPlayer):
    #we can call the init function from our soccerPlayer class since it will take the same values
    def __init__(self, width, height, x, y, BDY, jumping, jumpHeight, scoredGoal, goalCount, extraSpeed, collidedTimes, frozen, jumpHeightSecure, beenFreezed):
        super().__init__(width, height, x, y, BDY, jumping, jumpHeight, scoredGoal, goalCount, extraSpeed, collidedTimes, frozen, jumpHeightSecure, beenFreezed)


    def checkPlayerHittingBall(self, soccer, heightScreen, widthScreen):
        #in pygame the x point is represented as the leftmost point
        collided = False
        #check if the ball hits the left side of the player
        self.checkBallHitsMiddleHead(soccer, epsilon)
        #first let us check if the ball is inside the body of our player and to the right
        if (not self.checkBallHitsMiddleHead(soccer, epsilon) and 
        (soccer.y >= self.y - 7) and 
        (soccer.y + soccer.width  <= self.y + self.width) and 
        (soccer.x > self.x + 2)  and
        (soccer.x + soccer.width < self.x + self.width) and 
        (abs(soccer.x - self.x)) > abs(soccer.x + soccer.width - self.x - self.width)):
            soccer.BDY *= -1
            collided = True
            self.collidedTimes += 1

        #checks if it is inside the player's body and if it is to the left of it
        elif (not self.checkBallHitsMiddleHead(soccer, epsilon) and 
        (soccer.y >= self.y) and 
        (soccer.y + soccer.width  <= self.y + self.width) and 
        (soccer.x > self.x + 2)  and
        (soccer.x + soccer.width < self.x + self.width) and 
        (abs(soccer.x - self.x)) < abs(soccer.x + soccer.width - self.x - self.width)):
            # soccer.x = self.x - 10
            soccer.BDY = 9.5*math.sin(70)
            soccer.BDX = -7*math.cos(70) - 0.25
            collided = True
            self.collidedTimes += 1

        #Im going to make it so if the player is jumping and the ball is hit by the player the ball goes upwards

        #checking if it collides in the left
        if( (self.jumping) and (soccer.y + soccer.height <= self.y + self.height) and
        (soccer.y >= self.y) and (soccer.x > self.x) and (soccer.x <= self.x + 5)): 
            soccer.BDY = 11*math.sin(-65)
            soccer.BDX = -9*math.cos(70) - 0.25
            collided = True
            self.collidedTimes += 1

        #if it collides in the right 
        elif ((self.jumping) and (soccer.y + soccer.height <= self.y + self.width - 5) and
        (soccer.y >= self.y) and (soccer.x + soccer.width <= self.x + self.width - 3) and
        (soccer.x + soccer.width >= self.x + self.width + 5)): 
            soccer.BDY  = 10*math.sin(-70)
            soccer.BDX = 8*math.cos(70) + 0.25
            collided = True
            self.collidedTimes += 1

        #This checks if the ball was hit with the upper half of the body and
        if ((soccer.y >= self.y - 10) and 
        (soccer.y <= self.y + self.height/2) and 
        (soccer.x + soccer.width >= self.x + 25) and 
        (soccer.x + soccer.width <= self.x + self.width/2)):
            #if the player is jumping
            if self.jumping:
                soccer.BDY = 11*math.sin(-70)
                soccer.BDX = -9*math.cos(70) - 0.25

            elif soccer.BDY <0: #meaning the ball is moving upwards
                soccer.BDY = 11*math.sin(-70)
                soccer.BDX = -9*math.cos(70) - 1
                soccer.x -= 10
               
            elif soccer.BDY > 0:  #if the ball is moving downwards
                if soccer.BDX == 0:
                    soccer.BDX = -2
                    soccer.applyXMovement()

                elif soccer.BDX > 0:
                    soccer.BDX *= -1
                    soccer.applyXMovement()

                elif soccer.BDX < 0 :
                    soccer.BDX -= 0.5
                    soccer.applyXMovement()

                # soccer.x = self.x - 30
                soccer.applyGravity()
                    
            collided = True
            self.collidedTimes += 1
    

        #this applies to the lower half of the left side of the player
        elif ((soccer.y >= self.y) and 
        (soccer.y <= self.y + self.height)  and 
        (soccer.x + soccer.width >= self.x + 20) and 
        (soccer.x + soccer.width < self.x + self.width/2 )):
            #this first if statement applies for when the ball is not bouncing
            if soccer.BDX == 0 and abs(soccer.BDY) < 2:
                soccer.BDX = -3
                soccer.applyXMovement()
    
            #this second if statement applies if the ball is bouncing
            elif soccer.BDX == 0 and soccer.gravity != 0:
                soccer.BDX = -0.25
                # soccer.x = self.x - 20
                
            else:
                soccer.BDX *= -1

            soccer.x = self.x - 10
            collided = True
            self.collidedTimes += 1

        #check if the ball hits the right side of the player
        #first check for the upper half (head)

        if ((soccer.y >= self.y - 15) and 
        (soccer.y <= self.y + self.height/2) and 
        (soccer.x >= self.x + self.width/2) and 
        (soccer.x <= self.x + self.width - 5)):
            #if the player is jumping then we apply the sin and cos as if a force was applied creating a physics-parabola effect
            if self.jumping:
                soccer.BDY = -10*math.sin(70)
                soccer.BDX = 9*math.cos(70) + 0.25

            elif soccer.BDY < 0:            #this means the soccer is moving upwards
                soccer.BDY = -10*math.sin(70)
                soccer.BDX = 9*math.cos(70)
                soccer.x += 10
                
            elif soccer.BDY > 0 and soccer.y <= self.y + self.width/2:            #this checks if the ball is moving downwards
                soccer.BDX *= -1
                soccer.BDX += 2
                soccer.x += 10

            collided = True
            self.collidedTimes +=1 
            
        #lower half of right side of the player
        elif ((soccer.y >= self.y) and 
        (soccer.y <= self.y + self.height) and
        (soccer.x >= self.x + self.width/2) and 
        (soccer.x <= self.x + self.width - 20)):
            #the first if statement checks if the ball is not bouncing
            if soccer.BDX == 0 and abs(soccer.BDY) < 2:
                soccer.BDX = 3
                soccer.applyXMovement()
                
            #this applies for when the ball is bouncing
            elif soccer.BDX == 0 and soccer.gravity != 0:
                soccer.BDX = 0.25

            else:
                soccer.BDX *= -1

            soccer.x = self.x + self.width - 10
            collided = True
            self.collidedTimes += 1

        return collided


    def checkBallHitsMiddleHead(self, soccer, epsilon):
        #if the ball hits the player directly in the middle (so like directly in head)
        #doraemon has a bigger head so we need to change this
        if self.jumping and (
        ((soccer.y + soccer.height >= self.y - 5) and (soccer.x >= self.x) and
        (soccer.x + soccer.width <= self.x + self.width - 3)) and soccer.BDY > 0):
            soccer.BDY *= -1
            self.collidedTimes += 1
            return True

        elif ( not self.jumping and
        ((soccer.y + soccer.height >= self.y - 3) and (soccer.x >= self.x) and
        (soccer.x + soccer.width <= self.x + self.width - 3)) and soccer.BDY > 0):
            soccer.BDY *= -1.1
            self.collidedTimes += 1

            return True
        return False


##############################
#defining our variables
##############################
soccerWidth = 37
soccerHeight = soccerWidth
soccerX = widthScreen//2
soccerY = heightScreen//2 - 20
soccerBDY = 0
soccerBDX = 0
playerWidth = 81
playerHeight = 100
playerY = heightScreen - playerHeight
guestPlayerY = playerY
playerBDY = 0
soccerGravity = 0.25              #2*10**-4
airResistance = 2            #2*10**-1
friction = 10**-2
lightBlueRGB = (173, 216, 230)
marginErrorBounce = 10
epsilon = 1
jumping = False
jumpHeight = 8
jumpHeightPlayer = 8.5
secureJumpHeightPlayer = jumpHeightPlayer
secureJumpHeight = jumpHeight
scoredGoal = False
goalCount = 0
black = (0, 0, 0)
blue = (102, 178, 255)
font = pygame.font.Font('freesansbold.ttf', 32)
textGoal = font.render('GOOOOOOOOOOOOOAAAAAL', True, black, blue)
textGoalRectangle = textGoal.get_rect()
pressedButton = False
extraSpeed = 0
collidedTimes = 0
frozen = False
timeFrozen = None
wonGame = 7
beenFreezed = False
jumpImgShowing = False
speedImgShowing = False
xJumpImg, yJumpImg = ((random.randint(widthScreen//2 - 300, widthScreen//2 + 300), 40))
speedX, speedY = (random.randint(widthScreen//2 - 300, widthScreen//2 + 300), 40)
goalPost = 25
jumpImgWidth = 30
jumpImgHeight = 41
runFastWidth = 24
runFastHeight = 40
incrementJumpPlayer = False
incrementJumpGuestPlayer = False
score = ""
currentLeaderboard = []
firstScoreInts = ''
playerX = widthScreen - goalWidth - playerWidth
guestPlayerX = goalWidth + playerWidth/2
doramiHeight = 117
doramiWidth = 81
doramiY = heightScreen - doramiHeight
doramiX = (widthScreen) - (goalWidth + doramiWidth//2 + 40)
jumpHeightDorami = 7
jumpHeightSecureDorami = 7
#let's create three objects, our player, the other player and the soccer ball
soccer = Ball(soccerX, soccerY, soccerWidth, soccerHeight, soccerBDX, soccerBDY, friction, soccerGravity, airResistance)
player = SoccerPlayer(playerWidth, playerHeight, playerX, playerY, playerBDY, jumping, jumpHeightPlayer, scoredGoal, goalCount, extraSpeed, collidedTimes, frozen, secureJumpHeightPlayer, beenFreezed)
guestPlayer = DoraemonPlayer(playerWidth, playerHeight, guestPlayerX, guestPlayerY, playerBDY, jumping, jumpHeight, scoredGoal, goalCount, extraSpeed, collidedTimes, frozen, secureJumpHeight, beenFreezed)
dorami = DoramiPlayer(doramiWidth, doramiHeight, doramiX, doramiY, playerBDY, jumping, jumpHeightDorami, scoredGoal, goalCount, extraSpeed, collidedTimes, frozen, jumpHeightSecureDorami, beenFreezed)

#############################################################################
#THIS FUNCTION COMBINES A LOT OF THE FUNCTIONS ABOVE TO CHECK FOR A COLLISION AND FOR OUT OF BOUNDS
############################################################################
def checkForCollisionsAndOutOfBoundsAndGoal(heightScreen, widthScreen, epsilon, textGoal, textGoalRectangle, screen):
    #at the bginning of the loop make su   re to reset the goal varibale if there has previously been a goal scored
    if player.scoredGoal:
        player.scoredGoal = False
        screen.blit(textGoal, textGoalRectangle)

    elif guestPlayer.scoredGoal:
        guestPlayer.scoredGoal = False

    soccer.applyXMovement()

    soccer.applyGravity()

    soccer.checkForCollisionWithGround(heightScreen)

    #soccer.checkForAllowedXDirectionBall(widthScreen)

    player.checkPlayerHittingBall(soccer, widthScreen, heightScreen)
    guestPlayer.checkPlayerHittingBall(soccer, widthScreen, heightScreen)

    player.checkBallHitsMiddleHead(soccer, epsilon)
    guestPlayer.checkBallHitsMiddleHead(soccer, epsilon)

    soccer.checkForCollisionPostofGoal(goalHeight, goalWidth, widthScreen, heightScreen)

    soccer.checkFor1stPlayerGoal(player, widthScreen, heightScreen, goalWidth, goalHeight, guestPlayer)
    soccer.checkForGuestPlayerGoal(guestPlayer, widthScreen, heightScreen, goalWidth, goalHeight, player)
    
    player.checkBallNotMoving(guestPlayer, soccer, epsilon, heightScreen)


##################################################################
############## CREATE BUTTONS FUNCTIONS ##########################
##################################################################
def createStartPlaying2PlayerButton():
    #properties of the button
    xstartButton = 75         #295
    ystartButton = 498
    widthstartButton = 160
    heightstartButton = 55
    xCenterTextButton = xstartButton + (widthstartButton / 2)     #200
    yCenterTextButton = ystartButton + (heightstartButton / 2)
    black = (0, 0, 0)
    buttonColor = (102, 178, 255)
    textPlayingButton = "2 Player"
    fontButton = pygame.font.Font('freesansbold.ttf', 28)
    pressed = False
    #create the button and return it
    startPlaying2PlayerButton = Button(xstartButton, ystartButton, widthstartButton, heightstartButton, fontButton, black, buttonColor, textPlayingButton, xCenterTextButton, yCenterTextButton, pressed)
    return startPlaying2PlayerButton


#button for the AI
def createButtonAI():
    #properties of the button
    xButton = 875                       #660
    yButton = 498                       #498
    widthButton = 180                   #180
    heightButton = 55                   #55
    xCenterTextButton = xButton + (widthButton / 2)             #750
    yCenterTextButton = yButton + (heightButton / 2) + 2             #528
    black = (0, 0, 0)
    buttonColor = (102, 178, 255)
    textPlayingButton = "Single Player"
    fontButton = pygame.font.Font('freesansbold.ttf', 25)
    pressed = False
    #create the button and return it
    startPlayingAIButton = Button(xButton, yButton, widthButton, heightButton, fontButton, black, buttonColor, textPlayingButton, xCenterTextButton, yCenterTextButton, pressed)
    return startPlayingAIButton

#create the button of the instructions screen

def createInstructionsButton():
    #properties of the button
    xButton = (75 + 160 + 50 + 35)
    yButton = 498    
    widthButton = 180
    heightButton = 55
    xCenterTextButton = xButton + (widthButton / 2)
    yCenterTextButton = yButton + (heightButton / 2) + 2
    black = (0, 0, 0)
    buttonColor = (102, 178, 255)
    textPlayingButton = "Instructions"
    fontButton = pygame.font.Font('freesansbold.ttf', 25)
    pressed = False
    #create the button and return it
    instructionsButton = Button(xButton, yButton, widthButton, heightButton, fontButton, black, buttonColor, textPlayingButton, xCenterTextButton, yCenterTextButton, pressed)
    return instructionsButton

#create the back to intro screen button
def createBacktoIntroButton():
    global widthScreen
                       
    widthButton = 250               
    heightButton = 55   
    xButton = widthScreen//2 + 110 - widthButton                       
    yButton = 450                
    xCenterTextButton = xButton + (widthButton / 2)             
    yCenterTextButton = yButton + (heightButton / 2) + 2             
    black = (0, 0, 0)
    buttonColor = (102, 178, 255)
    textPlayingButton = "Back to Main Menu"
    fontButton = pygame.font.Font('freesansbold.ttf', 25)
    pressed = False
    #create the button and return it
    backToIntroButton = Button(xButton, yButton, widthButton, heightButton, fontButton, black, buttonColor, textPlayingButton, xCenterTextButton, yCenterTextButton, pressed)
    return backToIntroButton

#createt the leaderboard button
def createLeaderboardButton():
    global widthScreen
                       
    widthButton = 200               
    heightButton = 55   
    xButton = 585                       
    yButton = 498               
    xCenterTextButton = xButton + (widthButton / 2)             
    yCenterTextButton = yButton + (heightButton / 2) + 2             
    black = (0, 0, 0)
    buttonColor = (102, 178, 255)
    textPlayingButton = "Leaderboard"
    fontButton = pygame.font.Font('freesansbold.ttf', 25)
    pressed = False
    #create the button and return it
    leaderboardButton = Button(xButton, yButton, widthButton, heightButton, fontButton, black, buttonColor, textPlayingButton, xCenterTextButton, yCenterTextButton, pressed)
    return leaderboardButton

#create the easy AI Button
def createEasyButton():
    global widthScreen
                       
    widthButton = 200               
    heightButton = 55   
    xButton = widthScreen//2 - widthButton - 50                      
    yButton = heightScreen//2            
    xCenterTextButton = xButton + (widthButton / 2)             
    yCenterTextButton = yButton + (heightButton / 2) + 2             
    black = (0, 0, 0)
    buttonColor = (102, 178, 255)
    textPlayingButton = "Easy"
    fontButton = pygame.font.Font('freesansbold.ttf', 25)
    pressed = False
    #create the button and return it
    easyButton = Button(xButton, yButton, widthButton, heightButton, fontButton, black, buttonColor, textPlayingButton, xCenterTextButton, yCenterTextButton, pressed)
    return easyButton

#create the medium AI Button
def createMediumButton():
    global widthScreen
                       
    widthButton = 200               
    heightButton = 55   
    xButton = widthScreen//2 - widthButton + 250                   
    yButton = heightScreen//2            
    xCenterTextButton = xButton + (widthButton / 2)             
    yCenterTextButton = yButton + (heightButton / 2) + 2             
    black = (0, 0, 0)
    buttonColor = (102, 178, 255)
    textPlayingButton = "Hard"
    fontButton = pygame.font.Font('freesansbold.ttf', 25)
    pressed = False
    #create the button and return it
    mediumButton = Button(xButton, yButton, widthButton, heightButton, fontButton, black, buttonColor, textPlayingButton, xCenterTextButton, yCenterTextButton, pressed)
    return mediumButton

#create the pause button
def createPauseButton():
    global widthScreen

    x = widthScreen - 75
    y = 40
    width = 40
    height = 38 
    pressed = False
    return PauseGame(width, height, x, y, pressed)

##################################################################
############## CREATES THE LEADERBOARD SCREEN ####################
##################################################################

#only displays the top 3 scores
def createLeaderboardScreen(heightScreen, widthScreen, shinChanIntroImg, doraemonIntroImg, soccerIntroImg, startPlaying2PlayerButton, startPlayingAIButton, screen, epsilon, clock, player, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg, xJumpImg, incrementJumpPlayer, incrementJumpGuestPlayer, startInstructions, leaderboardButton):
    global currentLeaderboard

    text = ''
    text = ''
    text1 = ''
    text2 = ''
    numText = 0
    makeText = None
    makeTextRect = None
    white = (255, 255, 255)
    yellow = (255, 255, 0)
    blue = (0,191,255)
    red = (255, 0, 0)

    
    head = "Highest Scores are recorded"
    head1 = "Left Score is Doraemon"
    head2 = "Right Score is Shin-Chan"
    
    makeHead = font.render(head, True, red)
    makeHeadRect = makeHead.get_rect()
    makeHeadRect.center = (widthScreen//2, 60)
    
    makeHead1 = font.render(head1, True, blue)
    makeHeadRect1 = makeHead1.get_rect()
    makeHeadRect1.center = (widthScreen//2, 100)

    makeHead2 = font.render(head2, True, yellow)
    makeHeadRect2 = makeHead2.get_rect()
    makeHeadRect2.center = (widthScreen//2, 140)

    if len(currentLeaderboard) == 0:
        text = "No games played yet"
        makeText = font.render(text, True, white)
        makeTextRect = makeText.get_rect()
        makeTextRect.center = (widthScreen//2, heightScreen//2)

    elif len(currentLeaderboard) == 1:
        text = "1. " + str(currentLeaderboard[0])
        makeText = font.render(text, True, white)
        makeTextRect = makeText.get_rect()
        makeTextRect.center = (widthScreen//2 - 20, heightScreen//2 - 15)
        numText = 1

    elif len(currentLeaderboard) == 2:
        text = "1. " + str(currentLeaderboard[0])
        text1 = "2. " + str(currentLeaderboard[1])

        makeText = font.render(text, True, white)
        makeTextRect = makeText.get_rect()
        makeTextRect.center = (widthScreen//2 - 20 , heightScreen//2 - 25)

        makeText1 = font.render(text1, True, white)
        makeTextRect1 = makeText.get_rect()
        makeTextRect1.center = (widthScreen//2 - 20, heightScreen//2 + 20)

        numText = 2

    elif len(currentLeaderboard) >= 3:
        text ="1. " + str(currentLeaderboard[0])
        text1 = "2. " + str(currentLeaderboard[1])
        text2 = "3. " + str(currentLeaderboard[2])

        makeText = font.render(text, True, white)
        makeTextRect = makeText.get_rect()
        makeTextRect.center = (widthScreen//2 - 20, heightScreen//2 - 50)

        makeText1 = font.render(text1, True, white)
        makeTextRect1 = makeText.get_rect()
        makeTextRect1.center = (widthScreen//2 - 20, heightScreen//2)

        makeText2 = font.render(text2, True, white)
        makeTextRect2 = makeText2.get_rect()
        makeTextRect2.center = (widthScreen//2 - 20, heightScreen//2 + 50)
        numText = 3

    background = pygame.image.load("Instructions.jpg")

    backButton = createBacktoIntroButton()

    topLeft = (0, 0)

    leaderboardDisplay = True

    while leaderboardDisplay:

        for event in pygame.event.get():
            mouseCoordX, mouseCoordY = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            backButton.overButton(mouseCoordX, mouseCoordY)

            if event.type == pygame.MOUSEBUTTONDOWN:
                backButton.pressedButton(mouseCoordX, mouseCoordY)

            if event.type == pygame.QUIT:
                instructionsDisplay = False
                pygame.quit() 
                os._exit(0)


        if backButton.pressed:
            instructionsDisplay = False
            mainMenuAfterInstructions(widthScreen, heightScreen, shinChanIntroImg, doraemonIntroImg, soccerIntroImg, startPlaying2PlayerButton, startPlayingAIButton, screen, epsilon, clock, player, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg, xJumpImg, incrementJumpPlayer, incrementJumpGuestPlayer, startInstructions, leaderboardButton)
        
        screen.blit(background, topLeft)

        if numText == 0 or numText == 1:
            screen.blit(makeText, makeTextRect)

        elif numText == 2:
            screen.blit(makeText, makeTextRect)
            screen.blit(makeText1, makeTextRect1)

        elif numText == 3:
            screen.blit(makeText, makeTextRect)
            screen.blit(makeText1, makeTextRect1)
            screen.blit(makeText2, makeTextRect2)

        screen.blit(makeHead, makeHeadRect)
        screen.blit(makeHead2, makeHeadRect2)
        screen.blit(makeHead1, makeHeadRect1)
        backButton.displayButton(screen)
        pygame.display.flip()


#create the instructions screen
def createInstructionsScreen(heightScreen, widthScreen, shinChanIntroImg, doraemonIntroImg, soccerIntroImg, startPlaying2PlayerButton, startPlayingAIButton, screen, epsilon, clock, player, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg, xJumpImg, incrementJumpPlayer, incrementJumpGuestPlayer, startInstructions, leaderboardButton):
    global superJumpImg
    global runFastImg

    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (0, 255, 0)
    yellow = (255, 255, 0)
    blue = (0,191,255)
    red = (255, 0, 0)
    coral = (255,127,80)

    instructions = "Score 4 goals to win!" 
    instructionsText = font.render(instructions, True, white)
    instructionsRect = instructionsText.get_rect()
    instructionsRect.center = (200, 50)

    powers = '3 Powers Available'
    powersText = font.render(powers, True, red)
    powersRect = instructionsText.get_rect()
    powersRect.center = (widthScreen // 2, 80)

    extraSpeed = 'ExtraSpeed'
    extraSpeedText = font.render(extraSpeed, True, yellow)
    extraSpeedRect = extraSpeedText.get_rect()
    extraSpeedRect.center = (widthScreen // 2 - 400, 140)

    frozen = 'Freeze opponent'
    frozenText = font.render(frozen, True, blue)
    frozenRect = frozenText.get_rect()
    frozenRect.center = (widthScreen // 2 - 15, 140)

    superJump = 'SuperJump'
    superJumpText = font.render(superJump, True, coral)
    superJumpRect = frozenText.get_rect()
    superJumpRect.center = (widthScreen // 2 + 440, 140)

    superJumpD = 'Increases jump'
    superJumpDText = font.render(superJumpD, True, white)
    superJumpDRect = superJumpDText.get_rect()
    superJumpDRect.center = (widthScreen // 2 + 400, 260)

    superJumpD1 = 'by 0.50'
    superJumpD1Text = font.render(superJumpD1, True, white)
    superJumpD1Rect = superJumpD1Text.get_rect()
    superJumpD1Rect.center = (widthScreen // 2 + 400, 310)

    instructionsScreen = pygame.display.set_mode((widthScreen, heightScreen))
    instructionsScreenBackgroundImg = pygame.image.load("Instructions.jpg")
    instructionsDisplay = True

    frozen1 = 'Score 3 more goals'
    frozenText1 = font.render(frozen1, True, white)
    frozenText1Rect = frozenText1.get_rect()
    frozenText1Rect.center = (widthScreen//2 - 15, 200)

    frozen2 = 'than your opponnent.'
    frozenText2 = font.render(frozen2, True, white)
    frozenText2Rect = frozenText2.get_rect()
    frozenText2Rect.center = (widthScreen//2 - 15, 240)

    frozen3 = 'Only applicable once.'
    frozenText3 = font.render(frozen3, True, white)
    frozenText3Rect = frozenText3.get_rect()
    frozenText3Rect.center = (widthScreen//2 - 15, 300)

    speed1 = 'Increases speed'
    speed1Text = font.render(speed1, True, white)
    speed1TextRect = speed1Text.get_rect()
    speed1TextRect.center = (widthScreen//2 - 400, 250)

    speed2 = 'by 0.25'
    speed2Text = font.render(speed2, True, white)
    speed2TextRect = speed2Text.get_rect()
    speed2TextRect.center = (widthScreen//2 - 415, 290)

    backButton = createBacktoIntroButton()

    while instructionsDisplay:
        #to quit out of the screen
        for event in pygame.event.get():
            mouseCoordX, mouseCoordY = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            backButton.overButton(mouseCoordX, mouseCoordY)

            if event.type == pygame.MOUSEBUTTONDOWN:
                backButton.pressedButton(mouseCoordX, mouseCoordY)

            if event.type == pygame.QUIT:
                instructionsDisplay = False
                pygame.quit() 
                os._exit(0)


        if backButton.pressed:
            instructionsDisplay = False
            mainMenuAfterInstructions(widthScreen, heightScreen, shinChanIntroImg, doraemonIntroImg, soccerIntroImg, startPlaying2PlayerButton, startPlayingAIButton, screen, epsilon, clock, player, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg, xJumpImg, incrementJumpPlayer, incrementJumpGuestPlayer, startInstructions, leaderboardButton)
            
        instructionsScreen.blit((instructionsScreenBackgroundImg), (0,0))
        screen.blit(instructionsText, instructionsRect)
        screen.blit(powersText, powersRect)
        screen.blit(extraSpeedText, extraSpeedRect)
        screen.blit(frozenText, frozenRect)
        screen.blit(superJumpText, superJumpRect)
        screen.blit(superJumpImg, (widthScreen // 2 + 387, 180))
        screen.blit(runFastImg, ((widthScreen // 2 - 425, 170)))
        screen.blit(superJumpDText, superJumpDRect)
        screen.blit(superJumpD1Text, superJumpD1Rect)
        screen.blit(frozenText1, frozenText1Rect)
        screen.blit(frozenText2, frozenText2Rect)
        screen.blit(frozenText3, frozenText3Rect)
        screen.blit(speed1Text, speed1TextRect)
        screen.blit(speed2Text, speed2TextRect)
        backButton.displayButton(screen)
        pygame.display.flip()

#create the pause menu
def createPauseMenu(screen):
    global widthScreen
    blue = (102, 178, 255)
    rectWidth = 400
    rectHeight = 125
    rectX = widthScreen//2 - 175
    rectY = heightScreen//2 - rectHeight//2 + 125

    pygame.draw.rect(screen, blue, (rectX, rectY, rectWidth, rectHeight))

##############################################
#This function displays the menu screen#######
##############################################
def mainMenu(widthScreen, heightScreen, shinChanIntroImg, doraemonIntroImg, soccerIntroImg, startPlaying2PlayerButton, startPlayingAIButton, screen, epsilon, clock, player, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg, xJumpImg, incrementJumpPlayer, incrementJumpGuestPlayer, startInstructions, leaderboardButton):
    global time
    global piano

    introScreen = pygame.display.set_mode((widthScreen, heightScreen))
    firstDisplay = True
    introBackgroundImg = pygame.image.load("BrickWall.jpg")
    textIntro = font.render('Welcome to Shin-Dor Soccer', True, black, blue)
    textIntroRectangle = textIntro.get_rect()
    textIntroRectangle.center = (widthScreen//2, heightScreen//2)
    mixer.music.load("Intro Audio.mp3")
    mixer.music.play(-1)
    startInstructions.pressed = False
    #Initial Screen Loop
    while firstDisplay:

        #check if the user presses the button
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                firstDisplay = False
                pygame.quit() 
                os._exit(0)

            mouseCoordX, mouseCoordY = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

            startPlaying2PlayerButton.overButton(mouseCoordX, mouseCoordY)
            startPlayingAIButton.overButton(mouseCoordX, mouseCoordY)
            startInstructions.overButton(mouseCoordX, mouseCoordY)
            leaderboardButton.overButton(mouseCoordX, mouseCoordY)

            if(event.type == pygame.MOUSEBUTTONDOWN):

                startPlaying2PlayerButton.pressedButton(mouseCoordX, mouseCoordY)
                startPlayingAIButton.pressedButton(mouseCoordX, mouseCoordY)
                startInstructions.pressedButton(mouseCoordX, mouseCoordY)
                leaderboardButton.pressedButton(mouseCoordX, mouseCoordY)

        if startPlayingAIButton.pressed:
            mixer.music.pause()
            firstDisplay = False
            startPlayingAIButton.pressed = False
            player.frozen = False
            guestPlayer.frozen = False
            guestPlayer.extraSpeed = 0
            player.extraSpeed = 0
            time = 0
            doraemonMad()
           

        if startPlaying2PlayerButton.pressed:
            mixer.music.pause()
            firstDisplay = False
            startPlaying2PlayerButton.pressed = False
            player.frozen = False
            guestPlayer.frozen = False
            guestPlayer.extraSpeed = 0
            player.extraSpeed = 0
            time = 0
            twoPlayerScreen()
            #if the button is pressed we are done with the first display

        if startInstructions.pressed:
            firstDisplay = False
            createInstructionsScreen(heightScreen, widthScreen, shinChanIntroImg, doraemonIntroImg, soccerIntroImg, startPlaying2PlayerButton, startPlayingAIButton, screen, epsilon, clock, player, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg, xJumpImg, incrementJumpPlayer, incrementJumpGuestPlayer, startInstructions, leaderboardButton)

        if leaderboardButton.pressed:
            leaderboardButton.pressed = False
            firstDisplay = False
            createLeaderboardScreen(heightScreen, widthScreen, shinChanIntroImg, doraemonIntroImg, soccerIntroImg, startPlaying2PlayerButton, startPlayingAIButton, screen, epsilon, clock, player, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg, xJumpImg, incrementJumpPlayer, incrementJumpGuestPlayer, startInstructions, leaderboardButton)
        ################################
        #display of intro screen########
        ################################

        introScreen.blit((introBackgroundImg), (0,0))
        introScreen.blit(shinChanIntroImg, (17, 125))
        introScreen.blit(doraemonIntroImg, (725, 100))
        introScreen.blit(soccerIntroImg, (450, 20))
        introScreen.blit(textIntro, textIntroRectangle)
        startPlaying2PlayerButton.displayButton(introScreen)
        startPlayingAIButton.displayButton(introScreen)
        startInstructions.displayButton(introScreen)
        leaderboardButton.displayButton(introScreen)
        pygame.display.flip()

#we create this screen so that the music will not restart playing after hitting the go back to main screen after instructions
def mainMenuAfterInstructions(widthScreen, heightScreen, shinChanIntroImg, doraemonIntroImg, soccerIntroImg, startPlaying2PlayerButton, startPlayingAIButton, screen, epsilon, clock, player, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg, xJumpImg, incrementJumpPlayer, incrementJumpGuestPlayer, startInstructions, leaderboardButton):
    global piano

    introScreen = pygame.display.set_mode((widthScreen, heightScreen))
    firstDisplay = True
    introBackgroundImg = pygame.image.load("BrickWall.jpg")
    textIntro = font.render('Welcome to Shin-Dor Soccer', True, black, blue)
    textIntroRectangle = textIntro.get_rect()
    textIntroRectangle.center = (widthScreen//2, heightScreen//2)
    startInstructions.pressed = False
    #Initial Screen Loop
    while firstDisplay:

        #check if the user presses the button
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                firstDisplay = False
                pygame.quit() 
                os._exit(0)

            mouseCoordX, mouseCoordY = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

            startPlaying2PlayerButton.overButton(mouseCoordX, mouseCoordY)
            startPlayingAIButton.overButton(mouseCoordX, mouseCoordY)
            startInstructions.overButton(mouseCoordX, mouseCoordY)
            leaderboardButton.overButton(mouseCoordX, mouseCoordY)

            if(event.type == pygame.MOUSEBUTTONDOWN):

                startPlaying2PlayerButton.pressedButton(mouseCoordX, mouseCoordY)
                startPlayingAIButton.pressedButton(mouseCoordX, mouseCoordY)
                startInstructions.pressedButton(mouseCoordX, mouseCoordY)
                leaderboardButton.pressedButton(mouseCoordX, mouseCoordY)

        if startPlayingAIButton.pressed:
            mixer.music.pause()
            firstDisplay = False
            startPlayingAIButton.pressed = False
            player.frozen = False
            guestPlayer.frozen = False
            guestPlayer.extraSpeed = 0
            player.extraSpeed = 0
            player.jumpHeightSecure = 8.5
            player.jumpHeight = 8.5
            guestPlayer.jumpHeightSecure = 8
            guestPlayer.jumpHeight = 8
            time = 0
            doraemonMad()

        if startPlaying2PlayerButton.pressed:
            mixer.music.pause()
            firstDisplay = False
            startPlaying2PlayerButton.pressed = False
            twoPlayerScreen()
            #if the button is pressed we are done with the first display

        if startInstructions.pressed:
            firstDisplay = False
            createInstructionsScreen(heightScreen, widthScreen, shinChanIntroImg, doraemonIntroImg, soccerIntroImg, startPlaying2PlayerButton, startPlayingAIButton, screen, epsilon, clock, player, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg, xJumpImg, incrementJumpPlayer, incrementJumpGuestPlayer, startInstructions, leaderboardButton)

        if leaderboardButton.pressed:
            leaderboardButton.pressed = False
            firstDisplay = False
            createLeaderboardScreen(heightScreen, widthScreen, shinChanIntroImg, doraemonIntroImg, soccerIntroImg, startPlaying2PlayerButton, startPlayingAIButton, screen, epsilon, clock, player, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg, xJumpImg, incrementJumpPlayer, incrementJumpGuestPlayer, startInstructions, leaderboardButton)
        ################################
        #display of intro screen########
        ################################

        introScreen.blit((introBackgroundImg), (0,0))
        introScreen.blit(shinChanIntroImg, (17, 125))
        introScreen.blit(doraemonIntroImg, (725, 100))
        introScreen.blit(soccerIntroImg, (450, 20))
        introScreen.blit(textIntro, textIntroRectangle)
        startPlaying2PlayerButton.displayButton(introScreen)
        startPlayingAIButton.displayButton(introScreen)
        startInstructions.displayButton(introScreen)
        leaderboardButton.displayButton(introScreen)
        pygame.display.flip()

###################################################################
############ CODE AI PROJECT STARTS HERE ##########################
###################################################################

#basic intelligence will only move based on the soccer position
def applyBasicIntelligence(cpu, soccer, widthScreen, goalWidth):
    #first the AI should go towards the soccer
    epsilon = 10**-2
    #make sure the AI does not go out of bounds
    if not cpu.frozen:

        if cpu.x <= goalWidth//2:
            cpu.x = goalWidth//2
        #make sure the AI does not go outside of the right allowed bound
        if cpu.x + cpu.width >= widthScreen - goalWidth//2:
            cpu.x = widthScreen - cpu.width - goalWidth//2

        #if statemetns attempts the player to better hit the ball if it is coming at it when it is at the goal line clearance
        if cpu.x == goalWidth//2 and soccer.BDX < 0 and abs(soccer.x - cpu.x - cpu.width) <= 50:
            if abs(soccer.y + soccer.width - cpu.y) >= 5 and abs(soccer.y + soccer.width - cpu.y) <= 10:
                cpu.jump(soccer)
            else:
                cpu.x += 6
                cpu.jump(soccer)

        #to make the AI attack more
        if soccer.BDX > 0 and cpu.x >= widthScreen//2 :
            cpu.x += 5
        #make the AI to be able to realize when to defend
        elif soccer.BDX < 0 and cpu.x >= widthScreen//2:
            cpu.x -= 6

        if soccer.BDX < 0 and soccer.y + soccer.height < heightScreen - player.height and soccer.BDY < 0 and cpu.x >= goalWidth + 5 :
            cpu.x -= 6
            if abs(cpu.x - soccer.x) <= 20 and soccer.y + soccer.height > cpu.y:
                cpu.x += 6
        #to defend better the goal line
        if soccer.x <= widthScreen//2 - goalWidth and soccer.BDX < 0 and cpu.x >= goalWidth - cpu.width:
            cpu.x -= 6
            if cpu.x < goalWidth - cpu.width:
                cpu.x = goalWidth - cpu.width
            if abs(soccer.y - cpu.y) <= 6 and abs(soccer.x - cpu.x + cpu.width) <= soccer.width and soccer.BDY > 0:
                cpu.jump(soccer)
        
        #make the CPU attack more
        if soccer.x >= widthScreen//2 and soccer.BDX > 0:
            cpu.x += 2

        #if the  ball is close to the CPU make it move forward to hit the ball
        if abs(soccer.x - (cpu.x + cpu.width)) <= 10 and soccer.BDX > 0:
            cpu.x += 5
        
        #if the ball is right above the CPU make it jump
        if (soccer.x - (cpu.x + cpu.width) < 0 and soccer.x - (cpu.x + cpu.width) > -81) and abs(cpu.y - (soccer.y + soccer.height)) < 10 and (soccer.x - (widthScreen - goalWidth) <= 400):
            cpu.jump(soccer)
        #check if the other player hits the ball and go backwards if so
        if soccer.BDX >= 5*math.cos(50) and soccer.x >= widthScreen//2 + 100:
            cpu.x -= 5
        
        #this makes the AI move backwards if the soccer ball is going bakcwards
        elif abs(cpu.x + cpu.width - soccer.x) <= 65 and abs(cpu.x + cpu.width - soccer.x) >= 35 and  soccer.BDX < 0 and soccer.BDY > 0 :
            cpu.x -= 6      
        
        #if the player hits the ball move backwards
        elif player.checkPlayerHittingBall(soccer, heightScreen, widthScreen):
            cpu.x -= 6
        
        #check if the ball is closer to the other player and if it is retrocede in case it hits the ball
        elif abs(soccer.x + soccer.width - player.x) <= 5 and abs(soccer.x - cpu.x) > 5:
            cpu.x -= 6

        #if the soccer is not moving go towards it and hit it
        elif soccer.BDX == 0:
            if cpu.x + cpu.width < soccer.x:
                cpu.x += 6
        
        elif cpu.x + cpu.width < soccer.x - 20:
            cpu.x += 3.5
        
        #check if the cpu needs to jump to hit the ball
        if ((soccer.y  + soccer.height < cpu.y) and (soccer.x - (cpu.x + cpu.width) < 5) and (soccer.x > cpu.x + cpu.width) or (cpu.jumping)):
            if cpu.x + cpu.width < soccer.x:
                cpu.x += 2

            if cpu.jumpHeight + cpu.y <= soccer.y + soccer.height or cpu.jumping and soccer.y + soccer.width <= cpu.y:
                cpu.jump(soccer)
                cpu.x += 2

#medium level AI
#similar to simple but with some more conditions
def mediumAI(cpu, soccer, widthScreen, goalWidth):
       #first the AI should go towards the soccer
    epsilon = 10**-2
    #make sure the AI does not go out of bounds
    if cpu.x <= goalWidth//2:
        cpu.x = goalWidth//2
    #make sure the AI does not go outside of the right allowed bound
    if cpu.x + cpu.width >= widthScreen - goalWidth//2:
        cpu.x = widthScreen - cpu.width - goalWidth//2

    #if statemetns attempts the player to better hit the ball if it is coming at it when it is at the goal line clearance
    if cpu.x == goalWidth//2 and soccer.BDX < 0 and abs(soccer.x - cpu.x - cpu.width) <= 50:
        if abs(soccer.y + soccer.width - cpu.y) >= 5 and abs(soccer.y + soccer.width - cpu.y) <= 10:
            cpu.jump(soccer)
        else:
            cpu.x += 6 + cpu.extraSpeed
            cpu.jump(soccer)

    #to make the AI attack more
    if soccer.BDX > 0 and cpu.x >= widthScreen//2 :
        cpu.x += 5 + cpu.extraSpeed
    #make the AI to be able to realize when to defend
    elif soccer.BDX < 0 and cpu.x >= widthScreen//2:
        cpu.x -= (6 + cpu.extraSpeed)

    if soccer.BDX < 0 and soccer.y + soccer.height < heightScreen - player.height and soccer.BDY < 0 and cpu.x >= goalWidth + 5 :
        cpu.x -= (6 + cpu.extraSpeed)
        if abs(cpu.x - soccer.x) <= 20 and soccer.y + soccer.height > cpu.y:
            cpu.x += (6 + cpu.extraSpeed)
    #to defend better the goal line
    if soccer.x <= widthScreen//2 - goalWidth and soccer.BDX < 0 and cpu.x >= goalWidth - cpu.width:
        cpu.x -= (6 + cpu.extraSpeed)
        if cpu.x < goalWidth - cpu.width:
            cpu.x = goalWidth - cpu.width
        if abs(soccer.y - cpu.y) <= 6 and abs(soccer.x - cpu.x + cpu.width) <= soccer.width and soccer.BDY > 0:
            cpu.jump(soccer)
    
    #make the CPU attack more
    if soccer.x >= widthScreen//2 and soccer.BDX > 0:
        cpu.x += (2 + cpu.extraSpeed)

    #if the  ball is close to the CPU make it move forward to hit the ball
    if abs(soccer.x - (cpu.x + cpu.width)) <= 10 and soccer.BDX > 0:
        cpu.x += (5 + cpu.extraSpeed)
    
    #if the ball is right above the CPU make it jump
    if (soccer.x - (cpu.x + cpu.width) < 0 and soccer.x - (cpu.x + cpu.width) > -81) and abs(cpu.y - (soccer.y + soccer.height)) < 10:
        cpu.jump(soccer)
        timeJumped = time
    
    elif (soccer.x <= goalWidth + cpu.width + 30 and soccer.BDY > 0) and time:
        cpu.jump(soccer)

    elif abs(cpu.x + cpu.width - soccer.x) <= 20 and abs(soccer.y + soccer.height - cpu.y) <= 25 and soccer.BDY > 0:
        cpu.jump(soccer)
        cpu.x += (5 + cpu.extraSpeed)

    #check if the other player hits the ball and go backwards if so
    if soccer.BDX >= 5*math.cos(50) and soccer.x >= widthScreen//2 + 100:
        cpu.x -= (5 + cpu.extraSpeed)
    
    #this makes the AI move backwards if the soccer ball is going bakcwards
    elif abs(cpu.x + cpu.width - soccer.x) <= 65 and abs(cpu.x + cpu.width - soccer.x) >= 35 and  soccer.BDX < 0 and soccer.BDY > 0 :
        cpu.x -= (6 + cpu.extraSpeed)    
    
    #if the player hits the ball move backwards
    elif player.checkPlayerHittingBall(soccer, heightScreen, widthScreen):
        cpu.x -= (6 + cpu.extraSpeed)
    
    #check if the ball is closer to the other player and if it is retrocede in case it hits the ball
    elif abs(soccer.x + soccer.width - player.x) <= 5 and abs(soccer.x - cpu.x) > 5:
        cpu.x -= (6 + cpu.extraSpeed) 

    #if the soccer is not moving go towards it and hit it
    elif soccer.BDX == 0:
        if cpu.x + cpu.width < soccer.x:
            cpu.x += (6 + cpu.extraSpeed)
    
    elif cpu.x + cpu.width < soccer.x - 20:
        cpu.x += (3.5 + cpu.extraSpeed)
    
    #check if the cpu needs to jump to hit the ball
    if ((soccer.y  + soccer.height < cpu.y) and (soccer.x - (cpu.x + cpu.width) < 5) and (soccer.x > cpu.x + cpu.width) or (cpu.jumping)):
        if cpu.x + cpu.width < soccer.x:
            cpu.x += (2 + cpu.extraSpeed)

        if cpu.jumpHeight + cpu.y <= soccer.y + soccer.height or cpu.jumping and soccer.y + soccer.width <= cpu.y:
            cpu.jump(soccer)
            cpu.x += (2 + cpu.extraSpeed)


##################################################################
############## AI MAIN GAME OCCURS HERE  #########################
##################################################################
    
#Create the screen that will be popped if we select "Single Player"
def createScreenSinglePlayer(heightScreen, widthScreen, screen, epsilon, clock, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg, goalWidth, xJumpImg,incrementJumpPlayer, incrementJumpGuestPlayer):
    global jumpImgShowing
    global yJumpImg
    global timeFrozen
    global time
    global gameOver
    global timeWonGame
    global score
    global scoreList
    global speedImgShowing
    global jumpImgShowing
    global AIlevel
    global pauseButton
    global pauseImg
    global pauseGame
    global quitButton
    global xImg
    global restartButton
    global restartImg
    global stadiumImg
    global doramiChosen
    global doramiImg
    global player

    singlePlayerScreen = True
    lose = False
    win = False

    if doramiChosen: 
        player = dorami

    while singlePlayerScreen:

        if soccer.y <= goalHeight and soccer.x < goalWidth - soccer.width:
            player.goalCount += 1
            soccer.x = widthScreen//2
            soccer.y =  heightScreen//2 - 20
            pygame.display.flip()

        if soccer.y <= goalHeight and soccer.x + soccer.width > widthScreen -(goalWidth):
            guestPlayer.goalCount += 1
            soccer.x = widthScreen//2
            soccer.y =  heightScreen//2 - 20
            pygame.display.flip()
        
        if player.y + player.height > heightScreen:
            player.y = heightScreen - player.height

        if pauseButton.pressed:
            pauseGame = not pauseGame
            pauseButton.pressed = False

        if not pauseGame:

            time += 1

            clock.tick(1000)
            
            #stop the game when a player scores 7 goals
            #create our score string for the leaderBoard
            if gameOver:
                guestPlayer.y = heightScreen - guestPlayer.height
                player.y = heightScreen - player.height
                lose_Sound = mixer.Sound("Sad Violin Airhorn.mp3")
                win_Sound = mixer.Sound("Winning Sound.mp3")

                
                if guestPlayer.goalCount == 4:
                    lose_Sound.play()
                    lose = True

                elif player.goalCount == 4:
                    win_Sound.play()
                    win = True

                    
                #create confetti
                colorsDoraemon = [(102, 178, 255), (255, 255, 255)]
                colorsShinChan = [(255,0,0), (255, 255, 0)]
                for circle in range(3000):
                    if player.goalCount == 4:
                        color = colorsShinChan[random.randint(0, len(colorsShinChan) - 1)]
                    else:
                        color = colorsDoraemon[random.randint(0, len(colorsDoraemon) - 1)]
                    pygame.draw.circle(screen, color, ((random.randint(widthScreen//2 -400, widthScreen//2 + 450)), random.randint(heightScreen//2 , heightScreen//2 + 300)), 2)
                
                    pygame.display.flip()


                gameOver = False
                scoreList = [guestPlayer.goalCount, player.goalCount]
                score = str(scoreList[0]) + "-" + str(scoreList[1])
                player.frozen = False
                guestPlayer.frozen = False
                speedImgShowing = False
                jumpImgShowing = False
                player.jumping = False
                guestPlayer.jumping = False
                player.beenFreezed = False
                guestPlayer.beenFreezed = False

                
                soccer.BDY = 0
                soccer.BDX = 0
                player.x = widthScreen - goalWidth - player.width
                guestPlayer.x = goalWidth + guestPlayer.width/2
                guestPlayer.extraSpeed = 0
                player.extraSpeed = 0

                if not doramiChosen:
                    player.jumpHeightSecure = 8.5
                    player.jumpHeight = 8.5

                elif doramiChosen:
                    player.jumpHeightSecure = 7
                    player.jumpHeight = 7

                guestPlayer.jumpHeightSecure = 8
                guestPlayer.jumpHeight = 8
                soccer.x = widthScreen//2
                soccer.y = heightScreen//2 - 20

                pygame.time.wait(5000)
                lose_Sound.stop()
                fillLeaderboard()

                
                if lose:
                    lose_Sound.stop()
                    loserScreen()

                elif win:
                    win_Sound.stop()
                    winScreen()
                
            #check if one of the players has reached the maximum score allowed
            if (player.goalCount == 4 or guestPlayer.goalCount == 4) and not gameOver:
                gameOver = True
                timeWonGame = time
                player.frozen = True
                guestPlayer.frozen = True
            #to make sure when our playing is jumping and is frozen it does not stay in the air
            if player.frozen:
                player.y = heightScreen - player.height

            elif guestPlayer.frozen:
                guestPlayer.y = heightScreen - guestPlayer.height


            #check if the image has hit ground and check if any player gets the jump icon
            if (((player.y >= yJumpImg and player.y < yJumpImg + jumpImgHeight) or (player.y + player.height >= yJumpImg and player.y + player.height < yJumpImg + jumpImgHeight) or
            (player.y + player.height >= yJumpImg and player.y <= yJumpImg))
            and ((player.x + player.width > xJumpImg + 15 and player.x < xJumpImg) or
            (player.x < xJumpImg - 15 and player.x + player.width > xJumpImg + 30)) and
            jumpImgShowing and player.jumpHeightSecure != 9) and not incrementJumpPlayer:
                incrementJumpPlayer = True
                yJumpImg = 30
                jumpImgShowing = False

            #check for the other player
            elif (((guestPlayer.y >= yJumpImg and guestPlayer.y < yJumpImg + jumpImgHeight) or (guestPlayer.y + guestPlayer.height >= yJumpImg and guestPlayer.y + guestPlayer.height < yJumpImg + jumpImgHeight) or
            (guestPlayer.y + guestPlayer.height >= yJumpImg and guestPlayer.y <= yJumpImg))
            and ((guestPlayer.x + guestPlayer.width > xJumpImg + 15 and guestPlayer.x < xJumpImg) or
            (guestPlayer.x < xJumpImg - 15 and guestPlayer.x + guestPlayer.width > xJumpImg + 30)) and
            jumpImgShowing and player.jumpHeightSecure != 9) and not incrementJumpGuestPlayer:
                incrementJumpGuestPlayer = True
                yJumpImg = 30
                jumpImgShowing = False

            #apply the jumpImage powerup if it is showing
            elif jumpImgShowing and yJumpImg < heightScreen - 30:
                yJumpImg += 5

            elif yJumpImg == heightScreen - 30:
                jumpImgShowing = False
                yJumpImg = 30
                xJumpImg = random.randint(widthScreen//2 - 300, widthScreen//2 + 300)

            #now add the extra jumpheight if a player got it

            if incrementJumpPlayer and not player.jumping:
                incrementJumpPlayer = False
                player.jumpHeight += 0.5
                player.jumpHeightSecure += 0.5

            elif incrementJumpGuestPlayer and not guestPlayer.jumping:
                incrementJumpGuestPlayer = False
                guestPlayer.jumpHeight += 0.5
                guestPlayer.jumpHeightSecure += 0.5

            #the following code is applied to the freeze power
            #this power can only be achieved once since it is supreme and will pretty much allow you a free goal
            #if a player is winning by 3 goals the other player is frozen for a decent amount of seconds
            possibleTimeFrozen = applyPowers(player, guestPlayer, time, superJumpImg, screen, xJumpImg, yJumpImg)
            if isinstance(possibleTimeFrozen, int):
                timeFrozen = possibleTimeFrozen
            
            if isinstance(timeFrozen, int) and (time - timeFrozen) == 75:
                player.frozen = False
                guestPlayer.frozen = False

            if AIlevel == "Easy":
                applyBasicIntelligence(guestPlayer, soccer, widthScreen, goalWidth)
            if AIlevel == "Medium":
                mediumAI(guestPlayer, soccer, widthScreen, goalWidth)

            checkForCollisionsAndOutOfBoundsAndGoal(heightScreen, widthScreen, epsilon, textGoal, textGoalRectangle, screen)

            keyPressed = pygame.key.get_pressed()
            #this makes sure the player can move continously so that we do not have to press the key multiple times
            if not player.frozen:
                
                ###########################################@
                #ONLY USE THE KEYS l AND w TO SKIP THE GAME#
                ############################################


                if keyPressed[pygame.K_l]:
                    guestPlayer.goalCount = 4
                    fillLeaderboard()
                    gameOver = True
                 
                if keyPressed[pygame.K_w]:
                    player.goalCount = 4
                    fillLeaderboard()
                    gameOver = True

                if keyPressed[pygame.K_RIGHT] and player.x + player.width <= widthScreen - goalWidth + player.width:   #the purpose of the and is to ensure the player does not go outside of the right bound
                    player.x += 5.5
                    player.rectangleX = player.x
            
            
                if keyPressed[pygame.K_LEFT] and player.x >= goalWidth - player.width + 20:         #the purpose of the and is to ensure the player does not go outside of the left bound
                    player.x -= 5.5                      #0.15
                    player.rectangleX = player.x
                
                if not player.jumping and keyPressed[pygame.K_UP]:    #by putting this statement we ensure the player cannot jump while it is alredy jumping
                    player.jumping = True
                
                if player.jumping:
                    player.jump(soccer)
                #make sure we check for all our collisions and goals, etc

        #make sure the user can exit out of the game by pressing the top left exit button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                singlePlayerScreen = False
                pygame.quit()  	# ensures pygame module closes properly
                os._exit(0)	    # ensure the window closes

            if event.type == pygame.MOUSEBUTTONDOWN:

                (mouseX, mouseY) = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

                pauseButton.pressedPause(mouseX, mouseY)
                quitButton.pressedPause(mouseX, mouseY)
                playButton.pressedPause(mouseX, mouseY)
                restartButton.pressedPause(mouseX, mouseY)
        

        #proceed to load the screen 
        screen.blit(pygame.image.load(stadiumImg), (0,0))
        black = (0,0,0)
        green = (0, 255, 0)

        ##############################################
        #The following lines update the current position of the objects
        ##############################################
        screen.blit(soccerImg, (soccer.x, soccer.y))
        if not doramiChosen:
            screen.blit(playerImg, (player.x, player.y))
        else:
            screen.blit(doramiImg, (player.x, player.y))

        screen.blit(guestPlayerImg, (guestPlayer.x, guestPlayer.y))
        screen.blit(goalLeftImg, (0, heightScreen - goalHeight))
        screen.blit(goalRightImg, (widthScreen - goalWidth, heightScreen - goalHeight))
        screen.blit(pauseImg, (pauseButton.x, pauseButton.y))
        createGoalCount(player, guestPlayer, screen, widthScreen)
    
        if jumpImgShowing:
            screen.blit(superJumpImg, (xJumpImg, yJumpImg))
    
        if speedImgShowing:
            screen.blit(runFastImg, (speedX, speedY))

        if guestPlayer.y + guestPlayer.height > heightScreen:
            guestPlayer.y = heightScreen - guestPlayer.height
        
        
        #pause part of the code
        if pauseGame:

            paused = "Paused Game"
            pausedText = font.render(paused, True, (0, 0, 0))
            pausedTextRect = pausedText.get_rect()
            pausedTextRect.center = (575, 400)
            
            createPauseMenu(screen)
            screen.blit(pausedText, pausedTextRect)

            if pauseButton.pressed:
                pauseGame = not pauseGame
                pauseButton.pressed = False

            #resume the playing
            if playButton.pressed:
                pauseGame = not pauseGame
                playButton.pressed = False
            
            #restart the game from 0-0
            if restartButton.pressed:
                soccer.BDY = 0
                soccer.BDX = 0
                player.x = widthScreen - goalWidth - player.width
                guestPlayer.x = goalWidth + guestPlayer.width/2
                player.goalCount = 0
                guestPlayer.goalCount = 0
                guestPlayer.extraSpeed = 0
                player.extraSpeed = 0
                player.beenFreezed = False
                guestPlayer.beenFreezed = False

                if not doramiChosen:
                    player.jumpHeightSecure = 8.5
                    player.jumpHeight = 8.5

                elif doramiChosen:
                    player.jumpHeightSecure = 7
                    player.jumpHeight = 7

                guestPlayer.jumpHeightSecure = 8
                guestPlayer.jumpHeight = 8
                soccer.x = widthScreen//2
                soccer.y = heightScreen//2 - 20
                speedImgShowing = False
                jumpImgShowing = False
                restartButton.pressed = False
                pauseGame = not pauseGame
                player.jumping = False
                guestPlayer.jumping = False
                guestPlayer.y = heightScreen - guestPlayer.height
                player.y = heightScreen - player.height

            #quit the game
            if quitButton.pressed:
                pauseGame = not pauseGame
                quitButton.pressed = False
                guestPlayer.goalCount = 0
                player.goalCount = 0
                player.frozen = False
                guestPlayer.frozen = False
                speedImgShowing = False
                jumpImgShowing = False
                player.jumping = False
                player.beenFreezed = False
                guestPlayer.beenFreezed = False
                soccer.BDY = 0
                soccer.BDX = 0
                player.x = widthScreen - goalWidth - player.width
                guestPlayer.x = goalWidth + guestPlayer.width/2
                player.goalCount = 0
                guestPlayer.goalCount = 0
                guestPlayer.extraSpeed = 0
                player.extraSpeed = 0
                
                if not doramiChosen:
                    player.jumpHeightSecure = 8.5
                    player.jumpHeight = 8.5
                
                elif doramiChosen:
                    player.jumpHeightSecure = 7
                    player.jumpHeight = 7

                guestPlayer.jumpHeightSecure = 8
                guestPlayer.jumpHeight = 8
                soccer.x = widthScreen//2
                soccer.y = heightScreen//2 - 20
                guestPlayer.jumping = False
                player.jumping = False
                guestPlayer.y = heightScreen - guestPlayer.height
                player.y = heightScreen - player.height

                mainMenu(widthScreen, heightScreen, shinChanIntroImg, doraemonIntroImg, soccerIntroImg, startPlaying2PlayerButton, startPlayingAIButton, screen, epsilon, clock, player, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg, xJumpImg,incrementJumpPlayer, incrementJumpGuestPlayer, startInstructions, leaderboardButton)

            screen.blit(xImg, (widthScreen//2 - 85, heightScreen//2 + 137))
            screen.blit(playImg, (widthScreen//2, heightScreen//2 + 135))
            screen.blit(restartImg, (widthScreen//2 + 85, heightScreen//2 + 135))
    
        pygame.display.flip()

#screen where the user will be able to choose what level to play agains
def createAILevels(heightScreen, widthScreen, screen, epsilon, clock, player, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg, goalWidth, xJumpImg,incrementJumpPlayer, incrementJumpGuestPlayer):
    global AIlevel
    global easyButton
    global mediumButton
    global piano

    introBackgroundImg = pygame.image.load("Instructions.jpg")
    topLeft = (0, 0)
    white = (255, 255, 255)
    
    levelScreen = pygame.display.set_mode((widthScreen, heightScreen))
    createLevels = True

    text = "Pick the level of difficulty"
    makeText = font.render(text, True, white)
    makeTextRect = makeText.get_rect()
    makeTextRect.center = (widthScreen//2, 100)

    piano.play()
    while createLevels:

        for event in pygame.event.get():
            mouseCoordX, mouseCoordY = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            easyButton.overButton(mouseCoordX, mouseCoordY)
            mediumButton.overButton(mouseCoordX, mouseCoordY)

            if event.type == pygame.MOUSEBUTTONDOWN:
                easyButton.pressedButton(mouseCoordX, mouseCoordY)
                mediumButton.pressedButton(mouseCoordX, mouseCoordY)

            if event.type == pygame.QUIT:
                createLevels = False
                piano.stop()
                pygame.quit() 
                os._exit(0)


        if easyButton.pressed:
            AIlevel = "Easy"
            easyButton.pressed = False
            createLevels = False
            piano.stop()
            createScreenSinglePlayer(heightScreen, widthScreen, screen, epsilon, clock, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg, goalWidth, xJumpImg,incrementJumpPlayer, incrementJumpGuestPlayer)

        if mediumButton.pressed:
            AIlevel = "Medium"
            mediumButton.pressed = False
            createLevels = False
            piano.stop()
            createScreenSinglePlayer(heightScreen, widthScreen, screen, epsilon, clock, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg, goalWidth, xJumpImg,incrementJumpPlayer, incrementJumpGuestPlayer)
        
        levelScreen.blit(introBackgroundImg, topLeft)
        easyButton.displayButton(levelScreen)
        mediumButton.displayButton(levelScreen)
        levelScreen.blit(makeText, makeTextRect)
        pygame.display.flip()
    

##################################################
#Keeps track of the number of goals of each player
##################################################
def createGoalCount(player, guestPlayer, screen, widthScreen):
    goalDisplay = pygame.image.load("Show Score.png")
    numberLeft = guestPlayer.goalCount
    numberRight = player.goalCount
    scoreTextLeft = font.render(f'{numberLeft}', True, (255, 255, 255))        
    scoreTextRight = font.render(f'{numberRight}', True, (255, 255, 255))  
    scoreTextLeftRectangle = scoreTextLeft.get_rect() 
    scoreTextRightRectangle = scoreTextRight.get_rect()
    scoreTextRightRectangle.center = (widthScreen//2 + 78, 220)
    scoreTextLeftRectangle.center = (widthScreen//2  - 70 , 220)
    screen.blit(goalDisplay, (widthScreen//2 - 155, 25))
    screen.blit(scoreTextRight, scoreTextRightRectangle)
    screen.blit(scoreTextLeft, scoreTextLeftRectangle)

##########################################
####### SUPER POWERS FUNCTIONS ###########
##########################################

#the first power  will be to become faster every time you score
def applyExtraSpeed(player, guestPlayer, time, screen):
    global speedImgShowing
    global heightScreen
    global speedX
    global speedY

    if time % 300 == 0 and time != 0 and not speedImgShowing and not (guestPlayer.extraSpeed == 1.5 and player.extraSpeed == 1.5):
        screen.blit(runFastImg,(speedX, speedY))
        speedImgShowing = True

    #check if the image has hit ground and check if any player gets the jump icon
    elif (((player.y >= speedY and player.y < speedY + runFastHeight) or (player.y + player.height >= speedY and player.y + player.height < speedY + runFastHeight) or
    (player.y + player.height >= speedY and player.y <= runFastHeight))
    and ((player.x + player.width > speedX + 12 and player.x < speedX) or
    (player.x < speedX - 12 and player.x + player.width > speedX + 24)) and
    speedImgShowing and player.extraSpeed != 1.5):
        player.extraSpeed += 0.5
        speedY = 30
        speedImgShowing = False

    #check for the other player
    elif (((guestPlayer.y >= speedY and guestPlayer.y < speedY + runFastHeight) or (guestPlayer.y + guestPlayer.height >= speedY and guestPlayer.y + guestPlayer.height < speedY + runFastHeight) or
    (guestPlayer.y + guestPlayer.height >= speedY and guestPlayer.y <= runFastHeight))
    and ((guestPlayer.x + guestPlayer.width > speedX + 12 and guestPlayer.x < speedX) or
    (guestPlayer.x < speedX - 12 and guestPlayer.x + guestPlayer.width > speedX + 24)) and
    speedImgShowing and guestPlayer.extraSpeed != 1.5):
        guestPlayer.extraSpeed += 0.5
        speedY = 30
        speedImgShowing = False

    elif speedImgShowing and speedY < heightScreen - 40:
        speedY += 5

    elif speedY == heightScreen - 40:
        speedY = 30
        speedImgShowing = False
        speedX = random.randint(widthScreen//2 - 300, widthScreen//2 + 300)


#applies super jump to the player who is hitting the ball more often, aka being more engaging
def applySuperJump(player, guestPlayer, time, superJumpImg, screen, x, y):
    global jumpImgShowing
    global doramiChosen

    if doramiChosen:
        if time % 200 == 0 and not jumpImgShowing and time != 0 and not player.jumpHeightSecure == 7.5 and not guestPlayer.jumpHeightSecure == 8.5:
            screen.blit(superJumpImg, (x,y))
            jumpImgShowing = True

    elif not doramiChosen:
        if time % 200 == 0 and not jumpImgShowing and time != 0 and not player.jumpHeightSecure == 9 and not guestPlayer.jumpHeightSecure == 8.5:
            screen.blit(superJumpImg, (x,y))
            jumpImgShowing = True


#if someone is losing by 3 they get frozen by a certain amount of time
def applyGetFrozen(player, guestPlayer, time, screen):
    global beenFreezed
    red = (255, 0, 0)
    black = (0, 0, 0)
    font = pygame.font.Font('freesansbold.ttf', 32)
    textFrozen = font.render('Someone has been outscored and hence frozen!', True, red, black)
    textFrozenRect = textFrozen.get_rect()
    textFrozenRect.center = (widthScreen//2, 300)

    if ((player.goalCount - guestPlayer.goalCount) % 3 == 0 and player.goalCount + guestPlayer.goalCount != 0 and not guestPlayer.frozen
    and player.goalCount > guestPlayer.goalCount and not guestPlayer.beenFreezed):
        guestPlayer.frozen = True
        timeFrozen = time
        guestPlayer.beenFreezed = True
        return timeFrozen

    elif ((guestPlayer.goalCount - player.goalCount) % 3 == 0 and player.goalCount + guestPlayer.goalCount != 0 and not player.frozen 
    and guestPlayer.goalCount > player.goalCount and not player.beenFreezed) :
        player.frozen = True
        timeFrozen = time
        player.beenFreezed = True
        return timeFrozen


#power where the player scores a goal (opponent and ball move towards the goal)

#this function calls all the superpowers and applies them all together
def applyPowers(player, guestPlayer, time, superJumpImg, screen, x, y):
    global jumpImgShowing

    applyExtraSpeed(player, guestPlayer, time, screen)

    applySuperJump(player, guestPlayer, time, superJumpImg, screen, x, y)

    timeFrozen = applyGetFrozen(player, guestPlayer, time, screen)

    return timeFrozen


##################################################################
############## CREATES OUR LEADERBOARD ###########################
##################################################################
#creates our leaderBoard with the best scores sorted in order of best to worst
def fillLeaderboard():
    global score
    global currentLeaderboard
    global firstScoreInts
    global compareScore

    currentLeaderboard = []
    fileL = readFile('Leaderboard')
    saveScores = ""
    #check if the length of the file is 0 and if so add the score
    if len(fileL) == 0:
        writeFile('Leaderboard', score)
        currentLeaderboard.append(score)
   
    else:
        #convert our file into a list containing all the scores. Ex: ['2-0', '2-1', '2-2']
        for savedScore in fileL.split(","):
            currentLeaderboard.append(savedScore)

        for i in range(len(currentLeaderboard)):
            compareScore = currentLeaderboard[i]
            if len(score) != 0:
                #we do not want to save the same score twice
                if (int(compareScore[0]) == int(score[0]) and int(compareScore[2]) == int(score[2])):
                    return
                #check if the score is better than other scores
                if abs(int(compareScore[0]) - int(compareScore[2])) < abs(int(score[0]) - int(score[2])):
                    currentLeaderboard.insert(i, score)
                    #to save the scores put them in a string
                    for everyScore in currentLeaderboard:
                        saveScores += everyScore + ","
                    writeFile('Leaderboard', saveScores[0:len(saveScores) - 1])
                    return

        if len(score) != 0:    
            #let's say our score was not greater than any of the previous but it was smaller.... we still add it
            if abs(int(compareScore[0]) - int(compareScore[2])) > abs(int(score[0]) - int(score[2])):
                currentLeaderboard.append(score)
                #again, save all the scores in saveScores
                for everyScore in currentLeaderboard:
                    saveScores += everyScore + ","

                #finally we can write all the scores into the file
                writeFile('Leaderboard', saveScores[0:len(saveScores) - 1])


##################################################################
############## TWO PLAYER MAIN GAME HERE #########################
##################################################################
#this function contains the code for the two player screen
def twoPlayerScreen():
    global player
    global guestPlayer
    global heightScreen
    global widthScreen
    global time
    global yJumpImg
    global xJumpImg
    global incrementJumpPlayer
    global jumpImgShowing
    global incrementJumpGuestPlayer
    global timeFrozen
    global gameOver
    global timeWonGame
    global scoreList
    global score
    global speedImgShowing
    global jumpImgShowing
    global pauseButton
    global pauseImg
    global pauseGame
    global quitButton
    global xImg
    global restartButton
    global restartImg
    global dorami
    global doramiImg
    global stadiumImg
    global doramiChosen

    time += 1
    play = True

    if doramiChosen:
        player = dorami

    while play:
        
        if pauseButton.pressed:
                pauseGame = not pauseGame
                pauseButton.pressed = False

        if not pauseGame:

            time += 1

            if player.frozen:
                player.y = heightScreen - player.height

            elif guestPlayer.frozen:
                guestPlayer.y = heightScreen - guestPlayer.height

            if gameOver:
                lose_Sound = mixer.Sound("Sad Violin Airhorn.mp3")
                win_Sound = mixer.Sound("Winning Sound.mp3")
                if guestPlayer.goalCount == 4:
                    lose_Sound.play()
                elif player.goalCount == 4:
                    win_Sound.play()

                colorsDoraemon = [(102, 178, 255), (255, 255, 255)]
                colorsShinChan = [(255,0,0), (255, 255, 0)]
                #draw the confetti
                for circle in range(3000):
                    if player.goalCount == 4:
                        color = colorsShinChan[random.randint(0, len(colorsShinChan) - 1)]
                    else:
                        color = colorsDoraemon[random.randint(0, len(colorsDoraemon) - 1)]
                    pygame.draw.circle(screen, color, ((random.randint(widthScreen//2 -400, widthScreen//2 + 450)), random.randint(heightScreen//2 , heightScreen//2 + 300)), 2)
                    pygame.display.flip()

                play = False
                gameOver = False
                scoreList = [guestPlayer.goalCount, player.goalCount]
                score = str(scoreList[0]) + "-" + str(scoreList[1])
                guestPlayer.goalCount = 0
                player.goalCount = 0
                player.frozen = False
                guestPlayer.frozen = False
                speedImgShowing = False
                jumpImgShowing = False
                player.jumping = False
                guestPlayer.jumping = False
                player.beenFreezed = False
                guestPlayer.beenFreezed = False
                fillLeaderboard()
                AIlevel = None

                if not doramiChosen:
                    player.jumpHeightSecure = 8.5
                    player.jumpHeight = 8.5
                elif doramiChosen:
                    player.jumpHeightSecure = 7
                    player.jumpHeight = 7
                
                guestPlayer.jumpHeight = 8
                guestPlayer.jumpHeightSecure = 8
                pygame.time.wait(5000)
                lose_Sound.stop()
                mainMenu(widthScreen, heightScreen, shinChanIntroImg, doraemonIntroImg, soccerIntroImg, startPlaying2PlayerButton, startPlayingAIButton, screen, epsilon, clock, player, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg, xJumpImg,incrementJumpPlayer, incrementJumpGuestPlayer, startInstructions, leaderboardButton)
            #check if one of the players has reached the maximum score allowed
            if (player.goalCount == 4 or guestPlayer.goalCount == 4) and not gameOver:
                player.frozen = True
                guestPlayer.frozen = True
                gameOver = True
                timeWonGame = time
            #to make sure when our playing is jumping and is frozen it does not stay in the air
            if player.frozen:
                player.y = heightScreen - player.height

            elif guestPlayer.frozen:
                guestPlayer.y = heightScreen - guestPlayer.height

            #check if the image has hit ground and check if any player gets the jump icon
            if (((player.y >= yJumpImg and player.y < yJumpImg + jumpImgHeight) or (player.y + player.height >= yJumpImg and player.y + player.height < yJumpImg + jumpImgHeight) or
            (player.y + player.height >= yJumpImg and player.y <= yJumpImg))
            and ((player.x + player.width > xJumpImg + 15 and player.x < xJumpImg) or
            (player.x < xJumpImg - 15 and player.x + player.width > xJumpImg + 30)) and
            jumpImgShowing and player.jumpHeightSecure != 9) and not incrementJumpPlayer:
                incrementJumpPlayer = True
                yJumpImg = 30
                jumpImgShowing = False

            #check for the other player
            elif (((guestPlayer.y >= yJumpImg and guestPlayer.y < yJumpImg + jumpImgHeight) or (guestPlayer.y + guestPlayer.height >= yJumpImg and guestPlayer.y + guestPlayer.height < yJumpImg + jumpImgHeight) or
            (guestPlayer.y + guestPlayer.height >= yJumpImg and guestPlayer.y <= yJumpImg))
            and ((guestPlayer.x + guestPlayer.width > xJumpImg + 15 and guestPlayer.x < xJumpImg) or
            (guestPlayer.x < xJumpImg - 15 and guestPlayer.x + guestPlayer.width > xJumpImg + 30)) and
            jumpImgShowing and guestPlayer.jumpHeightSecure != 8.5) and not incrementJumpGuestPlayer:
                incrementJumpGuestPlayer = True
                yJumpImg = 30
                jumpImgShowing = False

            #apply the jumpImage powerup if it is showing
            elif jumpImgShowing and yJumpImg < heightScreen - 30:
                yJumpImg += 5

            elif yJumpImg == heightScreen - 30:
                jumpImgShowing = False
                yJumpImg = 30
                xJumpImg = random.randint(widthScreen//2 - 300, widthScreen//2 + 300)

            #now add the extra jumpheight if a player got it

            if incrementJumpPlayer and not player.jumping:
                incrementJumpPlayer = False
                player.jumpHeight += 0.5
                player.jumpHeightSecure += 0.5

            elif incrementJumpGuestPlayer and not guestPlayer.jumping:
                incrementJumpGuestPlayer = False
                guestPlayer.jumpHeight += 0.5
                guestPlayer.jumpHeightSecure += 0.5

            #the following code is applied to the freeze power
            #this power can only be achieved once since it is supreme and will pretty much allow you a free goal
            #if a player is winning by 3 goals the other player is frozen for a decent amount of seconds
            possibleTimeFrozen = applyPowers(player, guestPlayer, time, superJumpImg, screen, xJumpImg, yJumpImg)
            if isinstance(possibleTimeFrozen, int):
                timeFrozen = possibleTimeFrozen
            
            if isinstance(timeFrozen, int) and (time - timeFrozen) == 150:
                player.frozen = False
                guestPlayer.frozen = False
            

            clock.tick(10000)
            
            keyPressed = pygame.key.get_pressed() #gets the key that it is being pressed

            #this makes sure the player can move continously so that we do not have to press the key multiple times

            if not player.frozen:

                if keyPressed[pygame.K_RIGHT] and player.x + player.width <= widthScreen - goalWidth + player.width:   #the purpose of the and is to ensure the player does not go outside of the right bound
                    player.x += 6 + player.extraSpeed                 #0.15
                    player.rectangleX = player.x
                
                if keyPressed[pygame.K_LEFT] and player.x >= goalWidth - player.width + 20:         #the purpose of the and is to ensure the player does not go outside of the left bound
                    player.x -= abs(6 + player.extraSpeed)                   #0.15
                    player.rectangleX = player.x
                
                if not player.jumping and keyPressed[pygame.K_UP]:    #by putting this statement we ensure the player cannot jump while it is alredy jumping
                    player.jumping = True
                
                if player.jumping:
                    player.jump(soccer)

            #To move the guest player... 

            if not guestPlayer.frozen:

                if keyPressed[pygame.K_s] and guestPlayer.x + guestPlayer.width <= widthScreen - goalWidth + guestPlayer.width:   #the purpose of the and is to ensure the player does not go outside of the right bound
                    guestPlayer.x += 6 + guestPlayer.extraSpeed
                
                if keyPressed[pygame.K_a] and guestPlayer.x >= goalWidth - guestPlayer.width + 20:          #the purpose of this and is to ensure the player does not go outside of the left bound                                 
                    guestPlayer.x -= 6 + guestPlayer.extraSpeed
                
                if not guestPlayer.jumping and keyPressed[pygame.K_SPACE]: 
                    guestPlayer.jumping = True
                
                if guestPlayer.jumping:
                    guestPlayer.jump(soccer)
            

            checkForCollisionsAndOutOfBoundsAndGoal(heightScreen, widthScreen, epsilon, textGoal, textGoalRectangle, screen)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                play = False
                pygame.quit()
                os._exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                (mouseX, mouseY) = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                pauseButton.pressedPause(mouseX, mouseY)
                quitButton.pressedPause(mouseX, mouseY)
                playButton.pressedPause(mouseX, mouseY)
                restartButton.pressedPause(mouseX, mouseY)
        
        
        #sets the background color of the display
        screen.blit(pygame.image.load(stadiumImg), (0,0))
        ##############################################
        #The following lines update the current position of the objects
        ##############################################
        screen.blit(soccerImg, (soccer.x, soccer.y))

        #make sure we are displaying the right player
        if doramiChosen:
            screen.blit(doramiImg, (player.x, player.y))
        else:
            screen.blit(playerImg, (player.x, player.y))

        screen.blit(guestPlayerImg, (guestPlayer.x, guestPlayer.y))
        screen.blit(goalLeftImg, (0, heightScreen - goalHeight))
        screen.blit(goalRightImg, (widthScreen - goalWidth, heightScreen - goalHeight))
        screen.blit(pauseImg, (pauseButton.x, pauseButton.y))
        createGoalCount(player, guestPlayer, screen, widthScreen)

        if jumpImgShowing:
            screen.blit(superJumpImg, (xJumpImg, yJumpImg))
        
        if speedImgShowing:
            screen.blit(runFastImg, (speedX, speedY))


        #pause part of the code
        if pauseGame:

            paused = "Paused Game"
            pausedText = font.render(paused, True, (0, 0, 0))
            pausedTextRect = pausedText.get_rect()
            pausedTextRect.center = (575, 400)
            
            createPauseMenu(screen)
            screen.blit(pausedText, pausedTextRect)

            if pauseButton.pressed:
                pauseGame = not pauseGame
                pauseButton.pressed = False

            #resume the playing
            if playButton.pressed:
                pauseGame = not pauseGame
                playButton.pressed = False
            
            #restart the game from 0-0
            if restartButton.pressed:
                soccer.BDY = 0
                soccer.BDX = 0
                player.x = widthScreen - goalWidth - player.width
                guestPlayer.x = goalWidth + guestPlayer.width/2
                player.goalCount = 0
                guestPlayer.goalCount = 0
                guestPlayer.extraSpeed = 0
                player.extraSpeed = 0

                if doramiChosen:
                    player.jumpHeightSecure = 7
                    player.jumpHeight = 7
                elif not doramiChosen:
                    player.jumpHeightSecure = 8.5
                    player.jumpHeight = 8.5
                
                guestPlayer.jumpHeightSecure = 8
                guestPlayer.jumpHeight = 8
                soccer.x = widthScreen//2
                soccer.y = heightScreen//2 - 20
                speedImgShowing = False
                jumpImgShowing = False
                restartButton.pressed = False
                pauseGame = not pauseGame
                player.jumping = False
                guestPlayer.jumping = False
                guestPlayer.y = heightScreen - guestPlayer.height
                player.y = heightScreen - player.height
                player.beenFreezed = False
                guestPlayer.beenFreezed = False

            #quit the game
            if quitButton.pressed:
                player.jumping = False
                guestPlayer.jumping = False
                guestPlayer.y = heightScreen - guestPlayer.height
                player.y = heightScreen - player.height
                pauseGame = not pauseGame
                quitButton.pressed = False
                speedImgShowing = False
                jumpImgShowing = False
                player.beenFreezed = False
                guestPlayer.beenFreezed = False
                play = False
                soccer.BDY = 0
                soccer.BDX = 0
                player.x = widthScreen - goalWidth - player.width
                guestPlayer.x = goalWidth + guestPlayer.width/2
                player.goalCount = 0
                guestPlayer.goalCount = 0
                guestPlayer.extraSpeed = 0
                player.extraSpeed = 0

                if doramiChosen:
                    player.jumpHeightSecure = 7
                    player.jumpHeight = 7
                elif not doramiChosen:
                    player.jumpHeightSecure = 8.5
                    player.jumpHeight = 8.5

                guestPlayer.jumpHeight = 8
                soccer.x = widthScreen//2
                soccer.y = heightScreen//2 - 20
                mainMenu(widthScreen, heightScreen, shinChanIntroImg, doraemonIntroImg, soccerIntroImg, startPlaying2PlayerButton, startPlayingAIButton, screen, epsilon, clock, player, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg, xJumpImg,incrementJumpPlayer, incrementJumpGuestPlayer, startInstructions, leaderboardButton)

            screen.blit(xImg, (widthScreen//2 - 85, heightScreen//2 + 137))
            screen.blit(playImg, (widthScreen//2, heightScreen//2 + 135))
            screen.blit(restartImg, (widthScreen//2 + 85, heightScreen//2 + 135))

            

        pygame.display.flip()

##################################################################
############## SINGLE PLAYER MODE SCREENS ########################
##################################################################

#the screen where the player will choose a player
def choosePlayer(widthScreen, heightScreen, shinChanIntroImg, doraemonIntroImg, soccerIntroImg, startPlaying2PlayerButton, startPlayingAIButton, screen, epsilon, clock, player, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg, xJumpImg, incrementJumpPlayer, incrementJumpGuestPlayer, startInstructions, leaderboardButton):
    global shinChanChosen
    global doramiChosen

    yellow = (255, 255, 0)
    width = 1024
    height = 640
    doramiSize = (150, 209)

    chooseText = "Choose a player"
    chooseText = font.render(chooseText, True, (255, 0, 0))
    chooseTextRect = chooseText.get_rect()
    chooseTextRect.center = (width//2, 75)

    #https://www.fesliyanstudios.com/royalty-free-music/downloads-c/scary-horror-music/8
    background_Sound = mixer.Sound("ChooseMusic.mp3")

    
    screen = pygame.display.set_mode((width, height))
    background = pygame.image.load("Choose Character.jpg")
    topLeft = (0, 0)
    #Image from: https://www.pngwave.com/png-clip-art-vufqe
    doramiChoose = pygame.image.load("DoramiChoose.png")
    #Image from: https://www.clipartkey.com/view/bbimmw_crayon-shin-chan-png/
    shinChanChoose = pygame.image.load("ShinChanChoose.png")

    doramiCoord = (525, 315)
    shinChanCoord = (250, 375)
    shinChanWidth = 150
    shinChanHeight = 175
    doramiWidth = 125
    doramiHeight = 174

    choose = True

    while choose:
        background_Sound.play()
        screen.blit(background, topLeft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                instructionsDisplay = False
                pygame.quit() 
                os._exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                #check if the user clicked for shin chan
                mouseCoordX, mouseCoordY = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                if (mouseCoordX >= shinChanCoord[0] and mouseCoordX <= shinChanCoord[0] + shinChanWidth) and (mouseCoordY >= shinChanCoord[1] and mouseCoordY <= shinChanCoord[1] + shinChanHeight):
                    shinChanChosen = True
                    run = False
                    afterChoosingPlayer(widthScreen, heightScreen, shinChanIntroImg, doraemonIntroImg, soccerIntroImg, startPlaying2PlayerButton, startPlayingAIButton, screen, epsilon, clock, player, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg, xJumpImg, incrementJumpPlayer, incrementJumpGuestPlayer, startInstructions, leaderboardButton, background_Sound)
                #check if the user clicked for dorami
                elif ((mouseCoordX >= doramiCoord[0] and mouseCoordX <= doramiCoord[0] + doramiWidth) and (mouseCoordY >= doramiCoord[1] and mouseCoordY <= doramiCoord[1] + doramiHeight)):
                    doramiChosen = True
                    run = False
                    afterChoosingPlayer(widthScreen, heightScreen, shinChanIntroImg, doraemonIntroImg, soccerIntroImg, startPlaying2PlayerButton, startPlayingAIButton, screen, epsilon, clock, player, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg, xJumpImg, incrementJumpPlayer, incrementJumpGuestPlayer, startInstructions, leaderboardButton, background_Sound)
                    

        screen.blit(doramiChoose, doramiCoord)
        screen.blit(shinChanChoose, shinChanCoord)
        screen.blit(chooseText, chooseTextRect)
        pygame.display.flip()

#in this screen we will tell the user to pick single player to continue with the story of this mode!
def afterChoosingPlayer(widthScreen, heightScreen, shinChanIntroImg, doraemonIntroImg, soccerIntroImg, startPlaying2PlayerButton, startPlayingAIButton, screen, epsilon, clock, player, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg, xJumpImg, incrementJumpPlayer, incrementJumpGuestPlayer, startInstructions, leaderboardButton, background_Sound):
    global time
    global nobitaJail

    #Image made by Daniela Ruiz Gomez
    blood = pygame.image.load("Blood Resized.png")

    time = 0
    run = True
    #Image from : https://www.shutterstock.com/es/search/background+game+prison?image_type=illustration
    background = pygame.image.load("Choose Character.jpg")

    topLeft = (0, 0)
    width = 1024
    height = 640
    screen = pygame.display.set_mode((width, height))
    red = (255, 0, 0)
    white = (255, 255, 255)
    coral = (255,127,80)
    green = (0, 255, 0)
    circles = 0
    firstRun = True

    save = "Save Nobita..."
    saveText = font.render(save, True, blue)
    saveTextRect = saveText.get_rect()
    saveTextRect.center = (width//2, 30)

    save1 = "On Single Player Mode..."
    saveText1 = font.render(save1, True, blue)
    saveText1Rect = saveText1.get_rect()
    saveText1Rect.center = (width//2, 90)

    save2 = "...Maybe..."
    saveText2 = font.render(save2, True, green)
    saveText2Rect = saveText2.get_rect()
    saveText2Rect.center = (width//2, 190)

    save3 = "Press to continue"
    saveText3 = font.render(save3, True, red)
    saveText3Rect = saveText3.get_rect()
    saveText3Rect.center = (width//2, 230)

    while run:
        time += 1

        if firstRun:
            screen.blit(background, topLeft)
            screen.blit(nobitaJail, (250, 150))
            screen.blit(blood, topLeft)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit() 
                os._exit(0)
            #check if the user pressed to continue with the game
            if circles == 200 and event.type == pygame.MOUSEBUTTONDOWN:
                background_Sound.stop()
                run = False
                mainMenu(widthScreen, heightScreen, shinChanIntroImg, doraemonIntroImg, soccerIntroImg, startPlaying2PlayerButton, startPlayingAIButton, screen, epsilon, clock, player, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg, xJumpImg, incrementJumpPlayer, incrementJumpGuestPlayer, startInstructions, leaderboardButton)

        
        if circles != 200:
            pygame.time.wait(20)
            if time % 2 == 0:
                pygame.draw.circle(screen, red, (random.randint(10, 302), random.randint(200 , heightScreen - 20)), 20)
            else:
                pygame.draw.circle(screen, red, (random.randint(700, widthScreen - 20), random.randint(200 , heightScreen - 20)), 20)
            circles += 1

        if circles == 200:
            screen.blit(saveText1, saveText1Rect)
            screen.blit(saveText2, saveText2Rect)
            screen.blit(saveText3, saveText3Rect)


        screen.blit(saveText, saveTextRect)
        pygame.display.flip()
        firstRun = False

#this draws the screen where doraemon appears mad next to nobita
def doraemonMad():
    global piano

    width = 1024
    height = 640
    screen = pygame.display.set_mode((width, height))

    #From: https://chatsticker.com/sticker/doraemons-many-emotions/19964
    #Drawn by Daniela Ruiz Gomez
    doraemon = pygame.image.load("Mad Doraemon Resized2.png")

    #Image from : https://www.shutterstock.com/es/search/background+game+prison?image_type=illustration
    background = pygame.image.load("Choose Character.jpg")
    topLeft = (0,0)
    coral = (255,127,80)
    red = (255, 0, 0)
    blue = (102, 178, 255)
    run = True

    text1t = "Doraemon is fed up..."
    text1 = font.render(text1t, True, coral)
    text1Rect = text1.get_rect()
    text1Rect.center = (width//2, height//2 - 300)

    text2t = "He will try to end Nobita..."
    text2 = font.render(text2t, True, red)
    text2Rect = text2.get_rect()
    text2Rect.center = (width//2, height//2 - 250)

    text3t = "Press anywhere to continue"
    text3 = font.render(text3t, True, blue)
    text3Rect = text3.get_rect()
    text3Rect.center = (width//2, heightScreen//2 - 100)
    
    #jail from : https://www.tornado-studios.com/stock-3d-models/jail-cell-01
    #nobita crying from Doraemon series
    #image made by Daniela Ruiz Gomez
    nobita = pygame.image.load("Nobita Jail Resized.png")

    while run:
        screen.blit(background, topLeft)

        piano.play()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                os._exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                saveNobita(piano)

        
        screen.blit(doraemon, (widthScreen//2 + 100, 200))
        screen.blit(nobita, (175, 150))
        screen.blit(text1, text1Rect)
        screen.blit(text2, text2Rect)
        screen.blit(text3, text3Rect)
        pygame.display.flip()


#this screen is the save Nobita screen
def saveNobita(piano):
    global nobitaJail

    width = 1024
    height = 640

    #Image from : https://www.shutterstock.com/es/search/background+game+prison?image_type=illustration
    background = pygame.image.load("Choose Character.jpg")
    screen = pygame.display.set_mode((width, height))
    topLeft = (0,0)
    green = (0, 255, 0)
    red = (255, 0, 0)

    text3t = "Press anywhere to continue"
    text3 = font.render(text3t, True, red)
    text3Rect = text3.get_rect()
    text3Rect.center = (width//2, heightScreen - 5)

    text4t = "BEAT DORAEMON TO SAVE NOBITA!"
    text4 = font.render(text4t, True, green)
    text4Rect = text4.get_rect()
    text4Rect.center = (width//2 + 20, heightScreen//2 - 100)
    

    run = True

    while run:
        screen.blit(background, topLeft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                os._exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                createAILevels(heightScreen, widthScreen, screen, epsilon, clock, player, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg, goalWidth, xJumpImg,incrementJumpPlayer, incrementJumpGuestPlayer)

        screen.blit(text3, text3Rect)
        screen.blit(text4, text4Rect)
        screen.blit(nobitaJail, (250, 150))
        pygame.display.flip()

#this screen will be showing when the user wins
def winScreen():
    global player
    global guestPlayer

    guestPlayer.goalCount = 0
    player.goalCount = 0

    end_Sound = mixer.Sound("End Song.mp3")
    width = 1100
    height = 619
    green = (0, 255, 0)
    
    run = True
    screen = pygame.display.set_mode((width, height))

    #https://co.pinterest.com/pin/449515606542665350/
    doraemon = pygame.image.load("Doraemon Triste Resized.png")
    
    #https://favpng.com/png_search/doraemon-shizuka/3
    nobita = pygame.image.load("Nobita Happy Standing Resized.png")

    #https://www.pngflow.com/en/free-transparent-png-mztuj
    dorami = pygame.image.load("Dorami End Resized.png")
    
    #https://www.uihere.com/free-cliparts/shinnosuke-nohara-crayon-shin-chan-kasukabe-character-shinchan-4248406/download
    shinChan = pygame.image.load("ShinChan End.png")
    #https://downloads.khinsider.com/game-soundtracks/album/doraemon-snes
    background = pygame.image.load("Disco.jpg")

    text4t = "YOU WON!"
    text4 = font.render(text4t, True, green)
    text4Rect = text4.get_rect()
    text4Rect.center = (width//2 + 20, heightScreen//2 - 50 )

    colorRect = (0, 0, 0)
    colorText = (0, 255, 0)

    rectX, rectY = width//2 - 70, height//2 - 100
    rectWidth, rectHeight = 185, 75

    while run:

        end_Sound.play()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                end_Sound.stop()
                pygame.quit()
                os._exit(0)
            
            mouseCoordX, mouseCoordY = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

            if mouseCoordX >= rectX and mouseCoordX <= rectX + rectWidth and mouseCoordY >= rectY and mouseCoordY <+ rectY + rectHeight: 
                text4 = font.render(text4t, True, (0,0,0))
                colorRect = green
            else:
                text4 = font.render(text4t, True, green)
                colorRect = (0, 0, 0)

            #Press in the "YOU WON!" label to go back to the main menu
            if event.type == pygame.MOUSEBUTTONDOWN and (mouseCoordX >= rectX and mouseCoordX <= rectX + rectWidth and mouseCoordY >= rectY and mouseCoordY <+ rectY + rectHeight):
                run = False
                end_Sound.stop()
                text4 = font.render(text4t, True, green)
                colorRect = (0, 0, 0)
                mainMenu(widthScreen, heightScreen, shinChanIntroImg, doraemonIntroImg, soccerIntroImg, startPlaying2PlayerButton, startPlayingAIButton, screen, epsilon, clock, player, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg, xJumpImg, incrementJumpPlayer, incrementJumpGuestPlayer, startInstructions, leaderboardButton)


        screen.blit(background, (0,0))
        pygame.draw.rect(screen, colorRect, (rectX, rectY, rectWidth, rectHeight))
        screen.blit(text4, text4Rect)
        screen.blit(nobita, (width//2 - 50, height//2))
        screen.blit(dorami, (width//2 - 250, height//2))
        screen.blit(shinChan, (width//2  + 150, height//2))
        screen.blit(doraemon, (45, height - 540))
        pygame.display.flip()

#this will create the loser screen
def loserScreen():
    global player
    global guestPlayer

    guestPlayer.goalCount = 0
    player.goalCount = 0

    red = (255, 0, 0)
    balck = (0, 0, 0)
    run = True

    width = 801
    height = 800

    #Image from : https://www.vectorstock.com/royalty-free-vector/halloween-background-with-cemetery-in-full-moon-vector-22369104
    background = pygame.image.load("Cementery.jpg")
    scream = mixer.Sound("Scream.mp3")
    nobita = pygame.image.load("Nobita Help Resized.png")
    
    text4t = "NOBITA DIED!"
    text4 = font.render(text4t, True, red)
    text4Rect = text4.get_rect()
    text4Rect.center = (width//2, heightScreen//2 - 200)

    rectX, rectY = width//2 - 125, heightScreen//2 - 230
    rectWidth, rectHeight = 250, 60
    topLeft = (0, 0)

    colorRect = black
    screen = pygame.display.set_mode((width, height))

    scream.play()

    while run:
        screen.blit(background, topLeft)
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                run = False
                scream.stop()
                pygame.quit()
                os._exit(0)

            mouseCoordX, mouseCoordY = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

            if mouseCoordX >= rectX and mouseCoordX <= rectX + rectWidth and mouseCoordY >= rectY and mouseCoordY <+ rectY + rectHeight: 
                text4 = font.render(text4t, True, black)
                colorRect = red
            else:
                text4 = font.render(text4t, True, red)
                colorRect = black

            if event.type == pygame.MOUSEBUTTONDOWN and (mouseCoordX >= rectX and mouseCoordX <= rectX + rectWidth and mouseCoordY >= rectY and mouseCoordY <+ rectY + rectHeight):
                text4 = font.render(text4t, True, red)
                colorRect = black
                scream.stop()
                mainMenu(widthScreen, heightScreen, shinChanIntroImg, doraemonIntroImg, soccerIntroImg, startPlaying2PlayerButton, startPlayingAIButton, screen, epsilon, clock, player, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg, xJumpImg, incrementJumpPlayer, incrementJumpGuestPlayer, startInstructions, leaderboardButton)

        pygame.draw.rect(screen, colorRect, (rectX, rectY, rectWidth, rectHeight))
        screen.blit(text4, text4Rect)
        screen.blit(nobita, (width//2 - 400, height - 500))
        pygame.display.flip()

################################################
################################################
############  MAIN GAME LOOP AHEAD #############
################################################
################################################

compareScore = 0
timeWonGame = 0
runPygame = True
gameOver = False
startPlaying2PlayerButton = createStartPlaying2PlayerButton()
startPlayingAIButton = createButtonAI()
startInstructions = createInstructionsButton()
leaderboardButton = createLeaderboardButton()
easyButton = createEasyButton()
mediumButton = createMediumButton()

widthQuit, heightQuit, xQuit, yQuit, pressedQuit = (35, 35, widthScreen//2 - 85, heightScreen//2 + 137, False)
pauseButton = createPauseButton()
quitButton = PauseGame(widthQuit, heightQuit, xQuit, yQuit, pressedQuit)

widthPlay, heightPlay, xPlay, yPlay, pressedQuitPlay = (38, 38, widthScreen//2 , heightScreen//2 + 135, False)
playButton = PauseGame(widthPlay, heightPlay, xPlay, yPlay, pressedQuitPlay)
screen.blit(guestPlayerImg, (guestPlayer.x, guestPlayer.y))
widthRe, heightRe, xRe, yRe, pressedRestart = (38, 38, widthScreen//2 + 85, heightScreen//2 + 135, False)
restartButton = PauseGame(widthRe, heightRe, xRe, yRe, pressedRestart)

AIlevel = None
pauseGame = False

shinChanChosen = False
doramiChosen = False

#https://www.thedarkpiano.com/creepy-piano-music
piano = mixer.Sound("Piano.mp3")

while runPygame:
    #fillleaderboard before starting to play
    fillLeaderboard()
    choosePlayer(widthScreen, heightScreen, shinChanIntroImg, doraemonIntroImg, soccerIntroImg, startPlaying2PlayerButton, startPlayingAIButton, screen, epsilon, clock, player, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg, xJumpImg, incrementJumpPlayer, incrementJumpGuestPlayer, startInstructions, leaderboardButton)
    mainMenu(widthScreen, heightScreen, shinChanIntroImg, doraemonIntroImg, soccerIntroImg, startPlaying2PlayerButton, startPlayingAIButton, screen, epsilon, clock, player, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg, xJumpImg,incrementJumpPlayer, incrementJumpGuestPlayer, startInstructions, leaderboardButton)
