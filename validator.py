import re

class Validator:
    def validate_function(self, expr):
        if not expr.strip():
            return False, "Ошибка: выражение функции не может быть пустым"

        if expr.count('(') != expr.count(')'):
            return False, "Ошибка синтаксиса"

        if re.search(r'(sin|cos|tan|log|sqrt)', expr.lower()):
            return False, "Ошибка: допускаются только рациональные функции"

        if re.search(r'[a-wy-zA-Z]', expr):
            return False, "Ошибка: функция должна зависеть только от переменной x"

        if re.search(r'\*\*\s*\d*\.\d+', expr):
            return False, "Ошибка: допускаются только рациональные функции"

        if re.search(r'[+\-]{2,}', expr.replace(' ', '')):
            return False, "Ошибка синтаксиса"

        if re.search(r'[^0-9xX+\-*/^(). ]', expr):
            return False, "Ошибка синтаксиса"

        return True, ""