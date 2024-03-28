import regex

from error.compile import CompileError, CompileErrorCode, Label
from location import Location
from compiler.token import TT, Token

DIGIT_RE = r"[0-9]"
ID_START_RE = r"[\p{XID_Start}\p{Extended_Pictographic}\p{Emoji_Component}]"
ID_CONTINUE_RE = r"[\p{XID_Continue}\p{Extended_Pictographic}\p{Emoji_Component}]"

KEYWORDS = {
    "더하기": TT.ADD,
    "빼기": TT.SUB,
    "곱하기": TT.MULT,
    "나누기": TT.DIV,
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
        self.tokens = list[Token]()
        self.errors = list[CompileError]()

    def tokenize(self) -> tuple[list[Token], list[CompileError]]:
        while not self.is_at_end():
            self.location.start = self.location.end

            c = self.advance()
            match c:
                case "(":
                    self.add_token(TT.LPAREN)
                case ")":
                    self.add_token(TT.RPAREN)
                case ".":
                    self.add_token(TT.DOT)
                case ",":
                    self.add_token(TT.COMMA)
                case "/":
                    self.add_token(TT.SLASH)
                case "+":
                    self.add_token(TT.PLUS)
                case "-":
                    self.add_token(TT.MINUS)

                case " " | "\t" | "\r" | "\n":
                    pass

                # case "(":
                #     self.comment()

                case '"':
                    self.string()

                case _:
                    if self.is_digit(c):
                        self.number()
                    elif self.is_id_start(c):
                        self.identifier()
                    else:
                        self.add_error(
                            CompileError(
                                CompileErrorCode.UNEXPECTED_CHAR, [Label(self.location)]
                            )
                        )

        self.tokens.append(Token(TT.EOF, "", self.location))
        return (self.tokens, self.errors)

    def identifier(self):
        while self.is_id_continue(self.peek()):
            self.advance()

        text = self.location.source[self.location.start : self.location.end]
        tokentype = KEYWORDS.get(text)
        if tokentype is None:
            tokentype = TT.IDENTIFIER
        self.add_token(tokentype)

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
                CompileError(
                    CompileErrorCode.UNTERMINATED_COMMENT, [Label(self.location)]
                )
            )

        self.advance()

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            char = self.advance()

            if char == "\\":
                self.advance()

        if self.is_at_end():
            return self.add_error(
                CompileError(
                    CompileErrorCode.UNTERMINATED_STRING, [Label(self.location)]
                )
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

    def add_token(self, tokentype: str):
        lexeme = self.location.source[self.location.start : self.location.end]
        self.tokens.append(Token(tokentype, lexeme, self.location))

    def add_error(self, error: CompileError):
        self.errors.append(error)
        print(error.code, error.labels[0].location.start, error.labels[0].location.end)

    def is_at_end(self) -> bool:
        return self.location.end >= len(self.location.source)
