from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout

from board.BoardState import BoardState
from board.BoardWidget import BoardWidget
from board.Field import Field
from tutorial.TutorialStep import TutorialStep


class TutorialWindow(QDialog):
    """
    Shows help information about the GoGoGo application.
    """
    finished = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent, Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        # Disable the maximize button on macOS
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setModal(True)
        self.setWindowTitle('GoGoGo Tutorial')
        self.setWindowIcon(QIcon('icons/app.png'))

        self.title = QLabel()
        self.title.setStyleSheet('font-size:15px')
        icon = QLabel()
        icon.setPixmap(QPixmap('icons/app.png').scaledToWidth(20))

        title_layout = QHBoxLayout()
        title_layout.setAlignment(Qt.AlignLeft)
        title_layout.addWidget(icon)
        title_layout.addWidget(self.title)

        self.description = QLabel()
        self.description.setWordWrap(True)
        self.board = BoardWidget()
        self.board.clicked_field.connect(self.clicked_field)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_step)

        layout = QVBoxLayout()
        layout.addLayout(title_layout)
        layout.addWidget(self.description)
        layout.addWidget(self.board)
        layout.addWidget(self.next_button)
        self.setLayout(layout)

        self.steps = []
        self.current_step = 0
        self.create_steps()
        self.show_step()

    def reset(self):
        self.current_step = 0
        self.show_step()

    def clicked_field(self, field: Field):
        step = self.steps[self.current_step]
        if step.field_to_click == field:
            if step.show_invalid_move:
                self.board.show_invalid_move(field)
            self.current_step += 1
            self.show_step()
        else:
            self.board.show_invalid_move(field)

    def next_step(self):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.show_step()
        else:
            self.close()

    def show_step(self):
        step = self.steps[self.current_step]
        if step.title:
            self.title.setText(step.title)
        if step.description:
            self.description.setText(step.description)
        self.board.set_state(step.board_state)
        self.next_button.setDisabled(step.field_to_click is not None)
        if self.current_step == len(self.steps) - 1:
            self.next_button.setText("Finish Tutorial")

    def create_steps(self):

        # Step 1
        capture_state = BoardState()
        capture_state.state = [[-1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, 0, 0, 0, -1, -1],
                               [-1, 0, 1, 1, 1, 0, -1],
                               [-1, -1, 0, -1, 0, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1]]

        self.steps.append(
            TutorialStep("Capturing", "1. Surround stones of your opponent to capture them", capture_state, Field(4, 3),
                         False))

        after_capture_state = capture_state.clone()
        after_capture_state.set_field_value(Field(3, 2), -1)
        after_capture_state.set_field_value(Field(3, 3), -1)
        after_capture_state.set_field_value(Field(3, 4), -1)
        after_capture_state.set_field_value(Field(4, 3), 0)

        self.steps.append(TutorialStep(None, "You captured 3 stones", after_capture_state, None, False))

        no_capture_state = capture_state.clone()
        no_capture_state.set_field_value(Field(3, 4), -1)

        # Step 2
        self.steps.append(
            TutorialStep(None, "2. You can't capture when there is space inside", no_capture_state, Field(4, 3),
                         False))

        after_no_capture_state = no_capture_state.clone()
        after_no_capture_state.set_field_value(Field(4, 3), 0)
        self.steps.append(
            TutorialStep(None, "Close the hole to capture", after_no_capture_state, Field(3, 4), False))

        closed_hole_state = after_capture_state.clone()
        closed_hole_state.set_field_value(Field(3, 4), 0)

        self.steps.append(TutorialStep(None, "You captured 2 stones", closed_hole_state, None, False))

        # Step 3
        wall_capture_state = BoardState()
        wall_capture_state.state = [[-1, -1, -1, -1, -1, -1, -1],
                                    [-1, -1, -1, -1, -1, -1, -1],
                                    [-1, -1, -1, -1, -1, -1, 0],
                                    [-1, -1, -1, -1, -1, 0, 1],
                                    [-1, -1, -1, -1, 0, 1, 1],
                                    [-1, -1, 0, 1, 1, 1, 1],
                                    [-1, -1, 0, 1, 1, 1, 1]]

        self.steps.append(
            TutorialStep(None, "3. Walls can help you to capture stones", wall_capture_state, Field(4, 3),
                         False))

        after_wall_capture_state = wall_capture_state.clone()
        after_wall_capture_state.state = [[-1, -1, -1, -1, -1, -1, -1],
                                          [-1, -1, -1, -1, -1, -1, -1],
                                          [-1, -1, -1, -1, -1, -1, 0],
                                          [-1, -1, -1, -1, -1, 0, -1],
                                          [-1, -1, -1, 0, 0, -1, -1],
                                          [-1, -1, 0, -1, -1, -1, -1],
                                          [-1, -1, 0, -1, -1, -1, -1]]

        self.steps.append(
            TutorialStep(None, "You captured 10 stones", after_wall_capture_state, None, False))

        # Step 4
        suicide_state = BoardState()
        suicide_state.state = [[-1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, 1, -1, -1, -1],
                               [-1, -1, 1, -1, 1, -1, -1],
                               [-1, -1, -1, 1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1]]

        self.steps.append(
            TutorialStep("Suicide rule", "4. You can't play in a place where you would be captured immediately",
                         suicide_state,
                         Field(3, 3),
                         True))

        self.steps.append(TutorialStep(None, None, suicide_state, None, False))

        # Step 5
        ko_state = BoardState()
        ko_state.state = [[-1, -1, -1, -1, -1, -1, -1],
                          [-1, -1, -1, -1, -1, -1, -1],
                          [-1, -1, -1, 0, 1, -1, -1],
                          [-1, -1, 0, -1, 0, 1, -1],
                          [-1, -1, -1, 0, 1, -1, -1],
                          [-1, -1, -1, -1, -1, -1, -1],
                          [-1, -1, -1, -1, -1, -1, -1]]

        self.steps.append(
            TutorialStep("KO rule", "5. Imagine this board state", ko_state, None, False))

        ko_state_captured = ko_state.clone()
        ko_state_captured.set_field_value(Field(3, 3), 1)
        ko_state_captured.set_field_value(Field(3, 4), -1)
        self.steps.append(
            TutorialStep(None,
                         "White captured your stone, but You can't recapture because this would lead to an infinite loop",
                         ko_state_captured,
                         Field(3, 4),
                         True))

        self.steps.append(TutorialStep(None, None, ko_state_captured, None, False))

        empty_state = BoardState()
        empty_state.state = [[-1, -1, -1, -1, -1, -1, -1],
                             [-1, 1, 1, -1, -1, 0, -1],
                             [1, -1, -1, -1, 0, -1, 0],
                             [1, -1, 1, 1, 0, -1, 0],
                             [1, -1, -1, 1, 0, -1, 0],
                             [-1, 1, 1, -1, -1, 0, -1],
                             [-1, -1, -1, -1, -1, -1, -1]]

        self.steps.append(
            TutorialStep(
                "Finish", "Well done, you are now ready to play",
                empty_state,
                None,
                False))
