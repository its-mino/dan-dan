class Player:
    hand = None
    battlefield = None

    def __init__(self):
        self.hand = []
        self.battlefield = []

    def reset(self):
        self.hand = []
        self.battlefield = []

    def getHand(self):
        return self.hand

    def getBattlefield(self):
        return self.battlefield

    def addCardToHand(self, card):
        self.hand.append(card)

    def removeCardFromHand(self, num):
        self.hand.remove(num)

    def addCardToBattlefield(self, card):
        self.battlefield.append(card)

    def removeCardFromBattlefield(self, num):
        self.battlefield.remove(num)

