from enum import Enum
from abc import ABC, abstractmethod
from Tools import Colors


class MessageType(Enum):
    DEFAULT = 1


class Message:
    """Implements a simple message"""
    def __init__(self, text, messageType, senderID, receiverID):
        self.text = text
        self.messageType = messageType
        self.senderID = senderID
        self.receiverID = receiverID


class MessageHandler(ABC):
    """Class representing a base message handler"""

    messageType = None

    def __init__(self):
        pass

    @abstractmethod
    def handle(self, message):
        pass


class DefaultMessageHandler(MessageHandler):
    """Implements the default message handler"""

    messageType = MessageType.DEFAULT

    def handle(self, message):
        if "hello" in message.text.lower():
            messageHeader = f'{Colors.ORANGE}[{"DefaultMessageHandler": >32}] HELLO MESSAGE DETECTED'
            print(f'{messageHeader: <95}: {message.text}{Colors.ENDC}')