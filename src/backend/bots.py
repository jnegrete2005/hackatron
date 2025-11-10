import asyncio
import argparse


def get_bot_args():
    parser = argparse.ArgumentParser(description="Run the game with specified bot Docker images.")
    parser.add_argument(
        "--bot1",
        type=str,
        default="random-bot:latest",
        help="Docker image for Bot 1"
    )
    parser.add_argument(
        "--bot2",
        type=str,
        default="random-bot:latest",
        help="Docker image for Bot 2"
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Run the game in automatic mode without waiting for keypresses"
    )
    args = parser.parse_args()
    return args.bot1, args.bot2, args.auto


async def launch_bots(bot_1_image: str, bot_2_image: str) -> tuple[asyncio.subprocess.Process | None, asyncio.subprocess.Process | None]:
    """
    Launch the bot Docker containers and return their subprocess handles.

    :param bot_1_image: The Docker image for bot 1.
    :type bot_1_image: str
    :param bot_2_image: The Docker image for bot 2.
    :type bot_2_image: str

    :return: A tuple containing the subprocess handles for bot 1 and bot 2.
    :rtype: tuple[asyncio.subprocess.Process | None, asyncio.subprocess.Process | None]

    """

    DOCKER_BASE_COMMAND = [
        "docker", "run",
        "-i",
        "--rm",
        "--network", "none",
        "--memory", "512m",
        "--cpus", "1",
    ]

    try:
        bot_1 = await asyncio.create_subprocess_exec(
            *DOCKER_BASE_COMMAND + [bot_1_image],
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        bot_2 = await asyncio.create_subprocess_exec(
            *DOCKER_BASE_COMMAND + [bot_2_image],
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        return bot_1, bot_2

    except Exception as e:
        print(f"Error launching bots: {e}")
        return None, None


async def terminate_bots(
    bot_1: asyncio.subprocess.Process | None,
    bot_2: asyncio.subprocess.Process | None
) -> None:
    """
    Terminate the bot Docker containers.

    :param bot_1: The subprocess handle for bot 1.
    :type bot_1: asyncio.subprocess.Process | None
    :param bot_2: The subprocess handle for bot 2.
    :type bot_2: asyncio.subprocess.Process | None
    """

    print("Terminating bots...")

    try:
        if bot_1:
            _, p1_errors = await bot_1.communicate(None)
            if p1_errors:
                print("--- Errores del Bot 1 ---")
                print(p1_errors.decode('utf-8'))
                print("-------------------------")

        if bot_2:
            _, p2_errors = await bot_2.communicate(None)
            if p2_errors:
                print("--- Errores del Bot 2 ---")
                print(p2_errors.decode('utf-8'))
                print("-------------------------")
    except ProcessLookupError:
        # Esto puede pasar si el proceso NUNCA se inició
        print("ProcessLookupError al leer errores, los bots probablemente nunca se lanzaron.")
    except Exception as e:
        print(f"Error leyendo stderr de los bots: {e}")

    # Ahora podemos terminarlos (aunque 'communicate' ya espera a que terminen)
    if bot_1 and bot_1.returncode is None:  # Solo termina si sigue vivo
        bot_1.terminate()
    if bot_2 and bot_2.returncode is None:  # Solo termina si sigue vivo
        bot_2.terminate()

    print("Limpieza completa.")
