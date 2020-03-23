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
        self.type = {'manual': ManualPlayer, 'naive': NaiveAI, 'ql': QLAI}

class ManualPlayer(Player):
    """ Manual player class. """
    def get_command(self, game):
        """ Check for game inputs via keyboard when in manual mode. """
        # Get the key that is pressed
        keys = pygame.key.get_pressed()
        command = ''

        # Check for arrow key
        if keys[pygame.K_LEFT]:
            command = 'left'
        if keys[pygame.K_RIGHT]:
            command = 'right'

        # Start the game by pressing SPACE if game is in init state
        if keys[pygame.K_SPACE] and game.state == bo.STATE_BALL_IN_PADDLE:
            command = 'space'
        # Restart the game by pressing RETURN if game is in game over state
        if keys[pygame.K_RETURN] and (game.state == bo.STATE_GAME_OVER or
                                      game.state == bo.STATE_WON):
            command = 'return'
        return command


class NaiveAI(Player):
    """ Naive AI player class. """
    def get_command(self, game):
        """ The naive AI follows the ball's horizontal position. """
        ball_pos, paddle_pos = game.ball.center, game.paddle.center
        command = ''
        
        if game.state == 0:
            command = 'space'
        if game.state == 1 and ball_pos > paddle_pos:
            command = 'right'
        if game.state == 1 and ball_pos < paddle_pos:
            command = 'left'
        if game.state in (2, 3):
            command = 'return'
        return command


class QLAI(Player):
    """ AI player class for use with QL algorithms. """
    def get_command(self, game):
        """ . """
        command = ''
        return command
