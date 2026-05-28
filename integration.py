from abc import ABC, abstractmethod

class Integration(ABC):
    '''Абстрактный базовый класс для всех калькуляторов интегралов'''
    @abstractmethod
    def calculate(self):
        '''Абстрактный метод. Должен быть реализован в каждом дочернем классе. Выполняет вычисление интеграла.'''
        pass