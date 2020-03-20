import arcade
import random

# Screen Constants
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
SCREEN_TITLE = "Breakout"
SCREEN_COLOR = arcade.color.BLACK

# Wall Constants
WALL_Y = SCREEN_HEIGHT / 2
WALL_HEIGHT = 560
WALL_WIDTH = 24
WALL_COLOR = arcade.color.GRAY

# Roof Constants
ROOF_X = SCREEN_WIDTH / 2
ROOF_Y = 600
ROOF_HEIGHT = 24
ROOF_WIDTH = 480
ROOF_COLOR = arcade.color.GRAY

# Block Constants
BLCK_WIDTH = 36
BLCK_HEIGHT = 12
BLCK_PER_LINE = 12
BLCK_NUM_LINES = 8

# Paddle Constants
PDDL_X = 240
PDDL_Y = 100
PDDL_WIDTH = 50
PDDL_HEIGHT = 10
PDDL_COLOR = arcade.color.VIVID_SKY_BLUE

# Ball Constants
BALL_X = 240
BALL_Y = 115
BALL_RADIUS = 5
BALL_COLOR = arcade.color.RED

# Score Constants


class Shape:

    def __init__(self, x, y, width, height, color, 
                 angle=0, delta_x=0, delta_y=0, delta_angle=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.angle = angle
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.delta_angle = delta_angle

    def move(self):
        self.x += self.delta_x
        self.y += self.delta_y
        self.angle += self.delta_angle


class Rectangle(Shape):

    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height,
                                     self.color)


class Circle(Shape):

    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.radius, self.color)


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        # Call the parent class and set up the window
        super().__init__(width, height, title)

        # Lists to track objects
        self.wall_list = None
        self.block_list = None

        # Variables for single instance objects
        self.roof = None
        self.paddle = None
        self.ball = None
        self.score = None

        arcade.set_background_color(SCREEN_COLOR)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        # Create the shape lists
        self.wall_list= []
        self.block_list = []

        # Setup the walls
        l_wall = Rectangle(WALL_WIDTH/2, WALL_Y, 
                           WALL_WIDTH, WALL_HEIGHT, WALL_COLOR)
        r_wall = Rectangle(SCREEN_WIDTH-WALL_WIDTH/2, WALL_Y, 
                           WALL_WIDTH, WALL_HEIGHT, WALL_COLOR)
        self.wall_list.extend([l_wall, r_wall])

        # Setup the blocks
        block_xs = [(WALL_WIDTH + BLCK_WIDTH/2) + (BLCK_WIDTH * n)
                    for n in range(BLCK_PER_LINE)]
        block_ys = [400 + (10 * n) for n in range(BLCK_NUM_LINES)]
        block_colors = [arcade.color.YELLOW, arcade.color.YELLOW,
                        arcade.color.GREEN, arcade.color.GREEN,
                        arcade.color.ORANGE, arcade.color.ORANGE,
                        arcade.color.RED, arcade.color.RED]
        for i in range(BLCK_NUM_LINES):
            for j in range(BLCK_PER_LINE):
                x, y = block_xs[j], block_ys[i]
                color = block_colors[i]
                block = Rectangle(x, y, BLCK_WIDTH, BLCK_HEIGHT, color)
                self.block_list.append(block)

        # Setup the roof
        roof = Rectangle(ROOF_X, ROOF_Y, ROOF_WIDTH, ROOF_HEIGHT, ROOF_COLOR)
        self.roof = roof

        # Setup the paddle
        paddle = Rectangle(PDDL_X, PDDL_Y, PDDL_WIDTH, PDDL_HEIGHT, PDDL_COLOR)
        self.paddle = paddle

        # Setup the ball
        ball = Circle(BALL_X, BALL_Y, BALL_RADIUS, BALL_COLOR)
        self.ball = ball


    def on_draw(self):
        """ Render the screen. """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color and erase what we drew last frame.
        arcade.start_render()

        # Call draw() on all objects
        for wall in self.wall_list:
            wall.draw()
        for block in self.block_list:
            block.draw()
        self.roof.draw()
        self.paddle.draw()
        self.ball.draw()

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """ Called whenever the user lets off a previously pressed key. """
        pass


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()

    # Run the program
    arcade.run()


if __name__ == "__main__":
    main()