#####################################################################################
# 15-112:Fundamentals of Programming and Computer Science
# Carnegie Mellon University
# Final Project: ShinDor Soccer
# By: Alejandro Ruiz
#####################################################################################
#NOT YET FINISHED

import pygame
import os
import math
import time
from pygame import mixer

pygame.init()

#creates the screen, where 800 is width and 600 is the height
widthScreen = 1100    #800
heightScreen = 600  #600
clock = pygame.time.Clock()
screen = pygame.display.set_mode((widthScreen, heightScreen))
screen.blit(pygame.image.load("Day Background.png"), (0,0))

#Tile and Icon of the window
pygame.display.set_caption("ShinDor Soccer")

#declare variables

##Soccer gotten from: http://www.pngmart.com/image/592
soccerImg = pygame.image.load("Soccer.png")
soccerMask = pygame.mask.from_surface(soccerImg)
#Doraemon gotten from: https://www.pngfind.com/mpng/hJohToh_free-download-doraemon-png-clipart-doraemon-doraemon-transparent/
guestPlayerImg = pygame.image.load("Doraemon Left.png")
guestPlayerMask = pygame.mask.from_surface(guestPlayerImg)
#Shin Chan gotten from: https://www.seekpng.com/ipng/u2q8u2a9r5t4q8q8_shin-chan-shin-chan/
playerImg = pygame.image.load("Shin Chan Right.png")
playerMask = pygame.mask.from_surface(playerImg)
#Goal Image gotten from: https://www.seekpng.com/idown/u2q8e6y3t4w7y3r5_soccer-goal-sprite-006-soccer-goal-sprite-sheet/
goalLeftImg = pygame.image.load("Goal Left.png")
goalRightImg = pygame.image.load("Goal Right.png")
goalHeight = 250
goalWidth = 127


#Doraemon intro png gotten from: http://pluspng.com/png-83346.html
doraemonIntroImg = pygame.image.load("Doraemon Intro.png")

#Shin Chan intro png gotten from:https://www.uihere.com/free-cliparts/crayon-shin-chan-comedy-film-anime-youtube-crayon-1565529
shinChanIntroImg = pygame.image.load("Shin Chan Intro.png")

#Soccer Intro png gotten from: https://clipartpng.com/?855,soccer-ball-png-clipart
soccerIntroImg = pygame.image.load("Soccer Intro.png")

#############################
#create classes for ball, players and buttons
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

    def displayButton(self, screen):
        textButton = self.font.render(self.text, True, self.color1)
        buttonRectangle = textButton.get_rect()
        buttonRectangle.center = (self.xCenter, self.yCenter)
        pygame.draw.rect(screen, self.colorButton, (self.x, self.y, self.width, self.height))
        screen.blit(textButton, buttonRectangle)

    def pressedButton(self):
        for event in pygame.event.get():

            if(event.type == pygame.MOUSEBUTTONDOWN):
                mouseCoordX, mouseCoordY = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

                #now check that the mouseCoordX and mouseCoordY are in the range of the rectangle we drew
                if ((mouseCoordX >= self.x and mouseCoordX <= self.x + self.width) and 
                (mouseCoordY >= self.y and mouseCoordY <= self.y + self.height)):
                    self.pressed = True
                #check if the mouse coordinates are inside the button range. If it is the button has been pressed

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
        #check if the ball is going more downwards than the "floor" of the screen
        if self.y + self.height >= heightScreen and self.BDY > 0:
            self.BDY *= -1
            self.BDY += self.airResistance
            self.y = heightScreen - self.width
            if self.BDX > 0:
                self.BDX -= self.friction
            elif self.BDX < 0:
                self.BDX += self.friction
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
        if (self.y >= 0 and 
        (self.y + self.height <= heightScreen - goalHeight + 20) and 
        ( (self.x <= goalWidth) or
        (self.x + self.width >= widthScreen - goalWidth))):
            self.BDX *= -1
            if self.BDX < 0:
                self.x -= 5
            else:
                self.x += 5

    def checkFor1stPlayerGoal(self, player, widthScreen, heightScreen, goalWidth, goalHeight, guestPlayer):
        ###########################
        #Check for goal in the left
        ###########################

        #I am just going to add the 5 to account for the post
        if ((self.x < goalWidth - self.width) and (self.y + self.height > heightScreen - goalHeight + 30)):
            self.x = 0
            player.scoredGoal = True
            self.BDX = 0
            self.BDY = 0
            self.y = heightScreen//2 - 20
            self.x = widthScreen//2
            player.goalCount += 1
            player.x = widthScreen - playerWidth - goalWidth - 5
            guestPlayer.x = goalWidth + 5
            goal_Sound = mixer.Sound("Goal Audio.mp3")
            goal_Sound.play()

    
    def checkForGuestPlayerGoal(self, guestPlayer, widthScreen, heightScreen, goalWidth, goalHeight, player):
        ############################
        #Check for goal in the right
        ############################
        if self.x + self.width > (widthScreen - goalWidth + 1.5*self.width) and self.y + self.height > (heightScreen - goalHeight + 30):
            self.x = widthScreen - self.width
            guestPlayer.scoredGoal = True
            self.BDX = 0
            self.BDY = 0
            self.y = heightScreen//2 - 20
            self.x = widthScreen//2
            guestPlayer.goalCount += 1
            guestPlayer.x = goalWidth + 5
            player.x = widthScreen - playerWidth - goalWidth - 5
            goal_Sound = mixer.Sound("Goal Audio.mp3")
            goal_Sound.play()
    
    
    def checkForBallCollisionsAndGravity(self, heightScreen, widthScreen, epsilon):

        self.applyGravity()
        self.applyXMovement()
        self.checkForCollisionWithGround(heightScreen)
        self.checkForAllowedXDirectionBall(widthScreen)

class SoccerPlayer(object):

    def __init__(self, width, height, x, y, BDY, jumping, jumpHeight, scoredGoal, goalCount):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.BDY = BDY
        self.jumping = jumping
        self.jumpHeight = jumpHeight
        self.scoredGoal = scoredGoal
        self.goalCount = goalCount
    
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

        elif self.jumpHeight >= -jumpHeight and self.jumpHeight <= 0:
            self.y += 1/2 * (self.jumpHeight ** 2)
            self.jumpHeight -= 1
            self.checkPlayerHittingBall(soccer, heightScreen, widthScreen)
            self.checkBallHitsMiddleHead(soccer, epsilon)

        #if ourJumpHeight surpasses negative 10 we have reached ground and hence we stop jumping
        elif self.jumpHeight < -jumpHeight:
            self.jumpHeight = jumpHeight
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
            soccer.x = self.x - 5
            soccer.BDY = 10*math.sin(70)
            soccer.BDX = -10*math.cos(70)
            collided = True

        #Im going to make it so if the player is jumping and the ball is hit by the player the ball goes upwards

        #checking if it collides in the left
        if( (self.jumping) and (soccer.y + soccer.height <= self.y + self.height) and
        (soccer.y >= self.y) and (soccer.x > self.x) and (soccer.x <= self.x + 5)):
            soccer.BDY = 10*math.sin(-70)
            soccer.BDX = -10*math.cos(70)
            collided = True
        #if it collides in the right 
        elif ((self.jumping) and (soccer.y + soccer.height <= self.y + self.width - 5) and
        (soccer.y >= self.y) and (soccer.x + soccer.width <= self.x + self.width) and 
        (soccer.x + soccer.width >= self.x + self.width +5)): 
            soccer.BDY  = 10*math.sin(-70)
            soccer.BDX = 10*math.cos(70)
            collided = True
        #This checks if the ball was hit with the upper half of the body
        if ((soccer.y >= self.y) and 
        (soccer.y <= self.y + self.height/2) and 
        (soccer.x + soccer.width >= self.x + 20) and 
        (soccer.x + soccer.width < self.x + self.width/2)):
            #if the player is jumping
            if self.jumping:
                soccer.BDY = 9*math.sin(-70)
                soccer.BDX = -12*math.cos(70)
        
            elif soccer.BDY <0: #meaning the ball is moving upwards
                soccer.BDY = 8*math.sin(-70)
                soccer.BDX = -8*math.cos(70)
                soccer.x -= 10

            elif soccer.BDY > 0:  #if the ball is moving downwards
                soccer.BDX *= -1
                soccer.BDX -= 1
                soccer.BDY = 5
                soccer.x -= 5

            collided = True

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

        #check if the ball hits the right side of the player
        #first check for the upper half (head)

        if ((soccer.y >= self.y) and 
        (soccer.y <= self.y + self.height/2) and 
        (soccer.x >= self.x + self.width/2) and 
        (soccer.x <= self.x + self.width - 20)):
            #if the player is jumping then we apply the sin and cos as if a force was applied creating a physics-parabola effect
            if self.jumping:
                soccer.BDY = -12*math.sin(70)
                soccer.BDX = 12*math.cos(70)

            elif soccer.BDY < 0:            #this means the soccer is moving upwards
                soccer.BDY = -10*math.sin(70)
                soccer.BDX = 8*math.cos(70)
                soccer.x += 10

            elif soccer.BDY > 0 and soccer.y <= self.y + self.width/2:            #this checks if the ball is moving downwards
                soccer.BDX *= -1
                soccer.BDX += 2
                soccer.x += 10

            collided = True

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

        return collided
    def checkBallHitsMiddleHead(self, soccer, epsilon):
        #if the ball hits the player directly in the middle (so like directly in head)
        if (
        ((abs(soccer.y + soccer.height - self.y + 6)) <= epsilon) and (soccer.x >= self.x) and
        (soccer.x + soccer.width <= self.x + self.width - 3)) and soccer.BDY > 0:
            soccer.BDY *= -1
            return True
        return False

    ########################################################################
    #CURRENTLY NOT WORKING##################################################
    ########################################################################
    def checkBallNotMoving(self, otherPlayer, soccer, epsilon, heightScreen):
        if ((abs(soccer.BDY) < 2) and (abs(self.x - (soccer.x + soccer.width)) <= 5) and (abs(soccer.x  - (otherPlayer.x + otherPlayer.width)) <= 5) and 
        (abs(self.y + self.height - heightScreen) <= epsilon) and (abs(otherPlayer.y + otherPlayer.height - heightScreen) <= epsilon)):
            soccer.BDY = -3
            soccer.y = heightScreen//2

#We will make the collisions a little bit different for Doraemon since he has a wider head and different body than Shin Chan
class DoraemonPlayer(SoccerPlayer):
    #we can call the init function from our soccerPlayer class since it will take the same values
    def __init__(self, width, height, x, y, BDY, jumping, jumpHeight, scoredGoal, goalCount):
        super().__init__(width, height, x, y, BDY, jumping, jumpHeight, scoredGoal, goalCount)

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

        #checks if it is inside the player's body and if it is to the left of it
        elif (not self.checkBallHitsMiddleHead(soccer, epsilon) and 
        (soccer.y >= self.y) and 
        (soccer.y + soccer.width  <= self.y + self.width) and 
        (soccer.x > self.x + 2)  and
        (soccer.x + soccer.width < self.x + self.width) and 
        (abs(soccer.x - self.x)) < abs(soccer.x + soccer.width - self.x - self.width)):
            soccer.x = self.x - 10
            soccer.BDY = 9.5*math.sin(70)
            soccer.BDX = -7*math.cos(70)
            collided = True
        #Im going to make it so if the player is jumping and the ball is hit by the player the ball goes upwards

        #checking if it collides in the left
        if( (self.jumping) and (soccer.y + soccer.height <= self.y + self.height) and
        (soccer.y >= self.y) and (soccer.x > self.x) and (soccer.x <= self.x + 5)):
            soccer.BDY = 11*math.sin(-70)
            soccer.BDX = -9*math.cos(70)
            collided = True
        #if it collides in the right 
        elif ((self.jumping) and (soccer.y + soccer.height <= self.y + self.width - 5) and
        (soccer.y >= self.y) and (soccer.x + soccer.width <= self.x + self.width - 3) and
        (soccer.x + soccer.width >= self.x + self.width + 5)): 
            soccer.BDY  = 10*math.sin(-70)
            soccer.BDX = 8*math.cos(70)
            collided = True
        #This checks if the ball was hit with the upper half of the body and
        if ((soccer.y >= self.y - 3) and 
        (soccer.y <= self.y + self.height/2) and 
        (soccer.x + soccer.width >= self.x ) and 
        (soccer.x + soccer.width <= self.x + self.width/2)):
            #if the player is jumping
            if self.jumping:
                soccer.BDY = 11*math.sin(-70)
                soccer.BDX = -9*math.cos(70)

            elif soccer.BDY <0: #meaning the ball is moving upwards
                soccer.BDY = 11*math.sin(-70)
                soccer.BDX = -9*math.cos(70)
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
                
                soccer.x = self.x - 30
                soccer.applyGravity()

            collided = True
    

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
                soccer.x = self.x - 20
                
            else:
                soccer.BDX *= -1
            
            soccer.x = self.x - 10
            collided = True

        #check if the ball hits the right side of the player
        #first check for the upper half (head)

        if ((soccer.y >= self.y - 3) and 
        (soccer.y <= self.y + self.height/2) and 
        (soccer.x >= self.x + self.width/2) and 
        (soccer.x <= self.x + self.width - 5)):
            #if the player is jumping then we apply the sin and cos as if a force was applied creating a physics-parabola effect
            if self.jumping:
                soccer.BDY = -11*math.sin(70)
                soccer.BDX = 9*math.cos(70)

            elif soccer.BDY < 0:            #this means the soccer is moving upwards
                soccer.BDY = -11*math.sin(70)
                soccer.BDX = 9*math.cos(70)
                soccer.x += 10
                
            elif soccer.BDY > 0 and soccer.y <= self.y + self.width/2:            #this checks if the ball is moving downwards
                soccer.BDX *= -1
                soccer.BDX += 2
                soccer.x += 10

            collided = True
            
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

        return collided


    def checkBallHitsMiddleHead(self, soccer, epsilon):
        #if the ball hits the player directly in the middle (so like directly in head)
        #doraemon has a bigger head so we need to change this
        if (
        ((soccer.y + soccer.height >= self.y - 5) and (soccer.x >= self.x) and
        (soccer.x + soccer.width <= self.x + self.width - 3)) and soccer.BDY > 0):
            soccer.BDY *= -1
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
playerX = widthScreen - playerWidth - goalWidth - 5   #playerX = 800 - 81 = 719 (rightMostPoint)
playerY = heightScreen - playerHeight
guestPlayerX = goalWidth + 5
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
scoredGoal = False
goalCount = 0
green = (0, 255, 0)
blue = (0, 0, 128)
font = pygame.font.Font('freesansbold.ttf', 32)
textGoal = font.render('GOOOOOOOOOOOOOAAAAAL', True, green, blue)
textGoalRectangle = textGoal.get_rect()
pressedButton = False
###################################
#let's create three objects, our player, the other player and the soccer ball
#####################################################
soccer = Ball(soccerX, soccerY, soccerWidth, soccerHeight, soccerBDX, soccerBDY, friction, soccerGravity, airResistance)
player = SoccerPlayer(playerWidth, playerHeight, playerX, playerY, playerBDY, jumping, jumpHeight, scoredGoal, goalCount)
guestPlayer = DoraemonPlayer(playerWidth, playerHeight, guestPlayerX, guestPlayerY, playerBDY, jumping, jumpHeight, scoredGoal, goalCount)


#############################################################################
#THIS FUNCTION COMBINES A LOT OF THE FUNCTIONS ABOVE TO CHECK FOR A COLLISION AND FOR OUT OF BOUNDS
############################################################################
def checkForCollisionsAndOutOfBoundsAndGoal(heightScreen, widthScreen, epsilon, textGoal, textGoalRectangle, screen):
    #at the beginning of the loop make sure to reset the goal varibale if there has previously been a goal scored
    if player.scoredGoal == True:
        player.scoredGoal = False
        screen.blit(textGoal, textGoalRectangle)

    soccer.applyXMovement()

    soccer.applyGravity()

    soccer.checkForCollisionWithGround(heightScreen)

    soccer.checkForAllowedXDirectionBall(widthScreen)

    player.checkPlayerHittingBall(soccer, widthScreen, heightScreen)
    guestPlayer.checkPlayerHittingBall(soccer, widthScreen, heightScreen)

    player.checkBallHitsMiddleHead(soccer, epsilon)
    guestPlayer.checkBallHitsMiddleHead(soccer, epsilon)

    soccer.checkForCollisionPostofGoal(goalHeight, goalWidth, widthScreen, heightScreen)

    soccer.checkFor1stPlayerGoal(player, widthScreen, heightScreen, goalWidth, goalHeight, guestPlayer)
    soccer.checkForGuestPlayerGoal(guestPlayer, widthScreen, heightScreen, goalWidth, goalHeight, player)
    
    player.checkBallNotMoving(guestPlayer, soccer, epsilon, heightScreen)

#############################################
#first let us define the button to play the game
#############################################
def createStartPlaying2PlayerButton():
    #properties of the button
    xstartButton = 295
    ystartButton = 498
    widthstartButton = 160
    heightstartButton = 55
    xCenterTextButton = 375
    yCenterTextButton = 525
    green = (0, 255, 0)
    buttonColor = (0, 0, 128)
    textPlayingButton = "2 Player"
    fontButton = pygame.font.Font('freesansbold.ttf', 28)
    pressed = False
    #create the button and return it
    startPlaying2PlayerButton = Button(xstartButton, ystartButton, widthstartButton, heightstartButton, fontButton, green, buttonColor, textPlayingButton, xCenterTextButton, yCenterTextButton, pressed)
    return startPlaying2PlayerButton

#################################################
#create the button to start playing against the AI
##################################################

def createButtonAI():
    #properties of the button
    xButton = 660
    yButton = 498
    widthButton = 180
    heightButton = 55
    xCenterTextButton = 750
    yCenterTextButton = 528
    green = (0, 255, 0)
    buttonColor = (0, 0, 128)
    textPlayingButton = "Single Player"
    fontButton = pygame.font.Font('freesansbold.ttf', 25)
    pressed = False
    #create the button and return it
    startPlayingAIButton = Button(xButton, yButton, widthButton, heightButton, fontButton, green, buttonColor, textPlayingButton, xCenterTextButton, yCenterTextButton, pressed)
    return startPlayingAIButton

##############################################
#This function displays the first screen######
##############################################
def firstScreen(widthScreen, heightScreen, shinChanIntroImg, doraemonIntroImg, soccerIntroImg, startPlaying2PlayerButton, startPlayingAIButton, screen, epsilon, clock, player, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg):
    introScreen = pygame.display.set_mode((widthScreen, heightScreen))
    firstDisplay = True
    introBackgroundImg = pygame.image.load("Intro Background.jpg")
    textIntro = font.render('Welcome to Shin-Dor Soccer', True, green, blue)
    textIntroRectangle = textIntro.get_rect()
    textIntroRectangle.center = (widthScreen//2, heightScreen//2)
    mixer.music.load("Intro Audio.mp3")
    mixer.music.play(-1)
    #Initial Screen Loop
    while firstDisplay:

        startPlaying2PlayerButton.pressedButton()
        startPlayingAIButton.pressedButton()

        if startPlaying2PlayerButton.pressed:
            mixer.music.pause()
            firstDisplay = False
            #if the button is pressed we are done with the first display
        
        elif startPlayingAIButton.pressed:
            mixer.music.pause()
            firstDisplay = False
            createScreenSinglePlayer(heightScreen, widthScreen, screen, epsilon, clock, player, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg, goalWidth)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                firstDisplay = False
                pygame.quit() 
                os._exit(0)
        ################################
        #display of intro screen########
        ################################

        introScreen = pygame.display.set_mode((widthScreen, heightScreen))
        introScreen.blit((introBackgroundImg), (0,0))
        introScreen.blit(shinChanIntroImg, (17, 125))
        introScreen.blit(doraemonIntroImg, (725, 100))
        introScreen.blit(soccerIntroImg, (450, 20))
        introScreen.blit(textIntro, textIntroRectangle)
        startPlaying2PlayerButton.displayButton(introScreen)
        startPlayingAIButton.displayButton(introScreen)
        pygame.display.flip()

###################################################################
############ CODE AI PROJECT STARTS HERE ##########################
###################################################################
#basic intelligence will only move based on the soccer position
def applyBasicIntelligence(cpu, soccer, widthScreen, goalWidth):
    #first the AI should go towards the soccer
    epsilon = 10**-2
    #make sure the AI does not go out of bounds
    if cpu.x <= goalWidth//2:
        cpu.x = goalWidth//2
    #make sure the AI does not go outside of the right allowed bound
    if cpu.x + cpu.width >= widthScreen - goalWidth//2:
        cpu.x = widthScreen - cpu.width - goalWidth//2

    #to defend better the goal line
    if soccer.x <= widthScreen//2 - goalWidth and soccer.BDX < 0 and cpu.x >= goalWidth - cpu.width:
        cpu.x -= 5
        if cpu.x < goalWidth - cpu.width:
            cpu.x = goalWidth - cpu.width
        if abs(soccer.y - cpu.y) <= 6 and abs(soccer.x - cpu.x + cpu.width) <= soccer.width and soccer.BDY > 0:
            print("Im jumping \n")
            cpu.jump(soccer)

    #if the  ball is close to the CPU make it move forward
    if abs(soccer.x - cpu.x + cpu.width) <= 10:
        cpu.x += 5
    
    #if the ball is right above the CPU make it jump
    if (soccer.x - (cpu.x + cpu.width) < 0 and soccer.x - (cpu.x + cpu.width) > -81) and abs(cpu.y - (soccer.y + soccer.height)) < 10:
        cpu.jump(soccer)
    
    if (soccer.x <= goalWidth + cpu.width + 30 and soccer.BDY > 0):
        cpu.jump(soccer)
    if abs(cpu.x + cpu.width - soccer.x) <= 20 and abs(soccer.y + soccer.height - cpu.y) <= 25 and soccer.BDY > 0:
        cpu.jump(soccer)
        cpu.x += 5

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
        #print(f'Moved forward \n')
    
    #check if the cpu needs to jump to hit the ball
    if ((soccer.y  + soccer.height < cpu.y) and (soccer.x - (cpu.x + cpu.width) < 5) and (soccer.x > cpu.x + cpu.width) or (cpu.jumping)):
        if cpu.x + cpu.width < soccer.x:
            cpu.x += 2

        if cpu.jumpHeight + cpu.y <= soccer.y + soccer.height or cpu.jumping and soccer.y + soccer.width <= cpu.y:
            cpu.jump(soccer)
            cpu.x += 2
    
#Create the screen that will be popped if we select "Single Player"
def createScreenSinglePlayer(heightScreen, widthScreen, screen, epsilon, clock, player, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg, goalWidth):
    singlePlayerScreen = True

    while singlePlayerScreen:

        applyBasicIntelligence(guestPlayer, soccer, widthScreen, goalWidth)

        checkForCollisionsAndOutOfBoundsAndGoal(heightScreen, widthScreen, epsilon, textGoal, textGoalRectangle, screen)

        clock.tick(1000)

        keyPressed = pygame.key.get_pressed()
        #this makes sure the player can move continously so that we do not have to press the key multiple times
        if keyPressed[pygame.K_RIGHT] and player.x + player.width <= widthScreen - goalWidth + player.width:   #the purpose of the and is to ensure the player does not go outside of the right bound
            player.x += 6      
            player.rectangleX = player.x
    
    
        if keyPressed[pygame.K_LEFT] and player.x >= goalWidth - player.width + 20:         #the purpose of the and is to ensure the player does not go outside of the left bound
            player.x -= 6                       #0.15
            player.rectangleX = player.x
        
        if not player.jumping and keyPressed[pygame.K_UP]:    #by putting this statement we ensure the player cannot jump while it is alredy jumping
            player.jumping = True
            applyBasicIntelligence(guestPlayer, soccer, widthScreen, goalWidth)
        
        if player.jumping:
            player.jump(soccer)
            #make sure we check for all our collisions and goals, etc
        

        #make sure the user can exit out of the game by pressing the top left exit button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                singlePlayerScreen = False
                pygame.quit()  	# ensures pygame module closes properly
                os._exit(0)	    # ensure the window closes
        

        #proceed to load the screen 
        screen.blit(pygame.image.load("Day Background.png"), (0,0))
        black = (0,0,0)
        green = (0, 255, 0)
        #rectangle for debugging purposes
        #rectangle of player1 and ellipse
        pygame.draw.rect(screen, black,(player.x + 18, player.y + 25, player.width - 38, player.height  - 28),5)
        pygame.draw.ellipse(screen, green, (player.x + 7, player.y + 5, player.width - 16, player.height - 55), 4)

        #rectangle of guestPlayer and ellipse
        pygame.draw.rect(screen, black, (guestPlayer.x + 6, guestPlayer.y + 50, guestPlayer.width - 23, guestPlayer.height - 47), 5)
        pygame.draw.ellipse(screen, green, (guestPlayer.x - 5, guestPlayer.y - 5, guestPlayer.width + 2 , guestPlayer.height - 35), 4)
        ######################################

        ##############################################
        #The following lines update the current position of the objects
        ##############################################
        screen.blit(soccerImg, (soccer.x, soccer.y))
        screen.blit(playerImg, (player.x, player.y))
        screen.blit(guestPlayerImg, (guestPlayer.x, guestPlayer.y))
        screen.blit(goalLeftImg, (0, heightScreen - goalHeight))
        screen.blit(goalRightImg, (widthScreen - goalWidth, heightScreen - goalHeight))
        createGoalCount(player, guestPlayer, screen, widthScreen)
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


###################################################
###################################################
############## MAIN GAME LOOP #####################
###################################################
###################################################

runPygame = True
firstRun = True

while runPygame:

    #createScreenSinglePlayer(heightScreen, widthScreen, screen, epsilon, clock, player, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg, goalWidth)
    
    if firstRun:
        startPlaying2PlayerButton = createStartPlaying2PlayerButton()
        startPlayingAIButton = createButtonAI()

    # initial screen
    if not startPlaying2PlayerButton.pressed and not startPlayingAIButton.pressed:
        firstScreen(widthScreen, heightScreen, shinChanIntroImg, doraemonIntroImg, soccerIntroImg, startPlaying2PlayerButton, startPlayingAIButton, screen, epsilon, clock, player, guestPlayer, soccer, soccerImg, playerImg, guestPlayerImg, goalLeftImg, goalRightImg)


    clock.tick(10000)

    keyPressed = pygame.key.get_pressed() #gets the key that it is being pressed

    #this makes sure the player can move continously so that we do not have to press the key multiple times

    if keyPressed[pygame.K_RIGHT] and player.x + player.width <= widthScreen - goalWidth + player.width:   #the purpose of the and is to ensure the player does not go outside of the right bound
        player.x += 6                  #0.15
        player.rectangleX = player.x
    
    
    if keyPressed[pygame.K_LEFT] and player.x >= goalWidth - player.width + 20:         #the purpose of the and is to ensure the player does not go outside of the left bound
        player.x -= 6                       #0.15
        player.rectangleX = player.x
    
    if not player.jumping and keyPressed[pygame.K_UP]:    #by putting this statement we ensure the player cannot jump while it is alredy jumping
        player.jumping = True
    
    if player.jumping:
        player.jump(soccer)

    #To move the guest player... 

    if keyPressed[pygame.K_s] and guestPlayer.x + guestPlayer.width <= widthScreen - goalWidth + guestPlayer.width:   #the purpose of the and is to ensure the player does not go outside of the right bound
        guestPlayer.x += 8
    
    if keyPressed[pygame.K_a] and guestPlayer.x >= goalWidth - guestPlayer.width + 20:          #the purpose of this and is to ensure the player does not go outside of the left bound                                 
        guestPlayer.x -= 8
    
    if not guestPlayer.jumping and keyPressed[pygame.K_SPACE]: 
        guestPlayer.jumping = True
    
    if guestPlayer.jumping:
        guestPlayer.jump(soccer)
    

    checkForCollisionsAndOutOfBoundsAndGoal(heightScreen, widthScreen, epsilon, textGoal, textGoalRectangle, screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runPygame = False
            pygame.quit()  	# ensures pygame module closes properly
            os._exit(0)	    # ensure the window closes
            
    #sets the background color of the display
    screen.blit(pygame.image.load("Day Background.png"), (0,0))
    #######################################
    black = (0,0,0)
    green = (0, 255, 0)
    #rectangle for debugging purposes
    #rectangle of player1 and ellipse
    pygame.draw.rect(screen, black,(player.x + 18, player.y + 25, player.width - 38, player.height  - 28),5)
    pygame.draw.ellipse(screen, green, (player.x + 7, player.y + 5, player.width - 16, player.height - 55), 4)

    #rectangle of guestPlayer and ellipse
    pygame.draw.rect(screen, black, (guestPlayer.x + 6, guestPlayer.y + 50, guestPlayer.width - 23, guestPlayer.height - 47), 5)
    pygame.draw.ellipse(screen, green, (guestPlayer.x - 5, guestPlayer.y - 5, guestPlayer.width + 2 , guestPlayer.height - 35), 4)
    ######################################

    ##############################################
    #The following lines update the current position of the objects
    ##############################################
    screen.blit(soccerImg, (soccer.x, soccer.y))
    screen.blit(playerImg, (player.x, player.y))
    screen.blit(guestPlayerImg, (guestPlayer.x, guestPlayer.y))
    screen.blit(goalLeftImg, (0, heightScreen - goalHeight))
    screen.blit(goalRightImg, (widthScreen - goalWidth, heightScreen - goalHeight))
    createGoalCount(player, guestPlayer, screen, widthScreen)
    pygame.display.flip()

    firstRun = False
