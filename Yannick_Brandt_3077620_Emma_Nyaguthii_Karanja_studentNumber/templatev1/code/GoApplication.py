from configuration.ConfigurationWindow import ConfigurationWindow
from configuration.GameConfiguration import GameConfiguration
from game.GameWindow import GameWindow


class GoApplication():

    def __init__(self):
        super().__init__()

        self.game_window = GameWindow()
        self.game_window.configure_game.connect(self.show_configuration_window)
        self.configuration_window = ConfigurationWindow()
        self.configuration_window.start_game.connect(self.show_game_window)

        self.show_configuration_window()

    def show_configuration_window(self):
        self.configuration_window.show()
        self.game_window.hide()

    def show_game_window(self, conf: GameConfiguration):
        self.game_window.start_new_game(conf)
        self.game_window.show()
        self.configuration_window.hide()
