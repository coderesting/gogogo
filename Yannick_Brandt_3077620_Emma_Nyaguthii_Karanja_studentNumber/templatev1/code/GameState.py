from enum import Enum

from BoardState import BoardState


class GameStatus(Enum):
    END_TWO_PASSES = 0
    END_RESIGN = 1
    END_NO_MOVES = 2
    TURN_PLAYER_0 = 3
    TURN_PLAYER_1 = 4
    INVALID_MOVE_KO = 5
    INVALID_MOVE_SUICIDE = 6
    INVALID_MOVE_OCCUPIED = 7
    ANALYSIS = 8


class GameState:
    board_state: BoardState
    player_states = []
    status: GameStatus

    def __init__(self, board_state, player_states, status):
        self.board_state = board_state
        self.player_states = player_states
        self.status = status
