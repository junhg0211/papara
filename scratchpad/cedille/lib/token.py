from .location import *


class TT:
    DOT = "`.`"
    COMMA = "`,`"
    SLASH = "`/`"
    LPAREN = "`(`"
    RPAREN = "`)`"

    ADD = "`더하기`"
    SUB = "`빼기`"
    MULT = "`곱하기`"
    DIV = "`나누기`"

    IDENTIFIER = "식별자"
    NUMBER = "숫자"
    STRING = "문자열"

    IF = "`만약`"
    THEN = "`이면`"
    WHILE = "`동안`"
    FOR = "`하여`"
    END = "`하기`"

    TAKE = "`받고`"

    EOF = "파일의 끝"


class Token:
    def __init__(self, type: TT, lexeme: str, location: Location) -> None:
        self.type = type
        self.lexeme = lexeme
        self.location = location

    def __repr__(self) -> str:
        return f"{self.type}: '{self.lexeme}'"
