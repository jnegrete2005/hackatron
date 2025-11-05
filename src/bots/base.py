from src.backend.GameState import GameState
from src.backend.player import Player


class BaseBot:
    """
    Base class for the bots that will play the Tron game.

    Your bot **must** inherit from this class and implement the `get_move` method.
    """

    def __init__(self, player: Player | None = None, game_state: GameState | None = None):
        pass

    def get_move(self, game_state: GameState) -> int:
        """
        This method should be implemented by subclasses to return the next move.

        :param game_state: The current state of the game.
        :type game_state: GameState

        :raise NotImplementedError: If the method is not implemented by a subclass.

        :return: The next move to be made.
        :rtype: int
        """
        raise NotImplementedError("Subclasses must implement this method.")
