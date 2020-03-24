""" Breakout (inspired by Atari Breakout) """
import sys
import random
import pygame
import player

# Screen Constants
SCREEN_SIZE = 480, 640
STATS_X, STATS_Y = 100, 10
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
PADDLE_WIDTH, PADDLE_HEIGHT = 75, 8
MAX_PADDLE_X = SCREEN_SIZE[0] - PADDLE_WIDTH
PADDLE_Y = SCREEN_SIZE[1] - PADDLE_HEIGHT - 10
PADDLE_SPEED = 30

# Brick Constants
BRICK_WIDTH, BRICK_HEIGHT = 30, 6
BRICK_LINES, BRICK_PER_LINE = 8, 12
BRICK_COLORS = [RED, RED, ORANGE, ORANGE, GREEN, GREEN, YELLOW, YELLOW]

# Mode Constants
MODE_BALL_IN_PADDLE = 0
MODE_PLAYING = 1
MODE_WON = 2
MODE_GAME_OVER = 3


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
        self.game_num = 1
        self.player_type = player_type
        self.player = player.Player().type[player_type]()

        # Set pygame clock, window, title, and font
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.font = pygame.font.Font(None, 30)
        pygame.display.set_caption("Breakout")

        # Create the game objects and containers
        self.lives, self.score, self.hits, self.mode = None, None, None, None
        self.bricks, self.bricks_bool, self.num_bricks = None, None, None
        self.ball, self.ball_vel, self.paddle = None, None, None

        self.init_game(seed)

    def init_game(self, seed=None, lives=3, mode=MODE_BALL_IN_PADDLE):
        """ Initialize the game mode. """
        # Set constants
        self.lives, self.score, self.hits = lives, 0, 0
        self.mode = mode

        # Create objects
        self.bricks = []
        self.bricks_bool = []
        self.num_bricks = 0
        self.create_bricks()
        self.paddle = pygame.Rect(300, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ball = pygame.Rect(300, PADDLE_Y - BALL_DIAMETER,
                                BALL_DIAMETER, BALL_DIAMETER)

        # Set ball to move using a random choice of direction (upwards)
        if seed:
            random.seed(seed)
        self.ball_vel = [random.uniform(-8, 8), -12]

    def create_bricks(self):
        """ Create all bricks. """
        # Set brick position and create append to bricks list
        x_pos, y_pos = 5, 85

        # Create bricks (from top left to bottom right)
        for i in range(BRICK_LINES):
            brick_line = []
            bricks_bool_line = []
            for _ in range(BRICK_PER_LINE):
                brick_line.append(Brick(x_pos, y_pos, BRICK_COLORS[i]))
                bricks_bool_line.append(1)
                self.num_bricks += 1
                x_pos += BRICK_WIDTH + 10
            self.bricks.append(brick_line)
            self.bricks_bool.append(bricks_bool_line)
            x_pos = 5
            y_pos += BRICK_HEIGHT + 5

    def start_game(self):
        """ Start the game by launching the ball. """
        self.mode = MODE_PLAYING

    def do_action(self, action):
        """ Perform the action. """
        # Check for left arrow key and update position
        if action == 'left':
            self.paddle.left -= PADDLE_SPEED
            if self.paddle.left < 0:
                self.paddle.left = 0

        # Check for right arrow key and update position
        if action == 'right':
            self.paddle.right += PADDLE_SPEED
            if self.paddle.left > MAX_PADDLE_X:
                self.paddle.left = MAX_PADDLE_X

        # Start the game by pressing SPACE if game is in init mode
        if action == 'space' and self.mode == MODE_BALL_IN_PADDLE:
            self.start_game()
        # Restart the game by pressing RETURN if game is in game over mode
        elif action == 'return' and (self.mode == MODE_GAME_OVER or
                                     self.mode == MODE_WON):
            self.game_num += 1
            self.init_game()

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

    def update_ball_velocity(self, ball_vel):
        """ Update the ball velocity. """
        boost = 4 if self.hits in (2, 4) else 0
        return -(ball_vel + boost)

    def nudge_ball(self):
        """ Nudge ball if it collides on a paddle edge. """
        ball_center, paddle_center = self.ball.center[0], self.paddle.center[0]
        paddle_left, paddle_right = self.paddle.left, self.paddle.right
        h_vel = self.ball_vel[0]

        if paddle_left <= ball_center < (paddle_center - 15):
            self.ball_vel[0] = -abs(h_vel*1.4) if h_vel != 0 else -1
        elif paddle_right >= ball_center > (paddle_center + 15):
            self.ball_vel[0] = abs(h_vel*1.4) if h_vel != 0 else 1

    def handle_collision(self):
        """ Handle ball collision events. """
        # Check for collision with brick
        for i, brick_line in enumerate(self.bricks):
            for j, brick in enumerate(brick_line):
                if self.ball.colliderect(brick.brick):
                    self.score += brick.score
                    self.num_bricks -= 1
                    self.ball_vel[1] = -self.ball_vel[1]
                    self.bricks[i].remove(brick)
                    self.bricks_bool[i][j] = 0
                    break

        # Check for won game
        if self.num_bricks == 0:
            self.mode = MODE_WON

        # Check for collision with paddle
        if self.ball.colliderect(self.paddle):
            self.hits += 1
            self.ball.top = PADDLE_Y - BALL_DIAMETER
            self.ball_vel[1] = self.update_ball_velocity(self.ball_vel[1])
            self.nudge_ball()

        # Check for ball going below paddle y position
        elif self.ball.top > self.paddle.top:
            print('ball below paddle: -1 live')
            self.lives -= 1
            if self.lives > 0:
                self.mode = MODE_BALL_IN_PADDLE
            else:
                self.mode = MODE_GAME_OVER

    def handle_current_mode(self):
        """ Get and handle action based on current game mode. """
        if self.mode == MODE_PLAYING:
            self.move_ball()
            self.handle_collision()
        elif self.mode == MODE_BALL_IN_PADDLE:
            self.ball.left = self.paddle.left + self.paddle.width / 2
            self.ball.top = self.paddle.top - self.ball.height
            self.show_message("PRESS SPACE TO LAUNCH THE BALL")
        elif self.mode == MODE_GAME_OVER:
            self.show_message("GAME OVER. PRESS ENTER TO PLAY AGAIN")
        elif self.mode == MODE_WON:
            self.show_message("YOU WON! PRESS ENTER TO PLAY AGAIN")

    def reward(self):
        """ If game over, -1 for each remaining brick. Else, score. """
        if self.mode == MODE_GAME_OVER:
            return -len(self.bricks)
        return self.score

    def show_stats(self):
        """ Display game information. """
        if self.font:
            s = f"SCORE: {self.score} LIVES: {self.lives} GAME: {self.game_num}"
            font_surface = self.font.render(s, False, WHITE)
            self.screen.blit(font_surface, (STATS_X, STATS_Y))

    def show_message(self, message):
        """ Display game messages. """
        if self.font:
            size = self.font.size(message)
            font_surface = self.font.render(message, False, WHITE)
            x_val = (SCREEN_SIZE[0] - size[0]) / 2
            y_val = (SCREEN_SIZE[1] - size[1]) / 2
            self.screen.blit(font_surface, (x_val, y_val))

    def get_state(self):
        """ Outputs game state info. """
        brick_list = [item for sublist in self.bricks_bool for item in sublist]
        return [self.ball.center[0], self.ball.center[1],
                self.ball_vel[0], self.ball_vel[1],
                self.paddle.center[0]] + brick_list

    def run(self):
        """ Run Breakout. """
        # Check for quit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.clock.tick(FPS)
        self.screen.fill(BLACK)
        action = self.player.get_action(self)
        self.do_action(action)
        self.handle_current_mode()

        pygame.draw.rect(self.screen, CYAN, self.paddle)
        pygame.draw.circle(self.screen, WHITE, (
            self.ball.left + BALL_RADIUS,
            self.ball.top + BALL_RADIUS), BALL_RADIUS)
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
    game = Breakout(player_type, seed)

    # Start the game loop
    if player_type in ['manual', 'naive']:
        while True:
            game.run()

if __name__ == "__main__":
    main()
