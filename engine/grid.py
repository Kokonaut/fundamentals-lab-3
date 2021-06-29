import pyglet


class Grid:

    LETTERS = 'abcdefghijklmnopqrstuvwxyz'

    def __init__(self, rows, cols, window_width):
        if cols > 24:
            raise ValueError("Too many columns")
        self.rows = rows
        self.cols = cols
        self.cell_length = int(window_width / self.cols)

        self.size = self.cell_length
        self.offset = self.cell_length / 2

    def convert_int_to_letter(self, number):
        if number > 24:
            raise ValueError("Number outside alphabet range")
        return self.LETTERS[number]

    def convert_letter_to_int(self, letter):
        return self.LETTERS.index(letter)

    def calculate_xy_values(self, coord_x, coord_y):
        """
        coord_string is of format "{character}{number}"
        For example, c4, indicating
            x = 2
            y = 4
        Returns x, y position in pixels
        """
        # Shift coord by 1 due to labels taking up first spot
        pix_x = (coord_x + 1) * self.size + self.offset
        pix_y = (coord_y + 1) * self.size + self.offset
        return pix_x, pix_y

    def calculate_grid_position(self, pix_x, pix_y):
        coord_x = self.translate_pixel_to_cell(pix_x)
        coord_y = self.translate_pixel_to_cell(pix_y)
        return coord_x, coord_y

    def calculate_grid_position_name(self, pix_x, pix_y):
        coord_x, coord_y = self.calculate_grid_position(pix_x, pix_y)
        return self.get_grid_position_name(coord_x, coord_y)

    def get_grid_position_name(self, coord_x, coord_y):
        char_x = self.convert_int_to_letter(coord_x)
        return char_x + str(coord_y)

    def calculate_grid_position_from_name(self, name):
        # name is of format {letter}{number} eg d4
        if len(name) != 2:
            raise ValueError('Invalid position name format')
        coord_x = self.convert_letter_to_int(name[0])
        coord_y = int(name[1])
        return coord_x, coord_y

    def calculate_xy_from_name(self, name):
        coord_x, coord_y = self.calculate_grid_position_from_name(name)
        return self.calculate_xy_values(coord_x, coord_y)

    def translate_pixel_to_cell(self, pixel_measure):
        cell = pixel_measure // self.cell_length
        # Subtract one due to the text labels taking up first spot
        cell -= 1
        return int(cell)

    def get_x_lines(self):
        x_lines = list()
        for i in range(1, self.cols):
            x_lines.append(self.size * i + self.offset)
        return x_lines

    def get_y_lines(self):
        y_lines = list()
        for i in range(1, self.rows):
            y_lines.append(self.size * i + self.offset)
        return y_lines

    def draw_grid(self):
        """
        Draw the grid lines of the board
        """
        pyglet.gl.glColor4f(0.63, 0.63, 0.63, 1.0)

        # Horizontal lines
        for i in range(self.rows):
            pyglet.graphics.draw(
                2, pyglet.gl.GL_LINES,
                ('v2i',
                    (
                        0,
                        i * self.cell_length,
                        self.cols * self.cell_length,
                        i * self.cell_length
                    )
                 )
            )
        # Vertical lines
        for j in range(self.cols):
            pyglet.graphics.draw(
                2, pyglet.gl.GL_LINES,
                ('v2i',
                    (
                        j * self.cell_length,
                        0,
                        j * self.cell_length,
                        self.cols * self.cell_length,
                    )
                 )
            )
