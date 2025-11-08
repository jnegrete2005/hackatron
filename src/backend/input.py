import asyncio


async def get_input(game: str, bot: asyncio.subprocess.Process) -> int:
    """
    Get the input from the appropriate bot based on the player number.

    :param game: The current game state with player number included as a JSON string.
    :type game: str
    :param bot: The subprocess handle for the bot
    :type bot: asyncio.subprocess.Process
    """
    if bot is None or bot.stdin is None or bot.stdout is None:
        raise ValueError("Bot subprocess is None")
    try:
        bot.stdin.write((game + "\n").encode("utf-8"))
        await bot.stdin.drain()

        output = await bot.stdout.readline()

        if not output:
            print("No output received from bot")
            return -1

        print(f"Received output from bot: {output.strip().decode('utf-8')}")
        return int(output.strip().decode('utf-8'))
    except Exception as e:
        print(f"Error getting input from bot: {e}")
        return -1
    finally:
        print("Finished get_input function")
        print()
