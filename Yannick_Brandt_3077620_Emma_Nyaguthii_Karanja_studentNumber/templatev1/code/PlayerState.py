class PlayerState:
    is_playing: bool
    remaining_time: int
    captured_stones: int
    consecutive_passes: int

    def __init__(self):
        self.reset()

    def reset(self):
        self.is_playing = False
        self.remaining_time = 900  # 15min in seconds
        self.captured_stones = 0
        self.consecutive_passes = 0
