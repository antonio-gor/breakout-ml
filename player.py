"""
Breackout player classes. There are three types:
    Manual: manual player controlled via the keyboard.
    Naive_AI: explicit AI that follows the ball's horizontal position.
    QL_AI: AI trained via Q-Learning algorithms
"""
import pygame
import breakout as bo


class ManualPlayer():
    """ Manual player class. """
    def get_command(self, game):
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


class NaiveAI():
    """ Naive AI player class. """
    def get_command(self, game):
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


class QLAI():
    """ AI player class for use with QL algorithms. """
    def get_command(self, game):
        """ Recieve command from QL-Learning Model. """
        state = game.get_state()
        print(state)
        # command = self.get_command(state)
        # game.do_command(command)

    def run(self, game):
        """ . """
        game.run()


CLASS = {'manual': ManualPlayer(), 'naive': NaiveAI(), 'ql': QLAI()}
INPUT = {'manual': ManualPlayer.get_command,
         'naive': NaiveAI.get_command,
         'ql': QLAI.get_command}

def get_command(game, player, player_type):
    """ Get command from appropriate command method."""
    return INPUT[player_type](player, game)
