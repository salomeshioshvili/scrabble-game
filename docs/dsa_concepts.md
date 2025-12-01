# DSA Concepts Used

This project uses a few core data structures and simple algorithms. Below are short, beginner-friendly explanations of what is used and why.

## Trie (prefix tree)
- What it is: A tree where each node represents a letter. Words are paths from the root to a terminal marker.
- Why used: Looking up whether a word exists or whether a prefix is valid is very fast (time proportional to the word length).
- Where: Used by WordLookup to validate words and support prefix checks for move generation.

## 2D Array (board grid)
- What it is: A simple list of rows, each row is a list of cells.
- Why used: The Scrabble board is a fixed-size grid (15×15). A 2D array offers direct access to any (row, col) cell.
- Where: Board.grid stores Tile objects or None.

## Adjacency / Simple Graph checks
- What it is: Checking the four neighbors (up/down/left/right) of a cell.
- Why used: To ensure placed tiles connect to existing tiles and to extract words formed across rows or columns.
- Where: Board.is_connected and the word extraction helpers.

## Backtracking
- What it is: A search technique that builds candidates step-by-step and abandons a candidate as soon as it cannot become valid.
- Current use: The project contains a simplified move generator that tests plausible placements. Full recursive backtracking with deep pruning is not implemented but planned.
- Benefit: Full backtracking with "Trie prefix pruning" reduces explored branches dramatically (you stop extending a partial word if no dictionary word starts with that prefix).

## Greedy selection for suggestions
- What it is: Generate many candidate moves and pick the one with the highest immediate score.
- Why used: It's fast to implement and usually yields good moves for a simple AI.
- Limitation: Does not plan for future rack balance or opponent blocking.

## Scoring logic
- What it is: For each word formed, sum letter values, apply letter multipliers for newly placed tiles, then apply word multipliers; add bingo bonus when 7 tiles used.
- Important note: Bonuses (DL/TL/DW/TW) apply only when the tile is newly placed on that bonus square.


