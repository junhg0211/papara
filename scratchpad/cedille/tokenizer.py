import regex

from lib.error import *
from lib.location import *
from lib.token import *

DIGIT_RE = r"[0-9]"
ID_START_RE = r"[\p{XID_Start}\p{Extended_Pictographic}\p{Emoji_Component}]"
ID_CONTINUE_RE = r"[\p{XID_Continue}\p{Extended_Pictographic}\p{Emoji_Component}]"

KEYWORDS = {
    "만약": TT.IF,
    "이면": TT.THEN,
    "동안": TT.WHILE,
    "하여": TT.FOR,
    "하기": TT.END,
    "받고": TT.TAKE,
}


class Tokenizer:
    def __init__(self, filename: str, source: str) -> None:
        self.location = Location(filename, source, 0, 0)
        self.tokens = list()
        self.errors = list()

    def tokenize(self) -> tuple[list[Token], list[Error]]:
        while not self.is_at_end():
            self.location.start = self.location.end

            c = self.advance()
            match c:
                case ".":
                    self.add_token(TT.DOT)
                case ",":
                    self.add_token(TT.COMMA)

                case " " | "\t" | "\r" | "\n":
                    pass

                case "(":
                    self.comment()

                case '"':
                    self.string()

                case _:
                    if self.is_digit(c):
                        self.number()
                    elif self.is_id_start(c):
                        self.identifier()
                    else:
                        self.add_error(
                            Error(ErrorCode.UnexpectedChar, [Label(self.location)])
                        )

        self.tokens.append(Token(TT.EOF, "", self.location))
        return (self.tokens, self.errors)

    def identifier(self):
        while self.is_id_continue(self.peek()):
            self.advance()

        text = self.location.source[self.location.start : self.location.end]
        type = KEYWORDS.get(text)
        if type is None:
            type = TT.IDENTIFIER
        self.add_token(type)

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        if self.peek() == "." and self.is_digit(self.peek_next()):
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()

        self.add_token(TT.NUMBER)

    def comment(self):
        while self.peek() != ")" and not self.is_at_end():
            self.advance()

        if self.is_at_end():
            return self.add_error(
                Error(ErrorCode.UnterminatedComment, [Label(self.location)])
            )

        self.advance()

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            char = self.advance()

            if char == "\\":
                self.advance()

        if self.is_at_end():
            return self.add_error(
                Error(ErrorCode.UnterminatedString, [Label(self.location)])
            )

        self.advance()
        self.add_token(TT.STRING)

    def advance(self) -> str:
        char = self.location.source[self.location.end]
        self.location.end += 1
        return char

    def matches(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.location.source[self.location.end] != expected:
            return False

        self.location.end += 1
        return True

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.location.source[self.location.end]

    def peek_next(self) -> str:
        if self.location.end + 1 >= len(self.location.source):
            return "\0"
        return self.location.source[self.location.end + 1]

    def is_id_start(self, char: str) -> bool:
        return regex.match(ID_START_RE, char) is not None

    def is_id_continue(self, char: str) -> bool:
        return regex.match(ID_CONTINUE_RE, char) is not None

    def is_digit(self, char: str) -> bool:
        return regex.match(DIGIT_RE, char) is not None

    def add_token(self, type: TT):
        lexeme = self.location.source[self.location.start : self.location.end]
        self.tokens.append(Token(type, lexeme, self.location))

    def add_error(self, error: Error):
        self.errors.append(error)
        print(error.code, error.labels[0].location.start, error.labels[0].location.end)

    def is_at_end(self) -> bool:
        return self.location.end >= len(self.location.source)
