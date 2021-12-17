class PlayerState:
    is_playing: bool
    remaining_time = None
    captured_stones: int
    territory: int
    consecutive_passes: int

    def __init__(self):
        self.reset()

    def clone(self):
        player_state = PlayerState()
        player_state.is_playing = self.is_playing
        player_state.remaining_time = self.remaining_time
        player_state.captured_stones = self.captured_stones
        player_state.territory = self.territory
        player_state.consecutive_passes = self.consecutive_passes
        return player_state

    def reset(self):
        self.is_playing = False
        self.remaining_time = None  # 15min in seconds
        self.captured_stones = 0
        self.territory = 0
        self.consecutive_passes = 0
