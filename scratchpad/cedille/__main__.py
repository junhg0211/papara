from tokenizer import *

if __name__ == "__main__":
    tokenizer = Tokenizer(
        "test.ppr",
        """., ., ,,, ..12313....,.,...,,,,..
        ,.,.132132,,,,,,  ,.,....
        12.123
        "asdfasdf"
        (asdf)
        "asdf\\"asdf\\t\\a\sd\f\\"\\'"
        asdfkjdfsl
        가나다라
        sdf가낭ㄹ dsfl다か 아😊a 😩aaa
        만약 이면 동안 하여 하기 하여여여 만약약 만약이면 a하기
        1asdf
        .1
        1.
        1.1.1
        """,
    )
    print(tokenizer.tokenize())
