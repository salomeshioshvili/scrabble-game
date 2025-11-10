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
        """Initialise premium square positions"""
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


