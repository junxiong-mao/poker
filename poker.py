from collections import namedtuple
from collections import Counter
from enum import Enum

class Card(namedtuple('Card', 'face, suit')):
    def __repr__(self):
        return ''.join(self)

# suit = '♥︎ ♦︎ ♣︎ ♠︎'.split()
suit = 'H D C S'.split()
# ordered strings of faces
faces   = '2 3 4 5 6 7 8 9 10 j q k a'
lowaces = 'a 2 3 4 5 6 7 8 9 10 j q k'
# faces as lists
face   = faces.split()
lowace = lowaces.split()

class HandType(Enum):
    STRAIGHT_FLUSH = 0
    FOUR_OF_A_KIND = 1
    FULL_HOUSE = 2
    FLUSH = 3
    STRAIGHT = 4
    THREE_OF_A_KIND = 5
    TWO_PAIR = 6
    ONE_PAIR = 7
    HIGH_CARD = 8

def straight_flush(hand):
    suits = [card.suit for card in hand]
    suit_collections = Counter(suits)
    flush_suit = max(suit_collections.keys(), key=(lambda k: suit_collections[k]))
    if suit_collections[flush_suit] < 5:
        return False
    
    straight_faces = [card.face for card in hand if card.suit == flush_suit]
    if len(straight_faces) < 5:
        return False

    tie_breaker = False
    for f, fs in [(lowace, lowaces), (face, faces)]:
        straight_faces = sorted(straight_faces, key=lambda face: f.index(face))
        for trimed_faces in [straight_faces[i:i+5] for i in range(0, len(straight_faces) - 4)]:
            if ' '.join(trimed_faces) in fs:
                tie_breaker = [trimed_faces[-1]]

    if not tie_breaker:
        return False

    return HandType.STRAIGHT_FLUSH, tie_breaker

def four_of_a_kind(hand):
    all_faces = [card.face for card in hand]
    face_collections = Counter(all_faces)
    most_face = max(face_collections.keys(), key=(lambda k: face_collections[k]))
    if face_collections[most_face] < 4:
        return False
    
    all_faces = [hand_face for hand_face in all_faces if hand_face != most_face]
    assert len(all_faces) == 3, 'Invalid face combination'
    all_faces = sorted(all_faces, key=lambda f: face.index(f))
    tie_breaker = [most_face, all_faces[-1]]
    return HandType.FOUR_OF_A_KIND, tie_breaker

def full_house(hand):
    all_faces = [card.face for card in hand]
    face_collections = Counter(all_faces)
    face_amount_sorted = sorted(face_collections.keys(), key=lambda face: face_collections[face])
    c1 = face_amount_sorted[-1]
    c2 = face_amount_sorted[-2]
    if face_collections[c1] < 3:
        return False
    if face_collections[c2] < 2:
        return False

    if face_collections[c2] == 2:
        tie_breaker = [c1, c2]
    elif face_collections[c2] == 3:
        tie_breaker = sorted([c1, c2], reverse=True)
    return HandType.FULL_HOUSE, tie_breaker

def flush(hand):
    suits = [card.suit for card in hand]
    suit_collections = Counter(suits)
    flush_suit = max(suit_collections.keys(), key=(lambda k: suit_collections[k]))
    if suit_collections[flush_suit] < 5:
        return False
    
    flush_hand = [card.face for card in hand if card.suit == flush_suit]
    flush_hand = sorted(flush_hand, key=lambda f: face.index(f), reverse=True)
    tie_breaker = flush_hand[0:5]
    return HandType.FLUSH, tie_breaker

def straight(hand):
    tie_breaker = False
    straight_faces = [card.face for card in hand]
    for f, fs in [(lowace, lowaces), (face, faces)]:
        straight_faces = sorted(straight_faces, key=lambda face: f.index(face))
        for trimed_faces in [straight_faces[i:i+5] for i in range(0, len(straight_faces) - 4)]:
            if ' '.join(trimed_faces) in fs:
                tie_breaker = [trimed_faces[-1]]

    if not tie_breaker:
        return False

    return HandType.STRAIGHT, tie_breaker

def three_of_a_kind(hand):
    all_faces = [card.face for card in hand]
    hand_collection = Counter(all_faces)
    face_three = max(hand_collection.keys(), key=(lambda k: hand_collection[k]))
    if hand_collection[face_three] < 3:
        return False
    
    all_faces = sorted(filter(lambda face: face != face_three, all_faces), key=lambda f: face.index(f), reverse=True)
    tie_breaker = [face_three] + all_faces[0:2]
    return HandType.THREE_OF_A_KIND, tie_breaker

def two_pair(hand):
    all_faces = [card.face for card in hand]
    pairs = [f for f in set(all_faces) if all_faces.count(f) == 2]
    if len(pairs) < 2:
        return False
    pairs = sorted(pairs, key=lambda f: face.index(f), reverse=True)
    two_pairs = pairs[0:2]
    all_faces = sorted(filter(lambda f: f not in two_pairs, all_faces), key=lambda f: face.index(f), reverse=True)
    tie_breaker = two_pairs + [all_faces[0]]
    return HandType.TWO_PAIR, tie_breaker

def one_pair(hand):
    all_faces = [card.face for card in hand]
    pairs = [f for f in set(all_faces) if all_faces.count(f) == 2]
    if len(pairs) < 1:
        return False
    
    pairs = sorted(pairs, key=lambda f: face.index(f), reverse=True)
    pair = pairs[0:1]
    all_faces = sorted(filter(lambda f: f not in pair, all_faces), key=lambda f: face.index(f), reverse=True)
    tie_breaker = pair + all_faces[0:3]
    return HandType.ONE_PAIR, tie_breaker

def high_card(hand):
    all_faces = [card.face for card in hand]
    all_faces = sorted(all_faces, key=lambda f: face.index(f), reverse=True)
    tie_breaker = all_faces[0:5]
    return HandType.HIGH_CARD, tie_breaker

handrankorder =  (straight_flush, four_of_a_kind, full_house,
                  flush, straight, three_of_a_kind,
                  two_pair, one_pair, high_card)

def sort_hands(candidate_hands, tie_breakers):
    if (len(candidate_hands) == 0 or len(tie_breakers) == 0):
        return []

    sorted_hands = []
    sorted_tie_breakers = tie_breakers
    for i in reversed(range(len(sorted_tie_breakers[0]))):
        sorted_tie_breakers = sorted(sorted_tie_breakers, key=lambda t: face.index(t[i]), reverse=True)
    
    for tie_breaker in sorted_tie_breakers:
        sorted_hands.append(candidate_hands[tie_breakers.index(tie_breaker)])
    
    return sorted_hands

def rank(hands, public_cards):
    """
    REQUIRS: hands is a list of 'hand', which is a list of 2 cards
             public_cards is a list of 5 cards

    RETURNS: ordered hands, which is a list of list of two cards.
             the order is determined from largest to smallest
    """
    full_hands = []
    construct_hands = handy(hands, public_cards)
    cnt = 0
    for ranker in handrankorder:
        candidate_hands = []
        tie_breakers = []
        for hand in construct_hands:
            result = ranker(hand)
            if result != False:
                hand_type, tie_breaker = result
                candidate_hands.append(hand)
                tie_breakers.append(tie_breaker)
        
        for hand in candidate_hands:
            construct_hands.remove(hand)
        
        for hand in sort_hands(candidate_hands, tie_breakers):
            full_hands.append((hand, HandType(cnt)))
        
        cnt += 1

    ordered_hands = []
    for hand in full_hands:
        hand_card = [card for card in hand[0] if card not in public_cards]
        ordered_hands.append((hand_card, hand[1]))

    return ordered_hands

def handy(hands, public_cards):
    construct_hands = []
    for hand in hands:
        construct_hands.append(hand + public_cards)
    return construct_hands
