class Error:
    def __init__(self, name, details):
        self.name = name
        self.details = details
    
    def __repr__(self):
        return f"{self.name}: {self.details}"


class IllegalCharError(Error):
    def __init__(self, details):
        super().__init__("IllegalCharError", details)

class UnexpectedCharError(Error):
    def __init__(self, details):
        super().__init__("UnexpectedCharError", details)

class InvalidSyntaxError(Error):
    def __init__(self, details):
        super().__init__("InvalidSyntaxeError", details)

class RuntimeError(Error):
    def __init__(self, details):
        super().__init__("RuntimeError", details)