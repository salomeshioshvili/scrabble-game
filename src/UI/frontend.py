"""
Scrabble Game Frontend (UI)
---------------------------

Graphical Board + Player Rack using game2dboard.

Responsibilities of this module:
- Render Scrabble board UI
- Display placed tiles and bonus squares visually
- Allow selecting tiles from the rack
- Allow placing tiles onto the board
- Provide interaction buttons (Submit, Undo, Pass, Shuffle)
- Delegate validation and scoring to game.py (controller)

Important:
    This file should NOT contain business logic.
    All rule checking (legal placements, scoring, turn logic)
    must be handled in the Game class.

Dependencies:
    - game2dboard (Tk based)
    - A Game instance (your backend)

"""

from game2dboard import Board

# ------------------------------------------------------------------
# SCRABBLE BONUS COLORS (Customize these as desired)
# ------------------------------------------------------------------
BONUS_COLORS = {
    "start": "yellow",
    "double_word": "pink",
    "triple_word": "red",
    "double_letter": "lightblue",
    "triple_letter": "blue"
}


class ScrabbleUI:
    """
    A graphical UI wrapper around the game backend.

    Parameters
    ----------
    game : Game
        The backend game controller responsible for logic.

    Attributes
    ----------
    board : Board
        The graphical representation.
    selected_tile : str or None
        Letter the player has chosen from their rack.
    """

    def __init__(self, game):
        self.game = game
        self.board = Board(15, 15)
        self.board.title = "Scrabble"
        self.board.cell_size = 40
        self.board.on_mouse_click = self._on_board_click
        self.selected_tile = None
        self.placements = {}  # {(row, col): tile}

        # Draw initial UI
        self._draw_bonus_cells()
        self._render_tiles()
        self._render_buttons()
        self._render_rack()

    # ------------------------------------------------------------------
    # DRAWING HELPERS
    # ------------------------------------------------------------------
    def _draw_bonus_cells(self):
        """Color Scrabble squares based on bonus type."""
        for row in range(15):
            for col in range(15):
                bonus = self.game.board.get_bonus(row, col)
                if bonus:
                    self.board.bg[row][col] = BONUS_COLORS[bonus]

    def _render_tiles(self):
        """Draw backend tile letters onto board squares."""
        for row in range(15):
            for col in range(15):
                tile = self.game.board.get_tile(row, col)
                self.board[row][col] = tile.letter if tile else ""

    def _render_rack(self):
        """Draw player rack letters underneath board."""
        rack = self.game.current_player.rack
        for i, tile in enumerate(rack):
            self.board.text[15][i] = tile.letter

        self.board.text[15][7] = "Rack:"  # Label

    def _render_buttons(self):
        """Create UI buttons along bottom row."""
        self.board.text[16][2] = "[Submit]"
        self.board.text[16][4] = "[Undo]"
        self.board.text[16][6] = "[Pass]"
        self.board.text[16][8] = "[Shuffle]"

    # ------------------------------------------------------------------
    # CLICK HANDLER
    # ------------------------------------------------------------------
    def _on_board_click(self, btn, row, col):
        """
        Handles every click event.

        Behavior:
        - Click rack -> select tile
        - Click board -> place tile
        - Click button -> trigger action
        """
        # Clicked a rack tile
        if row == 15:
            rack = self.game.current_player.rack
            if col < len(rack):
                self.selected_tile = rack[col]
            return

        # Clicked Submit
        if row == 16 and col == 2:
            self._submit_move()
            return

        # Undo last placement
        if row == 16 and col == 4:
            self._undo()
            return

        # Pass turn
        if row == 16 and col == 6:
            self._pass_turn()
            return

        # Shuffle rack
        if row == 16 and col == 8:
            self._shuffle()
            return

        # Click board square to place tile
        if self.selected_tile:
            self.board[row][col] = self.selected_tile.letter
            self.placements[(row, col)] = self.selected_tile
            self.selected_tile = None

    # ------------------------------------------------------------------
    # ACTION BUTTONS
    # ------------------------------------------------------------------
    def _submit_move(self):
        """Send placed tiles to backend for validation."""
        ok = self.game.play_move(self.placements)
        if ok:
            self.placements.clear()
            self._render_tiles()
            self._render_rack()

    def _undo(self):
        """Remove unsubmitted placements."""
        for (row, col) in self.placements:
            self.board[row][col] = ""
        self.placements.clear()

    def _pass_turn(self):
        """Tell backend player is passing."""
        self.game.pass_turn()
        self._render_rack()

    def _shuffle(self):
        """Randomize rack order visually + backend."""
        self.game.shuffle_rack()
        self._render_rack()

    # ------------------------------------------------------------------
    # MAIN LOOP
    # ------------------------------------------------------------------
    def show(self):
        """
        Display the Scrabble window and block execution.
        """
        self.board.show(calling_thread_blocking=True)
