from integration import Integration
import math

class DefiniteIntegralCalculator(Integration):
    '''Вычисляет определённый интеграл методом трапеций'''
    def __init__(self, expr: str, lower_limit: float, upper_limit: float, intervals_count: int = 1000):
        '''Инициализирует калькулятор определённого интеграла'''
        self.expr = expr
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.intervals_count = intervals_count

    def f(self, x: float) -> float:
        '''Вычисляет значение подынтегральной функции в точке x'''
        return eval(self.expr, {"x": x})

    def calculate(self) -> tuple[float | None, str]:
        '''Вычисляет определённый интеграл методом трапеций'''
        try:
            step_size = (self.upper_limit - self.lower_limit) / self.intervals_count
            result = 0.5 * (self.f(self.lower_limit) + self.f(self.upper_limit))
            for i in range(1, self.intervals_count):
                x = self.lower_limit + i * step_size
                try:
                    val = self.f(x)
                except ZeroDivisionError:
                    return None, f"Ошибка: функция не определена в точке x = {x}"
                if not math.isfinite(val):
                    return None, f"Ошибка: функция не определена в точке x = {x}"
                result += val
            return result * step_size, ""
        except ZeroDivisionError:
            return None, f"Ошибка: функция не определена в точке x = {self.lower_limit}"
        except Exception:
            return None, "Ошибка вычисления"