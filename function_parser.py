import re

class FunctionParser:
    def to_evaluable(self, expr):
        expr = expr.replace(' ', '').lower()
        expr = expr.replace('х', 'x')
        expr = expr.replace('^', '**')
        expr = re.sub(r'(\d)(x)', r'\1*\2', expr)
        expr = re.sub(r'(x)(\d)', r'\1*\2', expr)
        expr = re.sub(r'(\))(\()', r'\1*\2', expr)
        expr = re.sub(r'(\d)(\()', r'\1*\2', expr)
        expr = re.sub(r'(\))(x)', r'\1*\2', expr)
        return expr