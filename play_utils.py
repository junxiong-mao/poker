from random import shuffle
from poker import Card, face, suit

code_to_suit_map = {
    'S': '♠︎',
    'H': '♥︎',
    'C': '♣︎',
    'D': '♦︎'
}


def construct_deck():
    deck = []
    for f in face:
        for s in suit:
            deck.append(Card(f, s))
    
    # Shuffle the deck for 10 times
    for i in range(10):
        shuffle(deck)
    
    return deck

def deal_card(deck, num):
    dealt_card = []
    for i in range(num):
        dealt_card.append(deck.pop())
    
    return dealt_card

def parse_hand(starting_hand):
    cards = starting_hand.split()
    hand = []
    if len(cards) != 2:
        return False
    
    for card in cards:
        suit = card[-1]
        face = card[0:-1]
        hand.append(Card(face, suit))
    
    return hand
