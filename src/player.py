# - Store each player's rack (letters) and current score.
# - Provide methods to add/remove/draw tiles.
# - Track player-specific state (e.g., consecutive passes).
# -*- coding: utf-8 -*-
from collections import deque
import random


# ================================================================
# TILE CLASS (BASIC EXAMPLE)
# ================================================================
class Tile:
    def __init__(self, letter, points):
        self.letter = letter
        self.points = points

    def __repr__(self):
        return f"{self.letter}({self.points})"


# ================================================================
# PLAYER CLASS (FULLY REPAIRED + EXPANDED)
# ================================================================
class Player:
    def __init__(self, name, rack=None, score=0):
        self.name = name
        self.rack = rack if rack else []   # List of Tile objects
        self.score = score
        self.passes = 0   # Track consecutive passes

    # Draw X tiles from the tile bag
    def draw_tiles(self, tile_bag, x):
        for _ in range(x):
            if tile_bag:
                self.rack.append(tile_bag.pop())  # Take from top of bag

    # Add a single tile
    def add_tile(self, tile):
        self.rack.append(tile)

    # Remove multiple tiles
    def remove_tiles(self, tiles_to_remove):
        for tile in tiles_to_remove:
            if tile in self.rack:
                self.rack.remove(tile)

    # Check if the player has a set of letters
    def has_tiles(self, letters):
        rack_letters = [tile.letter for tile in self.rack]

        for letter in letters:
            if letter not in rack_letters:
                return False
            rack_letters.remove(letter)

        return True

    # Add points to player score
    def add_score(self, points):
        self.score += points

    def pass_turn(self):
        self.passes += 1

    def reset_passes(self):
        self.passes = 0

    def __str__(self):
        rack_str = " ".join([tile.letter for tile in self.rack])
        return f"{self.name}: Score={self.score}, Rack=[{rack_str}]"


# ================================================================
# TURN ORDER QUEUE
# ================================================================
class TurnQueue:
    def __init__(self, players):
        self.queue = deque(players)

    # Returns current player without rotating
    def current_player(self):
        return self.queue[0]

    # Move current player to end of queue
    def next_turn(self):
        self.queue.rotate(-1)
        return self.queue[0]

    # Get queue as list
    def get_turn_order(self):
        return [player.name for player in self.queue]


# ================================================================
# TILE BAG EXAMPLE (SCRABBLE-LIKE)
# ================================================================
def generate_tile_bag():
    letters = {
        "A": (9, 1),
        "B": (2, 3),
        "C": (2, 3),
        "D": (4, 2),
        "E": (12, 1),
        "F": (2, 4),
        "G": (3, 2),
        "H": (2, 4),
        "I": (9, 1),
        "J": (1, 8),
        "K": (1, 5),
        "L": (4, 1),
        "M": (2, 3),
        "N": (6, 1),
        "O": (8, 1),
        "P": (2, 3),
        "Q": (1, 10),
        "R": (6, 1),
        "S": (4, 1),
        "T": (6, 1),
        "U": (4, 1),
        "V": (2, 4),
        "W": (2, 4),
        "X": (1, 8),
        "Y": (2, 4),
        "Z": (1, 10)
    }

    bag = []
    for letter, (quantity, points) in letters.items():
        for _ in range(quantity):
            bag.append(Tile(letter, points))

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

    # Give each player 7 tiles
    for p in [p1, p2, p3]:
        p.draw_tiles(bag, 7)

    turn_order = TurnQueue([p1, p2, p3])

    print("Initial Turn Order:", turn_order.get_turn_order())
    print(turn_order.current_player(), "goes first")

    # Rotate turns
    turn_order.next_turn()
    print("After rotation:", turn_order.get_turn_order())
    print("Current turn:", turn_order.current_player())

