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

            fig, ax = plt.subplots(figsize=(10, 10))

            ax.plot(x, y, linewidth=2)

            ax.spines['left'].set_position('zero')
            ax.spines['bottom'].set_position('zero')

            ax.spines['right'].set_color('none')
            ax.spines['top'].set_color('none')

            ax.set_xlim(-20, 20)
            ax.set_ylim(-20, 20)

            ax.set_aspect('equal')

            ax.grid(True)

            plt.subplots_adjust(
                left=0.03,
                right=0.97,
                top=0.95,
                bottom=0.05
            )

            plt.title("График первообразной", fontsize=18)

            plt.show()

        except Exception as e:
            print("Ошибка при построении графика")
            print(e)