from enum import Enum
from location import Location


class TT(Enum):
    LPAREN = "`(`"
    RPAREN = "`)`"
    DOT = "`.`"
    COMMA = "`,`"
    SLASH = "`/`"
    PLUS = "`+`"
    MINUS = "`-`"

    NUMBER = "숫자"
    STRING = "문자열"
    IDENTIFIER = "식별자"

    ADD = "`더하기`"
    SUB = "`빼기`"
    MULT = "`곱하기`"
    DIV = "`나누기`"

    IF = "`만약`"
    THEN = "`이면`"
    WHILE = "`동안`"
    FOR = "`하여`"
    END = "`하기`"
    TAKE = "`받고`"

    EOF = "파일의 끝"

    def __str__(self):
        return self.value


class Token:
    def __init__(self, tokentype: TT, lexeme: str, location: Location) -> None:
        self.tokentype = tokentype
        self.lexeme = lexeme
        self.location = location

    def __repr__(self) -> str:
        if f"`{self.lexeme}`" == self.tokentype.value or len(self.lexeme) == 0:
            return f"{self.tokentype}"

        return f"{self.tokentype}: '{self.lexeme}'"
