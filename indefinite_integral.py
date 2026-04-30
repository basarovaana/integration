from integration import Integration
import re
from fractions import Fraction


class IndefiniteIntegralCalculator(Integration):
    def __init__(self, expr):
        self.expr = expr.replace(" ", "").replace("^", "**")

    def format_term(self, coef, power):
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

    def _apply_power_rule(self, a, n):
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

    def integrate_term(self, term):
        term = term.strip()
        if not term: return None

        log_match = re.fullmatch(r'([\-+]?\d*)/\(x([\-+]\d+)\)', term) # a/(x+b)
        if log_match:
            raw_a, b = log_match.groups()

            if raw_a == '' or raw_a == '+':
                a = 1
            elif raw_a == '-':
                a = -1
            else:
                a = int(raw_a)

            if a == 1:
                prefix = ''
            elif a == -1:
                prefix = '-'
            else:
                prefix = str(a)
            return f"{prefix}ln|x{b}|"

        div_match = re.fullmatch(r'([\-+]?\d+)/x(\*\*(\d+))?', term)# a/x**n
        if div_match:
            a = int(div_match.group(1))
            n = -int(div_match.group(3)) if div_match.group(3) else -1
            return self._apply_power_rule(a, n)

        pow_match = re.fullmatch(r'([\-+]?\d*)\*?x(\*\*(\-?\d+))?', term)# a*x**n
        if pow_match:
            raw_a = pow_match.group(1)
            if raw_a == '' or raw_a == '+':
                a = 1
            elif raw_a == '-':
                a = -1
            else:
                a = int(raw_a)

            n = int(pow_match.group(3)) if pow_match.group(3) else 1
            return self._apply_power_rule(a, n)

        if re.fullmatch(r'[\-+]?\d+', term):# число
            return self.format_term(int(term), 1)

        return None

    def _split_rational(self, expr):
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
                    k = int(k_part)

                new_pow = n - m
                if new_pow == 0:
                    final_terms.append(str(k))
                elif new_pow < 0:
                    final_terms.append(f"{k}/x**{abs(new_pow)}")
                else:
                    final_terms.append(f"{k}*x**{new_pow}")
            return final_terms
        return None

    def calculate(self):
        try:
            if '/' in self.expr:
                if re.fullmatch(r'[\-+]?\d*/\(x[\-+]\d+\)', self.expr):
                    return self.integrate_term(self.expr)

                rational = self._split_rational(self.expr)
                if rational:
                    results = [self.integrate_term(t) for t in rational]
                    return " + ".join(filter(None, results)).replace("+ -", "- ")

            terms = re.findall(r'[+\-]?(?:(?<!\*)\d+/x(?:\*\*\d+)?|x(?:\*\*-?\d+)?|(?<!\*)\d+)', self.expr)
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
        except Exception:
            return None