class Formatter:
    def format_indefinite(self, expr):
        return f"{expr} + C" if expr else "Ошибка расчета"

    def format_definite(self, value):
        return f"{value:.3f}" if value is not None else "Ошибка расчета"