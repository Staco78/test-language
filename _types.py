from error import RuntimeError

class Number:
    def __init__(self, value):
        self.value = float(value)
    
    def __repr__(self):
        return str(int(self.value) if self.value.is_integer() else self.value)

    def operator_PLUS(self, other):
        return Number(self.value + other.value), None

    def operator_MINUS(self, other):
        return Number(self.value - other.value), None

    def operator_MUL(self, other):
        return Number(self.value * other.value), None

    def operator_DIVIDE(self, other):
        if other.value == 0:
            return None, RuntimeError("Division by zero")
        return Number(self.value / other.value), None

    def operator_EE(self, other):
        return Boolean(self.value == other.value), None

    def operator_NE(self, other):
        return Boolean(self.value != other.value), None

    def operator_GT(self, other):
        return Boolean(self.value > other.value), None

    def operator_GTE(self, other):
        return Boolean(self.value >= other.value), None

    def operator_LT(self, other):
        return Boolean(self.value < other.value), None

    def operator_LTE(self, other):
        return Boolean(self.value <= other.value), None


    def isTrue(self):
        return True if self.value > 0 else False


class undefined:
    def __repr__ (self):
        return "undefined"


class Boolean:
    def __init__(self, value):
        try:
            self.value = value.isTrue()
        except AttributeError:
            self.value = value

    def isTrue(self):
        return self.value

    def __repr__(self):
        return "true" if self.value else "false"

class true:
    def isTrue(self):
        return True

class false:
    def isTrue(self):
        return False

true = true()
false = false()