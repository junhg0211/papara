import re


class Mode:
    NONE = 0
    STRING = 1
    NUMBER = 2


def tokenize(source: str) -> list[str]:
    tokens = list()

    buffer = list()

    mode = Mode.NONE
    string_escape = False

    for letter in source:
        match mode:
            case Mode.NONE:
                if letter not in [' ', '\n']:
                    buffer.append(letter)

                if letter == '"':
                    mode = Mode.STRING
                    continue

                if letter in '0123456789-':
                    mode = Mode.NUMBER
                    continue

                if letter in [' ', '\n']:
                    if buffer:
                        tokens.append(''.join(buffer))
                    buffer.clear()
                    continue

                if letter in '.':
                    buffer.pop()
                    if buffer:
                        tokens.append(''.join(buffer))
                    tokens.append('.')
                    buffer.clear()
                    continue

            case Mode.STRING:
                buffer.append(letter)

                if string_escape:
                    string_escape = False
                    continue

                if letter == '\\':
                    string_escape = True
                    continue

                if letter == '\"':
                    tokens.append(''.join(buffer))
                    buffer.clear()
                    mode = Mode.NONE
                    continue
            
            case Mode.NUMBER:
                if letter != ' ':
                    buffer.append(letter)

                if letter == ' ':
                    tokens.append(''.join(buffer))
                    buffer.clear()
                    mode = Mode.NONE
                    continue

    return tokens


class Lexicon:
    LITERAL = 100
    LITERAL_STRING = 101
    LITERAL_FLOAT = 102
    LITERAL_INTEGER = 103
    ID = 200
    PUNCTUATION = 300
    PUNCTUATION_DOT = 301
    PUNCTUATION_COMMA = 302
    PUNCTUATION_PARENTHESIS = 303
    KEYWORD = 400
    KEYWORD_IF = 401
    KEYWORD_THEN = 402
    KEYWORD_IN = 403
    KEYWORD_WHILE = 404
    KEYWORD_EACH = 405
    KEYWORD_HAYEO = 406
    KEYWORD_BREAK = 407
    KEYWORD_CONTINUE = 408
    KEYWORD_END = 409
    KEYWORD_DOING = 410
    KEYWORD_RECEIVING = 411
    KEYWORD_OF = 412
    KEYWORD_BEING = 413
    KEYWORD_FUNCTION = 471
    KEYWORD_STRUCT = 472
    OPERATION_PLUS = 501
    OPERATION_MINUS = 502
    OPERATION_TIMES = 503
    OPERATION_OVER = 504
    OPERATION_MODULO = 505

lexicon_mapping = {
    Lexicon.LITERAL_STRING: re.compile(rf'\".*\"'),
    Lexicon.LITERAL_FLOAT: re.compile(rf'-?[0-9]+\.[0-9]+'),
    Lexicon.LITERAL_INTEGER: re.compile(rf'-?[0-9]+'),
    Lexicon.PUNCTUATION_DOT: re.compile(rf'\.'),
    Lexicon.PUNCTUATION_COMMA: re.compile(rf','),
    Lexicon.PUNCTUATION_PARENTHESIS: re.compile(rf'\(|\)'),
    Lexicon.KEYWORD_IF: re.compile(rf'만약'),
    Lexicon.KEYWORD_THEN: re.compile(rf'이면'),
    Lexicon.KEYWORD_IN: re.compile(rf'인'),
    Lexicon.KEYWORD_WHILE: re.compile(rf'동안'),
    Lexicon.KEYWORD_EACH: re.compile(rf'각'),
    Lexicon.KEYWORD_HAYEO: re.compile(rf'하여'),
    Lexicon.KEYWORD_BREAK: re.compile(rf'그만하기'),
    Lexicon.KEYWORD_CONTINUE: re.compile(rf'넘어가기'),
    Lexicon.KEYWORD_END: re.compile(rf'하기'),
    Lexicon.KEYWORD_DOING: re.compile(rf'하는'),
    Lexicon.KEYWORD_RECEIVING: re.compile(rf'받고'),
    Lexicon.KEYWORD_OF: re.compile(rf'의'),
    Lexicon.KEYWORD_BEING: re.compile(rf'인'),
    Lexicon.KEYWORD_FUNCTION: re.compile(rf'함수'),
    Lexicon.KEYWORD_STRUCT: re.compile(rf'묶음'),
    Lexicon.OPERATION_PLUS: re.compile(rf'더하기'),
    Lexicon.OPERATION_MINUS: re.compile(rf'빼기'),
    Lexicon.OPERATION_TIMES: re.compile(rf'곱하기'),
    Lexicon.OPERATION_OVER: re.compile(rf'나누기'),
    Lexicon.OPERATION_MODULO: re.compile(rf'나머지'),
}


def lexify(tokens: list):
    lexicons = list()

    for token in tokens:
        good = False
        for key, value in lexicon_mapping.items():
            if value.match(token) is not None:
                lexicons.append((key, token))
                good = True
                break

        if not good:
            lexicons.append((Lexicon.ID, token))

    return lexicons


def parse_sentences(lexicons):
    sentences = list()
    for lexicon in lexicons:
        pass


if __name__ == '__main__':
    from sys import argv
    with open(argv[1], 'r', encoding='utf-8') as file:
        content = file.read()
    print(content)
    print()
    print(tokens := tokenize(content))
    print()
    print(lexicons := lexify(tokens))