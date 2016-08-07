import os

class Screen:
    def __init__(self, *screen_print_functions):
        self.screen_print_functions = screen_print_functions


    def show(self, clear_after=True):
        for function in self.screen_print_functions:
            function()

        if clear_after:
            self.clear()

    def clear(self):
        try:
            os.system('clear')  # for Linux/OS X
        except:
            os.system('cls')  # for Windows


