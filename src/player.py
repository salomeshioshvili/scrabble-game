# test commit from scrabble-game repo

from collections import deque
import random
from typing import List, Optional, Deque


# ================================================================
# PLAYER CLASS (LETTER-ONLY VERSION)
# ================================================================
class Player:
    """
    Represents a Scrabble-style player who holds a rack of letter tiles.
    """

    def __init__(self, name: str, rack: Optional[List[str]] = None, score: int = 0):
        """
        Initialize a player with a name, optional rack, and initial score.

        Parameters
        ----------
        name : str
            Player name.
        rack : list[str] or None, optional
            Initial letters. A new empty rack is created if None.
        score : int, optional
            Starting score (default is 0).
        """
        self.name: str = name
        # Copy to avoid mutating a list passed from outside
        self.rack: List[str] = rack.copy() if rack is not None else []
        self.score: int = score
        self.passes: int = 0

    def draw_tiles(self, tile_bag: List[str], x: int) -> None:
        """
        Draw X tiles from the tile bag and add them to the player's rack.

        Stops early if the tile bag is exhausted.
        """
        for _ in range(x):
            if not tile_bag:
                break
            self.rack.append(tile_bag.pop())

    def add_tile(self, letter: str) -> None:
        """Add a single letter tile to the player's rack."""
        self.rack.append(letter)

    def remove_tiles(self, letters_to_remove: List[str], strict: bool = False) -> bool:
        """
        Remove multiple letters from the player's rack.

        If strict is True, it removes nothing and returns False if
        any requested letter is missing.
        """
        if strict and not self.has_tiles(letters_to_remove):
            return False

        for letter in letters_to_remove:
            if letter in self.rack:
                self.rack.remove(letter)
        return True

    def has_tiles(self, letters: List[str]) -> bool:
        """
        Check if the player has all letters needed.
        """
        temp_rack = self.rack.copy()
        for letter in letters:
            if letter not in temp_rack:
                return False
            temp_rack.remove(letter)
        return True

    def add_score(self, points: int) -> None:
        """Add points to the player's score."""
        self.score += points

    def pass_turn(self) -> None:
        """Increment the count of consecutive passes."""
        self.passes += 1

    def reset_passes(self) -> None:
        """Reset the pass counter to zero."""
        self.passes = 0

    def __str__(self) -> str:
        """Return a readable summary of the player's name, score, and rack."""
        rack_str = " ".join(self.rack)
        return f"{self.name}: Score={self.score}, Rack=[{rack_str}]"


# ================================================================
# TURN ORDER QUEUE
# ================================================================
class TurnQueue:
    """
    Represents a circular queue to manage player turn order.
    """

    def __init__(self, players: List[Player]):
        """
        Initialize the turn queue with a list of players.
        """
        if not players:
            raise ValueError("TurnQueue requires at least one player.")
        self.queue: Deque[Player] = deque(players)

    def current_player(self) -> Player:
        """
        Return the player whose turn it currently is.
        """
        return self.queue[0]

    def next_turn(self) -> Player:
        """
        Advance to the next player's turn and return them.
        """
        self.queue.rotate(-1)
        return self.queue[0]

    def get_turn_order(self) -> List[str]:
        """
        Return a list of player names representing current turn order.
        """
        return [player.name for player in self.queue]


# ================================================================
# TILE BAG — letters ONLY version
# ================================================================
def generate_tile_bag() -> List[str]:
    """
    Create a randomized Scrabble-style tile bag containing letter tiles.
    """
    letters = {
        "A": 9, "B": 2, "C": 2, "D": 4, "E": 12, "F": 2,
        "G": 3, "H": 2, "I": 9, "J": 1, "K": 1, "L": 4,
        "M": 2, "N": 6, "O": 8, "P": 2, "Q": 1, "R": 6,
        "S": 4, "T": 6, "U": 4, "V": 2, "W": 2, "X": 1,
        "Y": 2, "Z": 1
    }

    bag: List[str] = []
    for letter, qty in letters.items():
        bag.extend([letter] * qty)

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
    for p in (p1, p2, p3):
        p.draw_tiles(bag, 7)

    turn_order = TurnQueue([p1, p2, p3])

    print("Initial Turn Order:", turn_order.get_turn_order())
    print(turn_order.current_player(), "goes first")

    turn_order.next_turn()
    print("After rotation:", turn_order.get_turn_order())
    print("Current turn:", turn_order.current_player())
