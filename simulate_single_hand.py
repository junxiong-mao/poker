import poker
import sys, getopt
from play_utils import construct_deck, deal_card, parse_hand

def print_help():
    print("Usage:")
    print("python3 simulate_single_hand.py -p|--player <player number> -r|--round <simulation round> -s|--starting_hand <starting hand> ")
    return

def simulate_single_hand(starting_hand, player, rounds, verbose):
    win = 0
    for i in range(rounds):
        deck = construct_deck()
        deck.remove(starting_hand[0])
        deck.remove(starting_hand[1])
        hands = []
        hands.append(starting_hand)
        
        for i in range(int(player) - 1):
            dealt_card = deal_card(deck, 2)
            hands.append(dealt_card)
        
        public_cards = deal_card(deck, 5)
        winner_hand = poker.rank(hands, public_cards)[0]
        
        if winner_hand[0] == starting_hand:
            winner = 'User'
            win += 1
        else:
            winner = 'Opponent'
        
        if verbose:
            print('----------------- round %s -----------------' % i) 
            print("User: %s     Opponents: %s" % (hands[0], hands[1:]))
            print("%s" % public_cards)
            print(winner_hand[1])
            print('Winner: %s %s' % (winner, winner_hand[0]))

    rate = win / rounds

    if verbose:
        print('----------------- SIMULATION RESULTS -----------------') 
        print('User with hand %s wins with rate: %s' % (starting_hand, rate))
    return rate

def main(argv):
    player = None
    starting_hand = None
    verbose = False

    try:
        opts, args = getopt.getopt(argv, "hp:s:r:v", ['help', 'player=', 'starting_hand=', 'rounds=', 'verbose'])
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
        elif opt in ('-v', '--verbose'):
            verbose = True

    if player == None:
        print('Please specify player number')
        print_help()
        return
    
    if starting_hand == None:
        print('Please provide starting hand')
        print_help()
        return

    if rounds == None:
        print('Please specify simulation rounds')
        print_help()
        return

    player = int(player)
    rounds = int(rounds)

    try:
        starting_hand = parse_hand(starting_hand)
    except:
        print_help()
        return

    simulate_single_hand(starting_hand, player, rounds, verbose)

if __name__ == "__main__":
    main(sys.argv[1:])
