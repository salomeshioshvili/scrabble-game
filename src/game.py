from __future__ import annotations

import random
from typing import Dict, Iterable, List, Tuple

from .board import Board
from .dictionary import WordLookup
from .player import Player, TurnQueue, generate_tile_bag
from .tile import Tile
from .move_evaluator import calculate_move_score
from .move_suggester import suggest_best_move

Placement = Dict[Tuple[int, int], Tile]


class Game:
    """
    Thin controller that keeps the backend components wired together for the UI.
    """

    RACK_SIZE = 7

    def __init__(self, player_names: Iterable[str] | None = None, dictionary_path: str | None = None, bot_count: int = 0):
        self.board = Board()
        self.dictionary = WordLookup(dictionary_path)
        self.tile_bag = generate_tile_bag()

        names = list(player_names) if player_names else ["Player 1"]
        if not names and bot_count == 0:
            raise ValueError("At least one player is required.")

        self.players: List[Player] = [Player(name) for name in names]

        # Add bot players
        self.bot_players: List[Player] = []
        for i in range(bot_count):
            bot = Player(f"Bot {i + 1}")
            self.bot_players.append(bot)
            self.players.append(bot)

        for player in self.players:
            self.refill_rack(player)

        self.turn_queue = TurnQueue(self.players)

    @property
    def current_player(self) -> Player:
        return self.turn_queue.current_player()

    def is_bot_turn(self) -> bool:
        """Check if current player is a bot."""
        return self.current_player in self.bot_players

    def play_bot_move(self) -> bool:
        """Execute bot's move automatically."""
        if not self.is_bot_turn():
            return False

        bot_move = suggest_best_move(self.board, self.current_player.rack, self.dictionary)
        if bot_move:
            return self.play_move(bot_move)
        else:
            # Bot has no valid moves, pass turn
            self.pass_turn()
            return True

    def play_move(self, placements: Placement) -> bool:
        """
        Attempt to place the selected tiles on the board.
        Returns True if the move is accepted, False otherwise.
        """
        if not placements:
            return False

        player = self.current_player
        moves = list(placements.items())

        if not self.validate_tiles(player, moves):
            return False

        if not self.validate_connectivity(moves):
            return False

        # Temporarily place tiles to validate words
        placed_positions = [coords for coords, _ in moves]
        for (row, col), tile in moves:
            self.board.grid[row][col] = tile

        # Extract and validate all formed words
        words_formed = self.board.get_all_formed_words(placed_positions)

        # Must form at least one word
        if not words_formed:
            self.revert_placements(placed_positions)
            return False

        # All words must be valid
        for word, _ in words_formed:
            if not self.dictionary.is_valid_word(word):
                self.revert_placements(placed_positions)
                return False

        # Calculate and add score
        score = calculate_move_score(self.board, placements)
        player.add_score(score)

        # Finalize move
        player.remove_tiles([tile for _, tile in moves], strict=True)
        self.refill_rack(player)
        player.reset_passes()
        self.turn_queue.next_turn()
        return True

    def revert_placements(self, positions: List[Tuple[int, int]]) -> None:
        """Remove tiles from given positions."""
        for row, col in positions:
            self.board.grid[row][col] = None

    def is_game_over(self) -> bool:
        """Check if game should end."""
        # Game ends if all players pass consecutively
        if all(p.passes >= 2 for p in self.players):
            return True
        # Or if tile bag is empty and a player has no tiles
        if not self.tile_bag:
            return any(len(p.rack) == 0 for p in self.players)
        return False

    def pass_turn(self) -> None:
        """Pass the current turn."""
        self.current_player.pass_turn()
        self.turn_queue.next_turn()

    def shuffle_rack(self) -> None:
        """Shuffle the current player's rack."""
        random.shuffle(self.current_player.rack)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def validate_tiles(self, player: Player, moves: List[Tuple[Tuple[int, int], Tile]]) -> bool:
        for (row, col), tile in moves:
            if tile not in player.rack:
                return False
            if not self.board.is_valid_position(row, col):
                return False
            if not self.board.is_empty(row, col):
                return False
        return True

    def validate_connectivity(self, moves: List[Tuple[Tuple[int, int], Tile]]) -> bool:
        board_has_tiles = self.board.is_center_occupied()
        coordinates = [coords for coords, _ in moves]

        if not board_has_tiles:
            return (7, 7) in coordinates

        return any(self.board.is_connected(row, col) for row, col in coordinates)

    def refill_rack(self, player: Player) -> None:
        needed = max(0, self.RACK_SIZE - len(player.rack))
        if needed:
            player.draw_tiles(self.tile_bag, needed)
