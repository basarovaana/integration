import re

class Validator:
    '''Проверяет корректность пользовательского ввода перед вычислением'''
    def validate_function(self, expr: str) -> tuple[bool, str]:
        '''
        Последовательно проверяет выражение по нескольким правилам: непустота,
        баланс скобок, отсутствие функций от x, отсутствие посторонних переменных,
        целочисленность степеней, отсутствие двойных операторов, допустимость символов.
        '''
        if not expr.strip():
            return False, "Ошибка: выражение функции не может быть пустым"

        if expr.count('(') != expr.count(')'):
            return False, "Ошибка синтаксиса"

        if re.search(r'(sin|cos|tan|log|sqrt)\s*\(\s*x', expr.lower()):
            return False, "Ошибка: допускаются только числовые функции в коэффициентах"

        if re.search(r'[a-wy-zA-Z]', re.sub(r'(sin|cos|tan|log|ln|sqrt)', '', expr.lower())):
            return False, "Ошибка: функция должна зависеть только от переменной x"

        if re.search(r'\*\*\s*\d*\.\d+', expr):
            return False, "Ошибка: допускаются только рациональные функции"

        if re.search(r'[+\-]{2,}', expr.replace(' ', '')):
            return False, "Ошибка синтаксиса"
        temp_expr = re.sub(r'(sin|cos|tan|log|sqrt)', '', expr.lower())

        if re.search(r'[^0-9xX+\-*/^(). ]', temp_expr):
            return False, "Ошибка синтаксиса"

        return True, ""