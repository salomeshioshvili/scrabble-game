# - Test placement legality, adjacency, collisions, boundaries.
# - Test bonus square behaviors.
# - Test helper word extraction functions.
from src.board import Board

def test_is_valid_and_empty():
    b = Board()
    assert b.is_valid_position(0, 0)
    assert not b.is_valid_position(-1, 0)
    assert b.is_empty(0, 0)
    assert b.place_tile(0, 0, 'A')  # place succeeds
    assert not b.is_empty(0, 0)

def test_place_tile_and_collision_and_center():
    b = Board()
    # center initially empty
    assert b.is_empty(7, 7)
    assert b.place_tile(7, 7, '*')
    assert b.get_tile(7, 7) == '*'
    # cannot place where already occupied
    assert not b.place_tile(7, 7, 'B')

def test_get_tile_and_bonus_values():
    b = Board()
    # center bonus
    assert b.get_bonus(7, 7) == b.CENTER
    # known triple word corner
    assert b.get_bonus(0, 0) == b.TRIPLE_WORD
    # place and read tile
    assert b.place_tile(0, 0, 'Z')
    assert b.get_tile(0, 0) == 'Z'

def test_boundaries_and_invalid_access():
    b = Board()
    # placing out of bounds fails
    assert not b.place_tile(15, 15, 'X')
    # invalid get returns None
    assert b.get_tile(15, 0) is None
    assert b.get_bonus(-1, 0) is None

def test_sample_bonus_layout():
    b = Board()
    # sample checks for several bonus types
    assert b.get_bonus(1, 1) == b.DOUBLE_WORD
    assert b.get_bonus(1, 5) == b.TRIPLE_LETTER
    assert b.get_bonus(0, 3) == b.DOUBLE_LETTER

def test_is_center_occupied():
    b = Board()
    assert not b.is_center_occupied()
    b.place_tile(7, 7, 'A')
    assert b.is_center_occupied()

def test_is_connected_first_word():
    b = Board()
    # First word must use center
    assert not b.is_connected(0, 0)
    assert b.is_connected(7, 7)

def test_is_connected_adjacent_tiles():
    b = Board()
    b.place_tile(7, 7, 'A')
    # Adjacent to center should be connected
    assert b.is_connected(7, 8)
    assert b.is_connected(6, 7)
    assert not b.is_connected(5, 5)

class MockTile:
    def __init__(self, letter):
        self.letter = letter

def test_get_word_horizontal():
    b = Board()
    b.place_tile(5, 5, MockTile('C'))
    b.place_tile(5, 6, MockTile('A'))
    b.place_tile(5, 7, MockTile('T'))

    word, start_col, tiles = b.get_word_horizontal(5, 6)
    assert word == "CAT"
    assert start_col == 5
    assert len(tiles) == 3

def test_get_word_vertical():
    b = Board()
    b.place_tile(5, 5, MockTile('D'))
    b.place_tile(6, 5, MockTile('O'))
    b.place_tile(7, 5, MockTile('G'))

    word, start_row, tiles = b.get_word_vertical(6, 5)
    assert word == "DOG"
    assert start_row == 5
    assert len(tiles) == 3

def test_get_all_formed_words():
    b = Board()
    b.place_tile(5, 5, MockTile('C'))
    b.place_tile(5, 6, MockTile('A'))
    b.place_tile(5, 7, MockTile('T'))

    words = b.get_all_formed_words([(5, 5), (5, 6), (5, 7)])
    assert len(words) == 1
    assert words[0][0] == "CAT"
