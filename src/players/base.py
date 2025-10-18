from src.GameState import GameState


class BaseBot:
    def __init__(self):
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
