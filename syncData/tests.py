import unittest
from syncData.SyncDb import *


class syncDataTest(unittest.TestCase):
    def setUp(self):
        self.old = 'test'
        self.newCorrect = 'test'
        self.newWrong = 'tes'
        self.time = nextIteration()

    def test_confirmDifferences(self):
        one = confirmDifferences(self.newCorrect, self.old)
        two = confirmDifferences(self.newWrong, self.old)
        three = confirmDifferences(self.newCorrect, self.newWrong)
        self.assertFalse(one)
        self.assertTrue(two)
        self.assertTrue(three)

    def test_nextIteration(self):
        self.assertTrue(self.time > 0)
        self.assertTrue(self.time < 86400)

    def test_updateDatabase(self):
        pass


if __name__ == '__main__':
    unittest.main()
