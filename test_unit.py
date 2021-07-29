import unittest
from AutonomousAgent import AutonomousAgent


class TestMissingInterface(unittest.TestCase):

    def testMissingInterface(self):
        """Not providing an interface to the agent must result with an AttributeError"""

        with self.assertRaises(AttributeError):
            AutonomousAgent(None)


if __name__ == "__main__":
    unittest.main()
