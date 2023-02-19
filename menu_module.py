import pygame
import random
import time
import maze_module
import Sprite_classes
import Main_loop
import ctypes
import math
#imports the modules needed forthe program

def Base():
#This function is for the basic layout of the menu screens
    user32 = ctypes.windll.user32
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    #this imports the screen size
    W = math.floor(width/100)*100
    H = math.floor(height/100)*100
    #the screen resolution is rounded to the nearest 100 so that can split into grid


    all_sprite_list = pygame.sprite.Group()
    text_list = pygame.sprite.Group()
    #initiallies the sprite groups to be passed at end of function

    Bottom = Sprite_classes.Wall(0,int(H/2)+100,W,int(H-((H/2)+100)),[255,255,255])
    all_sprite_list.add(Bottom)
    #this creates the block of white at the bottom of the screen
    Title = Sprite_classes.Text(int((W)/3)+20,50,"Germ Escape",150,[255,255,255],int((2*W)/3),int(H/4))
    text_list.add(Title)


    #This makes the title in the top right hand corner
    #THE OTHER TWO THINGS THAT NEED TO BE RENDERED ARE THE MASCOT AND THE ENEMIES AT THE BOTTOM

    return[all_sprite_list,text_list]
    #this returns the sprite lists to whatever menu function is accessing it


def Menu_One():
    pygame.init()

    user32 = ctypes.windll.user32
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    #this imports the screen size
    W = math.floor(width/100)*100
    H = math.floor(height/100)*100
    #the screen resolution is rounded to the nearest 100 so that can split into grid
    #(NOTE CHANGE THIS LATER TO FIT THE WHOLE SCREEN)

    all_sprite_list = pygame.sprite.Group()
    text_list = pygame.sprite.Group()
    #initiallies the sprite groups to be passed at end of function

    screen = pygame.display.set_mode([W,H])
    #add pygame.FULLSCREEN when want to full screen
    #creates a screen to the width and height of the screen and puts it to fullscreen
    pygame.display.set_caption('Maze')
    #labels the maze

    clock = pygame.time.Clock()
    #initialises the gameclock (eg ticks per second)

    Basis = Base()
    all_sprite_list.add(Basis[0])
    text_list.add(Basis[1])
    #adds the relevant sprites for the base of the screen

    LoginButton = Sprite_classes.ResetButton(int((W)/3)+20, 200, 200 , 50, W, H, [0,0,0],"Login",int((W)/3)+20,225)
    all_sprite_list.add(LoginButton)
    text_list.add(LoginButton.text)
    #initialises the login button

    SignUpButton = Sprite_classes.ResetButton(int(W/3)+20, 300, 200 , 50, W, H,[0,0,0],"Sign Up",int((W)/3)+20,325)
    all_sprite_list.add(SignUpButton)
    text_list.add(SignUpButton.text)
    #initialises the sign up button

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                #ends the game
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and mouse[0] >= LoginButton.x and mouse[0] <= LoginButton.x+ LoginButton.width and mouse[1] >= LoginButton.y and mouse[1] <= LoginButton.y + LoginButton.height:
                #this plays if the left mouse button is clicked and in the login button zone
                Main_loop.MainLoop_Singleplayer(1,0,screen)
                #goes to login screen
                done = True
                #ends the game so it doesnt loop again
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and mouse[0] >= SignUpButton.x and mouse[0] <= SignUpButton.x+ SignUpButton.width and mouse[1] >= SignUpButton.y and mouse[1] <= SignUpButton.y + SignUpButton.height:
                #this plays if the left mouse button is clicked and in the sign up button zone
                Menu_Two(screen)
                #plays signup page
                done = True
                #ends the game so it doesnt loop again
            else:
                pass
        mouse = pygame.mouse.get_pos()
        #grabs the x and y location of the mouse
        LoginButton.buttonhovercheck(mouse)
        #this checks whether the mouse is hovering over the button (function in sprite_classes button object)
        SignUpButton.buttonhovercheck(mouse)
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

        pygame.display.flip()
        #updates the screen

        clock.tick(60)
        #loops 60 times a second (60[FPS)

    pygame.quit()

def Menu_Two(screen):
    pygame.init()

    user32 = ctypes.windll.user32
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    #this imports the screen size
    W = math.floor(width/100)*100
    H = math.floor(height/100)*100
    #the screen resolution is rounded to the nearest 100 so that can split into grid
    #(NOTE CHANGE THIS LATER TO FIT THE WHOLE SCREEN)

    all_sprite_list = pygame.sprite.Group()
    text_list = pygame.sprite.Group()
    #initiallies the sprite groups to be passed at end of function

    clock = pygame.time.Clock()
    #initialises the gameclock (eg ticks per second)

    Basis = Base()
    all_sprite_list.add(Basis[0])
    text_list.add(Basis[1])
    #adds the relevant sprites for the base of the screen

    SinglePlayer = Sprite_classes.ResetButton(int((W)/3)+20, 150, 200 , 50, W, H, [0,0,0],"Normal Game",int((W)/3)+20,175)
    all_sprite_list.add(SinglePlayer)
    text_list.add(SinglePlayer.text)
    #initialises the login button

    Multiplayer = Sprite_classes.ResetButton(int(W/3)+20, 225, 200 , 50, W, H,[0,0,0],"MultiPlayer",int((W)/3)+20,250)
    all_sprite_list.add(Multiplayer)
    text_list.add(Multiplayer.text)
    #initialises the sign up button

    LeaderBoards = Sprite_classes.ResetButton(int(W/3)+20, 300, 200 , 50, W, H,[0,0,0],"LeaderBoards",int((W)/3)+20,325)
    all_sprite_list.add(LeaderBoards)
    text_list.add(LeaderBoards.text)
    #initialises the sign up button

    TeacherArea = Sprite_classes.ResetButton(int(W/3)+20, 375, 200 , 50, W, H,[0,0,0],"Teacher Area",int((W)/3)+20,400)
    all_sprite_list.add(TeacherArea)
    text_list.add(TeacherArea.text)
    #initialises the sign up button

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                #ends the game
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and mouse[0] >= SinglePlayer.x and mouse[0] <= SinglePlayer.x+ SinglePlayer.width and mouse[1] >= SinglePlayer.y and mouse[1] <= SinglePlayer.y + SinglePlayer.height:
                #this plays if the left mouse button is clicked and in the SinglePlayer zone
                Main_loop.MainLoop_Singleplayer(1,0,screen)
                #]plays game
                done = True
                #ends the game so it doesnt loop again
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and mouse[0] >= Multiplayer.x and mouse[0] <= Multiplayer.x+ Multiplayer.width and mouse[1] >= Multiplayer.y and mouse[1] <= Multiplayer.y + Multiplayer.height:
                #this plays if the left mouse button is clicked and in the reset button zone
                Main_loop.MainLoop_Multiplayer(1,0,screen)
                #plays multiplayer
                done = True
                #ends the game so it doesnt loop again
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and mouse[0] >= LeaderBoards.x and mouse[0] <= LeaderBoards.x+ LeaderBoards.width and mouse[1] >= LeaderBoards.y and mouse[1] <= LeaderBoards.y + LeaderBoards.height:
                #this plays if the left mouse button is clicked and in the sign up button zone
                #plays leaderboards
                done = True
                #ends the game so it doesnt loop again
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and mouse[0] >= TeacherArea.x and mouse[0] <= TeacherArea.x+ TeacherArea.width and mouse[1] >= TeacherArea.y and mouse[1] <= TeacherArea.y + TeacherArea.height:
                #this plays if the left mouse button is clicked and in the sign up button zone
                #plays teacher area
                done = True
                #ends the game so it doesnt loop again
            else:
                pass
        mouse = pygame.mouse.get_pos()
        #grabs the x and y location of the mouse
        SinglePlayer.buttonhovercheck(mouse)
        #this checks whether the mouse is hovering over the button (function in sprite_classes button object)
        Multiplayer.buttonhovercheck(mouse)
        #this checks whether the mouse is hovering over the button (function in sprite_classes button object)
        LeaderBoards.buttonhovercheck(mouse)
        #this checks whether the mouse is hovering over the button (function in sprite_classes button object)
        TeacherArea.buttonhovercheck(mouse)
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

        pygame.display.flip()
        #updates the screen

        clock.tick(60)
        #loops 60 times a second (60[FPS)


Menu_One()
