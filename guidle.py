from turtle import Screen
import arcade
import arcade.gui
from matplotlib import style
from inspiration import SCREEN_HEIGHT, SCREEN_WIDTH
from actual.rpgdle import *
import random

RAINBOW = [(100,100,100),(25,25,150),(25,75,50),(139,25,25)]
class Rect:
    """ This class represents our rectangle """

    def __init__(self, width, height, x, y, color):

        self.width = width
        self.height = height
        self.center_x = x
        self.center_y = y
        self.color = color
        

    def draw(self):
        # Draw the rectangle
        arcade.draw_rectangle_filled(self.center_x,
                                     self.center_y,
                                     self.width,
                                     self.height,
                                     self.color)
class GameView(arcade.View):

    def __init__(self):
        self.isWinner = False
        self.guess = ""
        self.isGuessing = False
        self.isMessing = False
        self.no = True
        self.color = [200,50,50]
        self.last_max = 0
        super().__init__()
        arcade.set_background_color(arcade.color.PASTEL_YELLOW)
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.length = 6
        self.rang = 3
        self.game = Game(self.length,self.rang)
        self.styles=[]
        for i in range(4):
            style0 = {
                
                "border_width": 2,
                "border_color": None,
                "bg_color": RAINBOW[i],
                "bg_color_pressed": RAINBOW[i],
                "border_color_pressed": None,
                
            }
            self.styles.append(style0)
        self.mtyles=[]
        self.guess_mtyle = {
                
                "border_width": 4,
                "border_color": None,
                "bg_color": arcade.color.FERN_GREEN,

                # used if button is pressed
                "bg_color_pressed": arcade.color.FERN_GREEN,
                "border_color_pressed": (arcade.color.FERN_GREEN[0]-25,arcade.color.FERN_GREEN[1]-25,arcade.color.FERN_GREEN[2]-25),  # also used when hovered
                
            }
        for i in range(4):
            style0 = {
                
                "border_width": 2,
                "border_color": None,
                "bg_color": RAINBOW[i],

                # used if button is pressed
                "bg_color_pressed": (RAINBOW[i][0]+25,RAINBOW[i][1]+25,RAINBOW[i][2]+25),
                "border_color_pressed": (RAINBOW[i][0]-25,RAINBOW[i][1]-25,RAINBOW[i][2]-25),  # also used when hovered
                
            }
            self.mtyles.append(style0)
        
        

        
        self.enn_boxes = []
        self.enn_buttons = []
        self.enn_box_0 = arcade.gui.UIBoxLayout()
        self.enn_but_0 = arcade.gui.UIFlatButton(text="",
                                               width=75,height=75,style=self.styles[0])
        self.enn_box_0.add(self.enn_but_0)
        self.enn_boxes.append(self.enn_box_0)
        self.enn_buttons.append(self.enn_but_0)

        self.enn_box_1 = arcade.gui.UIBoxLayout()
        self.enn_but_1 = arcade.gui.UIFlatButton(text="",
                                               width=75,height=75,style=self.styles[0])
        self.enn_box_1.add(self.enn_but_1)
        self.enn_boxes.append(self.enn_box_1)
        self.enn_buttons.append(self.enn_but_1)

        self.enn_box_2 = arcade.gui.UIBoxLayout()
        self.enn_but_2 = arcade.gui.UIFlatButton(text="",
                                               width=75,height=75,style=self.styles[0])
        self.enn_box_2.add(self.enn_but_2)
        self.enn_boxes.append(self.enn_box_2)
        self.enn_buttons.append(self.enn_but_2)

        self.enn_box_3 = arcade.gui.UIBoxLayout()
        self.enn_but_3 = arcade.gui.UIFlatButton(text="",
                                               width=75,height=75,style=self.styles[0])
        self.enn_box_3.add(self.enn_but_3)
        self.enn_boxes.append(self.enn_box_3)
        self.enn_buttons.append(self.enn_but_3)

        self.enn_box_4 = arcade.gui.UIBoxLayout()
        self.enn_but_4 = arcade.gui.UIFlatButton(text="",
                                               width=75,height=75,style=self.styles[0])
        self.enn_box_4.add(self.enn_but_4)
        self.enn_boxes.append(self.enn_box_4)
        self.enn_buttons.append(self.enn_but_4)

        self.enn_box_5 = arcade.gui.UIBoxLayout()
        self.enn_but_5 = arcade.gui.UIFlatButton(text="",
                                               width=75,height=75,style=self.styles[0])
        self.enn_box_5.add(self.enn_but_5)
        self.enn_boxes.append(self.enn_box_5)
        self.enn_buttons.append(self.enn_but_5)
        
        
        for i in range(6):
            self.manager.add(
                arcade.gui.UIAnchorWidget(
                    anchor_x="center",
                    anchor_y="top",
                    align_x= -250+i*100,
                    align_y= -50,
                    
                    child=self.enn_boxes[i])
            )
        
        self.pla_boxes = [0,0,0,0,0,0]
        self.pla_buttons = [0,0,0,0,0,0]
        for i in range(6):
            self.pla_boxes[i] = arcade.gui.UIBoxLayout()
            self.pla_buttons[i] = arcade.gui.UIFlatButton(text="",
                                                width=75,height=75,style=self.styles[0])
            self.pla_boxes[i].add(self.pla_buttons[i])
        for i in range(6):
            self.manager.add(
                arcade.gui.UIAnchorWidget(
                    anchor_x="center",
                    anchor_y="top",
                    align_x= -250+i*100,
                    align_y= -575,
                    
                    child=self.pla_boxes[i])
            )
        
        self.pla2_boxes = [0,0,0,0,0,0]
        self.pla2_buttons = [0,0,0,0,0,0]
        for i in range(6):
            self.pla2_boxes[i] = arcade.gui.UIBoxLayout()
            self.pla2_buttons[i] = arcade.gui.UIFlatButton(text="",
                                                width=75,height=75,style=self.styles[0])
            self.pla2_boxes[i].add(self.pla2_buttons[i])
        for i in range(6):
            self.manager.add(
                arcade.gui.UIAnchorWidget(
                    anchor_x="center",
                    anchor_y="top",
                    align_x= -250+i*100,
                    align_y= -450,
                    
                    child=self.pla2_boxes[i])
            )
        self.guess_box = arcade.gui.UIBoxLayout()
        self.guess_button = arcade.gui.UIFlatButton(text=" ACT ",
                                                width=150,height=150,style=self.guess_mtyle)
        self.guess_box.add(self.guess_button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center",
                anchor_y="center",
                align_y=75,
                
                child=self.guess_box)
        )
        self.guess_button.on_click = self.make_mess
        
        for i in range(self.length):
            
                self.pla_boxes[i].remove(self.pla_buttons[i])
                self.pla_buttons[i] = arcade.gui.UIFlatButton(text="",
                                               width=75,height=75,style=self.styles[int(self.game.player1.bird[i])])
                self.pla_boxes[i].add(self.pla_buttons[i])
        self.pla4_buttons = [0,0,0]
        for i in range(3):
            self.pla4_buttons[i] = arcade.gui.UIFlatButton(text="",
                                                width=75,height=75,style=self.mtyles[i+1])

            self.pla4_buttons[i].onclick = lambda event : self.addToGuess(event,i+1)
    
    def start(self,event):
        while self.game.isGoing:
  
       
            if self.game.prompt(self.game.player1,self.game.player2):
                self.game.winner = self.game.player1
                break
            self.updnine()
            
        
    def make_guess(self,event):
        # actually make knife
        if self.isGuessing:
            
            for i in range(3):
                self.pla3_boxes[i].remove(self.pla3_buttons[i])
                self.manager.remove(self.pla3_boxes[i])
                
            self.isGuessing = False
            
        else:
            self.pla3_boxes = [0,0,0]
            self.pla3_buttons = [0,0,0]
            for i in range(3):
                self.pla3_boxes[i] = arcade.gui.UIBoxLayout()
                self.pla3_buttons[i] = arcade.gui.UIFlatButton(text="",
                                                    width=75,height=75,style=self.mtyles[i+1])
                self.pla3_boxes[i].add(self.pla3_buttons[i])
                
            for i in range(3):
                self.manager.add(
                    arcade.gui.UIAnchorWidget(
                        anchor_x="center",
                        anchor_y="top",
                        align_x= -100+i*100,
                        align_y= -250,
                        
                        child=self.pla3_boxes[i])
                )
            self.isGuessing = True
        self.updnine()
    def make_mess(self,event):
        
        # if self.isMessing:
            
        #     for i in range(3):
        #         self.pla4_boxes[i].remove(self.pla4_buttons[i])
        #         self.manager.remove(self.pla4_boxes[i])
                
        #     for i in range(6):
        #         self.pla5_boxes[i].remove(self.pla5_buttons[i])
        #         self.manager.remove(self.pla5_boxes[i])
               
        #     self.isMessing = False
            
        # else:
        #     self.pla4_boxes = [0,0,0]
        #     self.pla4_buttons = [0,0,0]
        #     for i in range(3):
        #         self.pla4_boxes[i] = arcade.gui.UIBoxLayout()
        #         self.pla4_buttons[i] = arcade.gui.UIFlatButton(text="",
        #                                             width=75,height=75,style=self.mtyles[i+1])

        #         self.pla4_buttons[i].onclick = lambda event : self.addToGuess(event,i+1)
        #         self.pla4_boxes[i].add(self.pla4_buttons[i])
                
        #     for i in range(3):
        #         self.manager.add(
        #             arcade.gui.UIAnchorWidget(
        #                 anchor_x="center",
        #                 anchor_y="top",
        #                 align_x= 100-i*100,
        #                 align_y= -350,
                        
        #                 child=self.pla4_boxes[i])
        #         )

        #     self.pla5_boxes = [0,0,0,0,0,0]
        #     self.pla5_buttons = [0,0,0,0,0,0]
        #     for i in range(6):
        #         self.pla5_boxes[i] = arcade.gui.UIBoxLayout()
        #         self.pla5_buttons[i] = arcade.gui.UIFlatButton(text="",
        #                                             width=75,height=75,style=self.styles[0])
        #         self.pla5_boxes[i].add(self.pla5_buttons[i])
                
        #     for i in range(6):
        #         self.manager.add(
        #             arcade.gui.UIAnchorWidget(
        #                 anchor_x="center",
        #                 anchor_y="top",
        #                 align_x= 250-i*100,
        #                 align_y= -225,
                        
        #                 child=self.pla5_boxes[i])
        #         )
        #     self.isMessing = True
        # print(self.game.player2.bird)
        # player = self.game.player1
        # opponent = self.game.player2
        # check, guess_bird = player.guessBird(opponent)
        # if check:
        #     print(f"{player.name} guessed {opponent.name}'s code, {guess_bird}! {opponent.name} is now dead!")
        #     self.isWinner =True;
        #     self.updnine();
            
        #     self.wins(player,opponent)
        # else:
        #     print(f"{player.name} tried to guess {opponent.name}'s code as {guess_bird}, but was wrong!")
        if not self.isWinner:
            self.updnine();
    def addToGuess(self,event,i):
        print("AHHHH")
        self.guess += str(i) 
        self.pla5_buttons[len(self.guess)-1] = arcade.gui.UIFlatButton(text="",
                                                    width=75,height=75,style=self.styles[i])
        if len(self.guess)==6:
            player = self.game.player1
            opponent = self.game.player2
            check, guess_bird = player.guessBird(opponent)
            if check:
                print(f"{player.name} guessed {opponent.name}'s code, {guess_bird}! {opponent.name} is now dead!")
                
                self.wins()
            else:
                print(f"{player.name} tried to guess {opponent.name}'s code as {guess_bird}, but was wrong!")
            self.guess = ""
            
    def updnine(self):
        
        if self.game.prompt(self.game.player1,self.game.player2):
            self.game.winner = self.game.player1
            self.isWinner = True
            
        if self.isWinner == False and self.game.prompt(self.game.player2,self.game.player1):
            self.game.winner = self.game.player2
            self.isWinner = True
        if self.isWinner:
            self.wins()
    
        # if act==0:
        #     self.game.player1.gunBird(self.game.player2)
        #     self.game.player2.gunBird(self.game.player1)
        # if act==1:
        #     self.game.player1.knifeBird(self.game.player2)
        #     self.game.player2.knifeBird(self.game.player1)
        # if act==2:
        #     self.game.player1.scareBird()
        #     self.game.player2.scareBird()
        # if act==3:
        #     self.game.player1.usurpBird()
        #     self.game.player2.usurpBird()
        # if act==4:
            
        #     player = self.game.player1
        #     opponent = self.game.player2
        #     check, guess_bird = player.guessBird(opponent)
        #     if check:
        #         print(f"{player.name} guessed {opponent.name}'s code, {guess_bird}! {opponent.name} is now dead!")
        #         self.wins(player,opponent)
        #     else:
        #         print(f"{player.name} tried to guess {opponent.name}'s code as {guess_bird}, but was wrong!")

        #     player = self.game.player2
        #     opponent = self.game.player1
        #     check, guess_bird = player.guessBird(opponent)
        #     if check:
        #         print(f"{player.name} guessed {opponent.name}'s code, {guess_bird}! {opponent.name} is now dead!")
        #         self.wins(player,opponent)
        #     else:
        #         print(f"{player.name} tried to guess {opponent.name}'s code as {guess_bird}, but was wrong!")
        for i in range(self.length):
            if self.game.player2.guessState[i]==2:
                
                self.enn_boxes[i].remove(self.enn_buttons[i])
                self.enn_buttons[i] = arcade.gui.UIFlatButton(text="",
                                               width=75,height=75,style=self.styles[int(self.game.player2.bird[i])])
                self.enn_boxes[i].add(self.enn_buttons[i])
            else:
                
                self.enn_boxes[i].remove(self.enn_buttons[i])
                self.enn_buttons[i] = arcade.gui.UIFlatButton(text="",
                                               width=75,height=75,style=self.styles[0])
                self.enn_boxes[i].add(self.enn_buttons[i])
                
        for i in range(self.length):
            if self.game.player1.guessState[i]==2:
                
                self.pla2_boxes[i].remove(self.pla2_buttons[i])
                self.pla2_buttons[i] = arcade.gui.UIFlatButton(text="",
                                               width=75,height=75,style=self.styles[int(self.game.player1.bird[i])])
                self.pla2_boxes[i].add(self.pla2_buttons[i])
            else:
                
                self.pla2_boxes[i].remove(self.pla2_buttons[i])
                self.pla2_buttons[i] = arcade.gui.UIFlatButton(text="",
                                               width=75,height=75,style=self.styles[0])
                self.pla2_boxes[i].add(self.pla2_buttons[i])
            
        for i in range(self.length):
            
                self.pla_boxes[i].remove(self.pla_buttons[i])
                self.pla_buttons[i] = arcade.gui.UIFlatButton(text="",
                                               width=75,height=75,style=self.styles[int(self.game.player1.bird[i])])
                self.pla_boxes[i].add(self.pla_buttons[i])
        if self.isWinner:
            print(f"{self.game.winner.name} has won!")

    def wins(self):
        for i in range(self.game.player1.bird_size):
            self.game.player1.guessState[i] = 2
            self.game.player2.guessState[i] = 2
        
        

    def on_draw(self):
        self.clear()
        self.manager.draw()
    
   