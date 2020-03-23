""" Player classes for Breakout. """
import pygame
import breakout as bo

class Player:
    """
    Breackout player class. There are three types:
        Manual: manual player controlled via the keyboard.
        Naive_AI: explicit AI that follows the ball's horizontal position.
        QL_AI: AI trained via Q-Learning algorithms
    """
    def __init__(self, player_type):
        self.player_type = player_type
        self.input_methods = {'manual': ManualPlayer.input,
                              'naive': NaiveAI.input,
                              'ql': QLAI.input}

    def get_command(self, game):
        """ Call the appropriate command input method. """
        method = self.input_methods[self.player_type]
        method(self, game)


class ManualPlayer(Player):
    """ Manual player class. """
    def input(self, game):
        """ Check for game inputs via keyboard when in manual mode. """
        # Get the key that is pressed
        keys = pygame.key.get_pressed()

        # Check for arrow key
        if keys[pygame.K_LEFT]:
            game.do_command('left')
        if keys[pygame.K_RIGHT]:
            game.do_command('right')

        # Start the game by pressing SPACE if game is in init state
        if keys[pygame.K_SPACE] and game.state == bo.STATE_BALL_IN_PADDLE:
            game.do_command('space')
        # Restart the game by pressing RETURN if game is in game over state
        elif keys[pygame.K_RETURN] and (game.state == bo.STATE_GAME_OVER or
                                        game.state == bo.STATE_WON):
            game.do_command('return')


class NaiveAI(Player):
    """ Naive AI player class. """
    def input(self, game):
        """ The naive AI follows the ball's horizontal position. """
        ball_pos, paddle_pos = game.ball.center, game.paddle.center

        if game.state == 0:
            game.do_command('space')
        elif game.state == 1 and ball_pos > paddle_pos:
            game.do_command('right')
        elif game.state == 1 and ball_pos < paddle_pos:
            game.do_command('left')
        else:
            game.do_command('return')


class QLAI(Player):
    """ AI player class for use with QL algorithms. """
    def input(self, game):
        """ Recieve command from QL-Learning Model. """
        state = game.get_state()
        # command = self.get_command(state)
        # game.do_command(command)