import unittest
from AutonomousAgent import AutonomousAgent
from Message import DefaultMessageHandler
from Behaviour import TimedBehaviour
from Interface import Interface
import time


class TestLostMessages(unittest.TestCase):

    def testLostMessages(self):
        """The first agent's sent message number must be equal to the second
        agent's received message number"""

        # Instantiate interface, agents and register message handler and behaviour
        interface = Interface()
        agentA = AutonomousAgent(interface)
        agentB = AutonomousAgent(interface)
        messageHandler = DefaultMessageHandler()
        agentA.registerMessageHandler(messageHandler)
        agentB.registerMessageHandler(messageHandler)
        agentA.registerBehaviour(TimedBehaviour(agentA.emitMessage, 2.0))
        agentB.registerBehaviour(TimedBehaviour(agentB.emitMessage, 2.0))

        # Set agentA outbox to agentB's inbox and viceversa
        agentA.receiverID = agentB.ID
        agentB.receiverID = agentA.ID

        # Run for 10 seconds (comment out the sleep line to run indefinitely)
        agentA.start()
        agentB.start()
        time.sleep(10)
        agentA.stop()
        agentB.stop()

        self.assertEqual(agentA.sentMessages, agentB.receivedMessages)


if __name__ == "__main__":
    unittest.main()
