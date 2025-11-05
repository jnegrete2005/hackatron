from src.backend.GameState import GameState
from src.backend.player import Player

from src.bots.player_1.bot import Bot as PlayerOneBot
from src.bots.player_2.bot import Bot as PlayerTwoBot


async def get_input(player: Player, game: GameState) -> int:
    """
    Get the input from the player
    """
    if player.number == 1:
        return PlayerOneBot(player).get_move(game)
    else:
        return PlayerTwoBot(player).get_move(game)
