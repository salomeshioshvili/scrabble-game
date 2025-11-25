from __future__ import annotations

import random
from typing import Dict, Iterable, List, Tuple

from .board import Board
from .dictionary import WordLookup
from .player import Player, TurnQueue, generate_tile_bag
from .tile import Tile

Placement = Dict[Tuple[int, int], Tile]


class Game:
    """
    Thin controller that keeps the backend components wired together for the UI.
    """

    RACK_SIZE = 7

    def __init__(self, player_names: Iterable[str] | None = None, dictionary_path: str | None = None):
        self.board = Board()
        self.dictionary = WordLookup(dictionary_path)
        self.tile_bag = generate_tile_bag()

        names = list(player_names) if player_names else ["Player 1", "Player 2"]
        if not names:
            raise ValueError("At least one player is required.")

        self.players: List[Player] = [Player(name) for name in names]
        for player in self.players:
            self._refill_rack(player)

        self.turn_queue = TurnQueue(self.players)

    @property
    def current_player(self) -> Player:
        return self.turn_queue.current_player()

    def play_move(self, placements: Placement) -> bool:
        """
        Attempt to place the selected tiles on the board.
        Returns True if the move is accepted, False otherwise.
        """
        if not placements:
            return False

        player = self.current_player
        moves = list(placements.items())

        if not self._validate_tiles(player, moves):
            return False

        if not self._validate_connectivity(moves):
            return False

        for (row, col), tile in moves:
            placed = self.board.place_tile(row, col, tile)
            if not placed:
                return False

        player.remove_tiles([tile for _, tile in moves], strict=True)
        self._refill_rack(player)
        player.reset_passes()
        self.turn_queue.next_turn()
        return True

    def pass_turn(self) -> None:
        player = self.current_player
        player.pass_turn()
        self.turn_queue.next_turn()

    def shuffle_rack(self) -> None:
        random.shuffle(self.current_player.rack)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _validate_tiles(self, player: Player, moves: List[Tuple[Tuple[int, int], Tile]]) -> bool:
        for (row, col), tile in moves:
            if tile not in player.rack:
                return False
            if not self.board.is_valid_position(row, col):
                return False
            if not self.board.is_empty(row, col):
                return False
        return True

    def _validate_connectivity(self, moves: List[Tuple[Tuple[int, int], Tile]]) -> bool:
        board_has_tiles = self.board.is_center_occupied()
        coordinates = [coords for coords, _ in moves]

        if not board_has_tiles:
            return (7, 7) in coordinates

        return any(self.board.is_connected(row, col) for row, col in coordinates)

    def _refill_rack(self, player: Player) -> None:
        needed = max(0, self.RACK_SIZE - len(player.rack))
        if needed:
            player.draw_tiles(self.tile_bag, needed)