## Author: Boris Chan
## Date: 08/12/2016
## Purpose: using pygame to create the first runnable game

import os
import pygame
import math
import random

## initial pygame module
pygame.init()

## colour
blue = (123, 169, 242)
green = (35, 119, 0)
red = (255, 0, 0)
black = (0, 0, 0)

## Surface - Game display
os.environ['SDL_VIDEO_WINDOW_POS'] = "200,75"
resolution = (800, 400)
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption('Obstacle Runner')

## Game Background
ground_y = 350
sky = (0, 0, 800, ground_y)
ground = (0, ground_y, 800, 50)
pygame.draw.rect(screen, blue, sky)
pygame.draw.rect(screen, green, ground)

## Player info
block_size = 20
player_init = (100, 330, block_size, block_size)
pygame.draw.rect(screen, red, player_init)

## load grphaics
pygame.display.update()

## Time setting
clock = pygame.time.Clock()
fps = 40

gravity = -0.5

class player(object):
    def __init__(self):
        self.x = 100
        self.y = 330
        self.velocity = 0
        self.isJump = True
        self.isDoubleJump = True
    
    def moveAndDraw(self):
        pygame.draw.rect(screen, blue, (self.x, self.y, block_size, block_size))
        self.velocity += gravity
        if self.y - self.velocity > ground_y - block_size:
            self.y = ground_y - block_size
        else:
            self.y -= self.velocity
        pygame.draw.rect(screen, red, (self.x, self.y, block_size, block_size))

    def jump(self):        
        if self.isJump:
           self.velocity = 10
           self.isJump = False
        elif self.isDoubleJump:
            self.velocity = 10
            self.isDoubleJump = False       
            
class obstacle(object):
    global speed 
    speed = 5
    def __init__(self):
        self.width = 30
        self.height = 60
        self.x = resolution[0] 
        self.y = ground_y - self.height        
    
    def moveAndDraw(self):        
        if self.x + self.width < 0:
            self.x = resolution[0]
            self.height = random.randint(30, 160)
            self.width = random.randint(30, (-self.height + 200))  
            self.y = ground_y - self.height
        pygame.draw.rect(screen, blue, (self.x, self.y, self.width, self.height))
        self.x -= speed        
        pygame.draw.rect(screen, black, (self.x, self.y, self.width, self.height))
    
class objectCollision():
    ## if the block touch the ground
    def isGrounded(self, P1):
        if P1.y + block_size == ground_y:
            P1.isJump = True
            P1.isDoubleJump = True
    
    ## if the block touch the barrier
    def isHit(self, P1, O1):
        if P1.x + block_size == O1.x and P1.y + block_size >= O1.y:
            return True        
        if P1.y + block_size >= O1.y and P1.x + block_size >= O1.x and P1.x <= O1.x + O1.width:
            return True    

def gameLoop():    
    ## Time setting
    gameOver = False
    gamePause = True  
    gameLost = False
    
    P1 = player()
    O1 = obstacle()
    collision = objectCollision()

    while not gameOver:
        ## Game Lose
        while gameLost:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        ## reset piece                        
                        P1.y = ground_y - block_size
                        O1.x = resolution[0]
                        ## load new graphics
                        pygame.draw.rect(screen, blue, sky)
                        pygame.draw.rect(screen, red, player_init)
                        pygame.display.update()

                        gameLost = False
        
        ## Game Pause
        while gamePause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = True
                    gamePause = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gameOver = True
                        gamePause = False
                    if event.key == pygame.K_SPACE:
                        gamePause = False
                    if event.key == pygame.K_p:
                        gamePause = False
                    
        ## Event handle
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    P1.jump()                              
                if event.key == pygame.K_p:
                    gamePause = True

        ## Move Player
        P1.moveAndDraw()
        O1.moveAndDraw()

        ## Object Collision
        collision.isGrounded(P1)
        collide = collision.isHit(P1, O1)
        if collide:
            gameLost = True  
            
        ## Update Frame
        pygame.display.update()
        clock.tick(fps)       
          

    pygame.quit()

gameLoop()
