#!/usr/local/bin/python3

import os
import unittest
import tempfile
import shutil

import highscores

class TestHighScore(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.curdir = os.getcwd()
        os.chdir(self.tmpdir)
        self.seed_scores = {'Dykstra':5, 'Kruk':11}
        for player, score in self.seed_scores.items():
            highscores.record(player, score)
        
    def tearDown(self):
        os.chdir(self.curdir)
        shutil.rmtree(self.tmpdir)

    def testNewHighScore(self):
        observed=highscores.record('Dykstra', 10)
        self.assertEqual(observed, 10)

    def testNotHighScore(self):
        observed=highscores.record('Kruk', 9)
        self.assertEqual(observed, 11)

    def testNewPlayer(self):
        observed=highscores.record('Daulton', 7)
        self.assertEqual(observed, 7)
        
if __name__ == "__main__":
    unittest.main()
    
