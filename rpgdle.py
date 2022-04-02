
import random
import time
from tokenize import maybe
import arcade
GAME_CARDS = ["FUNNN","KNIFE","SCARE","USURP"]
NUMTOBIRD= {1:"B",2:"G",3:"R"}
BIRDTONUM = {"B":1,"G":2,"R":3}
RAINBOW = [(100,100,100),arcade.color.DARK_RED,arcade.color.DARK_ORANGE,arcade.color.GOLD,arcade.color.DARK_GREEN,arcade.color.DARK_BLUE,arcade.color.DARK_PASTEL_PURPLE]
def createBird(poss,length):
    bird = ""
    for _ in range(length):
        poss_worm = random.randint(1,poss)
        while (bird.count(str(poss_worm)) >length/3):
            poss_worm = random.randint(1,poss)
        bird += str(poss_worm)
    return bird

class Player():
    def __init__(self, isPlayer,name,size,rang) :
        self.name = name
        self.isPlayer = isPlayer
        self.bird_size=size
        self.bird_range=rang
        self.bird = createBird(self.bird_range,self.bird_size)
        self.lettered = ""
        for char in self.bird:
            if char=="1":
                self.lettered += "B"
            if char=="2":
                self.lettered += "G"
            if char=="3":
                self.lettered += "R"
        self.guessState = []
        self.cards = []
        self.all_cards = []
        self.card_count = [7,7,3,4]
        self.sym_counts = []
        for i in range(self.bird_range):
            self.sym_counts.append(-1)
        for i in range(len(GAME_CARDS)):
            for _ in range(self.card_count[i]):
                self.all_cards.append(GAME_CARDS[i])

        self.limited = ["SCARE","USURP"]
        for card in GAME_CARDS:
            self.cards.append(card)
        for _ in range(self.bird_size):
            self.guessState.append(0)
    def showBird(self):
        shown = "-"
        shown2 = "-"
        for i in range(self.bird_size):
            if self.guessState[i]:
                shown+=self.lettered[i]
            else:
                shown+="?"
            shown2+=self.lettered[i]
            shown2+="-"
            shown+="-"
       
        print(f"----{shown}----")
        if self.isPlayer:
            print(f"----{shown2}----")
    def gunBird(self, target, key = -1):
        if key == -1:
            if self.isPlayer:
                spot = input(f"Choose a spot (1-{self.bird_size}) to reveal: ")
                while not spot.isnumeric():
                    spot = input(f"Invalid input, try again: ")
                spot = int(spot)
                while (target.guessState[spot-1]==2 or spot<1 or spot>self.bird_size):
                    if target.guessState[spot-1]==2:
                        spot = input("That spot has already been revealed! Try again: ")
                    else:
                        spot = input(f"Invalid input, try again: ")
                    while not spot.isnumeric():
                        spot = input(f"Invalid input, try again: ")
                    spot = int(spot)
            else:
                spot = random.randint(1,self.bird_size)
                count = 0
                while target.guessState[spot-1]==2 and count < 100:
                    spot = random.randint(1,self.bird_size)
                    count +=1
            target.guessState[spot-1] = 2
            print(f"{self.name} revealed {target.name}'s color #{spot}, which is {target.lettered[spot-1]}!")
        else:
            spot = key
            target.guessState[spot-1] = 2
            print(f"{self.name} revealed {target.name}'s color #{spot}, which is {target.lettered[spot-1]}!")

    def knifeBird(self,target, key=-1):
        if key == -1:
            if self.isPlayer:
                cow = (input(f"Choose a color (R,B,G) to count: "))
                while (cow != "R" and cow!="B" and cow!="G"):
                    cow = (input(f"Invalid input, try again: "))
                cow = BIRDTONUM[cow];
            else:
                cow = random.randint(1,self.bird_range)
                count =0
                while (target.sym_counts[cow-1]!=-1 and count<self.bird_range):
                    cow = random.randint(1,self.bird_range)
                    count += 1
            
            
            target.sym_counts[cow-1]=target.bird.count(str(cow))
            cow = str(cow)
            if (target.bird.count(cow)!=1):
                print(f"{self.name} found out that {target.name} has {target.bird.count(cow)} {NUMTOBIRD[int(cow)]}s!")
            else:
                print(f"{self.name} found out that {target.name} has one {NUMTOBIRD[int(cow)]}!")
        else:
            cow = str(key)
            if (target.bird.count(cow)!=1):
                print(f"{self.name} found out that there are {target.bird.count(cow)} {NUMTOBIRD[cow]}s!")
            else:
                print(f"{self.name} found out that there is one {NUMTOBIRD[cow]}!")

    def scareBird(self):
        temp = list(self.bird)
        random.shuffle(temp)
        self.bird = ''.join(temp)
        for _ in range(self.bird_size):
            self.guessState[_] = 0
        print(f"{self.name}'s colors have been shuffled!")
    
    def usurpBird(self, key=-1):
        if key==-1:
            if self.isPlayer:
                spot = input(f"Choose a spot (1-{self.bird_size}) to swap out: ")
                while not spot.isnumeric():
                    spot = input(f"Invalid input, try again: ")
                spot = int(spot)
                while (spot<1 or spot>self.bird_size):
                    
                    spot = input(f"Invalid input, try again: ")
                    while not spot.isnumeric():
                        spot = input(f"Invalid input, try again: ")
                    spot = int(spot)
            else:
                spot = random.randint(1,self.bird_size)
                while self.guessState.count(2) and self.guessState[spot-1]!=2:
                    spot = random.randint(1,self.bird_size)
        
            for i in range(self.bird_range):
                self.sym_counts[i] = -1
            self.guessState[spot-1] = 0
            self.bird = self.bird[:spot-1] + str(random.randint(1,self.bird_range)) + self.bird[spot:]
            print(f"{self.name} has changed their color #{spot}!")
        else:
            spot = key
            for i in range(self.bird_range):
                self.sym_counts[i] = -1
            self.guessState[spot-1] = 0
            self.bird = self.bird[:spot-1] + str(random.randint(1,self.bird_range)) + self.bird[spot:]
            print(f"{self.name} has changed their color #{spot}!")
        
        

    def guessBird(self,target, key=-1):
        #print(target.lettered)
        def check(bird):
            for i in range(target.bird_range):
                if target.sym_counts[i] !=-1:
                    if target.sym_counts[i] != bird.count(str(i+1)):
                        #print(bird)
                        return False
            for i in range(target.bird_size):
                if target.guessState[i]==2:
                    if target.bird[i] != bird[i]:
                        #print(bird)
                        return False
            return True
        if key==-1:
            if self.isPlayer:
                guess = input("Guess your opponent's code! (ex: BGBRGG)\n")
            else:
                bird = ""
                for _ in range(target.bird_size):
                    poss_worm = random.randint(1,target.bird_range)
                    bird += str(poss_worm)
                while (not check(bird)):
                    bird = ""
                    for _ in range(target.bird_size):
                        poss_worm = random.randint(1,target.bird_range)
                        bird += str(poss_worm)
                temp = ""
                for char in bird:
                    temp+=NUMTOBIRD[int(char)]
                guess = temp
            return guess == target.lettered, guess
        else:        
            return guess == target.bird, guess
        
        
    
    




    
class Game():
    def __init__(self,size,rang) :
        
        self.player1 = Player(1,"PLAYER",size,rang)
        self.winner = self.player1
        self.player2 = Player(0,"COMPUTER",size,rang)
        self.isGoing = True;
        
    def showGame(self):
        print("_________________________\n")
        print(f"{self.player2.name}:")
        print()
        self.player2.showBird()
        print()
        print(f"{self.player1.name}:")
        print()
        self.player1.showBird()
        print()
        print("_________________________")
    
    def prompt(self, player,opponent):
        if player.isPlayer:
            print()
            print("Choose an option!")
            print()
            random.shuffle(player.all_cards)
            while player.all_cards[0]==player.all_cards[1]:
                random.shuffle(player.all_cards)
            card_dis = "---"
            while (len(player.cards)):
                player.cards.pop()
            for i in range(2):
                card_dis += player.all_cards[i]
                player.cards.append(player.all_cards[i])
                card_dis += "---"
            card_dis += "GUESS" +"---\n"
            player.cards.append("GUESS")
            print(card_dis)
            choice = input()
            while choice not in player.cards:
                choice = input("That's not a valid option!\n")
            if choice in player.limited:   
                player.all_cards.remove(choice)
            print()
            choice=choice.upper()
            if choice == "FUNNN":
                player.gunBird(opponent)
            elif choice == "KNIFE":
                player.knifeBird(opponent)
            elif choice == "SCARE":
                player.scareBird()
            elif choice == "USURP":
                player.usurpBird()
            elif choice =="GUESS":
                check, guess_bird = player.guessBird(opponent)
                if check:
                    print(f"{player.name} guessed {opponent.name}'s code, {guess_bird}! {opponent.name} is now dead!")
                    return True
                else:
                    print(f"{player.name} tried to guess {opponent.name}'s code as {guess_bird}, but was wrong!")
            return False
        else:
            random.shuffle(player.all_cards)
            
            while (len(player.cards)):
                player.cards.pop()
            for i in range(2):
                player.cards.append(player.all_cards[i])
            player.cards.append("GUESS")
           
            if sum(opponent.guessState)==opponent.bird_size*2:
                choice = "GUESS"

                print(f"{player.name} guessed {opponent.name}'s code, {opponent.bird}!\n {opponent.name} is now dead!")
                return True
            else:
                
                choice=player.cards[random.randint(0,len(player.cards)-2)]
                isGood = 1
                for i in range(opponent.bird_range):
                    if opponent.sym_counts[i] == -1:
                        isGood = 0
                        break
                
                if "USURP" in player.cards and player.guessState.count(2)>=3:
                    choice = "USURP"
                if "USURP" in player.cards and player.guessState.count(2)<3:
                    if player.cards[0] == "USURP":
                        choice = player.cards[1]
                    else:
                        choice = player.cards[0]
                    if (not random.randint(0,3)):
                        choice = "GUESS"
                if "SCARE" in player.cards and player.guessState.count(2)>=3:
                    choice = "SCARE"
                if "SCARE" in player.cards and player.guessState.count(2)<3:
                    if player.cards[0] == "SCARE":
                        choice = player.cards[1]
                    else:
                        choice = player.cards[0]
                    if (not random.randint(0,3)):
                        choice = "GUESS"
                if "KNIFE" in player.cards and isGood:
                    if player.cards[0] == "KNIFE":
                        choice = player.cards[1]
                    else:
                        choice = player.cards[0]
                    if (not random.randint(0,3)):
                        choice = "GUESS"
                
                maybe_guess = random.randint(1,opponent.bird_range+2-opponent.guessState.count(2))
                if maybe_guess == 1:
                    choice = "GUESS"
                   # print("hi")

                
                
            if choice == "FUNNN":
                player.gunBird(opponent)
            elif choice == "KNIFE":
                player.knifeBird(opponent)
            elif choice == "SCARE":
                player.scareBird()
            elif choice == "USURP":
                player.usurpBird()
            elif choice == "GUESS":
                check, guess_bird = player.guessBird(opponent)
                if check:
                    print(f"{player.name} guessed {opponent.name}'s code, {guess_bird}! {opponent.name} is now dead!")
                    return True
                else:
                    print(f"{player.name} tried to guess {opponent.name}'s code as {guess_bird}, but was wrong!")
        
            return False
            


def main():
    game = Game(6,3)
    
    while game.isGoing:
        game.showGame()
       
        if game.prompt(game.player1,game.player2):
            game.winner = game.player1
            break
        if game.prompt(game.player2,game.player1):
            game.winner = game.player2
            break
    for i in range(game.player1.bird_size):
        game.player1.guessState[i] = 2
        game.player2.guessState[i] = 2
    game.showGame()
    print(f"{game.winner.name} has won!")
        
# main()