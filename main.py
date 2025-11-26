from src.game import Game
from src.UI.frontend import ScrabbleUI

# Initialize game with 1 human player and 1 bot
game = Game(player_names=["Us"], bot_count=1)
ui = ScrabbleUI(game)

ui.show()