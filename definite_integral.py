from integration import Integration
import math

class DefiniteIntegralCalculator(Integration):
    def __init__(self, expr, a, b, n=1000):
        self.expr = expr
        self.a = a
        self.b = b
        self.n = n

    def f(self, x):
        return eval(self.expr, {"x": x})

    def calculate(self):
        try:
            h = (self.b - self.a) / self.n
            s = 0.5 * (self.f(self.a) + self.f(self.b))
            for i in range(1, self.n):
                x = self.a + i * h
                try:
                    val = self.f(x)
                except ZeroDivisionError:
                    return None, f"Ошибка: функция не определена в точке x = {x}"
                if not math.isfinite(val):
                    return None, f"Ошибка: функция не определена в точке x = {x}"
                s += val
            return s * h, ""
        except ZeroDivisionError:
            return None, f"Ошибка: функция не определена в точке x = {self.a}"
        except Exception:
            return None, "Ошибка вычисления"