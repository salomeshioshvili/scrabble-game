# - Evaluate all generated moves and choose the best one.
# - Optionally implement strategies (e.g., maintain rack balance).
# - Return recommended moves for AI players or hint systems.
# - Do not modify board state here.

from typing import Dict, List, Optional, Tuple
from .board import Board
from .tile import Tile
from .move_generator import generate_moves
from .move_evaluator import calculate_move_score
from .dictionary import WordLookup

def suggest_best_move(board: Board, rack: List[Tile], dictionary: WordLookup) -> Optional[Dict[Tuple[int, int], Tile]]:
    """
    Find the highest-scoring valid move for the bot.

    Returns:
        Best placement dictionary or None if no valid moves
    """
    possible_moves = generate_moves(board, rack, dictionary)

    if not possible_moves:
        return None

    best_move = None
    best_score = -1

    for move in possible_moves:
        score = calculate_move_score(board, move)
        if score > best_score:
            best_score = score
            best_move = move

    return best_move
