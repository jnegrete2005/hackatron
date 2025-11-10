import asyncio
import json
import pygame

from src.backend.bots import launch_bots, get_bot_args, terminate_bots
from src.backend.consts import PLAYER_1, PLAYER_2
from src.backend.GameState import GameState
from src.backend.input import get_input
from src.backend.player import Player

from src.frontend.Frontend import Frontend


async def get_moves(
    game: GameState,
    bot_1: asyncio.subprocess.Process,
    bot_2: asyncio.subprocess.Process
) -> tuple[tuple[int, int], tuple[int, int]]:
    """
    Get moves from both players concurrently.

    :param game: The current game state.
    :type game: GameState
    :param bot_1: The subprocess handle for bot 1.
    :type bot_1: asyncio.subprocess.Process
    :param bot_2: The subprocess handle for bot 2.
    :type bot_2: asyncio.subprocess.Process

    :return: A tuple containing the moves of player 1 and player 2.
    :rtype: tuple[tuple[int, int], tuple[int, int]]
    """
    player_1, player_2 = game.player_1, game.player_2

    state_for_p1 = game.serialize_for_player(PLAYER_1)
    state_for_p2 = game.serialize_for_player(PLAYER_2)

    move_1, move_2 = await asyncio.gather(
        get_input(json.dumps(state_for_p1), bot_1),
        get_input(json.dumps(state_for_p2), bot_2)
    )

    if not Player.is_valid_move(move_1) or player_1.player_suicided(move_1):
        move_1 = player_1.previous_move
    if not Player.is_valid_move(move_2) or player_2.player_suicided(move_2):
        move_2 = player_2.previous_move

    return move_1, move_2


async def play(game: GameState, frontend: Frontend, bot_1: asyncio.subprocess.Process, bot_2: asyncio.subprocess.Process, auto_mode: bool) -> None:
    """
    Play the game until it's over.

    :param game: The current game state.
    :type game: GameState
    :param frontend: The frontend to draw the game board.
    :type frontend: Frontend
    :param bot_1: The subprocess handle for bot 1.
    :type bot_1: asyncio.subprocess.Process
    :param bot_2: The subprocess handle for bot 2.
    :type bot_2: asyncio.subprocess.Process
    """
    while not game.game_over:
        move_1, move_2 = await get_moves(game, bot_1, bot_2)
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
    bot_1_image, bot_2_image, auto_mode = get_bot_args()
    bot_1, bot_2 = await launch_bots(bot_1_image, bot_2_image)

    if bot_1 is None or bot_2 is None:
        print("Failed to launch bots. Exiting.")
        await terminate_bots(bot_1, bot_2)
        return

    game = GameState(16)
    frontend = Frontend(game, 30)
    frontend.draw_game_board()

    try:
        await play(game, frontend, bot_1, bot_2, auto_mode)
    except Exception as e:
        print(f"Error occurred while playing: {e}")
    finally:
        await terminate_bots(bot_1, bot_2)

if __name__ == "__main__":
    asyncio.run(main())
