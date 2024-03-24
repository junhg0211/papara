import re

from .location import Location
from .token import TT, Token

ID_RE = re.compile(r"[ㄱ-ㅎㅏ-ㅣ가-힣a-zA-Z]")
IDNUM_RE = re.compile(r"[ㄱ-ㅎㅏ-ㅣ가-힣a-zA-Z0-9]")

class Tokenizer:
    @staticmethod
    def from_file(filename: str) -> 'Tokenizer':
        """
        파일 이름을 받아서, 파일의 내용을 읽어 토크나이저를 생성해 반환한다.
        """
        with open(filename, 'r', encoding='utf-8') as file:
            return Tokenizer(filename, file.read())

    def __init__(self, filename: str, source: str):
        """
        filename: 파일 이름
        source: 토큰화할 코드
        """

        self.filename = filename
        self.source = source
        self.location = Location(self.filename, self.source, 0, 0)
        self.tokens = []
            
    def tokenize(self):
        while True:
            if self.is_at_end():
                break

            char = self.source[self.location.end]
            
            match char:
                case ' ' | '\r' | '\t' | '\n': self.advance()

                case '.': self.add_token(TT.DOT)
                case ',': self.add_token(TT.COMMA)
                
                case _:
                    if ID_RE.match(char) is not None:
                        while True:
                            self.advance()
                            if self.is_at_end():
                                break

                            char = self.source[self.location.end]

                            if IDNUM_RE.match(char) is None:
                                self.add_token(TT.IDENTIFIER)
                    else:
                        print("err")
                        break

        return self.tokens

    def add_token(self, type: TT):
        self.advance()
        self.tokens.append(Token(type, self.source[self.location.start:self.location.end], self.location))
        self.location.start = self.location.end

    def advance(self):
        self.location.end += 1

    def is_at_end(self):
        return self.location.end == len(self.source)


if __name__ == '__main__':
    from sys import argv
    source = """
    가나다라
    .,아. 아 아 ㄱㄴㄷ ㅏㅣ
    가.가
    """
    tokenizer = Tokenizer("test.ppr", source)
    print(tokenizer.tokenize())