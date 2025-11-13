from abc import ABC, abstractmethod


class IPlayerType(ABC):
    """
    Interface for player types for handling initialization and input.
    """

    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the player type.
        Returns True if initialization is successful, False otherwise.
        """
        pass

    @abstractmethod
    async def get_move(self, game_state_json: str) -> int:
        """
        Gets the next move from the input source.

        :param game_state_json: A JSON string representing the current game state.
        :type game_state_json: str

        :return: The move as an integer.
        :rtype: int
        """
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """
        Clean up any resources used by the player type.
        """
        pass
