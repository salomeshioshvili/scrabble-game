# - Generate all possible legal moves for a player's rack on the board.
# - Use recursion + prefix pruning to avoid generating invalid words.
# - Respect board adjacency rules and anchor points.
# - This is a major DSA component (backtracking, pruning, search).
# - Output should be a list of Move objects or similar structures.

from typing import Dict, List, Tuple, Set
from .board import Board
from .tile import Tile
from .dictionary import WordLookup
import random

def generate_moves(board: Board, rack: List[Tile], dictionary: WordLookup) -> List[Dict[Tuple[int, int], Tile]]:
    """
    Generate all valid moves for the given rack.
    Simplified version - generates basic moves.

    Returns:
        List of possible placements {(row, col): Tile}
    """
    moves = []

    if not board.is_center_occupied():
        # First move must cover center - try horizontal words
        moves.extend(generate_center_moves(rack, dictionary))
    else:
        # Find anchor points and try to place words
        moves.extend(generate_adjacent_moves(board, rack, dictionary))

    return moves

def generate_center_moves(rack: List[Tile], dictionary: WordLookup) -> List[Dict[Tuple[int, int], Tile]]:
    """Generate moves starting at center (7,7) going horizontally."""
    moves = []

    # Try all combinations of 2-7 tiles
    for length in range(2, min(8, len(rack) + 1)):
        # Try different starting positions in rack
        for start in range(len(rack) - length + 1):
            tiles = rack[start:start + length]
            word = ''.join(t.letter for t in tiles)

            if dictionary.is_valid_word(word):
                placement = {}
                for idx, tile in enumerate(tiles):
                    placement[(7, 7 + idx)] = tile
                moves.append(placement)

    return moves

def generate_adjacent_moves(board: Board, rack: List[Tile], dictionary: WordLookup) -> List[Dict[Tuple[int, int], Tile]]:
    """Generate moves by placing tiles adjacent to existing tiles."""
    moves = []

    # Find all empty squares next to filled squares
    for row in range(15):
        for col in range(15):
            if board.get_tile(row, col) is not None:
                # Try placing each rack tile in adjacent empty squares
                adjacent = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]

                for adj_row, adj_col in adjacent:
                    if not board.is_valid_position(adj_row, adj_col):
                        continue
                    if not board.is_empty(adj_row, adj_col):
                        continue

                    for tile in rack:
                        placement = {(adj_row, adj_col): tile}

                        # Temporarily place to check if it forms valid words
                        board.grid[adj_row][adj_col] = tile
                        words = board.get_all_formed_words([(adj_row, adj_col)])
                        board.grid[adj_row][adj_col] = None

                        # Check if all formed words are valid
                        if words:
                            all_valid = all(dictionary.is_valid_word(word) for word, _ in words)
                            if all_valid:
                                moves.append(placement)

    return moves

