# API Reference

## src/board.py

Class: Board
- Board()  
  Create a 15×15 Scrabble board with bonus squares initialized.

Properties / constants:
- TRIPLE_WORD, DOUBLE_WORD, TRIPLE_LETTER, DOUBLE_LETTER, NORMAL, CENTER

Methods:
- is_valid_position(row: int, col: int) -> bool  
  Check if (row,col) is inside the board bounds.

- is_empty(row: int, col: int) -> bool  
  True if position is valid and contains no tile.

- place_tile(row: int, col: int, tile) -> bool
  Place `tile` if empty. Returns True on success.

- get_tile(row: int, col: int) -> Tile | None  
  Return the Tile at position or None.

- get_bonus(row: int, col: int) -> str | None  
  Return bonus type (e.g., "TW","DL","★") or None if out of bounds.

- is_center_occupied() -> bool  
  True if center (7,7) has a tile.

- is_connected(row: int, col: int) -> bool  
  Determine whether placing at (row,col) connects to existing tiles.
  Special case: if board empty, only (7,7) is valid.

- get_word_horizontal(row: int, col: int) -> (str|None, int|None, list)  
  If tile exists at (row,col), return tuple (word, start_col, tiles)
  where tiles is list of (row, col, Tile). Returns (None, None, []) for single letters or empty cells.

- get_word_vertical(row: int, col: int) -> (str|None, int|None, list)  
  Similar to horizontal but vertical.

- get_all_formed_words(placed_positions: Iterable[Tuple[int,int]]) -> List[Tuple[str, list]]
  Given newly placed positions, returns list of (word, tiles) for all formed words
  (horizontal and vertical). Does not mutate board.

- are_placements_line(placements: Dict[Tuple[int,int], Tile]) -> bool
  Validate that all placements form a single contiguous line (same row or column with no gaps).
  Returns True if valid, False if placements are scattered or have gaps.

---

## src/dictionary.py

Class: WordLookup
- WordLookup(filepath: str | Path | None = None)  
  Loads a word list into an internal Trie. If no path provided, loads default data/words.txt.

Methods:
- clean(word: str) -> str  
  Normalize and validate a word (lowercase, alphabetic).

- load_words(filepath: str | Path) -> None  
  Populate trie from file (side effect: prints loaded count).

- is_valid_word(word: str) -> bool  
  True if word exists in the loaded dictionary (case-insensitive).

---

## src/trie.py

Class: Trie
- Trie()  
  Create an empty trie.

Methods:
- insert(word: str) -> None  
  Insert a word into the trie.

- search(word: str) -> bool  
  Return True if word exactly exists.

- startsWith(prefix: str) -> bool  
  Return True if any word in trie starts with prefix.

Side effects: mutates trie internal structure on insert.

---

## src/tile.py

Class: Tile
- Tile(letter: str, value: int)  
  Simple container for tile letter and point value. Public attributes: letter, value.

Functions:
- create_tiles() -> List[Tile]  
  Returns a list of Tile objects representing the standard Scrabble distribution.

---

## src/player.py

Class: Player
- Player(name: str, rack: Optional[List[Tile]] = None, score: int = 0)  
  Represents a player with a rack, score and pass counter.

Methods:
- draw_tiles(tile_bag: List[Tile], x: int) -> None  
  Draw up to x tiles from `tile_bag` and append to player's rack.

- add_tile(tile: Tile) -> None  
  Add a tile to the rack.

- remove_tiles(tiles_to_remove: Sequence[Union[Tile,str]], strict: bool = False) -> bool  
  Remove matching tiles from rack. If strict=True, returns False and does nothing when missing tiles.

- has_tiles(tiles: Sequence[Union[Tile,str]]) -> bool  
  True if player has all tiles (by Tile identity or letter).

- match_tile(tile: Union[Tile,str]) -> Optional[Tile]  
  Return a Tile instance from rack that matches input or None.

- add_score(points: int) -> None  
  Increment player's score.

- pass_turn() -> None  
  Increment the player's pass counter.

- reset_passes() -> None  
  Reset pass counter to 0.

- __str__() -> str  
  Human-readable representation "Name: Score=X, Rack=[...]".

Class: TurnQueue
- TurnQueue(players: List[Player])  
  Initialize turn order (raises ValueError on empty list).

Methods:
- current_player() -> Player  
  Return player whose turn it currently is.

- next_turn() -> Player  
  Advance queue to next player and return them (mutates queue).

- get_turn_order() -> List[str]  
  Return current turn order as list of names (non-mutating).

Function:
- generate_tile_bag() -> List[Tile]  
  Return a shuffled list of Tile objects (calls create_tiles); side effect: returns randomized list.

---

## src/move_generator.py

Functions:
- generate_moves(board: Board, rack: List[Tile], dictionary: WordLookup) -> List[Dict[Tuple[int,int], Tile]]  
  Return candidate placements for the rack. Simplified generator:
  - If board empty, tries center-start horizontal words.
  - Otherwise, tries one-tile adjacent placements next to existing tiles.
  Returned moves are dicts mapping (row,col) -> Tile. Generated moves are validated against dictionary (no board persistence).

- generate_center_moves(rack: List[Tile], dictionary: WordLookup) -> List[Dict[Tuple[int,int], Tile]]  
  Generate horizontal placements covering center (7,7) using 2–7 tiles from rack; validates words.

- generate_adjacent_moves(board: Board, rack: List[Tile], dictionary: WordLookup) -> List[Dict[Tuple[int,int], Tile]]  
  For each occupied cell, consider empty neighboring cells and single-tile placements that produce valid words.

---

## src/move_suggester.py

Function:
- suggest_best_move(board: Board, rack: List[Tile], dictionary: WordLookup) -> Optional[Dict[Tuple[int,int], Tile]]  
  Uses generate_moves to enumerate candidate moves and calculate_move_score to pick the highest-scoring move. Returns placement dict or None if no moves. Does not persist moves to board.

---

## src/move_evaluator.py

Function:
- calculate_move_score(board: Board, placements: Dict[Tuple[int,int], Tile]) -> int  
  Compute total score for the provided placements, including:
  - All words formed (primary and cross words).
  - Letter and word bonuses (only applied for newly placed tiles).
  - Bingo bonus (+50 if 7 tiles used).
  The function temporarily places tiles on board.grid for word extraction and restores original cells before returning. It does not permanently mutate the board.

Parameters:
- board: Board — current board state (reads bonuses and existing tiles)
- placements: dict mapping (row,col) to Tile for newly placed tiles

Returns: integer total move score.

---

## src/game.py

Class: Game
- Game(player_names: Iterable[str] | None = None, dictionary_path: str | None = None, bot_count: int = 0)  
  Orchestrates players, board, dictionary, tile bag and turn queue. Initializes players and fills racks.

Properties:
- RACK_SIZE (class-level)
- board: Board
- dictionary: WordLookup
- tile_bag: List[Tile]
- players: List[Player]
- bot_players: List[Player]
- turn_queue: TurnQueue

Methods:
- current_player() -> Player
  Return player whose turn it is.

- is_bot_turn() -> bool
  True if current player is a bot (in bot_players).

- play_bot_move() -> bool
  If bot turn, suggest_best_move and play it (via play_move). Returns True if bot acted or passed.

- play_move(placements: Dict[Tuple[int,int], Tile]) -> bool  
  Main move application routine:
  1. Validate tiles belong to current player and target cells are valid/empty.
  2. Validate connectivity (first move must use center).
  3. Validate placements form a contiguous line (are_placements_line).
  4. Temporarily place tiles, extract formed words, validate against dictionary.
  5. Calculate score via calculate_move_score and add to player.
  6. Remove used tiles from rack, refill, reset passes and advance turn.
  Returns True if move completed, False if invalid (and reverts temporary placements).

- revert_placements(positions: List[Tuple[int,int]]) -> None
  Remove tiles from given positions (set to None).

- is_game_over() -> bool
  Game end conditions:
  - All players have passed >= 2 times OR
  - tile_bag empty and at least one player has empty rack.

- pass_turn() -> None
  Current player increments pass counter and turn advances.

- shuffle_rack() -> None
  Shuffle current player's rack in-place.

Helpers (internal):
- validate_tiles(player: Player, moves: List[Tuple[Tuple[int,int], Tile]]) -> bool
  Ensure tiles belong to player, positions valid and empty.

- validate_connectivity(moves: List[Tuple[Tuple[int,int], Tile]]) -> bool
  Ensure move touches existing tiles or covers center if board empty.

- refill_rack(player: Player) -> None
  Draw tiles from tile_bag up to RACK_SIZE.

--- 
End of API reference.
