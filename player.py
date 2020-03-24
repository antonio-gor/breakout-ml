"""
Breackout player classes. There are three types:
    Manual: manual player controlled via the keyboard.
    Naive_AI: explicit AI that follows the ball's horizontal position.
    QL_AI: AI trained via Q-Learning algorithms
"""
import pygame
import breakout as bo


class Player:
    """ General player class. """
    def __init__(self):
        self.type = {'manual': ManualPlayer, 'naive': NaiveAI, 'ql': QLAI}


class ManualPlayer(Player):
    """ Manual player class. """
    def get_action(self, game):
        """ Check for game inputs via keyboard when in manual mode. """
        # Get the key that is pressed
        keys = pygame.key.get_pressed()
        action = ''

        # Check for arrow key
        if keys[pygame.K_LEFT]:
            action = 'left'
        if keys[pygame.K_RIGHT]:
            action = 'right'

        # Start the game by pressing SPACE if game is in init mode
        if keys[pygame.K_SPACE] and game.mode == bo.MODE_BALL_IN_PADDLE:
            action = 'space'
        # Restart the game by pressing RETURN if game is in game over mode
        if keys[pygame.K_RETURN] and (game.mode == bo.MODE_GAME_OVER or
                                      game.mode == bo.MODE_WON):
            action = 'return'
        return action


class NaiveAI(Player):
    """ Naive AI player class. """
    def get_action(self, game):
        """ The naive AI follows the ball's horizontal position. """
        ball_pos, paddle_pos = game.ball.center, game.paddle.center
        action = ''

        if game.mode == 0:
            action = 'space'
        if game.mode == 1 and ball_pos > paddle_pos:
            action = 'right'
        if game.mode == 1 and ball_pos < paddle_pos:
            action = 'left'
        if game.mode in (2, 3):
            action = 'return'
        return action


class QLAI(Player):
    """ AI player class for use with QL algorithms. """
    actions = {0: '', 1: 'left', 2: 'right'}

    def get_action(self, game):
        """ . """
        action = ''
        return action
