import sys
sys.path.append("../")
import poker
import unittest
from poker import Card
from play_utils import code_to_suit_map

ranker_tests = [
    ('2S 3S 4S 5S 6S 7S 8S', (poker.HandType.STRAIGHT_FLUSH, ['8'])),
    ('aS 2H 3C 4D 5S 10S jS', (poker.HandType.STRAIGHT, ['5'])),
    ('2H 3C 10D jH qC kC aD', (poker.HandType.STRAIGHT, ['a'])),
    ('2S 2H 2C 5C 7D 9H 10D', (poker.HandType.THREE_OF_A_KIND, ['2', '10', '9'])),
    ('2S 2H 10S 10H aD aH 5C', (poker.HandType.TWO_PAIR, ['a', '10', '5'])),
    ('2S 2H aS 10H 9C 8D 5S', (poker.HandType.ONE_PAIR, ['2', 'a', '10', '9'])),
    ('2S 4D aC jH qD 9H 5S', (poker.HandType.HIGH_CARD, ['a', 'q', 'j', '9', '5'])),
    #TODO: Add more tests
]

rank_tests = [
    (['5S 5D', '5C 6H'], '5H 6D 6C aD kH', [('5C 6H', poker.HandType.FULL_HOUSE), ('5S 5D', poker.HandType.FULL_HOUSE)]),
    (['5S 5D', 'jC 6H'], 'aH 6D 6C aD kH', [('jC 6H', poker.HandType.FULL_HOUSE), ('5S 5D', poker.HandType.TWO_PAIR)]),
    #TODO: Add more tests
]

def format_cards(cards_str):
    hand = []
    hand_list = cards_str.split()
    for card in hand_list:
        symbol = card[-1]
        face = card[0:-1]
        hand.append(Card(face, symbol))
    
    return hand

class PokerTests(unittest.TestCase):
    def test_ranker(self):
        for sample in ranker_tests:
            hand = format_cards(sample[0])
            result = False
            for ranker in poker.handrankorder:
                result = ranker(hand)
                if result != False:
                    break
            
            self.assertEqual(result, sample[1])

    def test_rank(self):
        for sample in rank_tests:
            hands = []
            result = []
            for cards_str in sample[0]:
                hands.append(format_cards(cards_str))
            public_cards = format_cards(sample[1])
            for semi_result in sample[2]:
                result.append((format_cards(semi_result[0]), semi_result[1]))
            self.assertEqual(result, poker.rank(hands, public_cards))
