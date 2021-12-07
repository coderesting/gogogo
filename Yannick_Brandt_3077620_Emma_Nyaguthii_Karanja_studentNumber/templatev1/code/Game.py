from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

from BoardState import BoardState
from Field import Field
from GameState import GameState
from PlayerState import PlayerState


class Game(QWidget):
    """
    This class represents a go game.
    It checks the validity of moves, calculates each player's score and keeps track of the game state.

    signal game_state_changed(gameState:GameState) the state of the game changed
    signal board_state_changed(boardState:BoardState) the state of the board changed
    signal player_state_changed(playerIdx:int, playerState:PlayerState) the state of one player (0 or 1) changed
    signal invalid_move(field:Field) the last played move was invalid
    """
    game_state_changed = pyqtSignal(GameState)
    board_state_changed = pyqtSignal(BoardState)
    player_state_changed = pyqtSignal(int, PlayerState)
    invalid_move = pyqtSignal(Field)

    board_state: BoardState
    history: list[BoardState]
    player_states: list[PlayerState]
    current_player: int

    def __init__(self):
        super(Game, self).__init__()
        self.reset()

    def reset(self):
        self.board_state = BoardState()
        self.history = []
        self.player_states = [PlayerState(), PlayerState()]
        self.current_player = 0

    def pass_stone(self):
        """Passes a stone to the other player. Two consecutive passes ent the game"""
        self.player_states[self.current_player].consecutive_passes += 1
        self.player_states[1 - self.current_player].captured_stones += 1

        self.player_state_changed.emit(self.current_player, self.player_states[self.current_player])
        self.player_state_changed.emit(1 - self.current_player, self.player_states[1 - self.current_player])

        if self.player_states[self.current_player].consecutive_passes == 2:
            self.set_game_state(GameState.END_TWO_PASSES)

    # Todo: implement later due to high complexity
    def calculate_score(self):
        pass

    def place_stone(self, field):
        """ Tries to place a stone on the board. This method can result in two actions:
        1. The move was valid and the stone is placed
        2. The move was invalid and the invalid_move signal is triggered

        :param field: field to put the stone on
        """
        if self.move_is_valid(field):
            self.board_state.set_field_value(field, self.current_player)
            self.player_states[self.current_player].consecutive_passes = 0

            captured_stones = self.remove_captured_stones(self.board_state, 1 - self.current_player)
            self.player_states[self.current_player].captured_stones += captured_stones

            self.history.append(self.board_state.clone())

            self.set_current_player(1 - self.current_player)
            self.board_state_changed.emit(self.board_state)
        else:
            self.invalid_move.emit(field)

    def set_current_player(self, current_player: int):
        self.current_player = current_player
        self.player_states[1 - self.current_player].is_playing = False
        self.player_states[self.current_player].is_playing = True

        self.player_state_changed.emit(self.current_player, self.player_states[self.current_player])
        self.player_state_changed.emit(1 - self.current_player, self.player_states[1 - self.current_player])

        if current_player == 0:
            self.set_game_state(GameState.TURN_PLAYER_0)
        else:
            self.set_game_state(GameState.TURN_PLAYER_1)

    def set_game_state(self, new_state: GameState):
        self.game_state_changed.emit(new_state)

    def move_is_valid(self, field: Field):
        """ Check if a move is valid:
        1. The field is free
        2. No ko move
        3. no suicide move

        :param field: field to check
        """
        # Check Free field
        if not self.board_state.get_field_value(field) == -1:
            self.set_game_state(GameState.INVALID_MOVE_OCCUPIED)
            return False

        # Check ko
        if self.check_ko(field):
            self.set_game_state(GameState.INVALID_MOVE_KO)
            return False

        # Check suicide
        if self.check_suicide(field):
            self.set_game_state(GameState.INVALID_MOVE_SUICIDE)
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
        return self.history[-2] == next_state

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
        captured_stones = 0
        for field in board_state:
            if board_state.get_field_value(field) == player_idx and not self.field_has_liberty(board_state, field):
                for connected_field in self.get_connected_fields(board_state, field):
                    board_state.set_field_value(connected_field, -1)
                    captured_stones += 1

        return captured_stones

    def field_has_liberty(self, board_state: BoardState, field: Field):
        for connected_field in self.get_connected_fields(board_state, field):
            for neighbor in connected_field.neighbors():
                if neighbor != field and board_state.get_field_value(neighbor) == -1:
                    return True
        return False

    def get_connected_fields(self, board_state: BoardState, field: Field):
        """ Returns all connected fields with the same value than the given field. The original field is also included

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
                if neighbor not in connected_stones and board_state.get_field_value(neighbor) == field_value:
                    propagation.append(neighbor)

        return connected_stones

    # Todo: implement later due to high complexity
    # def get_territories(self, player_idx: int):
    #     territory_fields = []
    #     for field in self.board_state:
    #         field_value = self.board_state.get_field_value(field)
    #         if field_value == 0:
    #             connected_fields = self.get_connected_fields(self.board_state, field)
    #             for connected_field in connected_fields:
