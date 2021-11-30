import sys

from PyQt5.QtWidgets import QApplication

from GoApplication import GoApplication

app = QApplication([])
myGo = GoApplication()
sys.exit(app.exec_())
