import pyglet
from engine.game import Game
from lab import lab_run_big, lab_actions_big

window_width = 1440
rows = 9
cols = 16
window_ratio = cols / rows
window_height = int(window_width / window_ratio)

# Set up a window
game_window = pyglet.window.Window(window_width, window_height)

game = Game(game_window, rows, cols)

sprite_base_path = "assets/archer_sprite_{num}/"
i = 1
for key in lab_actions_big:
    # Max 3 characters
    if i > 3:
        continue
    game.add_character(
        key,
        sprite_base_path.format(num=i),
        0, 0
    )
    i += 1

obstacles = [
    'c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7',
    'g0', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7',
    'k0', 'k1', 'k2', 'k3', 'k4', 'k5', 'k6', 'k7',
]
game.add_obstacles('assets/river/river_6.png', obstacles)

game.add_terrain('assets/background/bridge.png', ['c4', 'g7', 'k7'])

goals = ['b7', 'b3', 'i0', 'o1']
game.add_goals(goals)

game.add_finish('i5')

game.add_decision_func(lab_run_big)

if __name__ == '__main__':
    game.start_game()
    pyglet.app.run()
