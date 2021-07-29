import threading
import time
import uuid
import random
from Message import Message, MessageType, DefaultMessageHandler
from Behaviour import TimedBehaviour
from Interface import Interface
from Tools import Colors


class AutonomousAgent:
    """Class representing an autonomous agent"""

    words = ('hello', 'sun', 'world', 'space', 'moon', 'crypto', 'sky', 'ocean', 'universe', 'human')

    def __init__(self, interface, ID=None, receiverID=None):
        if not interface:
            raise AttributeError("Agent's interface was not provided.")

        self.interface = interface
        self.ID = ID if ID else uuid.uuid4().hex
        self.receiverID = receiverID
        self.handlers = {}
        self.behaviours = []
        self.stopFlag = False
        self.receivedMessages = 0
        self.sentMessages = 0


    def registerMessageHandler(self, handler):
        self.handlers[handler.messageType] = handler


    def registerBehaviour(self, behaviour):
        self.behaviours.append(behaviour)


    def messageCheckLoop(self):
        while not self.stopFlag:
            # Receive messages
            for message in self.interface.receiveMessages(self.ID):
                self.handlers[message.messageType].handle(message) # Handle the message
                self.receivedMessages += 1

                messageHeader = f'[{self.ID}] Message received from {message.senderID}'
                print(f'{messageHeader: <90}: {message.text: <20}') # Log the event

            # Wait a little bit to avoid heavy CPU usage
            time.sleep(0.1)


    def emitMessage(self):
        """Emits a random message based on the words set"""
        text = '-'.join(random.sample(self.words, 2))
        message = Message(text, MessageType.DEFAULT, self.ID, self.receiverID)
        self.interface.sendMessage(message) # Send to interface
        self.sentMessages += 1

        messageHeader = f'[{self.ID}] Message sent to {message.receiverID}'
        print(f'{messageHeader: <90}: {message.text: <20}') # Log the event


    def start(self):
        print(f'{Colors.BLUE}Agent {self.ID} is starting...{Colors.ENDC}') # Log the event
        self.loopThread = threading.Thread(target=self.messageCheckLoop)
        self.loopThread.start()
        for behaviour in self.behaviours:
            behaviour.start()


    def stop(self):
        print(f'{Colors.BLUE}Agent {self.ID} is stopping...{Colors.ENDC}') # Log the event
        self.stopFlag = True
        self.loopThread.join()
        for behaviour in self.behaviours:
            behaviour.stop()


if __name__ == "__main__":
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

    # Run for 20 seconds (comment out the sleep line to run indefinitely)
    agentA.start()
    agentB.start()
    time.sleep(20)
    agentA.stop()
    agentB.stop()