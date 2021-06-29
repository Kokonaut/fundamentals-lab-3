import pyglet
import time

from engine.character import CharacterSprite
from engine.grid import Grid
from engine.log_spam import LogSpam
from engine.throwable import Throwable


class Game:

    CHARACTER_SPEED = 100  # Character movement in pixels per second
    FPS = 30  # frames per second (aka speed of the game)
    THROWABLE_COMMANDS = {
        CharacterSprite.THROW_UP,
        CharacterSprite.THROW_DOWN,
        CharacterSprite.THROW_LEFT,
        CharacterSprite.THROW_RIGHT
    }
    THROW_DISTANCE = 2

    def __init__(self, window, rows, cols):
        # Set up batch and ordered groups
        self.bg_batch = pyglet.graphics.Batch()
        self.main_batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.OrderedGroup(0)
        self.midground = pyglet.graphics.OrderedGroup(1)
        self.terrainground = pyglet.graphics.OrderedGroup(2)
        self.foreground = pyglet.graphics.OrderedGroup(3)

        # Set up window and grid variables
        self.window = window
        self.window_block_width = cols
        self.cols = cols
        self.rows = rows
        self.grid = Grid(self.rows, self.cols, self.window.width)

        # Set up background
        bg_image = pyglet.image.load('assets/background/main_bg.png')
        self.bg_sprite = pyglet.sprite.Sprite(
            bg_image,
            batch=self.bg_batch,
            group=self.background
        )
        height_scale = self.window.height / self.bg_sprite.height
        width_scale = self.window.width / self.bg_sprite.width
        self.bg_sprite.scale = max(height_scale, width_scale)

        # Set up character sprite info
        self.characters = dict()
        self.throwables = list()

        # State keeping variables
        self.tick = 0
        self.log_spam = LogSpam()

        # Set up environment objects
        self.obstacles = dict()
        self.terrain = dict()
        self.goals = dict()
        self.finish = None
        self.num_goals = 0

        # Lab decision generator
        self.decision_func = None

    def on_draw(self):
        self.window.clear()
        self.bg_batch.draw()
        self.draw_grid()
        self.main_batch.draw()

    def start_game(self):
        self.window.push_handlers(
            on_draw=self.on_draw,
        )
        pyglet.clock.schedule_interval(self.update, 1.0 / self.FPS)

    def stop_game(self):
        print("Total steps taken: {steps}".format(steps=self.tick))
        print('Game shutting down')
        time.sleep(5)
        pyglet.clock.unschedule(self.update)
        self.window.remove_handlers()
        pyglet.app.exit()

    def add_decision_func(self, func):
        self.decision_func = func

    def set_character_commands(self, commands):
        self.commands = commands

    def update(self, dt):
        # Either in starting position or we reached destination on last update
        locked = False
        for id in self.characters:
            reached_destination = self.update_character(
                self.characters[id], dt)
            if not reached_destination:
                locked = True
        buff = list()
        for throwable in self.throwables:
            reached_destination = throwable.update(dt)
            if reached_destination:
                coord_name = self.grid.calculate_grid_position_name(
                    throwable.sprite.x,
                    throwable.sprite.y
                )
                if coord_name in self.goals:
                    self.goals[coord_name].append(throwable.sprite)
                else:
                    self.goals[coord_name] = [throwable.sprite]
            else:
                buff.append(throwable)
                locked = True
        self.throwables = buff
        if not locked:
            self.tick += 1
            self.set_next_actions()

    def set_next_actions(self):
        for id in self.characters:
            character = self.characters[id]
            self.update_character_action(character)
            self.set_character_destination(character)

    def update_character(self, character, dt):
        reached_destination = character.update(dt)
        if reached_destination:
            self.check_collision(character)
        return reached_destination

    def add_character(self, id, path, coord_x, coord_y):
        x, y = self.grid.calculate_xy_values(coord_x, coord_y)
        self.characters[id] = CharacterSprite(
            id,
            path,
            x,
            y,
            self.CHARACTER_SPEED,
            self.main_batch,
            self.foreground
        )

    def update_character_action(self, character):
        coord_name = self.grid.calculate_grid_position_name(
            character.x,
            character.y
        )

        log_message = "{char_name} at: {coord}".format(
            char_name=character.id,
            coord=coord_name
        )
        if self.log_spam.check(character.id, log_message):
            print(log_message)

        if self.decision_func:
            # Account for 0 indexed list of commands
            current_tick = self.tick - 1
            new_action = self.decision_func(character.id, current_tick)
            if new_action:
                if new_action in self.THROWABLE_COMMANDS:
                    self.handle_throw(character, new_action)
                    new_action = CharacterSprite.IDLE
                character.action = new_action
            else:
                character.action = CharacterSprite.IDLE

    def handle_throw(self, character, new_action):
        if len(character.items) == 0:
            return
        item = character.items.pop()
        dest_x, dest_y = self.get_throw_destination(
            character.x,
            character.y,
            new_action
        )
        self.throwables.append(
            Throwable(
                item,
                character.x,
                character.y,
                new_action,
                dest_x,
                dest_y,
                self.CHARACTER_SPEED * 4
            )
        )

    def check_collision(self, character):
        sprite_coord_name = self.grid.calculate_grid_position_name(
            character.x, character.y
        )
        obstacle_coord_name = self.check_obstacle_collision(sprite_coord_name)
        goal_coord_name = self.check_goal_collision(sprite_coord_name)
        if obstacle_coord_name:
            print("Ran into the obstacle at {name}. Game over!".format(
                name=obstacle_coord_name
            ))
            self.stop_game()
        if goal_coord_name:
            print("Got the treasure at {name}".format(name=goal_coord_name))
            for goal_item in self.goals[goal_coord_name]:
                goal_item.visible = False
                character.items.append(goal_item)
            del self.goals[goal_coord_name]
        self.check_finish_collision(sprite_coord_name, character)
        self.check_boundary_collision(character)

    def check_goal_collision(self, coord_name):
        if coord_name in self.goals:
            return coord_name
        return None

    def check_obstacle_collision(self, coord_name):
        if coord_name in self.obstacles and not coord_name in self.terrain:
            return coord_name
        return None

    def check_finish_collision(self, coord_name, character):
        finish_coord_name = self.grid.calculate_grid_position_name(
            self.finish.x,
            self.finish.y
        )
        if finish_coord_name == coord_name:
            if len(character.items) >= self.num_goals:
                print("You got all the treasure! You win!")
            else:
                print("You did not get all the treasure. Game over!")
            self.stop_game()

    def check_boundary_collision(self, sprite):
        coord_x, coord_y = self.grid.calculate_grid_position(
            sprite.x, sprite.y
        )
        if (
            coord_x < 0 or coord_y < 0
            or coord_x >= self.cols-1 or coord_y >= self.rows-1
        ):
            print("Out of bounds. Game over!")
            self.stop_game()

    def set_character_destination(self, character):
        current_x, current_y = self.grid.calculate_grid_position(
            character.x,
            character.y
        )
        next_x, next_y = self.get_next_destination(
            current_x,
            current_y,
            character.action
        )
        pixel_x, pixel_y = self.grid.calculate_xy_values(next_x, next_y)
        character.dest_x = pixel_x
        character.dest_y = pixel_y

    def get_next_destination(self, current_x, current_y, action):
        if action == CharacterSprite.UP:
            return current_x, current_y+1
        if action == CharacterSprite.DOWN:
            return current_x, current_y-1
        if action == CharacterSprite.LEFT:
            return current_x-1, current_y
        if action == CharacterSprite.RIGHT:
            return current_x+1, current_y
        return current_x, current_y

    def get_throw_destination(self, current_x, current_y, action):
        grid_x, grid_y = self.grid.calculate_grid_position(
            current_x,
            current_y
        )
        if action == CharacterSprite.THROW_UP:
            grid_y += self.THROW_DISTANCE
        elif action == CharacterSprite.THROW_DOWN:
            grid_y -= self.THROW_DISTANCE
        elif action == CharacterSprite.THROW_RIGHT:
            grid_x += self.THROW_DISTANCE
        elif action == CharacterSprite.THROW_LEFT:
            grid_x -= self.THROW_DISTANCE
        else:
            raise("Invalid throw action")
        return self.grid.calculate_xy_values(grid_x, grid_y)

    def draw_grid(self):
        self.grid.draw_grid()
        self.draw_grid_labels()

    def draw_grid_labels(self):
        self.draw_col_labels()
        self.draw_row_labels()

    def draw_col_labels(self):
        i = 0
        for x_pos in self.grid.get_x_lines():
            char = self.grid.convert_int_to_letter(i)
            i += 1
            col_label = pyglet.text.Label(
                text=char,
                x=x_pos,
                y=self.grid.offset,
                anchor_x='center'
            )
            col_label.draw()

    def draw_row_labels(self):
        i = 0
        for y_pos in self.grid.get_y_lines():
            row_label = pyglet.text.Label(
                text=str(i),
                x=self.grid.offset,
                y=y_pos,
                anchor_x='center'
            )
            i += 1
            row_label.draw()

    def add_obstacles(self, path, coords):
        for coord_name in coords:
            x, y = self.grid.calculate_xy_from_name(coord_name)
            sprite = self._add_terrain(path, x, y, self.midground)
            self.obstacles[coord_name] = sprite

    def _add_terrain(self, path, x, y, group):
        obstacle_image = pyglet.resource.image(path)
        obstacle_image.anchor_x = obstacle_image.width // 2
        obstacle_image.anchor_y = obstacle_image.height // 2
        obstacle_sprite = pyglet.sprite.Sprite(
            obstacle_image,
            batch=self.main_batch,
            x=x,
            y=y,
            group=group
        )
        height_scale = self.grid.cell_length / obstacle_sprite.height
        width_scale = self.grid.cell_length / obstacle_sprite.width
        obstacle_sprite.scale = min(height_scale, width_scale)
        return obstacle_sprite

    def add_terrain(self, path, coords):
        for coord_name in coords:
            x, y = self.grid.calculate_xy_from_name(coord_name)
            sprite = self._add_terrain(path, x, y, self.terrainground)
            self.terrain[coord_name] = sprite

    def add_goals(self, coords):
        for coord_name in coords:
            x, y = self.grid.calculate_xy_from_name(coord_name)
            sprite = self._add_goal(x, y)
            self.goals[coord_name] = [sprite]

    def _add_goal(self, x, y):
        goal_image = pyglet.resource.image('assets/diamond.png')
        goal_image.anchor_x = goal_image.width // 2
        goal_image.anchor_y = goal_image.height // 2
        goal_sprite = pyglet.sprite.Sprite(
            goal_image,
            batch=self.main_batch,
            x=x,
            y=y,
            group=self.terrainground
        )
        self.num_goals += 1
        return goal_sprite

    def add_finish(self, coord):
        x, y = self.grid.calculate_xy_from_name(coord)
        finish_image = pyglet.resource.image('assets/finish.png')
        finish_image.anchor_x = finish_image.width // 2
        finish_image.anchor_y = finish_image.height // 2
        self.finish = pyglet.sprite.Sprite(
            finish_image,
            batch=self.main_batch,
            x=x,
            y=y,
            group=self.midground
        )
        self.finish.scale = 0.33
