import asyncio
import json
import pygame

from src.backend.args import get_args
from src.backend.consts import PLAYER_1, PLAYER_2
from src.backend.GameState import GameState
from src.backend.player import Player

from src.backend.players.player_input import IPlayerType
from src.backend.players.bot_player import BotPlayer
from src.backend.players.human_player import HumanPlayer

from src.frontend.Frontend import Frontend


def create_player(bot_image: str | None, is_manual: bool) -> IPlayerType:
    """
    Create a player instance based on whether it's manual or bot.

    :param bot_image: The Docker image for the bot player.
    :type bot_image: str | None
    :param is_manual: Flag indicating if the player is manual.
    :type is_manual: bool
    :return: An instance of IPlayerType (either HumanPlayer or BotPlayer).
    :rtype: IPlayerType
    """
    if is_manual:
        return HumanPlayer()

    return BotPlayer(bot_image)


async def get_moves(
    game: GameState,
    player_1_input: IPlayerType,
    player_2_input: IPlayerType
) -> tuple[tuple[int, int], tuple[int, int]]:
    """
    Get moves from both players concurrently.

    :param game: The current game state.
    :type game: GameState
    :param player_1: The player 1 instance
    :type player_1: IPlayerType
    :param player_2: The player 2 instance
    :type player_2: IPlayerType
    :return: A tuple containing the moves of player 1 and player 2.
    :rtype: tuple[tuple[int, int], tuple[int, int]]
    """
    player_1, player_2 = game.player_1, game.player_2

    state_for_p1 = json.dumps(game.serialize_for_player(PLAYER_1))
    state_for_p2 = json.dumps(game.serialize_for_player(PLAYER_2))

    move_1, move_2 = await asyncio.gather(
        player_1_input.get_move(state_for_p1),
        player_2_input.get_move(state_for_p2)
    )

    if not Player.is_valid_move(move_1) or player_1.player_suicided(move_1):
        move_1 = player_1.previous_move
    if not Player.is_valid_move(move_2) or player_2.player_suicided(move_2):
        move_2 = player_2.previous_move

    return move_1, move_2


async def play(
    game: GameState,
    frontend: Frontend,
    player_1_input: IPlayerType,
    player_2_input: IPlayerType,
    auto_mode: bool
) -> None:
    """
    Play the game until it's over.

    :param game: The current game state.
    :type game: GameState
    :param frontend: The frontend to draw the game board.
    :type frontend: Frontend
    :param player_1: The player 1 instance
    :type player_1: IPlayerType
    :param player_2: The player 2 instance
    :type player_2: IPlayerType
    :param auto_mode: Flag indicating if the game should run in automatic mode.
    :type auto_mode: bool
    :return: None
    :rtype: None
    """
    while not game.game_over:
        move_1, move_2 = await get_moves(game, player_1_input, player_2_input)
        game.tick(move_1, move_2)
        frontend.draw_game_board()
        if not auto_mode:
            await wait_for_keypress()
        else:
            await asyncio.sleep(0.1)

    print("Game Over!")
    print(f"Winner: {f'Player {game.winner.number}' if game.winner else 'Draw'}")


async def wait_for_keypress():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return

        await asyncio.sleep(0.1)


async def main():
    """
    Initialize the game and frontend, then start playing.
    """
    bot_1_image, bot_2_image, auto_mode, manual1, manual2 = get_args()

    player_1_input: IPlayerType = create_player(bot_1_image, manual1)
    player_2_input: IPlayerType = create_player(bot_2_image, manual2)

    init_results = await asyncio.gather(
        player_1_input.initialize(),
        player_2_input.initialize()
    )

    if not all(init_results):
        print("Failed to initialize players. Exiting.")
        await asyncio.gather(
            player_1_input.cleanup(),
            player_2_input.cleanup()
        )
        return

    game = GameState(16)
    frontend = Frontend(game, 30)
    frontend.draw_game_board()

    try:
        await play(game, frontend, player_1_input, player_2_input, auto_mode)
    except Exception as e:
        print(f"Error occurred while playing: {e}")
    finally:
        await asyncio.gather(
            player_1_input.cleanup(),
            player_2_input.cleanup()
        )
        pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
