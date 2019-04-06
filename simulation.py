import poker
import sys, getopt
from poker import Card, face, suit
from random import shuffle

code_to_suit_map = {
    'S': '♠︎',
    'H': '♥︎',
    'C': '♣︎',
    'D': '♦︎'
}

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

def parse_hand(starting_hand):
    cards = starting_hand.split()
    hand = []
    if len(cards) != 2:
        return False
    
    for card in cards:
        suit = code_to_suit_map[card[-1]]
        face = card[0:-1]
        hand.append(Card(face, suit))
    
    return hand

def print_help():
    print("Usage:")
    print("python3 simulation -p|--player <player number> -r|--round <simulation round> -s|--starting_hand <starting hand> ")
    return

def main(argv):
    player = None
    starting_hand = None
    # By default takes 10000 rounds
    rounds = 10000

    try:
        opts, args = getopt.getopt(argv, "hp:s:r:", ['help', 'player=', 'starting_hand=', 'rounds'])
    except getopt.GetoptError:
        print_help()
        return
    
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            return
        elif opt in ('-p', '--player'):
            player = arg
        elif opt in ('-s', '--starting_hand'):
            starting_hand = arg
        elif opt in ('-r', '--rounds'):
            rounds = arg

    if player == None:
        print('Please provide player number!')
        print_help()
        return
    
    if starting_hand == None:
        print('Please provide starting hand')
        print_help()
        return

    try:
        starting_hand = parse_hand(starting_hand)
    except:
        print_help()
        return

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

if __name__ == "__main__":
    main(sys.argv[1:])