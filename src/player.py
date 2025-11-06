# - Store each player's rack (letters) and current score.
# - Provide methods to add/remove/draw tiles.
# - Track player-specific state (e.g., consecutive passes).
class Player():
  def __init__(self, rack, score):
    self.rack = rack  # List of Tile objects
    self.score = score

