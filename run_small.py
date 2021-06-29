import pyglet
from engine.game import Game
from lab import lab_run_small, lab_actions_small

window_width = 500
rows = 4
cols = 4
window_ratio = cols / rows
window_height = int(window_width / window_ratio)

# Set up a window
game_window = pyglet.window.Window(window_width, window_height)

game = Game(game_window, rows, cols)

sprite_base_path = "assets/archer_sprite_{num}/"
i = 1
for key in lab_actions_small:
    # Max 3 characters
    if i > 3:
        continue
    game.add_character(
        key,
        sprite_base_path.format(num=i),
        0, 0
    )
    i += 1

obstacles = ['b0', 'b1', 'b2']
game.add_obstacles('assets/river/river_6.png', obstacles)
game.add_terrain('assets/background/bridge.png', ['b0'])

goals = ['a2']
game.add_goals(goals)

game.add_finish('c2')

game.add_decision_func(lab_run_small)

if __name__ == '__main__':
    game.start_game()
    pyglet.app.run()
