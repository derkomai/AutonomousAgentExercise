import threading


class Interface:
    """Implements a communication interface. Messages are stored inside a dict
       where each key is a receiver ID paired with its incoming messages. A lock
       is used to handle concurrency from multiple agents."""

    def __init__(self):
        self.messages = {}
        self.lock = threading.Lock()

    def receiveMessages(self, receiverID):
        messages = []
        with self.lock:
            if receiverID in self.messages:
                messages = self.messages[receiverID]
                del self.messages[receiverID]
        return messages

    def sendMessage(self, message):
        with self.lock:
            if message.receiverID in self.messages:
                self.messages[message.receiverID].append(message)
            else:
                self.messages[message.receiverID] = [message]