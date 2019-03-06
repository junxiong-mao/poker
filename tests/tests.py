import sys
sys.path.append("../")
import poker
import unittest
from poker import Card

code_to_suit_map = {
    'S': '♠︎',
    'H': '♥︎',
    'C': '♣︎',
    'D': '♦︎'
}

test_hands = [
    ('2S 3S 4S 5S 6S 7S 8S', (poker.HandType.STRAIGHT_FLUSH, ['8'])),
    ('2S 2H 2C 5C 7D 9H 10D', (poker.HandType.THREE_OF_A_KIND, ['2', '10', '9']))
]

def format_hand(hand_str):
    hand = []
    hand_list = hand_str.split()
    for card in hand_list:
        symbol = code_to_suit_map[card[-1]]
        face = card[0:-1]
        hand.append(Card(face, symbol))
    
    return hand

class PokerTests(unittest.TestCase):
    def test_ranker(self):
        for test_hand in test_hands:
            hand_str = test_hand[0]
            hand = format_hand(hand_str)
            result = False
            for ranker in poker.handrankorder:
                result = ranker(hand)
                if result != False:
                    break
            
            self.assertEqual(result, test_hand[1])

if __name__ == '__main__':
    unittest.main()