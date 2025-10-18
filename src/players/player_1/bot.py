from base import BaseBot, GameState
from src.base.player import Player

from random import choice


class Bot(BaseBot):
    def __init__(self, player: Player):
        super().__init__()
        self.player = player
        self.moves = [1, 2, 3, 4]

    def get_move(self, game_state: GameState) -> int:
        """
        Returns a random move for the player.

        :param game_state: The current state of the game.
        :type game_state: GameState

        :return: A random move (1, 2, 3, or 4).
        :rtype: int
        """
        return choice(self.moves)
