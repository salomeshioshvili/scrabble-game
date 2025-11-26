# - Given a board and a move, compute total score.
# - Apply letter and word multiplier bonuses.
# - Score additional words formed perpendicularly.
# - Keep this logic pure (no board mutations).

from typing import Dict, Tuple
from .board import Board
from .tile import Tile

def calculate_move_score(board: Board, placements: Dict[Tuple[int, int], Tile]) -> int:
    """
    Calculate the total score for a move including all formed words and bonuses.

    Args:
        board: Current board state
        placements: Dictionary of {(row, col): Tile} for new placements

    Returns:
        Total score for the move
    """
    if not placements:
        return 0

    # Save original cells and temporarily place tiles
    original_cells = {}
    placed_positions = []
    for (row, col), tile in placements.items():
        original_cells[(row, col)] = board.grid[row][col]
        board.grid[row][col] = tile
        placed_positions.append((row, col))

    total_score = 0
    words_formed = board.get_all_formed_words(placed_positions)

    for word, tile_positions in words_formed:
        word_score = 0
        word_multiplier = 1

        for row, col, tile in tile_positions:
            tile_score = tile.value

            # Apply bonuses only for newly placed tiles
            if (row, col) in placements:
                bonus = board.get_bonus(row, col)
                if bonus == Board.DOUBLE_LETTER:
                    tile_score *= 2
                elif bonus == Board.TRIPLE_LETTER:
                    tile_score *= 3
                elif bonus == Board.DOUBLE_WORD or bonus == Board.CENTER:
                    word_multiplier *= 2
                elif bonus == Board.TRIPLE_WORD:
                    word_multiplier *= 3

            word_score += tile_score

        total_score += word_score * word_multiplier

    # Bingo bonus: 50 points for using all 7 tiles
    if len(placements) == 7:
        total_score += 50

    # Restore original cells (do not remove permanent placements)
    for (row, col), orig in original_cells.items():
        board.grid[row][col] = orig

    return total_score
