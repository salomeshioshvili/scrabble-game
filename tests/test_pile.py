# - Test drawing tiles, refilling player racks, and empty-bag scenarios.
# - Ensure tile frequencies match official distribution.
from collections import Counter
from src.tile import create_tiles, Tile

def test_create_tiles_count():
    tiles = create_tiles()
    assert len(tiles) == 100

def test_tile_instances_and_counts():
    tiles = create_tiles()
    assert all(isinstance(t, Tile) for t in tiles)
    counts = Counter(t.letter for t in tiles)
    assert counts['A'] == 9
    assert counts['_'] == 2
    assert counts['Z'] == 1

def test_tile_values_for_special_letters():
    tiles = create_tiles()
    values = {t.letter: t.value for t in tiles if t.letter in {'Q', 'Z', '_'}}
    assert values['Q'] == 10
    assert values['Z'] == 10
    assert values['_'] == 0
