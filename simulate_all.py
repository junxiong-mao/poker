from poker import suit, face
from simulate_single_hand import simulate_single_hand
from play_utils import construct_deck, deal_card, parse_hand

ROUNDS = 10

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

def main():
    hands = construct_hands()
    win_dict = {}
    for hand in hands:
        starting_hand = parse_hand(hand)
        rate = simulate_single_hand(starting_hand, 2, ROUNDS, False)
        win_dict[hand] = rate
    
    sorted_win_dict = sorted(win_dict.items(), key=lambda kv: kv[1])
            
    print(sorted_win_dict)



if __name__ == "__main__":
    main()
