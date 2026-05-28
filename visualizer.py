import numpy as np
import matplotlib.pyplot as plt
from function_parser import FunctionParser


class Visualizer:
    '''Строит трёхмерный график первообразной'''
    def __init__(self):
        '''Инициализирует визуализатор, создаёт экземпляр FunctionParser'''
        self.parser = FunctionParser()

    def plot_antiderivative(self, expr: str) -> None:
        '''Строит 3D-график функции на отрезке [-20, 20] с 2000 точками.
         Отображает окно matplotlib с подписями осей и заголовком.'''

        expr = self.parser.to_evaluable(expr)

        x = np.linspace(-20, 20, 2000)

        try:
            y = eval(expr)
            z = np.zeros_like(x)

            fig, ax = plt.subplots(figsize=(10, 10))

            ax = fig.add_subplot(111, projection='3d')

            ax.plot(x, y, z, linewidth=2)

            ax.set_xlim(-20, 20)
            ax.set_ylim(-20, 20)
            ax.set_zlim(-20, 20)

            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')

            ax.set_aspect('equal')

            ax.grid(True)

            plt.title("График первообразной", fontsize=18)

            plt.show()

        except SyntaxError:
            print("Ошибка синтаксиса при построении графика")

        except NameError:
            print("Ошибка имени переменной при построении графика")

        except ValueError:
            print("Ошибка значения при построении графика")