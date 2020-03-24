""" Env class for Breakout and QL player. """
import copy
import breakout as bo

class Gym:
    """ AI training environment for Breakout. """

    def __init__(self, game=bo.Breakout(player_type='ql', seed=None)):
        self.action_space_size = 3  # Number of actions the agent can perform
        self.observation_space_size = 101  # Size of the game state
        self.game = game
        self.player = game.player
        self.state = game.get_state()

    def reset(self):
        """ Reset the state of the environment to its initial playing mode. """
        self.game.init_game(lives=1, mode=bo.MODE_PLAYING)
        return self.game.output_state

    def step(self, action):
        """ Execute one time-step in a copy of the environment. """
        next_state = copy.deepcopy(self.game)  # TODO: fix copy method
        next_state.do_action(action)
        reward = next_state.reward()
        done = next_state.mode == bo.MODE_GAME_OVER
        info = self.game.get_state()
        return next_state, reward, done, info

    def run(self):
        """ Run the game environment. """
        # TODO
