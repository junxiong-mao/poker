from poker import suit, face
from simulate_single_hand import simulate_single_hand
from play_utils import construct_deck, deal_card, parse_hand
import getopt
import csv
import sys

def print_help():
    print('Usage:')
    print('python3 simulate_all.py -r|--rounds <simulation round>')

def construct_hands():
    global suit
    suit = suit[0:2]
    cards = []
    hands = []

    for f in face:
        for s in suit:
            cards.append(f + s)
    
    for d1 in cards:
        for d2 in cards:
            if d1 != d2:
                hands.append(d1 + ' ' + d2)
    
    return hands

def main(argv):
    rounds = None

    try:
        opts, args = getopt.getopt(argv, "hr:", ['help', 'rounds='])
    except getopt.GetoptError:
        print_help()
        return

    for opt, arg in opts:
        if opt == '-h':
            print_help()
            return
        elif opt in ('-r', '--rounds'):
            rounds = arg

    if rounds is None:
        print('Please specify simulation rounds')
        print_help()
        return

    rounds = int(rounds)

    hands = construct_hands()
    win_dict = {}
    for hand in hands:
        starting_hand = parse_hand(hand)
        rate = simulate_single_hand(starting_hand, 2, rounds, False)
        face1 = starting_hand[0].face
        face2 = starting_hand[1].face
        faces = face1 + face2
        suit1 = starting_hand[0].suit
        suit2 = starting_hand[1].suit
        if suit1 == suit2:
            suits = 'o'
        else:
            suits = 's'
        summary = faces + ',' +  suits
        win_dict[summary] = rate
    
    sorted_win_dict = sorted(win_dict.items(), key=lambda kv: kv[1], reverse=True)

    with open('simulate_all_%s.csv' % rounds, mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        for tup in sorted_win_dict:
            csv_writer.writerow([tup[0], tup[1]])
            
if __name__ == "__main__":
    main(sys.argv[1:])
