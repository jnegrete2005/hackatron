import asyncio

from src.backend.players.player_input import IPlayerType


class HumanPlayer(IPlayerType):
    """
    An IPlayerInput implementation that gets moves from a human
    via the command line.
    """

    async def initialize(self):
        """
        Initialize the human player.
        Always returns True as no special initialization is needed.
        """
        return True

    async def get_move(self, game_state_json: str) -> int:
        # Use asyncio.to_thread to run the blocking input() in a separate thread
        return await asyncio.to_thread(self._get_blocking_human_input)

    def _get_blocking_human_input(self) -> int:
        """This is the original __get_human_input logic."""
        input_str = \
            """
Left: 1
Up: 2
Right: 3
Down: 4
Enter your move: 
"""
        while True:
            try:
                user_input = input(input_str)
                move = int(user_input)
                if 1 <= move <= 4:
                    return move
                else:
                    print("Invalid move. Please enter a number between 1 and 4.")
            except ValueError:
                print("Invalid input. Please enter a valid integer between 1 and 4.")

    async def cleanup(self) -> None:
        # No cleanup needed for a human player
        pass
