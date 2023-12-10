from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def signal(self, indicators: dict):
        pass

    @abstractmethod
    def get_indicator(self, name: str):
        pass
