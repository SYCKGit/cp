class MoreThanOneE(SyntaxError):
    def __init__(self):
        super().__init__("There is more than one e")

class UnknownStatement(SyntaxError):
    def __init__(self):
        super().__init__("Unknown Statement")

class UnknownIdentifier(Exception):
    def __init__(self, identifer: str):
        self.identifier = identifer
        super().__init__(f"Unknown Identifier: {identifer}")