from enum import Enum

from board.BoardState import BoardState


class WinnerStatus(Enum):
    NONE = -1
    PLAYER_0 = 0
    PLAYER_1 = 1
    DRAW = 2


class GameStatus(Enum):
    END_TWO_PASSES = 0
    END_RESIGN = 1
    END_NO_MOVES = 2
    END_TIMEOUT = 3
    TURN_PLAYER_0 = 4
    TURN_PLAYER_1 = 5
    ANALYSIS = 9


def is_end_status(status: GameStatus):
    return status == GameStatus.END_RESIGN or status == GameStatus.END_NO_MOVES or \
           status == GameStatus.END_TWO_PASSES or status == GameStatus.END_TIMEOUT


def is_playing_status(status: GameStatus):
    return status == GameStatus.TURN_PLAYER_0 or status == GameStatus.TURN_PLAYER_1


class GameState:
    board_state: BoardState
    player_states = []
    status: GameStatus

    def __init__(self, board_state, player_states, status):
        self.board_state = board_state
        self.player_states = player_states
        self.status = status
