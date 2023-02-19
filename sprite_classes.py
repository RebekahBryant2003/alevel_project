import pygame
import random
import math

class Object(pygame.sprite.Sprite):
   type ='RECTANGLE'
   #for draw function default is RECTANGLE
   def change_colour(self,colour):
      #This is used to change the colour or any object in our game
      self.image.fill(colour)

class Moving_Objects(Object):
#this function is shared by all moving objects (eg the players and the enemies)
     changex = 0
     changey = 0
     #sets vectors to 0 as default
     def update(self):

        collisions = [[False,False],[False,False]]
        #makes list of collisions for this round for corner collisions
        #this is in the form [X collision, is to the right?] [y collisions, Is Below?]

        # Move left/right
        self.rect.x += self.changex
        # Move up/down
        block_hit_list = pygame.sprite.spritecollide(self, self.walls,False)
        #this checks to see if the walls and Moving_object sprite collides, False makes sure they dont delete eachothe
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit

            collisions[0][0] = True
            #this tells that collision in x direction has happened

            if self.changex > 0:
            #if the player is moving in the x direction
                self.rect.right = block.rect.left
                collisions[0][1] = True
                #this indicates that the first collision is to the right of enemy (because posative x)
              
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
                collisions[0][1] = False
                #this indicates that the first collision is to the left of enemy (because negative x)

            if self.player == False and self.changey == 0:
                self.changey = 2
                self.overwritey = True
            #if the enemy is directly beside the player but stuck behind wall it will move out of wall
        if len(block_hit_list) == 0 and self.player == False:
            self.overwritey = False
        #if the enemy is no longer beside wall returns to normal movement

        self.rect.y += self.changey
         # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.walls,False)
        for block in block_hit_list:
            # Reset our position based on the top/bottom of the object.

            collisions [1][0] = True
            #This says there has been a collision in the y direction

            if self.changey > 0:
                self.rect.bottom = block.rect.top
                collisions [1][1] = True
                ##this indicates that the second collision is to the below of enemy (because posative y)
            else:
                self.rect.top = block.rect.bottom
                collisions[1][1] = False
                #this indicates that the second collision is to the above of enemy (because negative y)

            if self.player == False and self.changex == 0:
                self.changex = 2
                self.overwritex = True
            #if the enemy is directly under or above the player but stuck behind wall it will move out of wall

        if len(block_hit_list) == 0 and self.player == False:
            self.overwritex = False
        #if the enemy is no longer above below wall returns to normal movement
        
        if self.player == True:
            self.furtherupdates()
            #does the other updates for the player such as coins and checking whether won/lost

        else: #if the object is an enemy check for corner collisions

            if collisions[0][0] == True and collisions[1][0] == True:
            #if there has been two collisions (one in the x direction on in the y direction
                self.overwritex = False
                self.overwritey = False
                #resets these as this bigger issue will be solved by this algorithm

                self.overwritecorners = True
                #this tells computer there is collision in a corner
                self.ticker = 0 
                if collisions[0][1] == True:
                    self.changex = -1
                else:
                    self.changex = 1
                #sets the changex to opposite sign of what it was

                if collisions[1][1] == True:
                    self.changey = -1
                else:
                    self.changey = 1
                #sets the changey to opposite sign of what it was
                   

  

class Wall(Object):
#walls class holds all the sprites for the walls
    def __init__(self,x,y,width,height,colour,endblock = False):
    #this is the constructor class for the walls
        #super().__init__()
        #calls the parents constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width,height])
        #specifys the size of the wall
        while colour == [0,0,0] and endblock == False:
            colour = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
            #this makes sure the colour isnt black
        self.image.fill(colour)
        #sets the colour of the wall to passed in value
        self.colour = colour
        self.rect = self.image.get_rect()
        #makes the sprite a rectangle
        self.rect.y = y
        self.rect.x = x
        #specifys the top left hand corner of the rectangle as x an y      

class Text(Object):
#text class holds all the sprites for the text
    def __init__(self,x,y,text,size,colour,width,height):
     #constructor class for all the text
     pygame.sprite.Sprite.__init__(self)
     super(Text, self).__init__()
     self.font = pygame.font.SysFont("comicsans", size)
     self.written = text
     self.textSurf = self.font.render(str(text), 1, colour)
     self.image = pygame.Surface((width, height))
     self.x = x
     self.y = y
     self.image.blit(self.textSurf, [x,y])
     #this creates the text on screen
     self.colour = colour
     self.type ='TEXT'
     #this is for the drawing function so that it renders as text not as rectangle
    def change_colour(self,colour):
        #overrights one in object because lower in chain
        self.textSurf = self.font.render(str(self.written),1,colour)
        self.colour = colour
        #changes colour of text
    def change_text(self,text):
        #changes text (for score)
        self.textSurf = self.font.render(str(text),1,self.colour)
        self.written = text
        #updates text


class Character(Moving_Objects):
#character class for the character sprite
    def __init__(self,x,y,level,wall_list,ENDBLOCK,multiplayer,H,coin_list,Top_left,WRONGBLOCK =pygame.sprite.Group(),score = 0,enemy_list = pygame.sprite.Group()):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10/level,10/level])
        #this creates a image surface for the character sprite
        self.image.fill([255,255,255])
        self.colour = [255,255,255]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
 
        self.ENDBLOCK = ENDBLOCK
        self.WRONGBLOCK = WRONGBLOCK
        self.finish = False
        self.won = False

        self.walls = wall_list
        self.coins_list = coin_list
        self.enemies = enemy_list
        if Top_left == False:
            self.score = Text(20,H-50,score,30,(255,255,255),50,20)
            #sets score to bottom left
        else:#for multiplayer
            self.score = Text(20,50,score,30,(255,255,255),50,20)
            #sets score to bottom right
        #gets score from last game if it is first game it is 0

        self.player = True
        #to distinguish between player and the enemies

    def changespeedx(self,x):
        self.changex = x
    def changespeedy(self,y):
        self.changey = y
  
    def furtherupdates(self):
        end_hit_list = pygame.sprite.spritecollide(self,self.ENDBLOCK,False)
        for block in end_hit_list:
            self.finish = True
            self.won = True
        #this ends the game if it reaches the end
        end_hit_list = pygame.sprite.spritecollide(self,self.WRONGBLOCK,False)
        for block in end_hit_list:
            self.finish = True
        #this ends the game if it reaches the wrong answer
        end_hit_list = pygame.sprite.spritecollide(self,self.enemies,False)
        for block in end_hit_list:
            self.finish = True
        #this ends the game if player touches the enemy


        block_hit_list = pygame.sprite.spritecollide(self, self.coins_list,True)
        #this checks to see if the coins and the player collide and removes coin if it does
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            self.score.change_text(int(self.score.written)+10)
            #adds 10 to the score for every block given


class Coins (Object):
 #the coin class is an extension to the Object class which makes it a sprite
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10, 10])
        self.image.fill ((255,255,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        #these are the centre coordinates
        self.colour = (255,255,0)
        #sets colour
        self.type = 'CIRCLE'
        #for draw function so doesnt draw as rectangle
    #def drawcircle(self,screen):
    #    pygame.draw.circle(self.image,self.colour,(self.x,self.y),5)

class Enemies (Moving_Objects):
#Class for enemies
    def __init__(self,x,y):
    #initialiser class for enemies that takes x and y coordinates to spawn
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10,10])
        #this creates a image surface for the enemie class
        self.image.fill([255,0,0])
        self.colour = [255,0,0]
        #sets to red
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.player = False
        #for update class
        self.overwritex = False
        self.overwritey = False
        self.overwritecorners = False
        self.ticker = 10
        #used for exceptions in the movement

    def Vectors(self):
    #This function is used to work out the velociies of the enemy (to player)
        if self.overwritecorners == True:
        #if the enemy is stuck in a corner
            self.ticker = self.ticker+1
            #adds one to the timer
            if self.ticker == 10:
            #if it has used these vectors for 3 ticks
                self.overwritecorners = False
                self.ticker = 0
                #this makes it go back to normal algorithm

        elif self.overwritex == True or self.overwritey == True:
            pass
        #this is for when enemy is stuck and the collisions overwrite the vectors so that they can get enemy unstuck

        else:
            magnitude = math.sqrt(((self.Player.rect.x-self.rect.x)**2)+((self.Player.rect.y-self.rect.y)**2))
            #magnitude of vector from the enemy to the player
            if magnitude == 0:
                magnitude = 1
            #if its 0 its sets as 1 as cant divide by 0

            if magnitude >= 300:
            #if the enemy is 300 units or greater awayfrom the player it will not know the players movement
                if self.ticker >= 10:
                #if the enemy has had the same vectors the last 20 tics reset
                    self.changex = random.randint(-2,2)
                    self.changey = random.randint(-2,2)
                    #generates a random number between -2 and 2 for x and y vector 
                    self.ticker = 0
                else:
                   self.ticker =+ 1
            else:
            #when close to the player the enemy knows its position
                self.changex = math.floor(((2)*(self.Player.rect.x - self.rect.x)) / magnitude)
                self.changey = math.floor(((2)*(self.Player.rect.y - self.rect.y)) / magnitude)
                #this calculates the vector for the enemy to the player with the magnitude 3 square root 2 which is rounded down to the nearest integer


class TextBoxes(Object):
    def __init__ (x,y,width,height,colour,label):
        #the label is a array with its x and y coordinates
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width,height])
        #specifys the size of the wall
        self.image.fill(colour)
        #sets the colour of the wall to passed in value
        self.colour = colour
        self.rect = self.image.get_rect()
        #makes the sprite a rectangle
        self.rect.y = y
        self.rect.x = x
        #specifys the top left hand corner of the rectangle as x an y  
        self.label = Text(label[1],label[2],label[0],[255,255,255],100,50)
        #this is for the lavel of what it is
        self.text = ""
        self.text = Text(x+5,y+25,self.text,[0,0,0],width - 10, height - 10)
        #this makes the text the player will type in
        self.cursor = Wall(x+5,y+5,2,height-10,)
        #makes the cursor for where the player is typing
    def DrawCursor(self):

    def AddText (self,keystroke):
        self.text = self.text + str(keystroke)
    #adds the keystroked letter to the text
    def RemoveText (self):
        self.text = self.text[:-1]
    #removes letter from the text


   
class ResetButton (Object):
    def __init__(self,x,y,width,height,W,H,colour,text,textx,texty):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width,height])
        #this creates a image surface for the button
        self.image.fill(colour)
        self.colour = colour
        self.rect = self.image.get_rect()
        self.rect.x = x
        #x coordinate of top left
        self.rect.y = y
        #7 coordinate of top right
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        #saves the dimensions of the box
        if colour == [255,255,255]:
            self.textcolour = [0,0,0]
        else:
            self.textcolour = [255,255,255]
        #Makes the colour opposite to previous colour
        self.text =  Text(textx,texty,text,35,self.textcolour,70,50)
        #puts the text inside of the button
    def buttonhovercheck(self, mouse):
     #this is called every game tick to check whether mouse is hovering the button
        if mouse[0] >= self.x and mouse[0] <= self.x+ self.width and mouse[1] >= self.y and mouse[1] <= self.y + self.height:
            #checks the mouse posisition is over the button
            self.change_colour((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
            self.text.change_colour(self.colour)
            #changes colour of the text and the button
        else:
            self.change_colour(self.colour)
            #changes colour of the text and the button back to original
            self.text.change_colour(self.textcolour)

       
  
 

