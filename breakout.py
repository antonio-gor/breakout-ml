""" Breakout """
import sys
import random
import pygame

# Screen Constants
SCREEN_SIZE = 480, 640
STATS_X, STATS_Y = 140, 10
FPS = 60

# Color Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 128, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)

# Ball Constants
BALL_DIAMETER = 15  # TODO: Variable ball size
BALL_RADIUS = int(BALL_DIAMETER / 2)
MAX_BALL_X = SCREEN_SIZE[0] - BALL_DIAMETER
MAX_BALL_Y = SCREEN_SIZE[1] - BALL_DIAMETER

# Paddle Constant
PADDLE_WIDTH = 40  # TODO: Variable paddle width
PADDLE_HEIGHT = 8
MAX_PADDLE_X = SCREEN_SIZE[0] - PADDLE_WIDTH
PADDLE_Y = SCREEN_SIZE[1] - PADDLE_HEIGHT - 10
PADDLE_SPEED = 5

# Brick Constants
BRICK_WIDTH = 30
BRICK_HEIGHT = 6
BRICK_LINES = 8
BRICK_PER_LINE = 12
BRICK_COLORS = [RED, RED, ORANGE, ORANGE, GREEN, GREEN, YELLOW, YELLOW]

# State Constants
STATE_BALL_IN_PADDLE = 0
STATE_PLAYING = 1
STATE_WON = 2
STATE_GAME_OVER = 3


class Brick:
    """ Class for brick objects. """

    def __init__(self, x_ofs, y_ofs, color):
        self.brick = pygame.Rect(x_ofs, y_ofs, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = color

        if color == RED:
            self.score = 7
        elif color == ORANGE:
            self.score = 5
        elif color == GREEN:
            self.score = 3
        else:
            self.score = 1

    def draw(self, screen):
        """ Draw the brick onto the given screen. """
        pygame.draw.rect(screen, self.color, self.brick)


class Breakout:
    """ Class for Breakout game. """

    def __init__(self):
        pygame.init()

        # Set pygame window and title
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.font = pygame.font.Font(None, 30)
        pygame.display.set_caption("Breakout")

        # Create clock (to lock framerate at a constant value later)
        self.clock = pygame.time.Clock()

        # Create the game objects and containers
        self.lives = None
        self.score = None
        self.hits = None
        self.state = None

        self.bricks = None
        self.paddle = None
        self.ball = None
        self.ball_vel = None
        self.ball_speed = None

        self.init_game()

    def init_game(self):
        """ Initialize the game state. """

        # Set constants
        self.lives = 3
        self.score = 0
        self.hits = 0
        self.state = STATE_BALL_IN_PADDLE

        # Create objects
        self.bricks = []
        self.paddle = pygame.Rect(300, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ball = pygame.Rect(300, PADDLE_Y - BALL_DIAMETER,
                                BALL_DIAMETER, BALL_DIAMETER)

        # Set ball to move using a random choice of direction (except down)
        self.ball_speed = 5
        delta_x = random.uniform(-1, 1) * self.ball_speed  # TODO: Seed option
        delta_y = -1 * self.ball_speed
        self.ball_vel = [delta_x, delta_y]

        self.create_bricks()

    def create_bricks(self):
        """ Create all bricks. """

        # Set brick position and create append to bricks list
        y_ofs = 85
        x_ofs = 5

        # Create bricks (from top left to bottom right)
        for i in range(BRICK_LINES):
            brick_line = []
            for _ in range(BRICK_PER_LINE):
                brick = Brick(x_ofs, y_ofs, BRICK_COLORS[i])
                brick_line.append(brick)
                x_ofs += BRICK_WIDTH + 10
            self.bricks.append(brick_line)
            x_ofs = 5
            y_ofs += BRICK_HEIGHT + 5

    def start_game(self):
        """ Start the game by launching the ball. """
        self.state = STATE_PLAYING

    def do_command(self, command):
        """ Perform the command. """

        # Check for left arrow key and update position
        if command == 'left':
            self.paddle.left -= PADDLE_SPEED
            if self.paddle.left < 0:
                self.paddle.left = 0

        # Check for right arrow key and update position
        if command == 'right':
            self.paddle.right += PADDLE_SPEED
            if self.paddle.left > MAX_PADDLE_X:
                self.paddle.left = MAX_PADDLE_X

        # Start the game by pressing SPACE if game is in init state
        if command == 'space' and self.state == STATE_BALL_IN_PADDLE:
            self.start_game()
        # Restart the game by pressing RETURN if game is in game over state
        elif command == 'return' and (self.state == STATE_GAME_OVER or
                                      self.state == STATE_WON):
            self.init_game()

    def check_input(self):
        """ Check for game inputs via keyboard. """

        # Get the key that is pressed
        keys = pygame.key.get_pressed()

        # Check for left arrow key
        if keys[pygame.K_LEFT]:
            self.do_command('left')

        # Check for right arrow key
        if keys[pygame.K_RIGHT]:
            self.do_command('right')

        # Start the game by pressing SPACE if game is in init state
        if keys[pygame.K_SPACE] and self.state == STATE_BALL_IN_PADDLE:
            self.do_command('space')
        # Restart the game by pressing RETURN if game is in game over state
        elif keys[pygame.K_RETURN] and (self.state == STATE_GAME_OVER or
                                        self.state == STATE_WON):
            self.do_command('return')

    def update_ball_velocity(self, ball_vel):
        """ Update the ball  velocity. """
        if self.hits == 2:
            self.ball_speed = 10
            return -ball_vel * 2
        elif self.hits == 6:
            self.ball_speed = 15
            return int(-ball_vel * 1.5)
        return -ball_vel

    def move_ball(self):
        """ Move the ball object. """

        # Update ball position
        self.ball.left += self.ball_vel[0]
        self.ball.top += self.ball_vel[1]

        # Check and update ball position and velocity at walls
        if self.ball.left < 0:
            self.ball.left = 0
            self.ball_vel[0] = -self.ball_vel[0]
        elif self.ball.left >= MAX_BALL_X:
            self.ball.left = MAX_BALL_X
            self.ball_vel[0] = -self.ball_vel[0]

        # Check and update ball position and velocity at roof
        if self.ball.top < 0:
            self.ball.top = 0
            self.ball_vel[1] = -self.ball_vel[1]

    def handle_collision(self):
        """ Handle ball collision event. """

        # Check for collision with brick
        for i, brick_line in enumerate(self.bricks):
            for _, brick in enumerate(brick_line):
                if self.ball.colliderect(brick.brick):
                    self.score += brick.score
                    self.ball_vel[1] = -self.ball_vel[1]
                    self.bricks[i].remove(brick)
                    break

        # Check for won game
        if len(self.bricks) == 0:
            self.state = STATE_WON

        # Check for collision with paddle
        if self.ball.colliderect(self.paddle):
            self.ball.top = PADDLE_Y - BALL_DIAMETER
            self.hits += 1
            self.ball_vel[1] = self.update_ball_velocity(self.ball_vel[1])

        # Check for ball going below paddle y position
        elif self.ball.top > self.paddle.top:
            self.lives -= 1
            if self.lives > 0:
                self.state = STATE_BALL_IN_PADDLE
            else:
                self.state = STATE_GAME_OVER

    def show_stats(self):
        """ Display game state information. """

        if self.font:
            info = f"SCORE: {self.score}   LIVES: {self.lives}"
            font_surface = self.font.render(info, False, WHITE)
            self.screen.blit(font_surface, (STATS_X, STATS_Y))

    def show_message(self, message):
        """ Display game state messages. """

        if self.font:
            size = self.font.size(message)
            font_surface = self.font.render(message, False, WHITE)
            x_val = (SCREEN_SIZE[0] - size[0]) / 2
            y_val = (SCREEN_SIZE[1] - size[1]) / 2
            self.screen.blit(font_surface, (x_val, y_val))

    def run(self):
        """ Run Breakout. """

        input_type = 'manual'

        # Start the game loop
        running = True
        while running:
            # Set the framerate
            self.clock.tick(FPS)

            # Check for quit game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill(BLACK)

            # Check for automatic or manual input
            if input_type == 'manual':
                self.check_input()
            elif input_type == 'auto':
                pass
                # self.get_command()

            # Check current game state
            if self.state == STATE_PLAYING:
                self.move_ball()
                self.handle_collision()
            elif self.state == STATE_BALL_IN_PADDLE:
                self.ball.left = self.paddle.left + self.paddle.width / 2
                self.ball.top = self.paddle.top - self.ball.height
                self.show_message("PRESS SPACE TO LAUNCH THE BALL")
            elif self.state == STATE_GAME_OVER:
                self.show_message("GAME OVER. PRESS ENTER TO PLAY AGAIN")
            elif self.state == STATE_WON:
                self.show_message("YOU WON! PRESS ENTER TO PLAY AGAIN")

            # Draw paddle
            pygame.draw.rect(self.screen, CYAN, self.paddle)

            # Draw ball
            pygame.draw.circle(self.screen, WHITE, (
                self.ball.left + BALL_RADIUS,
                self.ball.top + BALL_RADIUS), BALL_RADIUS)

            # Draw all bricks
            for _, brick_line in enumerate(self.bricks):
                for _, brick in enumerate(brick_line):
                    brick.draw(self.screen)

            self.show_stats()
            pygame.display.flip()


def main():
    """ Init and run pygame. """
    Breakout().run()

if __name__ == "__main__":
    main()
