""""
    Desc: A blackjack game that utilizes tkinter. More info in rules"""


import tkinter as tk
import PIL.Image
from PIL import ImageTk
from tkinter import *
import random
from random import randrange

# By using states, buttons have to pressed at appropriate times
STATE_OF_GAME = 'start'  # start / play / end

# Makes the table by filling a grid of 12x5 with a green image
class background:
    def __init__(self, root):
        self.root = root
        self.y = []
        #img = Image.open("cards/" + "green2.png")
        img = PIL.Image.open("cards/" + "green2.png")
        img = img.resize((80, 120))
        #tkimage = ImageTk.PhotoImage(img)
        tkimage = PIL.ImageTk.PhotoImage(img)
        self.y.append(hold(img, tkimage, -1))
        for i in range(12):
            for j in range(5):
                #root.configure(background='black')
                tk.Label(self.root, background='green4',
                         image=self.y[0].b).grid(
                             row=j, column=i)  #<--just a long line continued

# Buttons
        button_1 = Button(root, text="HIT", command=lambda: dealFromButton(p1))
        # put buttons on the screen by row and column
        button_1.grid(row=2, column=5)

        button_2 = Button(root, text="STAY", command=lambda: passButtonHandler())
        # put buttons on the screen by row and column
        button_2.grid(row=2, column=6)

        button_3 = Button(root, text="PLAY", command=lambda: playButtonHandler())
        # put buttons on the screen by row and column
        button_3.grid(row=2, column=4)

        button_4 = Button(root, text="END", command=lambda: clearButtonHandler(self))
        # put buttons on the screen by row and column
        button_4.grid(row=2, column=7)

        # Text

        # Player score
        self.player_entry = tk.Entry(self.root, width=5)
        self.player_entry.grid(row=3, column=0)
        self.player_entry.delete(0, tk.END)
        self.player_entry.insert(0, "Player")

        # Dealer score
        self.dealer_entry = tk.Entry(self.root, width=5)
        self.dealer_entry.grid(row=1, column=0)
        self.dealer_entry.delete(0, tk.END)
        self.dealer_entry.insert(0, "Dealer")

        # Balance
        balance_label = tk.Label (self.root,text = "Balance",width = 6) 
        balance_label.grid(row=1,column=10)
        self.balance_entry = tk.Entry(self.root, width=6)
        self.balance_entry.grid(row=1, column=11)
        self.balance_entry.delete(0, tk.END)
        if STATE_OF_GAME == 'start':
          self.balance_entry.insert(0, "500")

        # Enter bet
        self.bet_entry = tk.Entry(self.root, width=7)
        self.bet_entry.grid(row=2, column=11)
        self.bet_entry.delete(0, tk.END)
        self.bet_entry.insert(0, "Enter bet")

        # Winner
        self.winner_entry = tk.Entry(self.root, width=6)
        self.winner_entry.grid(row=2, column=0)
        self.winner_entry.delete(0, tk.END)
        self.winner_entry.insert(0, "Winner")

        # Winnings
        winnings_label = tk.Label (self.root,text = "Winnings",width = 7) 
        winnings_label.grid(row=3,column=10)
        self.winnings_entry = tk.Entry(self.root, width=7)
        self.winnings_entry.grid(row=3, column=11)
        self.winnings_entry.insert(0, "0")

player_balance = 500
winnings = 0
# Finds score of a hand
def calculateScore(hand):
    score = 0
    ace_number = 0
    for i in range(len(hand)):
        card = hand[i].c
        value = card % 13
        value = int(value)
        value = value + 2
        if value >= 11 and value <= 13:
            value = 10
        elif value > 13:
            value = 11
            ace_number += 1
        score = score + value
        while score > 21 and ace_number > 0:
            score -= 10
            ace_number -= 1
    return score


#Bet takes in number only
def numberCheck():
    global player_balance
    bet = table.bet_entry.get()
    if bet.isdigit() and int(bet)<= int(player_balance):
        return True
    else:
        return False

# Handles Hit button
def dealFromButton(player):
    global STATE_OF_GAME, player_balance, winnings 
    if STATE_OF_GAME == 'play':
        score = calculateScore(player.hand)

        # Deals cards only if it is under 21
        if score < 21:
            player.hand.append(h.dealCard())
            new_score = calculateScore(player.hand)
            showHandPlayer()

            # If player busts, dealer's cards are revealed
            if new_score >= 21:
                showHandDealer()
                dealer_score = calculateScore(d.hand)
                showScoreDealer()

                # If dealer has natural, winner is decided
                if dealer_score == 21:
                    winner = "Dealer"

                    # Calculates balance and bet
                    player_bet = table.bet_entry.get()
                    winnings -= int(player_bet)
                    player_balance -= int(player_bet)
                    table.balance_entry.delete(0, tk.END)
                    table.balance_entry.insert(1, str(player_balance))

                    table.winnings_entry.delete(0, tk.END)
                    table.winnings_entry.insert(1, str(winnings))
                    # Displays dealer as winner
                    table.winner_entry.delete(0, tk.END)
                    table.winner_entry.insert(1, winner)
                else:
                    # If dealer is under 17, they have to hit
                    while dealer_score < 17:
                        d.hand.append(h.dealCard())
                        dealer_score = calculateScore(d.hand)
                        showHandDealer()
                        showScoreDealer()
                    winner = isWinner()
                    player_bet = table.bet_entry.get()

                    if winner == "PLAYER":
                      player_balance += int(player_bet)
                      winnings += int(player_bet)
                    elif winner == "DEALER":
                      player_balance -= int(player_bet)
                      winnings -= int(player_bet)
                    else:
                      player_balance = int(player_balance)
                      winnings = int(winnings)

                    showScoreDealer()

                    table.balance_entry.delete(0, tk.END)
                    table.balance_entry.insert(1, str(player_balance))

                    table.winnings_entry.delete(0, tk.END)
                    table.winnings_entry.insert(1, str(winnings))
                    
                    table.winner_entry.delete(0, tk.END)
                    table.winner_entry.insert(1, winner)


def passButtonHandler():
    global STATE_OF_GAME, player_balance, winnings
    if STATE_OF_GAME == 'play':
        STATE_OF_GAME = 'end'
        showHandDealer()
        showScoreDealer()
        dealer_score = calculateScore(d.hand)
        
        while dealer_score < 17:
            showHandDealer()
            d.hand.append(h.dealCard())
            showHandDealer()
            dealer_score = calculateScore(d.hand)
            showScoreDealer()
            
        winner = isWinner()
        player_bet = table.bet_entry.get()
        if winner == "PLAYER":
          player_balance += int(player_bet)
          winnings += int(player_bet)
        elif winner == "DEALER":
          player_balance -= int(player_bet)
          winnings -= int(player_bet)
        else:
          player_balance = int(player_balance)
          winnings = int(winnings)
        table.balance_entry.delete(0, tk.END)
        table.balance_entry.insert(1, str(player_balance))
        table.winnings_entry.delete(0, tk.END)
        table.winnings_entry.insert(1, str(winnings))
        table.winner_entry.delete(0, tk.END)
        table.winner_entry.insert(1, winner)


def playButtonHandler():
    global player_balance, winnings
    global STATE_OF_GAME
    if STATE_OF_GAME == 'start' and numberCheck():
        STATE_OF_GAME = 'play'
        for i in range(2):
            p1.hand.append(h.dealCard())
            d.hand.append(h.dealCard())
        showHandDealer(hide=True)
        showHandPlayer()
        
        #Player Natural
        score = calculateScore(p1.hand)
        if score == 21:
            dealer_score = calculateScore(d.hand)
            showHandDealer()
            showScoreDealer()

            if dealer_score == 21:
                winner = "Tie"
                table.winner_entry.insert(1, winner)
                dealer_score = calculateScore(d.hand)
                # No changes made to bet
            else:
              table.dealer_entry.delete(0, tk.END)
              table.dealer_entry.insert(1, str(dealer_score))
              winner = "Player"
              # Displays relevant info
              table.winner_entry.delete(0, tk.END)
              table.winner_entry.insert(1, winner)
              player_bet = table.bet_entry.get()
              player_balance += 1.5 * int(player_bet)
              winnings += 1.5 * int(player_bet)
              # natural gets 1.5x the bet
              table.balance_entry.delete(0, tk.END)
              table.balance_entry.insert(1, str(player_balance))
              table.winnings_entry.delete(0, tk.END)
              table.winnings_entry.insert(1, str(winnings))


def clearButtonHandler(self):
    global STATE_OF_GAME
    global p1, d, h, table
    
    #if STATE_OF_GAME == 'end':
    STATE_OF_GAME = 'start'
    # load = LoadDeck()
    p1 = player("player1", 500,0)
    d = player("dealer", 5000,0)
    h = House("house1")

    
    table.winner_entry.delete(0, tk.END)
    self.winner_entry.insert(0, "Winner")
    table.player_entry.delete(0, tk.END)
    self.player_entry.insert(0, "Player")
    table.dealer_entry.delete(0, tk.END)
    self.dealer_entry.insert(0, "Dealer")

    #Puts green squares over cards to clear space
    for i in range(12):
        #root.configure(background='black')
        tk.Label(self.root, background='green4',
                 image=self.y[0].b).grid(row=0, column=i)
        tk.Label(self.root, background='green4',
                 image=self.y[0].b).grid(row=4, column=i)


def showHandPlayer():
  #Displays player's hand
    x = p1.hand
    for i in range(len(x)):
        tk.Label(root, image=x[i].b).grid(row=4, column=i)
    score = calculateScore(p1.hand)
    table.player_entry.delete(0, tk.END)
    table.player_entry.insert(1, str(score))


def showHandDealer(hide=False):
  #Displays dealer's hands
    x = d.hand
    for i in range(len(x)):
        if i == len(x) - 1 and hide:
          # When hide is true, a card back is shown instead 
            tk.Label(root, image=h.back_card.b).grid(row=0, column=i)
        else:
            tk.Label(root, image=x[i].b).grid(row=0, column=i)

def showScoreDealer():
  dealer_score = calculateScore(d.hand) 
  table.dealer_entry.delete(0, tk.END)
  table.dealer_entry.insert(1, str(dealer_score))


def isWinner():
  # Checks for winner 
    winner = ""
    if calculateScore(p1.hand) == 21 and calculateScore(d.hand) == 21:
        winner = "TIE"
        
    elif calculateScore(p1.hand) > 21 and calculateScore(d.hand) > 21:
        winner = "TIE"
        
    elif calculateScore(p1.hand) == 21:
        winner = "PLAYER"

    elif calculateScore(d.hand) == 21:
        winner = "DEALER"

    elif calculateScore(p1.hand) == calculateScore(d.hand):
        winner = "TIE"

    elif calculateScore(p1.hand) > calculateScore(d.hand) and calculateScore(
            p1.hand) < 21:
        winner = "PLAYER"

    elif calculateScore(p1.hand) > calculateScore(d.hand) and calculateScore(
            p1.hand) > 21:
        winner = "DEALER"

    elif calculateScore(d.hand) > calculateScore(p1.hand) and calculateScore(
            d.hand) < 21:
        winner = "DEALER"

    elif calculateScore(d.hand) > calculateScore(p1.hand) and calculateScore(
            d.hand) > 21:
        winner = "PLAYER"
    return winner


def retCardName(x):
    return face(x) + "_of_" + suit(x) + ".png"


def face(x):
    n = x % 13
    if (n >= 0 and n <= 8):
        return str(n + 2)
    elif (n == 9):
        return "jack"
    elif (n == 10):
        return "queen"
    elif (n == 11):
        return "king"
    elif (n == 12):
        return "ace"

def suit(x):
    # Determines the suit of the card
    if x < 14:
        return "clubs"
    elif x >= 14 and x < 27:
        return "diamonds"
    elif x >= 27 and x > 40:
        return "hearts"
    else:
        return "spades"


def LoadDeck():
  #Puts the deck into an array
    x = []
    for i in range(52):
        img = PIL.Image.open("cards/" + retCardName(i))
        img = img.resize((80, 120))
        tkimage = ImageTk.PhotoImage(img)
        x.append(hold(img, tkimage, i))
    return x

def get_back_card():
    # The card back is stored here
    img = PIL.Image.open("cards/card back.png")
    img = img.resize((80, 120))
    tkimage = ImageTk.PhotoImage(img)
    return hold(img, tkimage, 0)

#object created for each elt in image list (array)
class hold:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

class House:
    def __init__(self, name):
        self.name = name
        self.deck = self.shuffle(LoadDeck())
        self.back_card = get_back_card()

    def shuffle(self, deck):
        new_deck = []
        while len(deck) > 0:
            new_card = deck.pop(randrange(0, len(deck)))
            new_deck.append(new_card)
        return new_deck

    def dealCard(self):
        return self.deck.pop()

class player:
    def __init__(self, n, balance, bet):
        self.name = n
        self.balance = balance
        self.bet = bet
        self.hand = []

root = tk.Tk()
# load = LoadDeck()
p1 = player("player1", 500, 0)
d = player("dealer", 500,0)
h = House("house1")
table = background(root)