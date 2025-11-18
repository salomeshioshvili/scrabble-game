# -*- coding: utf-8 -*-
from collections import deque
import random


# ================================================================
# PLAYER CLASS (LETTER-ONLY VERSION)
# ================================================================
class Player:
    def __init__(self, name, rack=None, score=0):
        self.name = name
        self.rack = rack if rack else []   # List of letters
        self.score = score
        self.passes = 0   # Track consecutive passes

    # Draw X tiles (letters) from the tile bag
    def draw_tiles(self, tile_bag, x):
        for _ in range(x):
            if tile_bag:
                self.rack.append(tile_bag.pop())

    # Add a single letter
    def add_tile(self, letter):
        self.rack.append(letter)

    # Remove multiple letters
    def remove_tiles(self, letters_to_remove):
        for letter in letters_to_remove:
            if letter in self.rack:
                self.rack.remove(letter)

    # Check if player has letters needed for a word
    def has_tiles(self, letters):
        temp_rack = self.rack.copy()

        for letter in letters:
            if letter not in temp_rack:
                return False
            temp_rack.remove(letter)

        return True

    # Add to score
    def add_score(self, points):
        self.score += points

    def pass_turn(self):
        self.passes += 1

    def reset_passes(self):
        self.passes = 0

    def __str__(self):
        rack_str = " ".join(self.rack)
        return f"{self.name}: Score={self.score}, Rack=[{rack_str}]"


# ================================================================
# TURN ORDER QUEUE
# ================================================================
class TurnQueue:
    def __init__(self, players):
        self.queue = deque(players)

    def current_player(self):
        return self.queue[0]

    def next_turn(self):
        self.queue.rotate(-1)
        return self.queue[0]

    def get_turn_order(self):
        return [player.name for player in self.queue]


# ================================================================
# TILE BAG — letters ONLY version
# ================================================================
def generate_tile_bag():
    letters = {
        "A": 9, "B": 2, "C": 2, "D": 4, "E": 12, "F": 2,
        "G": 3, "H": 2, "I": 9, "J": 1, "K": 1, "L": 4,
        "M": 2, "N": 6, "O": 8, "P": 2, "Q": 1, "R": 6,
        "S": 4, "T": 6, "U": 4, "V": 2, "W": 2, "X": 1,
        "Y": 2, "Z": 1
    }

    bag = []
    for letter, qty in letters.items():
        for _ in range(qty):
            bag.append(letter)

    random.shuffle(bag)
    return bag


# ================================================================
# EXAMPLE USAGE
# ================================================================
if __name__ == "__main__":
    bag = generate_tile_bag()

    p1 = Player("Alice")
    p2 = Player("Bob")
    p3 = Player("Charlie")

    # Give each player 7 letters
    for p in [p1, p2, p3]:
        p.draw_tiles(bag, 7)

    turn_order = TurnQueue([p1, p2, p3])

    print("Initial Turn Order:", turn_order.get_turn_order())
    print(turn_order.current_player(), "goes first")

    # Rotate turns
    turn_order.next_turn()
    print("After rotation:", turn_order.get_turn_order())
    print("Current turn:", turn_order.current_player())
