from abc import ABC, abstractmethod

class Cancelable(ABC):
    @abstractmethod
    def cancelar(self):
        pass

    @abstractmethod
    def es_cancelable(self):
        pass