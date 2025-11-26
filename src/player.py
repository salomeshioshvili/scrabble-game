from __future__ import annotations
from collections import deque
import random
from typing import Deque, List, Optional, Sequence, Union
from .tile import Tile, create_tiles

class Player:
    """
    Represents a Scrabble-style player who holds a rack of Tile objects.
    """

    def __init__(self, name: str, rack: Optional[List[Tile]] = None, score: int = 0):
        """
        Initialize a player with a name, optional rack, and initial score.

        Parameters
        ----------
        name : str
            Player name.
        rack : list[Tile] or None, optional
            Initial tiles. A new empty rack is created if None.
        score : int, optional
            Starting score (default is 0).
        """
        self.name: str = name
        # Copy to avoid mutating a list passed from outside
        self.rack: List[Tile] = rack.copy() if rack is not None else []
        self.score: int = score
        self.passes: int = 0

    def draw_tiles(self, tile_bag: List[Tile], x: int) -> None:
        """
        Draw X tiles from the tile bag and add them to the player's rack.

        Stops early if the tile bag is exhausted.
        """
        for _ in range(x):
            if not tile_bag:
                break
            self.rack.append(tile_bag.pop())

    def add_tile(self, tile: Tile) -> None:
        """Add a single Tile object to the player's rack."""
        self.rack.append(tile)

    def remove_tiles(self, tiles_to_remove: Sequence[Union[Tile, str]], strict: bool = False) -> bool:
        """
        Remove multiple tiles from the player's rack.

        If strict is True, it removes nothing and returns False if
        any requested tile is missing.
        """
        if strict and not self.has_tiles(tiles_to_remove):
            return False

        for tile in tiles_to_remove:
            match = self.match_tile(tile)
            if match:
                self.rack.remove(match)
        return True

    def has_tiles(self, tiles: Sequence[Union[Tile, str]]) -> bool:
        """
        Check if the player has all tiles needed.
        """
        temp_rack = self.rack.copy()
        for tile in tiles:
            match = None
            if isinstance(tile, Tile):
                match = tile if tile in temp_rack else None
            else:
                for rack_tile in temp_rack:
                    if rack_tile.letter == tile:
                        match = rack_tile
                        break
            if not match:
                return False
            temp_rack.remove(match)
        return True

    def match_tile(self, tile: Union[Tile, str]) -> Optional[Tile]:
        if isinstance(tile, Tile):
            return tile if tile in self.rack else None

        for rack_tile in self.rack:
            if rack_tile.letter == tile:
                return rack_tile
        return None

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
        rack_str = " ".join(tile.letter for tile in self.rack)
        return f"{self.name}: Score={self.score}, Rack=[{rack_str}]"


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
# TILE BAG HELPERS
# ================================================================
def generate_tile_bag() -> List[Tile]:
    """
    Create a randomized Scrabble-style tile bag containing Tile objects.
    """
    bag = create_tiles()
    random.shuffle(bag)
    return bag
