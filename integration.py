from abc import ABC, abstractmethod

class Integration(ABC):
    @abstractmethod
    def calculate(self):
        pass