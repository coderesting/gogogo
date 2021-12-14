from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout


class AboutWindow(QDialog):
    """
    Shows information about the Go application
    """

    def __init__(self, parent):
        super().__init__(parent, Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        # Prevent the window from being in the background
        self.setModal(True)
        self.setWindowTitle("About GoGoGo")
        self.setWindowIcon(QIcon("icons/app.png"))

        about_layout = QHBoxLayout()

        app_image = QLabel()
        app_image.setPixmap(QPixmap("icons/app.png"))
        app_image.setAlignment(Qt.AlignTop)
        about_layout.addWidget(app_image)

        info_layout = QVBoxLayout()

        name_label = QLabel("GoGoGo v1.0")
        name_label.setStyleSheet("font-size:20px")
        info_layout.addWidget(name_label)

        developer_label = QLabel("Designed and developed mostly by Yannick Brandt")
        info_layout.addWidget(developer_label)

        description_label = QLabel("""GoGoGo is a small student project designed and developed for an assignment \
at Griffith College Dublin. It allows two human players to play the board game go.
        """)
        description_label.setWordWrap(True)
        info_layout.addWidget(description_label)
        info_layout.setSpacing(10)
        info_layout.addStretch()

        about_layout.addLayout(info_layout)
        about_layout.setSpacing(10)
        about_layout.addStretch()

        self.setLayout(about_layout)

        # Fix the window size to the minimum size
        self.setFixedSize(self.sizeHint())
