class GameConfiguration:
    names = []
    handicap: float

    def __init__(self, names, handicap):
        self.names = names
        self.handicap = handicap
