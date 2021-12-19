from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout

from BigButton import BigButton
from board.BoardState import BoardState
from board.BoardWidget import BoardWidget
from board.Field import Field
from tutorial.TutorialStep import TutorialStep


class TutorialWindow(QDialog):
    """Shows an interactive tutorial on how to play go"""

    def __init__(self, parent):
        super().__init__(parent, Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setModal(True)
        self.setWindowTitle('How to play GoGoGo')
        self.setWindowIcon(QIcon('icons/app.png'))

        self.title = QLabel()
        self.title.setStyleSheet('font-size:17px')
        icon = QLabel()
        icon.setPixmap(QPixmap('icons/app.png').scaledToWidth(20))

        title_layout = QHBoxLayout()
        title_layout.setAlignment(Qt.AlignLeft)
        title_layout.addWidget(icon)
        title_layout.addWidget(self.title)

        self.description = QLabel()
        self.description.setStyleSheet('font-size:13px')
        self.description.setWordWrap(True)

        self.board = BoardWidget()
        self.board.clicked_field.connect(self.clicked_field)

        self.back_button = BigButton("Back")
        self.back_button.clicked.connect(self.previous_step)

        self.next_button = BigButton("Next")
        self.next_button.clicked.connect(self.next_step)
        self.next_button.setDefault(True)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.back_button, 1)
        # Make the next button bigger
        buttons_layout.addWidget(self.next_button, 2)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.addLayout(title_layout)
        layout.addWidget(self.description)
        layout.addWidget(self.board)
        layout.addLayout(buttons_layout)
        self.setLayout(layout)
        self.setContentsMargins(5, 5, 5, 5)

        self.steps = []
        self.current_step = 0
        self.create_steps()
        self.show_step()

    def reset(self):
        self.current_step = 0
        self.show_step()

    def clicked_field(self, field: Field):
        """The user clicked on a field

        :param field: clicked Field
        """
        step = self.steps[self.current_step]
        if step.field_to_click == field:
            if step.show_invalid_move:
                self.board.show_invalid_move(field)
            self.current_step += 1
            self.show_step()

    def next_step(self):
        """Show the next step or close the window when the end is reached"""
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.show_step()
        else:
            self.close()

    def previous_step(self):
        """Show the previous step"""
        if self.current_step > 0:
            self.current_step -= 1
            self.show_step()

    def show_step(self):
        """Update all widgets to show the current step"""
        step = self.steps[self.current_step]
        if step.title:
            self.title.setText(step.title)
        if step.description:
            self.description.setText(step.description)
        self.board.set_state(step.board_state)

        self.board.highlight_fields([step.field_to_click] if step.field_to_click else None)

        self.next_button.setDisabled(step.field_to_click is not None)
        self.next_button.setText("Finish Tutorial" if self.current_step == len(self.steps) - 1 else "Next")
        self.back_button.setDisabled(self.current_step == 0)
        # Remove the focus from the back button to prevent the user from thinking he/she should click it
        self.back_button.clearFocus()

    def create_steps(self):

        # Scoring 1
        scoring_state = BoardState()
        scoring_state.state = [[0, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, 0, 0, -1],
                               [-1, -1, -1, 0, -1, -1, 0],
                               [-1, -1, -1, 0, 0, 0, -1],
                               [-1, -1, -1, -1, -1, -1, -1]]

        self.steps.append(
            TutorialStep("Scoring 1",
                         "Your score is <b>10</b> (<b>8</b> Stones + <b>2</b> territory fields)<br>territory: number "
                         "of encapsulated fields",
                         scoring_state, None, False))

        scoring_state_2 = scoring_state.clone()
        scoring_state_2.state = [[0, -1, -1, -1, 1, -1, -1],
                                 [-1, -1, -1, -1, 1, -1, -1],
                                 [1, -1, -1, -1, 1, 1, 1],
                                 [1, -1, -1, -1, 0, 0, -1],
                                 [-1, -1, -1, 0, -1, -1, 0],
                                 [-1, -1, -1, 0, 0, 0, -1],
                                 [-1, -1, -1, -1, -1, -1, -1]]

        self.steps.append(
            TutorialStep("Scoring 2",
                         "The player with the highest score wins<br>Score: White <b>11</b> - <b>10</b> Black",
                         scoring_state_2,
                         None, False))

        # Capturing 1
        capture_state = BoardState()
        capture_state.state = [[-1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, 0, 0, 0, -1, -1],
                               [-1, 0, 1, 1, 1, 0, -1],
                               [-1, -1, 0, -1, 0, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1]]

        self.steps.append(
            TutorialStep("Capturing 1", "Surround stones of your opponent to capture them", capture_state, Field(4, 3),
                         False))

        after_capture_state = capture_state.clone()
        after_capture_state.set_field_value(Field(3, 2), -1)
        after_capture_state.set_field_value(Field(3, 3), -1)
        after_capture_state.set_field_value(Field(3, 4), -1)
        after_capture_state.set_field_value(Field(4, 3), 0)

        self.steps.append(
            TutorialStep("Capturing 1",
                         "Great. You captured <b>3</b> stones. <br>These are also added to your <b>score</br",
                         after_capture_state, None, False))

        no_capture_state = capture_state.clone()
        no_capture_state.set_field_value(Field(3, 4), -1)

        # Capturing 2
        self.steps.append(
            TutorialStep("Capturing 2", "You can't capture when there is space inside", no_capture_state, Field(4, 3),
                         False))

        after_no_capture_state = no_capture_state.clone()
        after_no_capture_state.set_field_value(Field(4, 3), 0)
        self.steps.append(
            TutorialStep("Capturing 2", "Close the hole to capture", after_no_capture_state, Field(3, 4), False))

        closed_hole_state = after_capture_state.clone()
        closed_hole_state.set_field_value(Field(3, 4), 0)

        self.steps.append(TutorialStep("Capturing 2", "You captured <b>2</b> stones", closed_hole_state, None, False))

        # Capturing 3
        wall_capture_state = BoardState()
        wall_capture_state.state = [[-1, -1, -1, -1, -1, -1, -1],
                                    [-1, -1, -1, -1, -1, -1, -1],
                                    [-1, -1, -1, -1, -1, -1, 0],
                                    [-1, -1, -1, -1, -1, 0, 1],
                                    [-1, -1, -1, -1, 0, 1, 1],
                                    [-1, -1, 0, 1, 1, 1, 1],
                                    [-1, -1, 0, 1, 1, 1, 1]]

        self.steps.append(
            TutorialStep("Capturing 3", "Walls can help you to capture stones", wall_capture_state, Field(4, 3), False))

        after_wall_capture_state = wall_capture_state.clone()
        after_wall_capture_state.state = [[-1, -1, -1, -1, -1, -1, -1],
                                          [-1, -1, -1, -1, -1, -1, -1],
                                          [-1, -1, -1, -1, -1, -1, 0],
                                          [-1, -1, -1, -1, -1, 0, -1],
                                          [-1, -1, -1, 0, 0, -1, -1],
                                          [-1, -1, 0, -1, -1, -1, -1],
                                          [-1, -1, 0, -1, -1, -1, -1]]

        self.steps.append(
            TutorialStep("Capturing 3", "You captured <b>11</b> stones", after_wall_capture_state, None, False))

        # Suicide rule
        suicide_state = BoardState()
        suicide_state.state = [[-1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, 1, -1, -1, -1],
                               [-1, -1, 1, -1, 1, -1, -1],
                               [-1, -1, -1, 1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1]]

        self.steps.append(
            TutorialStep("Suicide rule", "You can't play in a place where you would be captured immediately",
                         suicide_state, Field(3, 3), True))

        self.steps.append(
            TutorialStep("Suicide rule", "You can't play in a place where you would be captured immediately",
                         suicide_state, None, False))

        # KO rule
        ko_state = BoardState()
        ko_state.state = [[-1, -1, -1, -1, -1, -1, -1],
                          [-1, -1, -1, -1, -1, -1, -1],
                          [-1, -1, -1, 0, 1, -1, -1],
                          [-1, -1, 0, -1, 0, 1, -1],
                          [-1, -1, -1, 0, 1, -1, -1],
                          [-1, -1, -1, -1, -1, -1, -1],
                          [-1, -1, -1, -1, -1, -1, -1]]

        self.steps.append(TutorialStep("KO rule", "Imagine this board state", ko_state, None, False))

        ko_state_captured = ko_state.clone()
        ko_state_captured.set_field_value(Field(3, 3), 1)
        ko_state_captured.set_field_value(Field(3, 4), -1)
        self.steps.append(
            TutorialStep("KO rule",
                         "White captured your stone_pixmap, but you can't recapture because this would lead to an infinite "
                         "loop",
                         ko_state_captured, Field(3, 4), True))

        self.steps.append(TutorialStep("KO rule",
                                       "White captured your stone_pixmap, but you can't recapture because this would lead to "
                                       "an infinite loop", ko_state_captured, None, False))

        # Pass
        pass_state = BoardState()
        pass_state.state = [[1, 1, 1, 1, 1, -1, 1],
                            [-1, 1, 1, -1, 1, 1, -1],
                            [1, 1, -1, 1, 1, 1, 1],
                            [1, -1, 1, 1, 1, -1, 1],
                            [1, 1, 1, 1, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0],
                            [-1, 0, 0, -1, 0, -1, 0]]

        self.steps.append(
            TutorialStep("Pass",
                         "If you feel like you have no moves left you can pass.<br>The game ends after <b>2</b> "
                         "consecutive passes.", pass_state, None, True))

        # Finish
        go_state = BoardState()
        go_state.state = [[-1, -1, -1, -1, -1, -1, -1],
                          [-1, 1, 1, -1, -1, 0, -1],
                          [1, -1, -1, -1, 0, -1, 0],
                          [1, -1, 1, 1, 0, -1, 0],
                          [1, -1, -1, 1, 0, -1, 0],
                          [-1, 1, 1, -1, -1, 0, -1],
                          [-1, -1, -1, -1, -1, -1, -1]]

        self.steps.append(TutorialStep("Finish", "Well done, you are now ready to play", go_state, None, False))
