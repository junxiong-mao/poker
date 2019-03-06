import poker
from poker import Card, face, suit
from random import shuffle

#Configuration
starting_hand = [Card('k', '♦︎'), Card('k', '♥︎')]
opponents_num = 1
simulation_rounds = 10000


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

if __name__ == '__main__':
    win = 0
    for i in range(simulation_rounds):
        deck = construct_deck()
        deck.remove(starting_hand[0])
        deck.remove(starting_hand[1])
        hands = []
        hands.append(starting_hand)
        
        for i in range(opponents_num):
            dealt_card = deal_card(deck, 2)
            hands.append(dealt_card)
        
        public_cards = deal_card(deck, 5)
        winner_hand = poker.rank(hands, public_cards)[0]
        if winner_hand == starting_hand:
            win += 1
    
    print(win / simulation_rounds)
