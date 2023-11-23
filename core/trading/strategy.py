from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def signal(self):
        pass
