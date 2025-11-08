from random import randint

from .consts import PLAYER_1, PLAYER_2, N_STELLA, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, MOVE_UP


class Player:
    """
    Class representing a player in the game.
    """

    def __init__(self, number: int, size: int):
        """
        Initializes the player with a number and an initial position.

        :param number: The player number (1 or 2)
        :type number: int
        :param size: The size of the board
        :type size: int
        """
        self.__number: int = number
        self.__position: list[tuple[int, int]] = [self.__generate_initial_position(size)] + [None] * N_STELLA
        self.__previous_move: int = 0  # 0 means no previous move

    @property
    def number(self) -> int:
        """
        Get the player number.
        :return: The player number
        :rtype: int
        """
        return self.__number

    @property
    def previous_move(self) -> int:
        """
        Get the previous move made by the player.
        :return: The previous move
        :rtype: int
        """
        return self.__previous_move

    @property
    def position(self) -> list[tuple[int, int]]:
        """
        Get the current position of the player.
        :return: The current position
        :rtype: list[tuple[int, int]]
        """
        return self.__position

    def serialize(self) -> dict:
        """
        Serialize the player object to a dictionary.

        :return: The serialized player
        :rtype: dict
        """
        trail = [
            {"x": pos[0], "y": pos[1]}
            for pos in self.position
            if pos is not None
        ]
        head = trail[0] if trail else None

        return {
            "head": head,
            "trail": trail,
            "previous_move": self.__previous_move,
        }

    def __get_new_position(self, move: int) -> tuple[int, int]:
        """
        Calculate the new position of the player based on the move
        PRE: The move is valid (1 <= move <= 4)

        :param move: The move to make
        :type move: int

        :return: The new position of the player
        :rtype: tuple[int, int]
        """
        match move:
            case 1:  # Move left
                new_pos = (self.position[0][0], self.position[0][1] - 1)
            case 2:  # Move up
                new_pos = (self.position[0][0] - 1, self.position[0][1])
            case 3:  # Move right
                new_pos = (self.position[0][0], self.position[0][1] + 1)
            case 4:  # Move down
                new_pos = (self.position[0][0] + 1, self.position[0][1])

        return new_pos

    @staticmethod
    def is_valid_move(move: int) -> bool:
        """
        Check if the move is valid.
        :param move: The move to check
        :type move: int
        :return: True if the move is valid, False otherwise
        :rtype: bool
        """
        if not isinstance(move, int):
            return False

        return 1 <= move <= 4

    def move(self, move: int) -> None:
        """
        Move the player in the given direction.
        If the move is invalid, the player will use the previous move instead.

        :param move: The move to make
        :type move: int
        """
        try:
            new_position = self.__get_new_position(move)
        except Exception as e:
            if self.__previous_move == 0:
                new_position = self.__get_new_position(MOVE_UP)
                print(f"Invalid move {move} for player {self.__number}. No previous move available, using MOVE_UP instead. Error: {e}")
            else:
                new_position = self.__get_new_position(self.__previous_move)
                print(f"Invalid move {move} for player {self.__number}. Using previous move instead: {self.__previous_move}. Error: {e}")

        self.__position = [new_position] + self.__position[:-1]
        self.__previous_move = move

    def __generate_initial_position(self, size: int) -> tuple[int, int]:
        """
        Generate the random initial position for the player

        The board looks like this:

              0   1   2  ... n-1 n-2
            +---+---+---+---+---+---+
         0  | # | # | # |...| # | # |
            +---+---+---+---+---+---+
         1  | # |   | 1 | 1 | 1 | # |
            +---+---+---+---+---+---+
         2  | # | 2 |   | 1 | 1 | # |
            +---+---+---+---+---+---+
        ... |...| 2 | 2 |   | 1 |...|
            +---+---+---+---+---+---+
        n-2 | # | 2 | 2 | 2 |   | # |
            +---+---+---+---+---+---+
        n-1 | # | # | # |...| # | # |
            +---+---+---+---+---+---+

        :param size: The size of the board
        :type size: int
        :return: The initial position of the player
        :rtype: tuple[int, int]
        """
        if self.__number == PLAYER_1:
            col = randint(2, size - 2)
            row = randint(1, col - 1)

        elif self.__number == PLAYER_2:
            row = randint(2, size - 2)
            col = randint(1, row - 1)

        else:
            raise InvalidPlayerNumberError(f"Invalid player number: {self.__number}")

        return row, col

    def player_suicided(self, new_move: int) -> bool:
        """
        Check if the player suicided

        :return: True if the player suicided, False otherwise
        :rtype: bool
        """
        # Use int() to avoid errors
        match self.__previous_move:
            case 1:  # MOVE_LEFT
                return new_move == MOVE_RIGHT
            case 2:  # MOVE_UP
                return new_move == MOVE_DOWN
            case 3:  # MOVE_RIGHT
                return new_move == MOVE_LEFT
            case 4:  # MOVE_DOWN
                return new_move == MOVE_UP
            case _:
                return False


class InvalidPlayerNumberError(Exception):
    pass
