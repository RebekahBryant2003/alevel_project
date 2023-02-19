import pygame
import random
import time
import maze_module
import Sprite_classes
import ctypes
import math
#imports the modules needed forthe program

def MainLoop_Singleplayer(level,score,screen):
#This is the main game loop for the single player game

    all_sprite_list = pygame.sprite.Group()
    wall_list = pygame.sprite.Group()
    text_list = pygame.sprite.Group()
    WRONGBLOCK = pygame.sprite.Group()
    coins_list = pygame.sprite.Group()
    enemy_list = pygame.sprite.Group()
    #different sprite classes


    pygame.init()
    #initialises pygame
    user32 = ctypes.windll.user32
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    #this imports the screen size
    W = math.floor(width/100)*100
    H = math.floor(height/100)*100
    #the screen resolution is rounded to the nearest 100 so that can split into grid
    #(NOTE CHANGE THIS LATER TO FIT THE WHOLE SCREEN)

    clock = pygame.time.Clock()
    #initialises the gameclock (eg ticks per second)
    sprites =  maze_module.MazeGenerator(False,level)
    #this uses external module to generate the maze
    wall_list = sprites[0]
    all_sprite_list.add(wall_list)
    #adds the walls to the all_sprite_list variable
    text_list = sprites[1]
    #adds the text to the all_sprite_list variable
    END = pygame.sprite.Group()
    END.add(sprites[2])
    #this grabs the end sprite from the maze_generator
    WRONGBLOCK = sprites[3]
    #this grabs the wrong answers sprites from maze_generator
    Button = sprites[4]
    all_sprite_list.add(Button)
    text_list.add(Button.text)
    #pulls reset button from maze_module and adds to sprite list to be updated, as well as the text from the button attribute to be added to text_list
    coins_list.add(sprites[5])
    #pulls coins from the maze_module and adds to the coins list
    all_sprite_list.add(coins_list)
    #adds the coins_list to all_sprite_list so they are generated on screen
    
 
    enemy_list.add(sprites[6])
    all_sprite_list.add(sprites[6])
    #adds enemies to sprite lists

    Player = Sprite_classes.Character(50,50,1,wall_list,END,False,H,coins_list,False,WRONGBLOCK,score,enemy_list)
    all_sprite_list.add(Player)
    all_sprite_list.add(sprites[2])
    text_list.add(Player.score)

    for Enemy in enemy_list:
        Enemy.Player = Player
        Enemy.walls = wall_list
    #add the player as a arribute of the enemy


    done = False
    while not done:
    #loops until the pygame is finished
        for event in pygame.event.get():
            if event.type == pygame.QUIT or Player.finish == True :
                done = True
            #stops the program if the x is pressed
            elif event.type == pygame.KEYDOWN:
            #this registers the user is pressing a key down
                if event.key == pygame.K_LEFT:
                    Player.changespeedx(-3)
                elif event.key == pygame.K_RIGHT:
                    Player.changespeedx(3)
                elif event.key == pygame.K_UP:
                    Player.changespeedy( -3)
                elif event.key == pygame.K_DOWN:
                    Player.changespeedy(3)
                #this updates the players speed vectors based on the keypressed
 
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    Player.changespeedx(0)
                elif event.key == pygame.K_RIGHT:
                    Player.changespeedx(0)
                elif event.key == pygame.K_UP:
                    Player.changespeedy(0)
                elif event.key == pygame.K_DOWN:
                    Player.changespeedy(0)
            #this registers when the player stops pressing the key and sets vector to 0
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and mouse[0] >= Button.x and mouse[0] <= Button.x+ Button.width and mouse[1] >= Button.y and mouse[1] <= Button.y + Button.height:
                #this plays if the left mouse button is clicked and in the reset button zone
                MainLoop_Singleplayer(level,score,screen)
                #replays the level for a new map (passes old score as score reseting level
                done = True
                #ends the game so it doesnt loop again

        mouse = pygame.mouse.get_pos()
        #grabs the x and y location of the mouse
        Button.buttonhovercheck(mouse)
        #this checks whether the mouse is hovering over the button (function in sprite_classes button object)

        for enemy in enemy_list:
            enemy.Vectors()
        #updates to towards the player
            
        all_sprite_list.update()
        #updates all the sprites in the program
 
        screen.fill([0,0,0])
        #sets screen to black

        all_sprite_list.draw(screen)
        #draws sprites

        for text in text_list:
            screen.blit(text.textSurf, [text.x,text.y])
            #draws texts

        pygame.display.flip()
        #updates the screen


    
        clock.tick(60)
        #loops 60 times a second (60[FPS)

    if Player.won == True:
        MainLoop_Singleplayer(level+1,Player.score.written,screen)
        #loops when player wins
    if Player.won == False:
        pass
        #ends when player looses

def MainLoop_Multiplayer(level,score,screen):
#This is the main game loop for the single player game

    all_sprite_list = pygame.sprite.Group()
    wall_list = pygame.sprite.Group()
    text_list = pygame.sprite.Group()
    coins_list = pygame.sprite.Group()
    #different sprite classes

    screen.fill([0,0,0])
    #sets screen to black

    pygame.init()
    #initialises pygame
    user32 = ctypes.windll.user32
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    #this imports the screen size
    W = math.floor(width/100)*100
    H = math.floor(height/100)*100
    #the screen resolution is rounded to the nearest 100 so that can split into grid
    #(NOTE CHANGE THIS LATER TO FIT THE WHOLE SCREEN)

    clock = pygame.time.Clock()
    #initialises the gameclock (eg ticks per second)
    sprites =  maze_module.MazeGenerator(True,level)
    #this uses external module to generate the maze
    wall_list = sprites[0]
    all_sprite_list.add(wall_list)
    #adds the walls to the all_sprite_list variable
    text_list = sprites[1]
    #adds the text to the all_sprite_list variable
    END = pygame.sprite.Group()
    END.add(sprites[2])
    #this grabs the end sprite from the maze_generator
    Button = sprites[4]
    all_sprite_list.add(Button)
    text_list.add(Button.text)
    #pulls reset button from maze_module and adds to sprite list to be updated, as well as the text from the button attribute to be added to text_list

    coins_list.add(sprites[5])
    all_sprite_list.add(sprites[5])
    #adds coins to sprite lists


    PlayerOne = Sprite_classes.Character(50,50,1,wall_list,END, True,H,coins_list,True)
    all_sprite_list.add(PlayerOne)
    all_sprite_list.add(sprites[2])
    #This creates player 1
    text_list.add(PlayerOne.score)
    PlayerTwo = Sprite_classes.Character(50,H-50,1,wall_list,END, True,H,coins_list,False)
    all_sprite_list.add(PlayerTwo)
    #This creates player 2
    text_list.add(PlayerTwo.score)



    done = False
    while not done:
    #loops until the pygame is finished
        for event in pygame.event.get():
            if event.type == pygame.QUIT or PlayerOne.finish == True or PlayerTwo.finish == True:
                done = True
            #stops the program if the x is pressed
            elif event.type == pygame.KEYDOWN:
            #this registers the user is pressing a key down
                if event.key == pygame.K_LEFT:
                    PlayerOne.changespeedx(-3)
                elif event.key == pygame.K_RIGHT:
                    PlayerOne.changespeedx(3)
                elif event.key == pygame.K_UP:
                    PlayerOne.changespeedy( -3)
                elif event.key == pygame.K_DOWN:
                    PlayerOne.changespeedy(3)
                #this updates the player ones speed vectors based on the keypressed

                if event.key == pygame.K_a:
                    PlayerTwo.changespeedx(-3)
                elif event.key == pygame.K_d:
                    PlayerTwo.changespeedx(3)
                elif event.key == pygame.K_w:
                    PlayerTwo.changespeedy( -3)
                elif event.key == pygame.K_s:
                    PlayerTwo.changespeedy(3)
                #this updates the player twos speed vectors based on the keypressed
 
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    PlayerOne.changespeedx(0)
                elif event.key == pygame.K_RIGHT:
                    PlayerOne.changespeedx(0)
                elif event.key == pygame.K_UP:
                    PlayerOne.changespeedy(0)
                elif event.key == pygame.K_DOWN:
                    PlayerOne.changespeedy(0)
                #this registers when the player one stops pressing the key and sets vector to 0

                if event.key == pygame.K_a:
                    PlayerTwo.changespeedx(0)
                elif event.key == pygame.K_d:
                    PlayerTwo.changespeedx(0)
                elif event.key == pygame.K_w:
                    PlayerTwo.changespeedy(0)
                elif event.key == pygame.K_s:
                    PlayerTwo.changespeedy(0)
                #this registers when the player two stops pressing the key and sets vector to 0

 

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and mouse[0] >= Button.x and mouse[0] <= Button.x+ Button.width and mouse[1] >= Button.y and mouse[1] <= Button.y + Button.height:
                #this plays if the left mouse button is clicked and in the reset button zone
                MainLoop_Multiplayer(1,0,screen)
                #replays the level for a new map (passes old score as score reseting level
                done = True
                #ends the game so it doesnt loop again

        mouse = pygame.mouse.get_pos()
        #grabs the x and y location of the mouse
        Button.buttonhovercheck(mouse)
        #this checks whether the mouse is hovering over the button (function in sprite_classes button object)

            
        all_sprite_list.update()
        #updates all the sprites in the program
 
        screen.fill([0,0,0])
        #sets screen to black

        all_sprite_list.draw(screen)
        #draws sprites

        for text in text_list:
            screen.blit(text.textSurf, [text.x,text.y])
            #draws texts

        clock.tick(60)
        #loops 60 times a second (60[FPS)
