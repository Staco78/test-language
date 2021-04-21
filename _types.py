from error import RuntimeError

class Number:
    def __init__(self, value):
        self.value = float(value)
    
    def __repr__(self):
        return str(int(self.value) if self.value.is_integer() else self.value)

    def add(self, other):
        return Number(self.value + other.value), None

    def min(self, other):
        return Number(self.value - other.value), None

    def mul(self, other):
        return Number(self.value * other.value), None

    def divide(self, other):
        if other.value == 0:
            return None, RuntimeError("Division by zero")
        return Number(self.value / other.value), None

    def isTrue(self):
        return True if self.value > 0 else False


class undefined:
    def __repr__ (self):
        return "undefined"


class Boolean:
    def __init__(self, value):
        self.value = value.isTrue()

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