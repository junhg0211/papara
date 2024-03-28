from pprint import pprint
from compiler.tokenizer import Tokenizer

if __name__ == "__main__":
    tokenizer = Tokenizer(
        "test.ppr",
        """
        -1 더하기 +2.5 를 출력하기
        """,
    )
    pprint(tokenizer.tokenize())
