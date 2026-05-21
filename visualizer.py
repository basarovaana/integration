import numpy as np
import matplotlib.pyplot as plt
from function_parser import FunctionParser


class Visualizer:

    def __init__(self):
        self.parser = FunctionParser()

    def plot_antiderivative(self, expr):

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