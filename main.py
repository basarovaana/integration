from indefinite_integral import IndefiniteIntegralCalculator
from definite_integral import DefiniteIntegralCalculator
from formatter import Formatter
from validator import Validator
from function_parser import FunctionParser
from visualizer import Visualizer


def main():
    fmt = Formatter()
    val = Validator()
    parser = FunctionParser()
    vis = Visualizer()

    while True:
        print("1. Неопределенный интеграл")
        print("2. Определенный интеграл")
        print("3. Построить график первообразной")
        print("0. Выход")

        mode = input("Ваш выбор: ")

        if mode == '0':
            break

        if mode not in ['1', '2', '3']:
            print("Ошибка выбора\n")
            continue

        while True:
            expr = input("Введите функцию f(x): ")
            valid, msg = val.validate_function(expr)

            if not valid:
                print(msg)
                continue

            break

        expr = parser.to_evaluable(expr)

        if mode == '1':
            calc = IndefiniteIntegralCalculator(expr)
            result = calc.calculate()

            if result is None:
                print("Для данной функции аналитическое решение недоступно")
            else:
                print("Результат:", fmt.format_indefinite(result))

        elif mode == '2':
            while True:
                a_str = input("Нижний предел: ")

                try:
                    a = float(a_str)
                except ValueError:
                    print("Ошибка: пределы интегрирования должны быть числами")
                    continue

                b_str = input("Верхний предел: ")

                try:
                    b = float(b_str)
                except ValueError:
                    print("Ошибка: пределы интегрирования должны быть числами")
                    continue

                if a >= b:
                    print("Ошибка: должно выполняться условие a < b")
                    continue

                n_str = input("Количество разбиений n: ")

                try:
                    if '.' in n_str:
                        raise ValueError
                    n = int(n_str)
                except ValueError:
                    print("Ошибка: количество разбиений n должно быть целым числом больше 0")
                    continue

                if n <= 0:
                    print("Ошибка: количество разбиений n должно быть целым числом больше 0")
                    continue

                break

            calc = DefiniteIntegralCalculator(expr, a, b, n)
            value, err = calc.calculate()

            if err:
                print(err)
                print("Измените пределы интегрирования или функцию и попробуйте снова.")
            else:
                print("Результат:", fmt.format_definite(value))

        elif mode == '3':
            calc = IndefiniteIntegralCalculator(expr)
            result = calc.calculate()

            if result is None:
                print("Невозможно построить график")
            else:
                print("Первообразная:", result)
                vis.plot_antiderivative(result)

        print()


if __name__ == "__main__":
    main()