# Game Rules

- Board: 15 × 15 grid.
- Rack: Each player holds up to 7 tiles.
- Objective: Form valid words (left→right or top→bottom) using tiles from your rack.
- First move: Must cover the center square (7,7) and form at least one word.
- Placement rules:
  - New tiles must form a contiguous horizontal or vertical sequence.
  - New tiles must connect to existing tiles (share an edge) unless it is the first move.
  - All words created (the main word and any cross words) must be valid dictionary words.
- Scoring:
  - Word score = sum of letter values, applying letter and word multipliers from the board.
  - Only newly placed tiles consume the square bonuses (DL/TL/DW/TW).
  - Bingo: using all 7 tiles in one move grants +50 points.
- Passing & exchanging:
  - A player may pass their turn (counts toward consecutive passes).
  - Tile exchange (if implemented) typically consumes your turn and requires enough tiles in the bag.
- End of game:
  - Game ends when players pass repeatedly (e.g., two consecutive passes each) or when the tile bag is empty and a player has no tiles.
  - Final scoring adjustments (e.g., subtracting remaining rack points) depend on rules implemented in the project.
