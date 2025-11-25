from trie import Trie


"""Look up functionality using a Trie for efficient word validation."""
class WordLookup:
    def __init__(self, filepath="./data/words.txt"):
        self.trie = Trie()
        self.load_words(filepath)

    def clean(self, word: str) -> str:
        word = word.strip().lower()
        # Keep only alphabetic words (Scrabble uses A–Z)
        return word if word.isalpha() else ""

    def load_words(self, filepath: str):
        print("Loading dictionary...")
        count = 0

        with open(filepath, "r") as file:
            for line in file:
                word = self.clean(line)
                if word:
                    self.trie.insert(word)
                    count += 1

        print(f"Loaded {count} valid words into trie.")

    def is_valid_word(self, word: str) -> bool:
        return self.trie.search(word.lower())
    
