class Throwable:

    def __init__(self, sprite, x, y, direction, dest_x, dest_y, speed):
        self.sprite = sprite
        self.sprite.x = x
        self.sprite.y = y
        self.sprite.visible = True

        self.dest_x = dest_x
        self.dest_y = dest_y

        self.velocity_x = 0
        self.velocity_y = 0
        if direction == 'throw_up':
            self.velocity_y = speed
        elif direction == 'throw_down':
            self.velocity_y = -speed
        elif direction == 'throw_right':
            self.velocity_x = speed
        elif direction == 'throw_left':
            self.velocity_x = -speed

    def update(self, dt):
        curr_x = self.sprite.x
        curr_y = self.sprite.y
        next_x = curr_x + self.velocity_x * dt
        next_y = curr_y + self.velocity_y * dt

        reached_x = self.update_x(next_x)
        reached_y = self.update_y(next_y)
        return reached_x and reached_y

    def update_x(self, next_x):
        """
        Returns True/False if reached destination
        """
        if self.velocity_x > 0:
            if next_x < self.dest_x:
                self.sprite.x = next_x
                return False
            else:
                self.sprite.x = self.dest_x
                return True
        elif self.velocity_x < 0:
            if next_x > self.dest_x:
                self.sprite.x = next_x
                return False
            else:
                self.sprite.x = self.dest_x
                return True
        else:
            # In this case, there is no velocity, so always at destination
            return True

    def update_y(self, next_y):
        """
        Returns True/False if reached estination
        """
        if self.velocity_y > 0:
            if next_y < self.dest_y:
                self.sprite.y = next_y
                return False
            else:
                self.sprite.y = self.dest_y
                return True
        elif self.velocity_y < 0:
            if next_y > self.dest_y:
                self.sprite.y = next_y
                return False
            else:
                self.sprite.y = self.dest_y
                return True
        else:
            # In this case, there is no velocity, so always at destination
            return True
