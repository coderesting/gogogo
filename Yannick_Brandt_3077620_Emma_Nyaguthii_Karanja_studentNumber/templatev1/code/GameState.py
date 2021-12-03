from enum import Enum


class GameState(Enum):
    END_TWO_PASSES = 0
    END_RESIGN = 1
    END_NO_MOVES = 2
    TURN_PLAYER_0 = 3
    TURN_PLAYER_1 = 4
    INVALID_MOVE_KO = 5
    INVALID_MOVE_SUICIDE = 6
    INVALID_MOVE_OCCUPIED = 7
