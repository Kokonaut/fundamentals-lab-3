import pyglet
from engine.game import Game
from lab import lab_run_med, lab_actions_med

window_width = 800
rows = 6
cols = 8
window_ratio = cols / rows
window_height = int(window_width / window_ratio)

# Set up a window
game_window = pyglet.window.Window(window_width, window_height)

game = Game(game_window, rows, cols)

sprite_base_path = "assets/archer_sprite_{num}/"
i = 1
for key in lab_actions_med:
    # Max 3 characters
    if i > 3:
        continue
    game.add_character(
        key,
        sprite_base_path.format(num=i),
        0, 0
    )
    i += 1

obstacles = ['c0', 'c1', 'c2', 'c3', 'c4', 'f0', 'f1', 'f2', 'f3', 'f4']
game.add_obstacles('assets/river/river_6.png', obstacles)
game.add_terrain('assets/background/bridge.png', ['c0', 'f2'])

goals = ['a4', 'b2', 'e1']
game.add_goals(goals)

game.add_finish('g4')

game.add_decision_func(lab_run_med)

if __name__ == '__main__':
    game.start_game()
    pyglet.app.run()
