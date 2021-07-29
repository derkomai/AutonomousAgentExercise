from abc import ABC, abstractmethod
import threading
import time


class Behaviour(ABC):
    """Class representing a general behaviour"""

    def __init__(self, activationFunction):
        self.activationFunction = activationFunction


    @abstractmethod
    def setCondition(self):
        pass


    @abstractmethod
    def start(self):
        pass


    @abstractmethod
    def stop(self):
        pass


class TimedBehaviour(Behaviour):
    """Implements a timed behaviour that repeats every n seconds"""

    def __init__(self, activationFunction, sleepTime):
        self.activationFunction = activationFunction
        self.sleepTime = sleepTime


    def setCondition(self):
        pass


    def start(self):
        self.stopFlag = False
        self.conditionCheckThread = threading.Thread(target=self.run)
        self.conditionCheckThread.start()


    def stop(self):
        self.stopFlag = True
        self.conditionCheckThread.join()


    def run(self):
        while not self.stopFlag:
            self.activationFunction()
            time.sleep(self.sleepTime)