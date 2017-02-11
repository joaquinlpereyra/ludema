import os
import colorama

class Screen:
    def __init__(self, printing_functions, clear_after_print=True):
        colorama.init(autoreset=True)
        self.clear_after_print = clear_after_print
        self.printing_functions = printing_functions

    def show(self):
        [printing_function() for printing_function in self.printing_functions]

    def clear(self):
        try:
            os.system('clear')  # for Linux/OS X
        except:
            os.system('cls')  # for Windows
