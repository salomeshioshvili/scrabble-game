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
