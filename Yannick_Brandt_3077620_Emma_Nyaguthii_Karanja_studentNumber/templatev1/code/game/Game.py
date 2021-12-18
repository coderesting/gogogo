from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtWidgets import QWidget

from board.BoardState import BoardState
from board.Field import Field
from configuration.GameConfiguration import GameConfiguration
from game.GameState import GameState, GameStatus, WinnerStatus, is_end_status, is_playing_status
from game.player.PlayerState import PlayerState


class Game(QWidget):
    """
    This class represents a go game.
    It checks the validity of moves, calculates each player's score and keeps track of the game status.

    :signal game_status_changed(gameState:GameStatus): the status of the game changed
    :signal board_state_changed(boardState:BoardState): the status of the board changed
    :signal player_states_changed(playerStates:PlayerState[]): the status of at least one player changed
    :signal invalid_move(field:Field): the last played move was invalid
    """
    game_status_changed = pyqtSignal(GameStatus)
    board_state_changed = pyqtSignal(BoardState)
    player_states_changed = pyqtSignal(list)
    invalid_move = pyqtSignal(Field)

    def __init__(self):
        super(Game, self).__init__()

        self.board_state = None
        self.history = []
        self.player_states = []
        self.status = None
        self.current_player = 0
        # The configuration of the current game
        self.conf = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        # Count down every one second
        self.timer.setInterval(1000)
        self.timer.start()

    def update_timer(self):
        """ Count down the timer of the current player and ends the game if the time of one player reaches 0"""
        if is_playing_status(self.status) and self.conf.time_limit is not None:
            if self.player_states[self.current_player].remaining_time > 0:
                self.player_states[self.current_player].remaining_time -= 1
            else:
                self.set_game_status(GameStatus.END_TIMEOUT)
            self.player_states_changed.emit(self.player_states)

    def start_new_game(self, conf: GameConfiguration):
        """Starts a new game

        :conf: GameConfiguration to start the game with
        """
        self.conf = conf
        self.restart()

    def restart(self):
        """Restarts the current game"""
        self.board_state = BoardState()
        self.history = []
        self.player_states = [PlayerState(), PlayerState()]
        self.player_states[1].captured_stones += self.conf.handicap

        self.player_states[0].remaining_time = self.conf.time_limit
        self.player_states[1].remaining_time = self.conf.time_limit

        self.set_game_status(GameStatus.TURN_PLAYER_0)
        self.board_state_changed.emit(self.board_state)

        self.set_current_player(0)

        self.create_history_entry()

    def rewind(self, position: int):
        """ Rewind the GameState to a specific position in history.

        :position: rewind the game to this position (0 - num_game_steps)
        """
        state: GameState = self.history[position]
        self.game_status_changed.emit(GameStatus.ANALYSIS)
        self.player_states_changed.emit(state.player_states)
        self.board_state_changed.emit(state.board_state)

    def pass_stone(self):
        """Passes a stone to the other player. Two consecutive passes from one player end the game"""
        self.player_states[self.current_player].consecutive_passes += 1
        self.player_states[1 - self.current_player].captured_stones += 1

        self.set_current_player(1 - self.current_player)

        if self.player_states[1 - self.current_player].consecutive_passes == 2:
            self.set_game_status(GameStatus.END_TWO_PASSES)

    def place_stone(self, field):
        """ Tries to place a stone on the board. This method can result in two actions:
        1. The move was valid and the stone is placed
        2. The move was invalid and the invalid_move signal is triggered

        :param field: field to put the stone on
        """
        if not is_playing_status(self.status):
            return
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

    def set_current_player(self, current_player: int):
        """Updates the current player

        :param current_player: 0 or 1
        """
        self.current_player = current_player
        self.player_states[1 - self.current_player].is_playing = False
        self.player_states[self.current_player].is_playing = True

        self.player_states_changed.emit(self.player_states)
        self.set_game_status(GameStatus.TURN_PLAYER_0 if current_player == 0 else GameStatus.TURN_PLAYER_1)

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
        # Check if the field is free
        if not self.board_state.get_field_value(field) == -1:
            return False

        # Check ko
        if self.check_ko(field):
            return False

        # Check suicide
        if self.check_suicide(field):
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
        """ Checks if valid moves are available for the current BoardState and player"""
        free_fields = self.get_fields_of_type(-1)
        for field in free_fields:
            if self.move_is_valid(field):
                return True
        return False

    def field_has_liberty(self, board_state: BoardState, field: Field):
        """ Calculates if a field has at least one field of liberty

        :board_state: the BoardState to do the calculation on
        :field: the field to check the liberty for
        """
        for connected_field in self.get_connected_fields(board_state, field):
            for neighbor in connected_field.neighbors():
                if neighbor != field and board_state.get_field_value(neighbor) == -1:
                    return True
        return False

    def get_connected_fields(self, board_state: BoardState, field: Field):
        """ Returns all connected fields with the same value as the given field. The original field is also included.

        :param board_state: BoardState to search in
        :param field: field find connected fields for
        """

        # Flood fill algorithm
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
        """Creates and stores a snapshot of the current GameState in the history"""
        entry = GameState(self.board_state.clone(), [self.player_states[0].clone(), self.player_states[1].clone()],
                          self.status)
        self.history.append(entry)

    def calculate_territories(self, board_state: BoardState):
        """ Calculates and updates the territories of both players
        The algorithm is a simplified version of the physical go algorithm.
        It counts stones on the field and empty fields that are surrounded by one player.
        Note: dead stones are not removed from the board before counting since
        1. There is no algorithm that works 100% of the time
        2. A decent algorithm is pretty complex and not the main focus of this project

        :board_state: The state to calculate territories on
        """
        territories = [[], []]
        for field in board_state:
            # Skip already identified territory
            if field in territories[0] or field in territories[1]:
                continue
            field_owner = self.board_state.get_field_value(field)
            # -1 == free field
            if field_owner == -1:
                connected_fields = self.get_connected_fields(self.board_state, field)
                try:
                    territory_of = None
                    # Add connected fields to a player's territory if all neighbors of the fields are free
                    # or belong to the same player
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
                    continue

        for i in [0, 1]:
            # If there is only one stone on the field all remaining free fields would count as that players' territory
            # This should not be true and the territory needs to be set to zero
            if len(territories[i]) == 48:
                territories[i] = []
            self.player_states[i].territory = len(territories[i]) + len(self.get_fields_of_type(i))

    def get_fields_of_type(self, field_type: int):
        """ Returns all fields of one type

        :field_type: the field type to find fields for
        -1: No field owner
        0: owned by player 0
        1: owned by player 1
        """
        fields = []
        for field in self.board_state:
            if self.board_state.get_field_value(field) == field_type:
                fields.append(field)
        return fields

    def get_winner_status(self):
        """Calculate the WinnerStatus

        :returns: WinnerStatus of the current game
        """
        if not is_end_status(self.status):
            return WinnerStatus.NONE

        player0_score = len(self.get_fields_of_type(0)) + self.player_states[0].captured_stones + self.player_states[
            0].territory
        player1_score = len(self.get_fields_of_type(1)) + self.player_states[1].captured_stones + self.player_states[
            1].territory

        if player0_score > player1_score:
            return WinnerStatus.PLAYER_0
        elif player1_score > player0_score:
            return WinnerStatus.PLAYER_1
        else:
            return WinnerStatus.DRAW
