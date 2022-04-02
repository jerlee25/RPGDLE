import arcade
from actual.guidle import *

window = arcade.Window(750, 700, "RPGDLE")
start_view = GameView()
window.show_view(start_view)
arcade.run()
