from src.game import Game
from src.UI.frontend import ScrabbleUI

game = Game()
ui = ScrabbleUI(game)

ui.show()