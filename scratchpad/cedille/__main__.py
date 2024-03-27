from tokenizer import *

if __name__ == "__main__":
    tokenizer = Tokenizer(
        "test.ppr",
        """.,
        12 12.123
        (asdf)
        "asdfasdf"
        "asdf\\"asdf\\t\\a\sd\f\\"\\'"
        asdfkjdfsl
        가나다라
        sdf가나 dsfl다か 아😊a 😩aaa
        만약 이면 동안 하여 하기 하여여여 만약약 만약이면 a하기
        더하기 빼기 곱하기 나누기
        1asdf
        .1 1. 1.1.1
        """,
    )
    print(tokenizer.tokenize())
