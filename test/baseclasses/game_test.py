from unittest import TestCase
from src.baseclasses import Game


class MathsTests(TestCase):

    def test_sum(self):
        game = Game('Ace of Aces (Europe).zip')
        print(game.filename)
        self.assertEqual(4+1, 5)
