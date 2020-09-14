#Name: Snake Game
#Descripton: A classic snake game, eating the blocks and getting longer as it goes
#Author: Vo Trung Son
#Date 15/04/2019

import random
import tkinter as tk
import pygame
import sys
from tkinter import messagebox
pygame.init()

#Each block of the snake
class cube(object):
    """
    Class with instructions for the cubes that make up the snake """
    rows = 25
    w = 625
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
        """
        Set the initial state of the cubes that make up the snake """
        self.pos = start
        self.dirnx = 1              #Directions are already set so the cubes can start moving as soon as the game starts
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        """
        Set the direction for the cubes that make up the snake to move using """
        self.dirnx = dirnx          #Give the cubes the direction of the head of the snake
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)     #Move the position of the snake to that of the direction that the snake is moving in

    def draw(self, surface, eyes=False):
        """
        Function to draw the cubes that make up the snake """
        dis = self.w // self.rows       #distance between the cubes
        i = self.pos[0]                 #i stands for the x position
        j = self.pos[1]                 #j stands for the y position, so that we don't need to type self.pos[] again

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))  #Make sure that the cubes stay inside the squares of the grid, and that it doesn't overlap-
                                                                                 #the white lines of the grid. Also, this command draws the cubes
        if eyes:            
            centre = dis // 2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)                        #Bunch of codes just to draw the 2 eyes of the snake
            circleMiddle2 = (i*dis+dis-radius*2,j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle,radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
            

#The entire snake 
class snake(object):
    """
    Class with instructions for the entire snake """
    body = []                           #Create list for each cube that make up the snake
    turns = {}
    
    def __init__(self, color, pos):
        """
        Set the initial state of the snake when first starting """
        self.color = color              #Set color for the snake
        self.head = cube(pos)           #Set the head of the snake at the starting position, pos
        self.body.append(self.head)     #Put the head cube into the list
        self.dirnx = 0                  #Directions for moving the snake
        self.dirny = 1

    def move(self):
        """
        Set the instructions for the snake to move using """
        
        for event in pygame.event.get():        
            if event.type == pygame.QUIT:       #Quit the game when needed
                pygame.quit()
                sys.exit()
           
            keys = pygame.key.get_pressed()     #Get a dictionary of all the keys values and if they are pressed or not

            for key in keys:                    #Loop through all of the keys
                if keys[pygame.K_LEFT]:         #Instructions if Left key is pressed
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]         #Add the position of the head to the dictionary and make it equal to the direction of the turn.
                                                                                    #This is to determine which way the head of the snake is turning

                if keys[pygame.K_RIGHT]:        #Instructions if Right key is pressed
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                if keys[pygame.K_DOWN]:         #Instructions if Down key is pressed
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                if keys[pygame.K_UP]:           #Instructions if Up key is pressed
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):       #c stands for cube.
            p = c.pos[:]
            if p in self.turns:                 #For each cube, check whether its position equals the turning position of the head
                turns = self.turns[p]          #Get the direction for the movement
                c.move(turns[0], turns[1])        #Apply the direction to move the cube
                if i == len(self.body)-1:       #Check if it is the last cube, then remove the direction from that position.
                    self.turns.pop(p)           #Otherwise, every time you move into that position, the snake will turn automatically
            else:
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])        #Check when the snake moves to the edge of the screen, it re-enters the screen on the other side
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows-1)
                else: c.move(c.dirnx,c.dirny)                                           #If it doesn't move the edge, then it will follow the direction it is currently in
                    
 
    def reset(self, pos):
        """
        Reset the snake to its starting position after game over """
        self.head = cube(pos)               #Clearing all the lists, dictionaries and set the variables to its starting values
        self.body = []                      
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        """
        Function to determine where to add the snack onto the snake's body """
        tail = self.body[-1]                #Name the variable tail to the last block on the snake's body
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:                                         #This determines the current direction that the snake is moving in and then add-
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))        #the snack cube onto the appropriate side of the tail of the snake, depending on that direction.
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].dirnx = dx                    #Set the added snack cube to move to the direction that the snake is currently moving in
        self.body[-1].dirny = dy


    def draw(self, surface):
        """
        Function to draw the snake from scatch """
        for i, c in enumerate(self.body):       #Running through all the cubes that make up the snake
            if i == 0:                          #If the cube is the head of the snake, the True boolean will draw eyes onto that cube. The function to draw eyes is in the cube class
                c.draw(surface, True)   
            else:
                c.draw(surface)
        

def drawGrid(w, rows, surface):
    """
    Function to draw the game's window from scratch """
    sizeBetween = w // rows     #Set the distance between the rows and columns

    x = 0
    y = 0
    for l in range(rows):       #Set loop to place the exact position of each line
        x = x + sizeBetween
        y = y + sizeBetween

        pygame.draw.line(surface, (0,0,0), (x,0), (x,w))      #Pygame function to draw the lines 
        pygame.draw.line(surface, (0,0,0), (0,y), (w,y))
       

def redrawWindow(surface):
    """
    Function to redraw the game's window """
    global rows, width, s, snack     #Make these variables global to be used in other functions
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)

    pygame.display.update()

def game_intro(surface):
    """
    Function that creates the intro screen of the game """
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    intro = False
        
        surface.fill((0,0,0))
        
        title_font = pygame.font.SysFont("Sans", 40)
        title_text = title_font.render("Welcome to...", True, (255,255,255))
        surface.blit(title_text, (190, 100))

        title_font2 = pygame.font.SysFont("Sans", 70)
        title_text2 = title_font2.render("STEAK THE SNAKE", True, (255,215,0))
        surface.blit(title_text2, (50, 180))

        support_font = pygame.font.SysFont("Sans", 30)
        support_text = support_font.render("The best snake game to ever exist!", True, (255,255,255))
        surface.blit(support_text, (110, 300))

        support_text3 = support_font.render("You will be Steak, the snake, so go eat and eat!", True, (255,255,255))
        surface.blit(support_text3, (50, 380))

        support_text2 = support_font.render("Press 's' to start the game", True, (255,255,255))
        surface.blit(support_text2, (165, 500))
        
        pygame.display.update()

def game_over(surface):
    """Function that creates the gamee over screen when the player lost """
    game_over = True
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    game_over = False

        surface.fill((0,0,0))

        game_over_font = pygame.font.SysFont("Sans", 40)
        game_over_text = game_over_font.render("GAME OVER!", True, (255,255,255))
        surface.blit(game_over_text, (180,200))

        game_over_text2 = game_over_font.render("Score: {}".format(score), True, (255,215,0))
        surface.blit(game_over_text2, (230, 300))

        game_over_text3 = game_over_font.render("Press 's' to try again", True, (255,255,255))
        surface.blit(game_over_text3, (150, 450))
        

        pygame.display.update()

def randomSnack(rows, item):
    """
    Function to spawn the snack blocks """
    position = item.body        #Item is the snake

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x, y), (position)))) > 0:     #Filtering the list and making sure that the spawned block doesn't spawn on top of the snake or on top-
            continue                                                        #of another block
        else:
            break

    return (x, y) 
               

def message_box(subject, content):
    """
    Function to print a message box in the game """
    root = tk.Tk()                          #Display the message box at the top of the screen
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def score_counter(surface):
    """
    Function to display a live score feed at the top of the game's window """
    scorefont = pygame.font.SysFont("Sans", 30)                                          #Get a font from pyGame and name it scorefont
    scorefont2 = pygame.font.SysFont("Sans", 40)
    scoretext = scorefont.render("Steak's Score:", True, (255,255,255))    #Create a white text called scoretext, that displays updated score from the game
    scoretext2 = scorefont2.render("{}".format(score), True, (255,215,0))
    surface.blit(scoretext, (8, 12))                                        #Shove the created scoretext onto the game's window
    surface.blit(scoretext2, (175, 6))
    
    pygame.display.update()

def main():
    """
    The main function, used to run the game """
    #Create and set the initial size of the game screen
    global width, rows, s, snack, score         #Make these variables global to be used in other functions
    width = 625
    rows = 25
    win = pygame.display.set_mode((width, width))   #We have width twice because this will be a square

    game_intro(win)             #Call in the game introduction screen
    
    #Call in and named snake() function
    s = snake((255,0,0), (10,10))
    snack = cube(randomSnack(rows, s), color = (255,215,0))              #Call in the randomSnack function

    clock = pygame.time.Clock()

    #Set up loop to constantly update the status of the game for every frame
    flag = True
    while flag:        
        pygame.time.delay(50)                               #Delaying the movement speed of the snake
        if len(s.body) > 5 and len(s.body) <= 10:           #Increasing the speed of the snake, depending on its length
            clock.tick(12)                      
        elif len(s.body) > 10 and len(s.body) <= 30:
            clock.tick(15)
        elif len(s.body) > 30 and len(s.body) <= 50:
            clock.tick(20)
        elif len(s.body) > 50:
            clock.tick(30)
        else:
            clock.tick(10)
            
        score = (len(s.body)) - 1           #Storing the live updated score of the game inside the score variable
            
        s.move()                            #Activates the "move" loop above in the snake class
        if s.body[0].pos == snack.pos:      #If the snake touches the snack, one more cube is added to the snake's body
               s.addCube()                                                  
               snack = cube(randomSnack(rows, s), color = (255,215,0))       #When the snack is eaten, spawn another snack in a random position
        
        for x in range(len(s.body)):                                         #Run through and check whether the position of the head of the snake collided-
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1 : ])):   #with a cube of its own body. Pretty much, checking for collision.
                game_over(win)          # Call the game over function
                s.reset((10,10))
                break
            
        redrawWindow(win)       #Draw the game window created above
        score_counter(win)      #Draw the score counter at the top of the game's window
        
        

main()
