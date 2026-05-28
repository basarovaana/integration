from integration import Integration
import re
from fractions import Fraction


class IndefiniteIntegralCalculator(Integration):
    '''Вычисляет неопределённый интеграл рациональной функции аналитически'''
    def __init__(self, expr: str) -> None:
        '''Инициализирует калькулятор. Удаляет пробелы и заменяет ^ на **'''
        self.expr = expr.replace(" ", "").replace("^", "**")

    def format_term(self, coef, power: int) -> str:
        '''Форматирует один член многочлена в строку для вывода'''
        coef = Fraction(coef).limit_denominator(10 ** 9)
        if coef == 0:
            return ""
        if isinstance(coef, Fraction):
            if coef.denominator == 1:
                coef_str = str(coef.numerator)
            else:
                coef_str = f"{coef.numerator}/{coef.denominator}"
        else:
            coef_str = str(coef)

        if coef_str == "1":
            coef_str = ""
        elif coef_str == "-1":
            coef_str = "-"

        if power == 0:
            if coef_str == "":
                return "1"
            elif coef_str == "-":
                return "-1"
            else:
                return coef_str

        if power == 1:
            return f"{coef_str}x"
        return f"{coef_str}x^{power}"

    def _apply_power_rule(self, a, n: int) -> str:
        '''Применяет правило интегрирования степенной функции: ∫a·x^ndx = a/(n+1)·x^(n+1).
        При n = -1 возвращает логарифм.'''
        a = Fraction(a).limit_denominator(10 ** 9)
        if a == 0:
            return "0"
        if n == -1:
            if a == 1:
                prefix = ""
            elif a == -1:
                prefix = "-"
            else:
                prefix = str(a)
            return f"{prefix}ln|x|"
        new_n = n + 1
        return self.format_term(Fraction(a, new_n), new_n)

    def integrate_term(self, term: str) -> str | None:
        '''Интегрирует один член выражения: a/(x+b), a/x**n, a*x**n, число.'''
        term = term.strip()
        if not term: return None

        log_match = re.fullmatch(r'([\-+]?\d*\.?\d*)/\(x([\-+]\d+)\)', term)# a/(x+b)
        if log_match:
            raw_a, b = log_match.groups()

            if raw_a == '' or raw_a == '+':
                a = 1
            elif raw_a == '-':
                a = -1
            else:
                a = Fraction(raw_a).limit_denominator(10**9)

            if a == 1:
                prefix = ''
            elif a == -1:
                prefix = '-'
            else:
                prefix = str(a)
            return f"{prefix}ln|x{b}|"

        div_match = re.fullmatch(r'([\-+]?\d*\.?\d+)/x(\*\*(\d+))?', term)# a/x**n
        if div_match:
            a = float(div_match.group(1))
            n = -int(div_match.group(3)) if div_match.group(3) else -1
            return self._apply_power_rule(a, n)

        pow_match = re.fullmatch(r'([\-+]?\d*\.?\d*)\*?x(\*\*(\-?\d+))?', term)# a*x**n
        if pow_match:
            raw_a = pow_match.group(1)
            if raw_a == '' or raw_a == '+':
                a = 1
            elif raw_a == '-':
                a = -1
            else:
                a = float(raw_a)

            n = int(pow_match.group(3)) if pow_match.group(3) else 1
            return self._apply_power_rule(a, n)

        if re.fullmatch(r'[\-+]?\d*\.?\d+', term):# число
            coef = Fraction(term).limit_denominator(10 ** 9)
            return self.format_term(coef, 1)

        return None

    def _split_rational(self, expr: str) -> list[str] | None:
        '''Разбивает выражение вида (многочлен)/x**n на список отдельных членов после деления'''
        match = re.match(r'\((.*)\)/(x(\*\*(\d+))?)', expr) #(что-то)/x**n
        if match:
            num_content, den_str, _, m_str = match.groups()
            m = int(m_str) if m_str else 1
            sub_terms = re.findall(r'[+\-]?[^+\-]+', num_content)
            final_terms = []
            for st in sub_terms:
                p_match = re.search(r'x(\*\*(\d+))?', st)

                if p_match:
                    if p_match.group(2):
                        n = int(p_match.group(2))
                    else:
                        n = 1
                else:
                    n = 0

                k_part = st.split('x')[0].replace('*', '')

                if k_part == '' or k_part == '+':
                    k = 1
                elif k_part == '-':
                    k = -1
                else:
                    k = float(k_part)

                new_pow = n - m
                if new_pow == 0:
                    final_terms.append(str(k))
                elif new_pow < 0:
                    final_terms.append(f"{k}/x**{abs(new_pow)}")
                else:
                    final_terms.append(f"{k}*x**{new_pow}")
            return final_terms
        return None

    def calculate(self) -> str | None:
        '''Основной метод. Разбирает выражение на члены, интегрирует каждый и собирает результат'''
        try:
            if '/' in self.expr:
                if re.fullmatch(r'[\-+]?\d*/\(x[\-+]\d+\)', self.expr):
                    return self.integrate_term(self.expr)

                rational = self._split_rational(self.expr)
                if rational:
                    results = [self.integrate_term(t) for t in rational]
                    return " + ".join(filter(None, results)).replace("+ -", "- ")

            terms = re.findall( r'[+\-]?(?:(?<!\*)\d*\.?\d+/x(?:\*\*\d+)?|x(?:\*\*-?\d+)?|(?<!\*)\d*\.?\d+)',
                               self.expr)
            if not terms:
                terms = [self.expr]

            results = []
            for t in terms:
                res = self.integrate_term(t)
                if res:
                    results.append(res)
                else:
                    return None

            return " + ".join(results).replace("+ -", "- ")
        except ValueError:
            return None

        except re.error:
            return None