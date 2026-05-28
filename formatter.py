class Formatter:
    '''Форматирует результаты вычислений для вывода пользователю'''
    def format_indefinite(self, expr: str) -> str:
        '''Добавляет константу интегрирования + C к результату неопределённого интеграла'''
        return f"{expr} + C" if expr else "Ошибка расчета"

    def format_definite(self, value: float | None) -> str:
        '''Форматирует числовой результат определённого интеграла до трёх знаков после запятой'''
        return f"{value:.3f}" if value is not None else "Ошибка расчета"