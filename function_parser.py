import re
import math

class FunctionParser:
    '''Преобразует пользовательский ввод в вычисляемое Python-выражение.'''
    def to_evaluable(self, expr: str) -> str:
        '''
        Нормализует математическое выражение: удаляет пробелы,
        заменяет кириллическую х на латинскую x, ^ на **, расставляет явные знаки умножения,
        вычисляет числовые функции (sin, cos, tan, log, sqrt) от числовых аргументов.
        '''
        expr = expr.replace(' ', '').lower()
        expr = expr.replace('х', 'x')
        expr = expr.replace('^', '**')
        expr = re.sub(r'(\d)(x)', r'\1*\2', expr)
        expr = re.sub(r'(x)(\d)', r'\1*\2', expr)
        expr = re.sub(r'(\))(\()', r'\1*\2', expr)
        expr = re.sub(r'(\d)(\()', r'\1*\2', expr)
        expr = re.sub(r'(\))(x)', r'\1*\2', expr)
        expr = re.sub(r'(\d\.\d+)(x)', r'\1*\2', expr)
        for func in ['sin', 'cos', 'tan', 'log', 'sqrt']:
            pattern = rf'{func}\(([^()]+)\)'

            matches = re.findall(pattern, expr)

            for m in matches:
                value = eval(f'math.{func}({m})')
                expr = expr.replace(f'{func}({m})', str(value))
        return expr