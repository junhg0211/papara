from .location import Location

class TT:
    DOT = "."
    COMMA = ","
    IDENTIFIER = "식별자"
    NUMBER = "숫자"
    STRING = "문자열"

class Token:
    def __init__(self, type: TT, lexeme: str, location: Location) -> None:
        self.type = type
        self.lexeme = lexeme
        self.location = location

    def __repr__(self) -> str:
        return f"{self.type}: {self.lexeme}"