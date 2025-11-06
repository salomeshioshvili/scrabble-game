# - Represent individual tiles with a letter and point value.
# - Keep this file very lightweight.

class Tile:
    def __init__(self, letter: str, value: int):
        self.letter = letter
        self.value = value


def createTiles():
    """Creates standard Scrabble tiles with their point values.

    Returns:
        List[Tile]: A list of Tile objects representing the standard Scrabble set.
    """
    tile_distribution = {
        'A': (1, 9), 'B': (3, 2), 'C': (3, 2), 'D': (2, 4),
        'E': (1, 12), 'F': (4, 2), 'G': (2, 3), 'H': (4, 2),
        'I': (1, 9), 'J': (8, 1), 'K': (5, 1), 'L': (1, 4),
        'M': (3, 2), 'N': (1, 6), 'O': (1, 8), 'P': (3, 2),
        'Q': (10, 1), 'R': (1, 6), 'S': (1, 4), 'T': (1, 6),
        'U': (1, 4), 'V': (4, 2), 'W': (4, 2), 'X': (8, 1),
        'Y': (4, 2), 'Z': (10, 1), '_': (0, 2)  # Blank tiles
    }

    tileBag = []
    for letter, (value, count) in tile_distribution.items():
        for _ in range(count):
            tileBag.append(Tile(letter, value))
    return tileBag


TestTiles = createTiles()
print (f"Created {len(TestTiles)} tiles.")