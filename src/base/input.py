from src.GameState import GameState
from src.base.player import Player
from src.players.player_1.bot import Bot as PlayerOneBot


async def get_input(player: Player, game: GameState) -> int:
    """
    Get the input from the player
    """
    if player.number == 1:
        return PlayerOneBot(player).get_move(game)
    # Will implement later for player 2
    # else:
    #     return PlayerTwoBot(player).get_move(game)
    raise NotImplementedError("Bot for player 2 is not implemented yet.")
