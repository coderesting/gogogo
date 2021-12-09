class GameConfiguration:
    names = []
    handicap: float

    def __init__(self, name1, name2, handicap):
        self.names = [name1, name2]
        self.handicap = handicap
