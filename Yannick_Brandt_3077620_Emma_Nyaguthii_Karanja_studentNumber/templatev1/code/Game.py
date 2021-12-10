import time

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

from BoardState import BoardState
from Field import Field
from GameState import GameState, GameStatus
from PlayerState import PlayerState


class Game(QWidget):
    """
    This class represents a go game.
    It checks the validity of moves, calculates each player's score and keeps track of the game status.

    signal game_status_changed(gameState:GameState) the status of the game changed
    signal board_state_changed(boardState:BoardState) the status of the board changed
    signal player_state_changed(playerIdx:int, playerState:PlayerState) the status of one player (0 or 1) changed
    signal invalid_move(field:Field) the last played move was invalid
    """
    game_status_changed = pyqtSignal(GameStatus)
    board_state_changed = pyqtSignal(BoardState)
    player_state_changed = pyqtSignal(int, object)
    invalid_move = pyqtSignal(Field)

    def __init__(self):
        super(Game, self).__init__()

        self.board_state = None
        self.history = []
        self.player_states = []
        self.status = None
        self.current_player = 0

    def reset(self, handicap: float):
        self.board_state = BoardState()
        self.history = []
        self.player_states = [PlayerState(), PlayerState()]
        self.player_states[1].captured_stones += handicap

        self.set_game_status(GameStatus.TURN_PLAYER_0)
        self.board_state_changed.emit(self.board_state)
        self.player_state_changed.emit(0, self.player_states[0])
        self.player_state_changed.emit(1, self.player_states[1])

        self.current_player = 0

        self.create_history_entry()

    def rewind(self, position: int):
        state: GameState = self.history[position]
        self.game_status_changed.emit(GameStatus.ANALYSIS)
        self.player_state_changed.emit(0, state.player_states[0])
        self.player_state_changed.emit(1, state.player_states[1])
        self.board_state_changed.emit(state.board_state)

    def pass_stone(self):
        """Passes a stone to the other player. Two consecutive passes ent the game"""
        self.player_states[self.current_player].consecutive_passes += 1
        self.player_states[1 - self.current_player].captured_stones += 1

        self.player_state_changed.emit(0, self.player_states[0])
        self.player_state_changed.emit(1, self.player_states[1])

        if self.player_states[self.current_player].consecutive_passes == 2:
            self.set_game_status(GameStatus.END_TWO_PASSES)

    def place_stone(self, field):
        """ Tries to place a stone on the board. This method can result in two actions:
        1. The move was valid and the stone is placed
        2. The move was invalid and the invalid_move signal is triggered

        :param field: field to put the stone on
        """
        start = time.time()
        if self.move_is_valid(field):

            self.board_state.set_field_value(field, self.current_player)
            self.player_states[self.current_player].consecutive_passes = 0

            captured_stones = self.remove_captured_stones(self.board_state, 1 - self.current_player)
            self.player_states[self.current_player].captured_stones += captured_stones

            self.create_history_entry()

            self.calculate_territories(self.board_state)
            self.set_current_player(1 - self.current_player)
            self.board_state_changed.emit(self.board_state)

            if not self.valid_moves_available():
                self.set_game_status(GameStatus.END_NO_MOVES)
        else:
            self.invalid_move.emit(field)

        end = time.time()
        print(end - start)

    def set_current_player(self, current_player: int):
        self.current_player = current_player
        self.player_states[1 - self.current_player].is_playing = False
        self.player_states[self.current_player].is_playing = True

        self.player_state_changed.emit(0, self.player_states[0])
        self.player_state_changed.emit(1, self.player_states[1])

        if current_player == 0:
            self.set_game_status(GameStatus.TURN_PLAYER_0)
        else:
            self.set_game_status(GameStatus.TURN_PLAYER_1)

    def set_game_status(self, new_status: GameStatus):
        self.status = new_status
        self.game_status_changed.emit(new_status)

    def move_is_valid(self, field: Field):
        """ Check if a move is valid:
        1. The field is free
        2. No ko move
        3. no suicide move

        :param field: field to check
        """
        # Check Free field
        if not self.board_state.get_field_value(field) == -1:
            self.set_game_status(GameStatus.INVALID_MOVE_OCCUPIED)
            return False

        # Check ko
        if self.check_ko(field):
            self.set_game_status(GameStatus.INVALID_MOVE_KO)
            return False

        # Check suicide
        if self.check_suicide(field):
            self.set_game_status(GameStatus.INVALID_MOVE_SUICIDE)
            return False

        return True

    def check_ko(self, field: Field):
        """ Check a field for the ko rule

        :param field: field to check
        """
        if len(self.history) < 2:
            return False
        next_state = self.board_state.clone()
        next_state.set_field_value(field, self.current_player)
        self.remove_captured_stones(next_state, 1 - self.current_player)
        return self.history[-2].board_state == next_state

    def check_suicide(self, field: Field):
        """ Check a field for the suicide rule

        :param field: field to check
        """
        next_state = self.board_state.clone()
        next_state.set_field_value(field, self.current_player)
        self.remove_captured_stones(next_state, 1 - self.current_player)
        return not self.field_has_liberty(next_state, field)

    def remove_captured_stones(self, board_state: BoardState, player_idx: int):
        """ Removes all captured stones on the board from one player

        :param board_state: BoardState to remove stones from
        :param player_idx: only removes stones from this player
        :returns: number of removed stones
        """
        captured_stones = []
        for field in board_state:
            if field in captured_stones:
                continue
            if board_state.get_field_value(field) == player_idx and not self.field_has_liberty(board_state, field):
                for connected_field in self.get_connected_fields(board_state, field):
                    board_state.set_field_value(connected_field, -1)
                    captured_stones.append(connected_field)

        return len(captured_stones)

    def valid_moves_available(self):
        free_fields = self.get_fields_of_type(-1)
        for field in free_fields:
            if self.move_is_valid(field):
                return True
        return False

    def field_has_liberty(self, board_state: BoardState, field: Field):
        for connected_field in self.get_connected_fields(board_state, field):
            for neighbor in connected_field.neighbors():
                if neighbor != field and board_state.get_field_value(neighbor) == -1:
                    return True
        return False

    def get_connected_fields(self, board_state: BoardState, field: Field):
        """ Returns all connected fields with the same value as the given field. The original field is also included

        :param board_state: BoardState to search in
        :param field: field find connected fields for
        """
        field_value = board_state.get_field_value(field)
        connected_stones = []
        propagation = [field]
        while len(propagation) > 0:
            current_stone = propagation.pop()
            connected_stones.append(current_stone)
            for neighbor in current_stone.neighbors():
                if neighbor not in connected_stones and neighbor not in propagation and board_state.get_field_value(
                        neighbor) == field_value:
                    propagation.append(neighbor)

        return connected_stones

    def create_history_entry(self):
        entry = GameState(self.board_state.clone(), [self.player_states[0].clone(), self.player_states[1].clone()],
                          self.status)
        self.history.append(entry)

    def calculate_territories(self, board_state: BoardState):
        territories = [[], []]
        for field in board_state:
            if field in territories[0] or field in territories[1]:
                continue
            field_value = self.board_state.get_field_value(field)
            if field_value == -1:
                connected_fields = self.get_connected_fields(self.board_state, field)
                territory_of = None
                try:
                    for connected_field in connected_fields:
                        for neighbor in connected_field.neighbors():
                            neighbor_value = board_state.get_field_value(neighbor)
                            if neighbor_value == -1:
                                continue
                            elif territory_of is None:
                                territory_of = neighbor_value
                            elif neighbor_value != territory_of:
                                raise "No territory"
                    territories[territory_of] += connected_fields
                except Exception:
                    pass

        self.player_states[0].territory = len(territories[0]) + len(self.get_fields_of_type(0))
        self.player_states[1].territory = len(territories[1]) + len(self.get_fields_of_type(1))

    def get_fields_of_type(self, field_type: int):
        fields = []
        for field in self.board_state:
            if self.board_state.get_field_value(field) == field_type:
                fields.append(field)
        return fields
