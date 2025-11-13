import asyncio

from src.backend.players.player_input import IPlayerType


DOCKER_BASE_COMMAND = [
    "docker", "run",
    "-i",
    "--rm",
    "--network", "none",
    "--memory", "512m",
    "--cpus", "1",
]


class BotPlayer(IPlayerType):
    """
    An IPlayerInput implementation that launches and communicates
    with a Docker-based bot.
    """

    def __init__(self, bot_image: str):
        self.bot_image = bot_image
        self.process: asyncio.subprocess.Process | None = None

    async def initialize(self) -> bool:
        """Launches the Docker container for the bot."""
        if not self.bot_image:
            return False
        try:
            self.process = await asyncio.create_subprocess_exec(
                *DOCKER_BASE_COMMAND, self.bot_image,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            print(f"Bot {self.bot_image} launched successfully.")
            return True
        except Exception as e:
            print(f"Error launching bot {self.bot_image}: {e}")
            return False

    async def get_move(self, game_state_json: str) -> int:
        """Sends game state to the bot and reads its move."""
        if self.process is None or self.process.stdin is None or self.process.stdout is None:
            print(f"Bot {self.bot_image} process is not running or pipes are missing.")
            return -1  # Return invalid move

        try:
            self.process.stdin.write((game_state_json + "\n").encode("utf-8"))
            await self.process.stdin.drain()

            output = await self.process.stdout.readline()

            if not output:
                print(f"No output received from bot {self.bot_image}")
                return -1

            move_str = output.strip().decode('utf-8')
            print(f"Received output from bot {self.bot_image}: {move_str}")
            return int(move_str)

        except Exception as e:
            print(f"Error getting input from bot {self.bot_image}: {e}")
            return -1
        finally:
            print(f"Finished get_move for bot {self.bot_image}")
            print()

    async def cleanup(self) -> None:
        """Terminates the bot and prints any error output."""
        if self.process is None:
            return

        print(f"Terminating bot {self.bot_image}...")
        try:
            # Send EOF to stdin
            if self.process.stdin:
                self.process.stdin.close()
                await self.process.stdin.wait_closed()

            # Read stderr
            if self.process.stderr:
                errors = await self.process.stderr.read()
                if errors:
                    print(f"--- Errores del Bot {self.bot_image} ---")
                    print(errors.decode('utf-8'))
                    print("---------------------------------")

        except ProcessLookupError:
            print("ProcessLookupError; bot probably never launched.")
        except Exception as e:
            print(f"Error reading stderr from bot: {e}")

        # Terminate if still running
        if self.process.returncode is None:
            self.process.terminate()
            await self.process.wait()

        print(f"Bot {self.bot_image} cleanup complete.")
