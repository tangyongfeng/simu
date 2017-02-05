
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}
ROUNDSTATE =('WAIT','DEAL','HIT','OUTOFMONEY')
PLAYER_ACTION=('H','S','P','D')
JUDGMENTS =('PLAYER_WIN','DEALER_WIN','PUSH','PLAYER_BLACKJACK')

class Card:
    def __init__(self, suit, rank):

        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print ("Invalid card: ", suit, rank)

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank


class Hand:
    def __init__(self):
        self.handlist=[]        # create Hand object

    def __str__(self):
        ans = ""
        for i in range(len(self.handlist)):
            ans += str(self.handlist[i])
        return ans# return a string representation of a hand
    def get_count(self):
        return len(self.handlist)
    def add_card(self, card):
        self.handlist.append(card)      # add a card object to a hand

    def get_value(self):
        global sum
        sum=0
        for i in self.handlist:
            sum+=VALUES[i.rank]
        for i in self.handlist:
            if i.rank == 'A':
                if sum+10<=21:
                    sum+=10 #count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        return sum# compute the value of the hand, see Blackjack video

