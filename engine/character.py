import pyglet

from engine.util import get_files_in_path


class CharacterSprite:

    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'
    IDLE = 'idle'
    THROW_UP = 'throw_up'
    THROW_DOWN = 'throw_down'
    THROW_LEFT = 'throw_left'
    THROW_RIGHT = 'throw_right'

    def __init__(self, id, path, x, y, speed, batch=None, group=None, action=IDLE):
        self.id = id
        self.path = path
        self.batch = batch
        self.group = group
        # These are the true x/y we consider the sprite to be at
        self.x = x
        self.y = y
        self.scale = 0.25
        self.animation = None
        # Sprite x/y is offset due to the anchor point not being in center
        self.sprite = self._generate_sprite()
        self.action = action
        self.speed = speed
        self.dest_x = None
        self.dest_y = None

        self.items = list()

    def _generate_sprite(self):
        # Set up animation for character sprite
        walk_frames = [pyglet.resource.image(self.path + f)
                       for f in get_files_in_path(self.path)]
        self.animation = pyglet.image.Animation.from_image_sequence(
            walk_frames,
            duration=0.1,
            loop=True
        )

        # Set up character sprite
        character_sprite = pyglet.sprite.Sprite(
            self.animation,
            group=self.group,
            batch=self.batch,
            x=self.convert_x(),
            y=self.convert_y()
        )
        character_sprite.scale = self.scale

        return character_sprite

    def convert_x(self):
        # Need these to offset the sprite due to anchor being on the bottom left
        return self.x - self.animation.get_max_width() * self.scale / 2

    def convert_y(self):
        # Need these to offset the sprite due to anchor being on the bottom left
        return self.y - self.animation.get_max_height() * self.scale / 2

    def at_destination(self):
        return self.dest_x == None and self.dest_y == None

    def update(self, dt):
        # If destination not set, then don't move
        if self.at_destination():
            return True
        if self.action == CharacterSprite.UP:
            reached_dest = self.move_up(self.speed, dt, self.dest_y)
        elif self.action == CharacterSprite.DOWN:
            reached_dest = self.move_down(self.speed, dt, self.dest_y)
        elif self.action == CharacterSprite.RIGHT:
            reached_dest = self.move_right(self.speed, dt, self.dest_x)
        elif self.action == CharacterSprite.LEFT:
            reached_dest = self.move_left(self.speed, dt, self.dest_x)
        elif self.action == CharacterSprite.IDLE:
            reached_dest = True
        else:
            raise ValueError(
                "Got an unsupported action: {d}".format(d=self.action)
            )
        if reached_dest:
            self.wipe_destination()
        return reached_dest

    def wipe_destination(self):
        self.dest_x = None
        self.dest_y = None

    def move_up(self, speed, dt, dest_y):
        new_y = self.y + speed * dt
        reached_destination = False
        if new_y > dest_y:
            self.y = dest_y
            reached_destination = True
        else:
            self.y = new_y
        self.sprite.y = self.convert_y()
        return reached_destination

    def move_down(self, speed, dt, dest_y):
        new_y = self.y - speed * dt
        reached_destination = False
        if new_y < dest_y:
            self.y = dest_y
            reached_destination = True
        else:
            self.y = new_y
        self.sprite.y = self.convert_y()
        return reached_destination

    def move_right(self, speed, dt, dest_x):
        new_x = self.x + speed * dt
        reached_destination = False
        if new_x > dest_x:
            self.x = dest_x
            reached_destination = True
        else:
            self.x = new_x
        self.sprite.x = self.convert_x()
        return reached_destination

    def move_left(self, speed, dt, dest_x):
        new_x = self.x - speed * dt
        reached_destination = False
        if new_x < dest_x:
            self.x = dest_x
            reached_destination = True
        else:
            self.x = new_x
        self.sprite.x = self.convert_x()
        return reached_destination
