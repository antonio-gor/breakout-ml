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
BALL_DIAMETER = 15
BALL_RADIUS = int(BALL_DIAMETER / 2)
MAX_BALL_X = SCREEN_SIZE[0] - BALL_DIAMETER
MAX_BALL_Y = SCREEN_SIZE[1] - BALL_DIAMETER

# Paddle Constant
PADDLE_WIDTH, PADDLE_HEIGHT = 40, 8
MAX_PADDLE_X = SCREEN_SIZE[0] - PADDLE_WIDTH
PADDLE_Y = SCREEN_SIZE[1] - PADDLE_HEIGHT - 10
PADDLE_SPEED = 5

# Brick Constants
BRICK_WIDTH, BRICK_HEIGHT = 30, 6
BRICK_LINES, BRICK_PER_LINE = 8, 12
BRICK_COLORS = [RED, RED, ORANGE, ORANGE, GREEN, GREEN, YELLOW, YELLOW]

# State Constants
STATE_BALL_IN_PADDLE = 0
STATE_PLAYING = 1
STATE_WON = 2
STATE_GAME_OVER = 3


class Player:
    """
    Breackout player class. There are three types:
        Manual: manual player controlled via the keyboard.
        Naive_AI: explicit AI that follows the ball's horizontal position.
        QL_AI: AI trained via Q-Learning algorithms
    """

    def __init__(self, player_type):
        self.player_type = player_type
        self.input_methods = {'manual': self.manual_input,
                              'naive': self.naive_input,
                              'ql': self.ql_input}

    def get_command(self, game):
        """ Call the appropriate command input method. """
        method = self.input_methods[self.player_type]
        method(game)

    def manual_input(self, game):
        """ Check for game inputs via keyboard when in manual mode. """

        # Get the key that is pressed
        keys = pygame.key.get_pressed()

        # Check for arrow key
        if keys[pygame.K_LEFT]:
            game.do_command('left')
        if keys[pygame.K_RIGHT]:
            game.do_command('right')

        # Start the game by pressing SPACE if game is in init state
        if keys[pygame.K_SPACE] and game.state == STATE_BALL_IN_PADDLE:
            game.do_command('space')
        # Restart the game by pressing RETURN if game is in game over state
        elif keys[pygame.K_RETURN] and (game.state == STATE_GAME_OVER or
                                        game.state == STATE_WON):
            game.do_command('return')

    def naive_input(self, game):
        """ The naive AI follows the ball's horizontal position. """

        if game.state == 0:
            game.do_command('space')
        elif game.state == 1:
            ball_pos, paddle_pos = game.ball.center, game.paddle.center

            if ball_pos > paddle_pos:
                game.do_command('right')
            else:
                game.do_command('left')
        else:
            game.do_command('return')

    def ql_input(self, game):
        """ . """


class Brick:
    """ Class for brick objects. """

    def __init__(self, x_pos, y_pos, color):
        self.scores = {YELLOW: 1, GREEN: 3, ORANGE: 5, RED: 7}
        self.brick = pygame.Rect(x_pos, y_pos, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = color
        self.score = self.scores[color]

    def draw(self, screen):
        """ Draw the brick onto the given screen. """
        pygame.draw.rect(screen, self.color, self.brick)


class Breakout:
    """ Class for Breakout game. """

    def __init__(self, player_type='manual', seed=None):
        pygame.init()
        self.player = Player(player_type)

        # Set pygame clock, window, title, and font
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.font = pygame.font.Font(None, 30)
        pygame.display.set_caption("Breakout")

        # Create the game objects and containers
        self.lives, self.score, self.hits, self.state = None, None, None, None
        self.bricks, self.num_bricks, self.paddle = None, None, None
        self.ball, self.ball_vel, self.ball_speed = None, None, None

        self.init_game(seed)

    def init_game(self, seed=None):
        """ Initialize the game state. """

        # Set constants
        self.lives, self.score, self.hits = 3, 0, 0
        self.state = STATE_BALL_IN_PADDLE

        # Create objects
        self.bricks = []
        self.num_bricks = 0
        self.create_bricks()
        self.paddle = pygame.Rect(300, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ball = pygame.Rect(300, PADDLE_Y - BALL_DIAMETER,
                                BALL_DIAMETER, BALL_DIAMETER)

        # Set ball to move using a random choice of direction (upwards)
        if seed:
            random.seed(seed)
        self.ball_vel = [random.uniform(-5, 5), -5]

    def create_bricks(self):
        """ Create all bricks. """

        # Set brick position and create append to bricks list
        x_pos, y_pos = 5, 85

        # Create bricks (from top left to bottom right)
        for i in range(BRICK_LINES):
            brick_line = []
            for _ in range(BRICK_PER_LINE):
                brick_line.append(Brick(x_pos, y_pos, BRICK_COLORS[i]))
                self.num_bricks += 1
                x_pos += BRICK_WIDTH + 10
            self.bricks.append(brick_line)
            x_pos = 5
            y_pos += BRICK_HEIGHT + 5

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

    def update_ball_velocity(self, ball_vel):
        """ Update the ball  velocity. """

        if self.hits == 2:
            return -ball_vel * 2
        elif self.hits == 6:
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
        """ Handle ball collision events. """

        # Check for collision with brick
        for i, brick_line in enumerate(self.bricks):
            for _, brick in enumerate(brick_line):
                if self.ball.colliderect(brick.brick):
                    self.score += brick.score
                    self.num_bricks -= 1
                    self.ball_vel[1] = -self.ball_vel[1]
                    self.bricks[i].remove(brick)
                    break

        # Check for won game
        if self.num_bricks == 0:
            self.state = STATE_WON

        # Check for collision with paddle
        if self.ball.colliderect(self.paddle):
            self.hits += 1
            self.ball.top = PADDLE_Y - BALL_DIAMETER
            if (self.ball.center[0] >= self.paddle.left
                    and self.ball.center[0] < self.paddle.center[0] - 10):
                self.ball_vel[0] = self.update_ball_velocity(self.ball_vel[0]+2)
            elif (self.ball.center[0] <= self.paddle.right
                  and self.ball.center[0] > self.paddle.center[0] + 10):
                self.ball_vel[0] = self.update_ball_velocity(self.ball_vel[0]-2)
            self.ball_vel[1] = self.update_ball_velocity(self.ball_vel[1])

        # Check for ball going below paddle y position
        elif self.ball.top > self.paddle.top:
            self.lives -= 1
            if self.lives > 0:
                self.state = STATE_BALL_IN_PADDLE
            else:
                self.state = STATE_GAME_OVER

    def handle_current_state(self):
        """ Get and handle action based on current game state. """

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

        # Start the game loop
        running = True
        while running:

            # Check for quit game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Set the framerate and screen
            self.clock.tick(FPS)
            self.screen.fill(BLACK)

            # Get command from player
            self.player.get_command(self)

            # Check current game state
            self.handle_current_state()

            # Draw paddle and ball
            pygame.draw.rect(self.screen, CYAN, self.paddle)
            pygame.draw.circle(self.screen, WHITE, (
                self.ball.left + BALL_RADIUS,
                self.ball.top + BALL_RADIUS), BALL_RADIUS)

            # Draw all bricks
            for _, brick_line in enumerate(self.bricks):
                for _, brick in enumerate(brick_line):
                    brick.draw(self.screen)

            self.show_stats()
            pygame.display.flip()


def get_args():
    """ Get the arguements. """
    args = sys.argv
    player_type, seed = 'manual', None  # Default values
    if len(args) > 1:
        player_type = args[1]
    if len(args) > 2:
        seed = args[2]
    return player_type, seed

def main():
    """ Init and run pygame. """
    player_type, seed = get_args()
    Breakout(player_type, seed).run()

if __name__ == "__main__":
    main()
