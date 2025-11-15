"""
Core module implementing a fundamental component of the Scrabble
game system. This file contributes to board state management,
dictionary lookup performance, and scoring logic efficiency.
"""
# - Represent the 2D Scrabble board and store placed tiles.
# - Implement placement validation (bounds, connectivity, collisions).
# - Track bonus squares (double/triple letter/word).
# - Provide helper methods to extract formed words in both directions.
# - DO NOT compute scores here (delegate to move_evaluator.py).

class Board:
    """Represents the 15x15 Scrabble board"""
    TRIPLE_WORD = 'TW'
    DOUBLE_WORD = 'DW'
    TRIPLE_LETTER = 'TL'
    DOUBLE_LETTER = 'DL'
    NORMAL = '  '
    CENTER = '★'

    def __init__(self):
        self.size = 15
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)] #2D array
        self.bonus_squares = self.initialize_bonus_squares()

    def initialize_bonus_squares(self):
        """Initialise bonus square positions"""
        bonus = [[self.NORMAL for _ in range(self.size)] for _ in range(self.size)]

        # Triple word scores (corners + middle edges)
        tw_positions = [(0, 0), (0, 7), (0, 14), (7, 0), (7, 14), (14, 0), (14, 7), (14, 14)]
        for r, c in tw_positions:
            bonus[r][c] = self.TRIPLE_WORD

        # Double word scores (diagonal from corners)
        dw_positions = [(1, 1), (2, 2), (3, 3), (4, 4), (1, 13), (2, 12), (3, 11), (4, 10),
                        (13, 1), (12, 2), (11, 3), (10, 4), (13, 13), (12, 12), (11, 11), (10, 10)]
        for r, c in dw_positions:
            bonus[r][c] = self.DOUBLE_WORD

        # Triple letter scores
        tl_positions = [(1, 5), (1, 9), (5, 1), (5, 5), (5, 9), (5, 13),
                        (9, 1), (9, 5), (9, 9), (9, 13), (13, 5), (13, 9)]
        for r, c in tl_positions:
            bonus[r][c] = self.TRIPLE_LETTER

        # Double letter scores
        dl_positions = [(0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14),
                        (6, 2), (6, 6), (6, 8), (6, 12), (7, 3), (7, 11),
                        (8, 2), (8, 6), (8, 8), (8, 12), (11, 0), (11, 7), (11, 14),
                        (12, 6), (12, 8), (14, 3), (14, 11)]
        for r, c in dl_positions:
            bonus[r][c] = self.DOUBLE_LETTER

        # Center square
        bonus[7][7] = self.CENTER

        return bonus

    def is_valid_position(self, row, col):
        """Check if position is within board bounds"""
        return 0 <= row < self.size and 0 <= col < self.size

    def is_empty(self, row, col):
        """Check if a position is empty"""
        return self.is_valid_position(row, col) and self.grid[row][col] is None

    def place_tile(self, row, col, tile):
        """Place a tile on the board. Returns True if successful."""
        if self.is_empty(row, col):
            self.grid[row][col] = tile
            return True
        return False

    def get_tile(self, row, col):
        """Get tile at position, returns None if empty"""
        if self.is_valid_position(row, col):
            return self.grid[row][col]
        return None

    def get_bonus(self, row, col):
        """Get bonus square type at position"""
        if self.is_valid_position(row, col):
            return self.bonus_squares[row][col]
        return None

    def is_center_occupied(self):
        """Check if center square (7,7) has a tile"""
        return self.grid[7][7] is not None

    def is_connected(self, row, col):
        """Check if position connects to existing tiles"""
        if not self.is_center_occupied():
            return row == 7 and col == 7  # First word must cover center

        # Check if position already has tile or adjacent to one
        if not self.is_empty(row, col):
            return True

        # Check all 4 adjacent positions
        adjacent = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        for r, c in adjacent:
            if self.get_tile(r, c) is not None:
                return True
        return False

    def get_word_horizontal(self, row, col):
        """Extract horizontal word at position. Returns (word, start_col, tiles_used)"""
        if not self.is_valid_position(row, col) or self.grid[row][col] is None:
            return None, None, []

        # Find start of word
        start_col = col
        while start_col > 0 and self.grid[row][start_col - 1] is not None:
            start_col -= 1

        # Find end of word
        end_col = col
        while end_col < self.size - 1 and self.grid[row][end_col + 1] is not None:
            end_col += 1

        # Extract word
        if start_col == end_col:  # Single letter, not a word
            return None, None, []

        word = ""
        tiles = []
        for c in range(start_col, end_col + 1):
            tile = self.grid[row][c]
            word += tile.letter
            tiles.append((row, c, tile))

        return word, start_col, tiles

    def get_word_vertical(self, row, col):
        """Extract vertical word at position. Returns (word, start_row, tiles_used)"""
        if not self.is_valid_position(row, col) or self.grid[row][col] is None:
            return None, None, []

        start_row = row
        while start_row > 0 and self.grid[start_row - 1][col] is not None:
            start_row -= 1

        end_row = row
        while end_row < self.size - 1 and self.grid[end_row + 1][col] is not None:
            end_row += 1

        if start_row == end_row:
            return None, None, []

        word = ""
        tiles = []
        for r in range(start_row, end_row + 1):
            tile = self.grid[r][col]
            word += tile.letter
            tiles.append((r, col, tile))

        return word, start_row, tiles

    def get_all_formed_words(self, placed_positions):
        """Return words created by newly placed tiles as (word, positions) pairs."""
        words = []
        checked_horizontal = set()
        checked_vertical = set()

        for row, col in placed_positions:
            # Check horizontal word
            h_key = (row, None)
            if h_key not in checked_horizontal:
                word, start_col, tiles = self.get_word_horizontal(row, col)
                if word:
                    words.append((word, tiles))
                    checked_horizontal.add(h_key)

            # Check vertical word
            v_key = (None, col)
            if v_key not in checked_vertical:
                word, start_row, tiles = self.get_word_vertical(row, col)
                if word:
                    words.append((word, tiles))
                    checked_vertical.add(v_key)

        return words