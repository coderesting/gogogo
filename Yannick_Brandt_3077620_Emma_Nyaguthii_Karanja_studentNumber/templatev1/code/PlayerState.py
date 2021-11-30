class PlayerState:
    is_playing = False
    remaining_time = 900  # 15min in seconds
    captured_stones = 0

    def reset(self):
        self.is_playing = False
        self.remaining_time = 900
        self.captured_stones = 0
