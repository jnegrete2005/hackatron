from src.backend.player import Player
from src.backend.consts import PLAYER_1, PLAYER_2, WALL, PLAYERS_COLLIDED, BOTH_WALLS


class GameState:
    def __init__(
        self,
        size: int,
        player_1: Player | None = None,
        player_2: Player | None = None,
        board: list[list[int]] | None = None
    ):
        self.__size: int = size

        # Save the players' info
        self.__player_1: Player = player_1 or Player(PLAYER_1, size)
        self.__player_2: Player = player_2 or Player(PLAYER_2, size)

        # Initialize the board
        self.__board: list[list[int]] = board or [[0] * size for _ in range(size)]
        self.__walls: set[tuple[int, int]] = set()
        self.__init_walls()

        # Add the initial positions of the players to the board
        self.__board[self.__player_1.position[0][0]][self.__player_1.position[0][1]] = PLAYER_1
        self.__board[self.__player_2.position[0][0]][self.__player_2.position[0][1]] = PLAYER_2

        self.__game_over: bool = False
        self.__winner: Player | None = None

    @property
    def size(self) -> int:
        return self.__size

    @property
    def player_1(self) -> Player:
        return self.__player_1

    @property
    def player_2(self) -> Player:
        return self.__player_2

    @property
    def board(self) -> list[list[int]]:
        return self.__board

    @property
    def walls(self) -> set[tuple[int, int]]:
        return self.__walls

    @property
    def game_over(self) -> bool:
        return self.__game_over

    @property
    def winner(self) -> Player | None:
        return self.__winner

    def __init_walls(self) -> None:
        """
        Initialize the walls of the game board.
        The walls are placed on the edges of the board.
        """
        n = self.__size - 1
        for i in range(self.__size):
            self.__walls.add((0, i))
            self.__walls.add((n, i))
            self.__walls.add((i, 0))
            self.__walls.add((i, n))

            self.__board[0][i] = WALL
            self.__board[n][i] = WALL
            self.__board[i][0] = WALL
            self.__board[i][n] = WALL

    def __get_collision(self, player_1: Player, player_2: Player) -> int | None:
        """
        Check if a collision happened

        :param player_1: The first player
        :type player_1: Player
        :param player_2: The second player
        :type player_2: Player
        :return: The type of collision that happened or None if no collision happened
        :rtype: Player | PLAYERS_COLLIDED | BOTH_WALLS | None
        """
        # Check if the players collided into each other diagonally or head-on
        if player_1.position[0] == player_2.position[0] or \
                (player_1.position[1] == player_2.position[0] and player_1.position[0] == player_2.position[1]):
            return PLAYERS_COLLIDED

        elif player_1.position[0] in self.walls and player_2.position[0] in self.walls:
            return BOTH_WALLS

        elif player_1.position[0] in player_2.position or player_1.position[0] in self.walls:
            return player_2

        elif player_2.position[0] in player_1.position or player_2.position[0] in self.walls:
            return player_1

        return None

    def __handle_collisions(self) -> int | None:
        """
        Handle the collisions between the players and the walls.

        :return: The type of collision that happened or None if no collision happened
        :rtype: Player | PLAYERS_COLLIDED | BOTH_WALLS | None
        """
        collision = self.__get_collision(self.player_1, self.player_2)

        if collision is None:
            return None

        if collision == PLAYERS_COLLIDED:
            self.__winner = None
        elif collision == BOTH_WALLS:
            self.__winner = None
        else:
            self.__winner = collision

        self.__game_over = True

        return collision

    def __update_board(self, last_pos_1: tuple[int, int], last_pos_2: tuple[int, int]) -> None:
        """
        Update the game board with the players' new positions.

        :param last_pos_1: The last position of player 1 to remove from the board.
        :type last_pos_1: tuple[int, int]
        :param last_pos_2: The last position of player 2 to remove from the board.
        :type last_pos_2: tuple[int, int]
        """

        if last_pos_1 is not None:
            self.__board[last_pos_1[0]][last_pos_1[1]] = 0
        if last_pos_2 is not None:
            self.__board[last_pos_2[0]][last_pos_2[1]] = 0

        for pos_1, pos_2 in zip(self.__player_1.position, self.__player_2.position):
            if pos_1 is not None:
                self.__board[pos_1[0]][pos_1[1]] = PLAYER_1

            if pos_2 is not None:
                self.__board[pos_2[0]][pos_2[1]] = PLAYER_2

    def tick(self, move_1: int, move_2: int) -> None | int:
        """
        Process a game tick with the given moves for both players.
        :param move_1: Move for player 1.
        :type move_1: int
        :param move_2: Move for player 2.
        :type move_2: int

        :return: None if the game continues, or the type of collision that happened.
        :rtype: Player | PLAYERS_COLLIDED | BOTH_WALLS | None
        """
        # Get the players' last positions to remove them from the board
        last_pos_1 = self.player_1.position[-1]
        last_pos_2 = self.player_2.position[-1]

        # Move the players
        self.player_1.move(move_1)
        self.player_2.move(move_2)

        # Check for collisions
        collision = self.__handle_collisions()

        # Update the board with the new positions
        self.__update_board(last_pos_1, last_pos_2)

        return collision

    def __str__(self) -> str:
        res = ""
        for row in self.__board:
            res += " ".join(str(cell) for cell in row) + "\n"

        return res
