"""
Breackout player classes. There are three types:
    Manual: manual player controlled via the keyboard.
    Naive_AI: explicit AI that follows the ball's horizontal position.
    QL_AI: AI trained via Q-Learning algorithms
"""
import pygame
import breakout as bo


class Player():
    """ General player class. """
    def __init__(self):
        pass

class ManualPlayer(Player):
    """ Manual player class. """
    def get_command(self, game):
        """ Check for game inputs via keyboard when in manual mode. """
        # Get the key that is pressed
        keys = pygame.key.get_pressed()

        # Check for arrow key
        if keys[pygame.K_LEFT]:
            return 'left'
        if keys[pygame.K_RIGHT]:
            return 'right'

        # Start the game by pressing SPACE if game is in init state
        if keys[pygame.K_SPACE] and game.state == bo.STATE_BALL_IN_PADDLE:
            return 'space'
        # Restart the game by pressing RETURN if game is in game over state
        if keys[pygame.K_RETURN] and (game.state == bo.STATE_GAME_OVER or
                                        game.state == bo.STATE_WON):
            return 'return'


class NaiveAI(Player):
    """ Naive AI player class. """
    def get_command(self, game):
        """ The naive AI follows the ball's horizontal position. """
        ball_pos, paddle_pos = game.ball.center, game.paddle.center

        if game.state == 0:
            return 'space'
        if game.state == 1 and ball_pos > paddle_pos:
            return 'right'
        if game.state == 1 and ball_pos < paddle_pos:
            return 'left'
        return 'return'


class QLAI(Player):
    """ AI player class for use with QL algorithms. """
    action_space_size = 2
    observation_space_size = 101

    def reset(self, game):
        game.init_game(lives=1, state=bo.STATE_PLAYING)
        self.run(game)

    def run(self, game):
        """ . """
        for _ in range(1000):
            game.run()

    def get_command(self, game):
        return 'left'

    def step(self, game):
        """ Recieve command from QL-Learning Model. """
        state = game.get_state()
        # command = self.get_command(state)
        # game.do_command(command)


CLASS = {'manual': ManualPlayer, 'naive': NaiveAI, 'ql': QLAI}


"""
env.reset(): state -> game.init_game()
env.step(action): 

action_size: env.action_space_size # Number of actions
state_size: env.observation_space_size # Length of states
"""