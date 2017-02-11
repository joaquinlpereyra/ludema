import os
from ludema.screen import Screen

class Levels:
    def __init__(self, levels, on_successful_end, on_failure_end):
        self.levels = levels
        self.on_successful_end = on_successful_end
        self.on_failure_end = on_failure_end

    def play_all(self):
        for level in self.levels:
            result = level.play()
            if not result:
                return self.on_failure_end()
        return self.on_successful_end()


class Level:
    def __init__(self, board, control_function, on_won, on_lost, screen=None):
        self.board = board
        self.control_function = control_function
        self.on_won = on_won
        self.on_lost = on_lost
        self.screen = screen if screen else self._create_default_screen()

    def _create_default_screen(self):
        return Screen([lambda: print(self.board)], clear_after_print=True)

    def play(self):
        while not self.board.won and not self.board.lost:
            self.screen.show()
            self.control_function()

            if self.screen.clear_after_print:
                self.screen.clear()

        return self.on_won() if self.board.won else self.on_lost()
