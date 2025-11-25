from game2dboard import Board

# ------------------------------------------------------------------
# SCRABBLE BONUS COLORS (Customize these as desired)
# ------------------------------------------------------------------
BONUS_COLORS = {
    "★": "yellow",
    "DW": "pink",
    "TW": "red",
    "DL": "lightblue",
    "TL": "blue"
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
    selected_tile : Tile or None
        Tile instance the player has chosen from their rack.
    """

    BOARD_DIMENSION = 15          # logical scrabble board size (15x15)
    BOARD_COLS = 15               # columns used by the board itself
    EXTRA_UI_COLS = 7             # extra columns on the right for scoreboard/status
    TOTAL_COLS = BOARD_COLS + EXTRA_UI_COLS

    # Layout:
    # rows 0..14   -> board
    # row  15      -> rack
    # row  16      -> buttons
    RACK_ROW = BOARD_DIMENSION
    BUTTON_ROW = BOARD_DIMENSION + 1
    TOTAL_ROWS = BOARD_DIMENSION + 2

    RACK_OFFSET = 2               # where rack tiles start
    UI_COL_START = BOARD_COLS + 1 # first column for sidebar UI (scores, status)

    def __init__(self, game):
        self.game = game
        self.board = Board(self.TOTAL_ROWS, self.TOTAL_COLS)
        self.board.title = "Scrabble"
        self.board.cell_size = 40
        self.board.on_mouse_click = self._on_board_click
        self.board.on_start = self._apply_bonus_cells

        self.selected_tile = None
        self.selected_rack_index = None  # index in current player's rack

        self.placements = {}      # {(row, col): Tile}
        self.tile_positions = {}  # Tile -> (row, col)
        self._bonus_cells = []

        self.status_message = "Welcome to Scrabble!"

        # Draw initial UI
        self._draw_bonus_cells()
        self._render_tiles()
        self._render_rack()
        self._render_buttons()
        self._render_scoreboard()
        self._render_status()

    # ------------------------------------------------------------------
    # DRAWING HELPERS
    # ------------------------------------------------------------------
    def _draw_bonus_cells(self):
        """Cache Scrabble square bonus colors for later drawing."""
        for row in range(self.BOARD_DIMENSION):
            for col in range(self.BOARD_COLS):
                bonus = self.game.board.get_bonus(row, col)
                color = BONUS_COLORS.get(bonus)
                if color:
                    self._bonus_cells.append((row, col, color))

    def _apply_bonus_cells(self):
        """Apply cached bonus colors once the GUI canvas exists."""
        for row, col, color in self._bonus_cells:
            cell = self.board._cells[row][col]
            if cell:
                cell.bgcolor = color

    def _render_tiles(self):
        """Draw backend tile letters onto board squares."""
        for row in range(self.BOARD_DIMENSION):
            for col in range(self.BOARD_COLS):
                tile = self.game.board.get_tile(row, col)
                self.board[row][col] = tile.letter if tile else ""

    def _render_rack(self):
        """Draw player rack letters underneath board with simple 'tile' styling."""
        self._clear_row(self.RACK_ROW)

        rack = self.game.current_player.rack
        self.board[self.RACK_ROW][0] = "Rack:"
        start_col = self.RACK_OFFSET

        for i, tile in enumerate(rack):
            col = start_col + i
            if col >= self.BOARD_COLS:  # keep rack under the board portion
                break

            # Show as [A] style
            self.board[self.RACK_ROW][col] = f"[{tile.letter}]"

            # Color background to look like tiles
            cell = self.board._cells[self.RACK_ROW][col]
            if cell:
                if i == self.selected_rack_index:
                    cell.bgcolor = "orange"   # selected tile
                else:
                    cell.bgcolor = "wheat"    # normal rack tile

        # Clear any rack cells beyond current rack size
        for col in range(start_col + len(rack), self.BOARD_COLS):
            self.board[self.RACK_ROW][col] = ""
            cell = self.board._cells[self.RACK_ROW][col]
            if cell:
                cell.bgcolor = "white"

    def _render_buttons(self):
        """Create UI buttons along bottom row."""
        self._clear_row(self.BUTTON_ROW)

        self.board[self.BUTTON_ROW][2] = "[Submit]"
        self.board[self.BUTTON_ROW][4] = "[Undo]"
        self.board[self.BUTTON_ROW][6] = "[Pass]"
        self.board[self.BUTTON_ROW][8] = "[Shuffle]"

    def _render_scoreboard(self):
        """Show player names and scores in the right sidebar."""
        start_col = self.UI_COL_START

        # Clear scoreboard area
        for row in range(self.BOARD_DIMENSION):
            for col in range(start_col, self.TOTAL_COLS):
                self.board[row][col] = ""
                cell = self.board._cells[row][col]
                if cell:
                    cell.bgcolor = "#f0f0f0"

        self.board[0][start_col] = "Scores"

        for i, player in enumerate(self.game.players):
            row = 1 + i
            if row >= self.RACK_ROW:
                break  # don't clash with rack row

            prefix = "▶ " if player is self.game.current_player else "   "
            self.board[row][start_col] = f"{prefix}{player.name}: {player.score}"

    def _render_status(self):
        """Show a short status message in the sidebar under the buttons."""
        start_col = self.UI_COL_START

        # Clear status row area
        for col in range(start_col, self.TOTAL_COLS):
            self.board[self.BUTTON_ROW][col] = ""
            cell = self.board._cells[self.BUTTON_ROW][col]
            if cell:
                cell.bgcolor = "#f0f0f0"

        # Truncate if message is too long for the sidebar
        msg = self.status_message[: (self.TOTAL_COLS - start_col) * 2]
        self.board[self.BUTTON_ROW][start_col] = msg

    def _clear_row(self, row):
        """Utility to blank a UI-only row."""
        for col in range(self.TOTAL_COLS):
            self.board[row][col] = ""
            cell = self.board._cells[row][col]
            if cell:
                cell.bgcolor = "white"

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
        # Clicked inside right-side UI panel -> ignore (except on button row)
        if col >= self.BOARD_COLS and row < self.BUTTON_ROW:
            return

        # Clicked a rack tile
        if row == self.RACK_ROW and col < self.BOARD_COLS:
            rack = self.game.current_player.rack
            rack_index = col - self.RACK_OFFSET
            if 0 <= rack_index < len(rack):
                self.selected_tile = rack[rack_index]
                self.selected_rack_index = rack_index
                self._render_rack()
            return

        # Clicked Submit
        if row == self.BUTTON_ROW and col == 2:
            self._submit_move()
            return

        # Undo last placement
        if row == self.BUTTON_ROW and col == 4:
            self._undo()
            return

        # Pass turn
        if row == self.BUTTON_ROW and col == 6:
            self._pass_turn()
            return

        # Shuffle rack
        if row == self.BUTTON_ROW and col == 8:
            self._shuffle()
            return

        # Click board square to place tile
        if (
            self.selected_tile
            and row < self.BOARD_DIMENSION
            and col < self.BOARD_COLS
        ):
            # Don't overwrite existing tiles from previous turns
            if self.game.board.get_tile(row, col):
                return

            # If this tile was previously placed somewhere, clear that spot
            previous_pos = self.tile_positions.get(self.selected_tile)
            if previous_pos:
                prev_row, prev_col = previous_pos
                self.board[prev_row][prev_col] = ""
                self.placements.pop(previous_pos, None)

            # Place on board visually & track placement
            self.board[row][col] = self.selected_tile.letter
            self.placements[(row, col)] = self.selected_tile
            self.tile_positions[self.selected_tile] = (row, col)

            # Clear selection
            self.selected_tile = None
            self.selected_rack_index = None
            self._render_rack()

    # ------------------------------------------------------------------
    # ACTION BUTTONS
    # ------------------------------------------------------------------
    def _submit_move(self):
        """Send placed tiles to backend for validation."""
        if not self.placements:
            self.status_message = "No tiles placed."
            self._render_status()
            return

        ok = self.game.play_move(self.placements)

        # In either case, clear tentative placements
        self.placements.clear()
        self.tile_positions.clear()
        self.selected_tile = None
        self.selected_rack_index = None

        # Re-draw board and rack from backend state
        self._render_tiles()
        self._render_rack()

        if ok:
            self.status_message = f"Move accepted. Now: {self.game.current_player.name}"
        else:
            self.status_message = "Invalid move. Try again."

        self._render_scoreboard()
        self._render_status()

    def _undo(self):
        """Remove unsubmitted placements."""
        for row, col in list(self.placements.keys()):
            self.board[row][col] = ""
        self.placements.clear()
        self.tile_positions.clear()
        self.selected_tile = None
        self.selected_rack_index = None
        self._render_rack()
        self.status_message = "Placements cleared."
        self._render_status()

    def _pass_turn(self):
        """Tell backend player is passing."""
        self.game.pass_turn()
        self._undo()  # clears placements and rack selection
        self._render_rack()
        self._render_scoreboard()
        self.status_message = f"{self.game.current_player.name}'s turn."
        self._render_status()

    def _shuffle(self):
        """Randomize rack order visually + backend."""
        self.game.shuffle_rack()
        self.selected_tile = None
        self.selected_rack_index = None
        self._render_rack()
        self.status_message = "Rack shuffled."
        self._render_status()

    # ------------------------------------------------------------------
    # MAIN LOOP
    # ------------------------------------------------------------------
    def show(self):
        """
        Display the Scrabble window and block execution.
        """
        # Make sure UI is synced before showing
        self._render_tiles()
        self._render_rack()
        self._render_buttons()
        self._render_scoreboard()
        self._render_status()
        self.board.show()
