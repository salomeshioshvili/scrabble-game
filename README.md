# Scrabble Game - DSA Project

A Scrabble implementation in Python featuring advanced data structures and algorithms for efficient gameplay, word validation, and move generation.

---

## 📋 Table of Contents

- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Data Structures & Algorithms](#data-structures--algorithms)
- [Time & Space Complexity Analysis](#time--space-complexity-analysis)
- [Contributors](#contributors)

---

## 📁 Project Structure

```
scrabble-game/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── data/
│   └── words.txt          # Dictionary word list
├── docs/
│   ├── api_reference.md   # API documentation
│   ├── dsa_concepts.md    # DSA explanations
│   └── game_rules.md      # Scrabble rules
├── src/
│   ├── board.py           # Board representation & management
│   ├── dictionary.py      # Trie-based word validation
│   ├── game.py            # Game controller & state management
│   ├── move_evaluator.py  # Score calculation
│   ├── move_generator.py  # Legal move generation
│   ├── move_suggester.py  # AI move recommendations
│   ├── player.py          # Player & turn queue classes
│   ├── tile.py            # Tile representation
│   └── UI/
│       └── frontend.py    # Graphical user interface
└── tests/
    ├── test_board.py
    └── test_pile.py
```

---

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/salomeshioshvili/scrabble-game.git

# Navigate to project directory
cd scrabble-game

# Install dependencies
pip install -r requirements.txt
```

---

## 🎮 Usage

```bash
python main.py
```

**Game Controls:**
- Click on rack tiles to select
- Click on board to place selected tile
- **[Submit]** - Validate and submit your move
- **[Undo]** - Remove unsubmitted placements
- **[Pass]** - Skip your turn
- **[Shuffle]** - Randomize rack order

---

## 📊 Data Structures & Algorithms

### 1. Trie (Prefix Tree)
**Purpose:** Fast dictionary word validation and prefix checking

```
        root
       / | \
      C  D  H
      |  |  |
      A  O  E
      |  |  |
      T  G  L
            |
            L
            |
            O
```

**Operations:**
- `is_valid(word)` - Check if word exists in dictionary
- `is_prefix(prefix)` - Check if prefix can form valid words

### 2. 2D Array (Board Representation)
**Purpose:** Store tile placements and bonus square positions

```
15×15 Grid Structure:
┌────┬────┬────┬────┬────┐
│ TW │    │    │ DL │    │  TW = Triple Word
├────┼────┼────┼────┼────┤  DW = Double Word
│    │ DW │    │    │    │  TL = Triple Letter
├────┼────┼────┼────┼────┤  DL = Double Letter
│    │    │ DL │    │    │  ★  = Center (Start)
├────┼────┼────┼────┼────┤
│ DL │    │    │ TL │    │
├────┼────┼────┼────┼────┤
│    │    │    │    │ DW │
└────┴────┴────┴────┴────┘
```

### 3. Queue (Turn Management)
**Purpose:** Manage player turn order using circular queue

```python
# Using collections.deque for O(1) rotation
TurnQueue: [Player1] → [Player2] → [Player3] → [Player1]...
```

### 4. Priority Queue / Max-Heap (Move Suggestions)
**Purpose:** Rank and suggest best possible moves by score

```
        (45, "QUARTZ")
       /            \
  (32, "JAZZ")    (28, "XENON")
    /    \
(15,...)  (12,...)
```

### 5. Backtracking (Move Generation)
**Purpose:** Generate all valid word placements from rack tiles

```
Explore → Validate Prefix → Continue/Prune → Backtrack
```

---

## ⏱️ Time & Space Complexity Analysis

### Board Operations (`board.py`)

| Operation | Best Case | Worst Case | Space | Description |
|-----------|-----------|------------|-------|-------------|
| `__init__()` | O(n²) | O(n²) | O(n²) | Initialize n×n grid (n=15) |
| `initialize_bonus_squares()` | O(n²) | O(n²) | O(n²) | Set up bonus positions |
| `is_valid_position(row, col)` | O(1) | O(1) | O(1) | Bounds checking |
| `is_empty(row, col)` | O(1) | O(1) | O(1) | Check if cell is empty |
| `place_tile(row, col, tile)` | O(1) | O(1) | O(1) | Place tile at position |
| `get_tile(row, col)` | O(1) | O(1) | O(1) | Retrieve tile at position |
| `get_bonus(row, col)` | O(1) | O(1) | O(1) | Get bonus type at position |
| `is_connected(row, col)` | O(1) | O(1) | O(1) | Check adjacency (4 neighbors) |
| `get_word_horizontal(row, col)` | O(1) | O(n) | O(n) | Extract horizontal word |
| `get_word_vertical(row, col)` | O(1) | O(n) | O(n) | Extract vertical word |
| `get_all_formed_words(positions)` | O(k) | O(k × n) | O(k × n) | Get all words from k placements |

**Where:** n = board size (15), k = number of tiles placed

---

### Dictionary Operations (`dictionary.py` - Trie)

| Operation | Time Complexity | Space Complexity | Description |
|-----------|-----------------|------------------|-------------|
| `build_trie(words)` | O(W × L) | O(W × L) | Build trie from word list |
| `insert(word)` | O(m) | O(m) | Insert single word |
| `is_valid(word)` | O(m) | O(1) | Check if word exists |
| `is_prefix(prefix)` | O(m) | O(1) | Check if prefix is valid |
| `search(word)` | O(m) | O(1) | Search for word |

**Where:** W = number of words, L = average word length, m = query word length, A = alphabet size (26, treated as constant)

**Comparison with alternatives:**
| Data Structure | Lookup | Insert | Space | Prefix Check |
|----------------|--------|--------|-------|--------------|
| **Trie** | O(m) | O(m) | O(W×L) | O(m) ✅ |
| Hash Set | O(m) avg | O(m) | O(W×L) | O(W×L) ❌ |
| Sorted Array | O(m log W) | O(W) | O(W×L) | O(m log W) |

---

### Player & Turn Management (`player.py`)

| Operation | Time Complexity | Space Complexity | Description |
|-----------|-----------------|------------------|-------------|
| `Player.__init__()` | O(r) | O(r) | Initialize player with rack |
| `draw_tiles(bag, x)` | O(x) | O(1) | Draw x tiles from bag |
| `add_tile(letter)` | O(1) | O(1) | Add tile to rack |
| `remove_tiles(letters)` | O(r × k) | O(r) | Remove k tiles from rack |
| `has_tiles(letters)` | O(r × k) | O(r) | Check if player has tiles |
| `TurnQueue.__init__()` | O(p) | O(p) | Initialize with p players |
| `current_player()` | O(1) | O(1) | Get current player |
| `next_turn()` | O(1) | O(1) | Rotate to next player |

**Where:** r = rack size (7), k = tiles to check, p = number of players

---

### Tile Operations (`tile.py`)

| Operation | Time Complexity | Space Complexity | Description |
|-----------|-----------------|------------------|-------------|
| `Tile.__init__()` | O(1) | O(1) | Create tile object |
| `create_tiles()` | O(T) | O(T) | Generate full tile bag |
| `generate_tile_bag()` | O(T) | O(T) | Create shuffled bag |

**Where:** T = total tiles (100 in standard Scrabble)

---

### Move Evaluation (`move_evaluator.py`)

| Operation | Time Complexity | Space Complexity | Description |
|-----------|-----------------|------------------|-------------|
| `calculate_move_score()` | O(k × m + W × m) | O(W × m) | Calculate total score for a move |

**Breakdown:**
- Temporarily place/remove tiles: O(k)
- `get_all_formed_words()`: O(k × m) worst-case
- Score all words with bonuses: O(W × m)
- Bingo check: O(1)

**Where:** k = tiles placed (≤7), W = words formed, m = max word length (≤15)

---

### UI Operations (`frontend.py`)

| Operation | Time Complexity | Space Complexity | Description |
|-----------|-----------------|------------------|-------------|
| `_draw_bonus_cells()` | O(n²) | O(1) | Render bonus squares |
| `_render_tiles()` | O(n²) | O(1) | Render all board tiles |
| `_render_rack()` | O(r) | O(1) | Render player rack |
| `_on_board_click()` | O(1) | O(1) | Handle click event |

---

### Space Complexity Summary

| Component | Space | Description |
|-----------|-------|-------------|
| Board | O(n²) | 15×15 grid |
| Trie | O(W × L) | Dictionary storage |
| Tile Bag | O(T) | 100 tiles |
| Player Data | O(p × r) | Players with racks |

---

## 👥 Contributors

| Name | Role |
|------|------|
| **SALOME SHIOSHVILI** | Project Lead |
| **RAJI NASR ALLAH** | Developer |
| **ALAYIED MOHAMMED HASSAN Y** | Developer |

---

## 📚 References

- [Scrabble Rules](docs/game_rules.md)
- [API Documentation](docs/api_reference.md)
- [DSA Concepts](docs/dsa_concepts.md)
