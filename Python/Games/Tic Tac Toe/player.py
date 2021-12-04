import math
import random

class Player:
    def __init__(self, letter):
        # letter is x or o
        self.letter = letter

    # we want all plpayers to get their next move given a game
    def get_move(self, game):
        pass

    class RandomCompuetrPlayer(Player):
        def __init__(self, letter):
            super().__init__(letter)

        def get_move(self, game):
            pass

    class HumanPlayer(Player):
        def __init__(self, letter):
            super().__init__(letter)

        def get_move(self, game):
            pass
