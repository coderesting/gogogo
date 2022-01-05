class GameConfiguration:
    """Represents all settings for a game of go"""
    names = []
    handicap: float

    def __init__(self, names, handicap, time_limit):
        self.names = names
        self.handicap = handicap
        self.time_limit = time_limit
