from pathlib import Path
from .trie import Trie

"""Look up functionality using a Trie for efficient word validation."""
class WordLookup:
    """ Lightweight wrapper around the Trie that loads the Scrabble dictionary. """

    def __init__(self, filepath: str | Path | None = None):
        self.trie = Trie()
        default_path = Path(__file__).resolve().parents[1] / "data" / "words.txt"
        self.load_words(filepath or default_path)

    def clean(self, word: str) -> str:
        word = word.strip().lower()
        # Keep only alphabetic words (Scrabble uses A–Z)
        return word if word.isalpha() else ""

    def load_words(self, filepath: str | Path):
        """Populate the trie with valid dictionary entries."""
        path = Path(filepath)
        count = 0

        with path.open("r", encoding="utf-8") as file:
            for line in file:
                word = self.clean(line)
                if word:
                    self.trie.insert(word)
                    count += 1

        print(f"Loaded {count} valid words into trie.")

    def is_valid_word(self, word: str) -> bool:
        return self.trie.search(word.lower())
