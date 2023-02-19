import pygame
import random
import Sprite_classes
import ctypes
#used to import the screen size
import math

  
def MazeGenerator(multiplayer,levels):
    wall_list = pygame.sprite.Group()
    text_list = pygame.sprite.Group()
    WRONGBLOCK = pygame.sprite.Group()
    coins_list = pygame.sprite.Group()
    enemy_list = pygame.sprite.Group()

    level = 1
    user32 = ctypes.windll.user32
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    #this imports the screen size
    W = math.floor(width/100)*100
    collumns = W / 100
    H = math.floor(height/100)*100
    rows = H / 100
    #the screen resolution is rounded to the nearest 100 so that can split into grid
    #(NOTE CHANGE THIS LATER TO FIT THE WHOLE SCREEN)
    wall = Sprite_classes.Wall(0,0,W,10,[255,255,255])
    wall_list.add(wall)
    wall = Sprite_classes.Wall(0,0,10,H,[255,255,255])
    wall_list.add(wall)
    wall = Sprite_classes.Wall(0,H-10,W,10,[255,255,255])
    wall_list.add(wall)
    wall = Sprite_classes.Wall(W-10,0,10,H,[255,255,255])
    wall_list.add(wall)
    #these four walls are the walls for the boarders of the game

    #this is called in the mainloop to create a maze
    end = []
    start = []
    #sets the end and start rows and collumns for the round
    if multiplayer == False:
    #sets the start row and collumn to the end and start arrays for single player game
        start.append("0,0")
        #sets the start of single player game to grid position 0,0 (top left)
        num = math.floor((rows-1) / 4)
        #divides the rows for single player (bottom row is used for the question) into 4 (for answer options)
        current = 0
        for count in range(4):
            end.append(str(current) + "," + str(math.floor(collumns-1)))
            current = current + num
        #sets 4 end positions for the single player game, these are right hand collumn of screen and split in 4

        questionfile = open("Questions.csv","rb")
        #imports the question file which holds the questions and answer options
        lines = []
        question = []
        length = 0
        for row in questionfile:
            lines.append(row)
            length =+ 1
        #this imports all the questions in the file into variables in array
        questionfile.close()
        #closes external document
        chosen = str(random.choice(lines)).strip("b'").strip("\\r\\n")
        #this chooses a random question for the level and removes external information
        question = chosen.split(",")
        #this splits up the information in the line chosen (csv style document)
        answers = [question[1],question[2],question[3],question[4]]
        #this sets the answers into an array
        correct = answers[0]
        #this saves the correct answer in a document
        questions = question[0]
        #this saves the question to be outputted
    else:
    #sets the start and end positions for a multiplayer game
        start.append("0,0")
        #sets one start position to top left hand corner
        start.append(str(int(rows-1))+",0")
        #sets other start position to top bottom hand corner
        end.append(str(int(math.floor(rows/2)))+","+str(int(collumns-1)))
        #sets end position to right hand side middle grid

    for row in range(int(rows)):
        for collumn in range(int(collumns)):
    #these lines are a nested for loop that loops round the grid based on the level(10x10 for level 1)
            if str(row) + "," + str(collumn) in end:
            #creates text for end positions
                if multiplayer == False:
                    option = random.choice(answers)
                    answers.remove(option)
                    texts = Sprite_classes.Text((25/level+collumn*(100/level)),(25/level+row*(100/level)),option,25,[255,255,255],75,50)
                    text_list.add(texts)
                    #adds new sprite for one of the answer options
                    if option == correct:
                        ENDBLOCK = Sprite_classes.Wall((collumn*(100/level)),(row*(100/level))+10,90,80,[0,0,0],True)
                        #this is to create an 'inisible block' that if the player collides with it then it end
                    else:
                        BLOCK = Sprite_classes.Wall((collumn*(100/level)),(row*(100/level))+10,90,80,[0,0,0],True)
                        WRONGBLOCK.add(BLOCK)
                        #this is to create an 'invisible block' that if the player collides with it then it ends, adds to list of them
                    wall = Sprite_classes.Wall((collumn*(100/level)),(row*(100/level)),100,10,[255,255,255])
                    wall_list.add(wall)
                    wall = Sprite_classes.Wall((collumn*(100/level)),100+(row*(100/level)),100,10,[255,255,255])
                    wall_list.add(wall)
                    #creates a wall ontop and bottom of option box
                else:
                    text = "End"
                    texts = Sprite_classes.Text((25/level+collumn*(100/level)),(25/level+row*(100/level)),text,25,[255,255,255],75,50)
                    text_list.add(texts)
                    #creates text for end box
                    wall = Sprite_classes.Wall((collumn*(100/level)),(row*(100/level)),100,10,[255,255,255])
                    wall_list.add(wall)
                    wall = Sprite_classes.Wall((collumn*(100/level)),100+(row*(100/level)),100,10,[255,255,255])
                    wall_list.add(wall)
                    #creates a wall ontop and bottom of end box
                    ENDBLOCK = Sprite_classes.Wall((collumn*(100/level)),(row*(100/level))+10,90,80,[0,0,0],True)
                    #this is to create an 'inisible block' that if the player collides with it then it end
            elif str(row) + "," + str(collumn) in start:
            #this controls where the maze is a starting point
                text = "Start"
                texts = Sprite_classes.Text((25/level+collumn*(100/level)),(25/level+row*(100/level)),text,25,[255,255,255],75,50)
                text_list.add(texts)
                #creates text for start box
                wall = Sprite_classes.Wall((collumn*(100/level)),(row*(100/level)),100,10,[255,255,255])
                wall_list.add(wall)
                wall = Sprite_classes.Wall((collumn*(100/level)),100+(row*(100/level)),100,10,[255,255,255])
                wall_list.add(wall)
                #creates a wall ontop and bottom of start box

            elif str(row) + "," + str(collumn+1) in end or str(row) + "," + str(collumn+1) in start:
                pass
            #this elif statement makes the maze more likely to always be able to reach the end/ get out of the start
            #it does this by clearing the block before end and and the block after the start so its less likely lines will block the path

            elif multiplayer == True or row < rows-1: 
            #this controls generation of random maze
                for count in range(3):
                #creates two lines per grid square
                    x = 100
                    y = 100
                    while x == 100 and y == 100:
                        x = random.choice([0,50,100])
                        y = random.choice([0,50,100])
                    #imports random starting position for the line in grid but cannot be 100 100 as cant have minus dimensions
                    if x == 0 and y == 0:
                        w = [100,10,10,50]
                        h = [10,100,50,10]
                    elif x == 50 and y == 0:
                        w = [10,10,50]
                        h = [50,100,10]
                    elif x == 100 and y == 0:
                        w = [10,10]
                        h = [50,100]
                    elif x == 0 and y == 50:
                        w = [10,50,100]
                        h = [50,10,10]
                    elif x == 50 and y == 50:
                        w = [50,10]
                        h = [10,50]
                    elif x == 100 and y == 50:
                        w = [10]
                        h = [50]
                    elif x == 0 and y == 100:
                        w = [100,50]
                        h = [10,10]
                    else:
                        w = [50]
                        h = [10]
                    #idefines the possible width and height of each line based on grid

                    num = random.randint(0,len(w)-1)
                    #imports random number to choose line for the grid
                    colour = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
                    #makes the rectangle a random colour
                    wall = Sprite_classes.Wall((x+(collumn*(100/level))),(y+(row*(100/level))),w[num]/level,h[num]/level,colour)
                    #creates a wall rectange, the row and collumn * 100 makes sure its in the right square
                    wall_list.add(wall)
                    #adds the wall to the sprite list
                    wall_list.add(wall)

                    #adds the wall to the sprite list

            else:
              #this is where the question is outputted
              pass
    if multiplayer == False:
        wall = Sprite_classes.Wall(0,H - 100,W,10,[255,255,255])
        wall_list.add(wall)
        #creates wall across the bottom of the screen
        text =  Sprite_classes.Text(W/2,H - 50,questions,25,[255,255,255],750,50)
        text_list.add(text)
        #creates text with the question

    Button = Sprite_classes.ResetButton(W-100,H-80,80,60,W,H,[255,255,255],'Reset',W-90,H-70)
    #this is for the reset button, creates a sprite with class ResetButton in Sprite_class

    if multiplayer == False:
    #for coin and enemy spawning
        coins = Coin_generator(levels,end,start,rows-2,collumns,coins_list)
        Done = coins[0]
        coins_list = coins[1]
        enemies = Enemy_generator(Done, levels, end, start, rows-2, collumns,enemy_list) 
        enemy_list = enemies[0]
    else:
        coins = Coin_generator(levels,end,start,rows,collumns,coins_list)
        coins_list = coins[1]

    return [wall_list,text_list,ENDBLOCK,WRONGBLOCK,Button,coins_list,enemy_list]

def Coin_generator(levels, end, start, rows,collumns,coins_list):
#Responsible for spawning the Coins
        coins = 100 - (5*int(levels-1))
        #this is the counted for the amount of levels played
        Done = []
        #for the coins and enemies [that are already placed
        Positions = [20,70]
        #these are the predefined coordinates as defined in development

        for coin in range(coins):
        #cycles through the amount of coins needed as calculated above
            Free = False
            #for checking whether a grid position is free
            while Free == False:
            #this repeats until the algorithm finds a free space

                Grid_Row = random.randint(0,rows)
                Grid_Collumn = random.randint(0,collumns)
                #randomly generates a grid posistion for the coins to be spawned in

                if str(Grid_Row) + "," + str(Grid_Collumn) in end or str(Grid_Row) + "," + str(Grid_Collumn) in start:
                    Free = False
                    #checks if the grid posision is a start or end position therefore coins cannot spawn in them
                    #and sets to false so it finds a new posision
                else:
                #if the grid posision is free must pick on of the posisions

                    PosX = random.choice(Positions)
                    PosY = random.choice(Positions)
                    #this choses one of the four parts of the grid position

                    CoordX = (Grid_Collumn*100) + PosX
                    CoordY = (Grid_Row*100) + PosY
                    #This calculate the actual position of the coin

                    if str(CoordX) + "," + str(CoordY) in Done:
                    #checks whether the coordinate is aready used for a coin
                        Free = False
                    else:
                        Free = True
                        #if the coordinates are free it ends the while loop

            Coin = Sprite_classes.Coins(CoordX,CoordY)
            #this makes a new instance of the coin class with generated coordinates
            coins_list.add(Coin)
            #adds the coin to the list of objects
            Done.append(str(CoordX) + "," + str(CoordY))
            #adds coins coordinates to array done so that it tells the computer its taken that slot
        return [Done,coins_list]
        #Returns the Done as needed for enemy spawning and returns coin_list as needed for the game

def Enemy_generator(Done, levels, end, start, rows, collumns,enemy_list):
#responsible for spawning the enemies
     enemies = 5 + levels
     #this starts the game with 5 enemies and adds one each game
     Positions = [20,70]
     #these are the predefined coordinates as defined in development
     for enemy in range(enemies):
        #cycles through the amount of coins needed as calculated above
            Free = False
            #for checking whether a grid position is free
            while Free == False:
            #this repeats until the algorithm finds a free space

                Grid_Row = random.randint(0,rows)
                Grid_Collumn = random.randint(0,collumns)
                #randomly generates a grid posistion for the coins to be spawned in

                if str(Grid_Row) + "," + str(Grid_Collumn) in end or str(Grid_Row) + "," + str(Grid_Collumn) in start:
                    Free = False
                    #checks if the grid posision is a start or end position therefore coins cannot spawn in them
                    #and sets to false so it finds a new posision
                else:
                #if the grid posision is free must pick on of the posisions

                    PosX = random.choice(Positions)
                    PosY = random.choice(Positions)
                    #this choses one of the four parts of the grid position

                    CoordX = (Grid_Collumn*100) + PosX
                    CoordY = (Grid_Row*100) + PosY
                    #This calculate the actual position of the coin

                    if str(CoordX) + "," + str(CoordY) in Done:
                    #checks whether the coordinate is aready used for a coin
                        Free = False
                    else:
                        Free = True
                        #if the coordinates are free it ends the while loop

            Enemy = Sprite_classes.Enemies(CoordX,CoordY)
            #this makes a new instance of the coin class with generated coordinates
            enemy_list.add(Enemy)
            #adds the coin to the list of objects
            Done.append(str(CoordX) + "," + str(CoordY))
            #adds coins coordinates to array done so that it tells the computer its taken that slot
     return [enemy_list]
     #Returns the enemy list to the algorhithm
        
