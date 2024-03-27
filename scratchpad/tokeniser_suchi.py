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
                if letter not in [" ", "\n"]:
                    buffer.append(letter)

                if letter == '"':
                    mode = Mode.STRING
                    continue

                if letter in "0123456789-":
                    mode = Mode.NUMBER
                    continue

                if letter in [" ", "\n"]:
                    if buffer:
                        tokens.append("".join(buffer))
                    buffer.clear()
                    continue

                if letter in ".,":
                    buffer.pop()
                    if buffer:
                        tokens.append("".join(buffer))
                    tokens.append(letter)
                    buffer.clear()
                    continue

            case Mode.STRING:
                buffer.append(letter)

                if string_escape:
                    string_escape = False
                    continue

                if letter == "\\":
                    string_escape = True
                    continue

                if letter == '"':
                    tokens.append("".join(buffer))
                    buffer.clear()
                    mode = Mode.NONE
                    continue

            case Mode.NUMBER:
                if letter == ",":
                    tokens.append("".join(buffer))
                    buffer.clear()
                    tokens.append(",")
                    mode = Mode.NONE
                    continue

                if letter != " ":
                    buffer.append(letter)

                if letter == " ":
                    tokens.append("".join(buffer))
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
    Lexicon.LITERAL_STRING: re.compile(rf"\".*\""),
    Lexicon.LITERAL_FLOAT: re.compile(rf"-?[0-9]+\.[0-9]+"),
    Lexicon.LITERAL_INTEGER: re.compile(rf"-?[0-9]+"),
    Lexicon.PUNCTUATION_DOT: re.compile(rf"\."),
    Lexicon.PUNCTUATION_COMMA: re.compile(rf","),
    Lexicon.PUNCTUATION_PARENTHESIS: re.compile(rf"\(|\)"),
    Lexicon.KEYWORD_IF: re.compile(rf"만약"),
    Lexicon.KEYWORD_THEN: re.compile(rf"이면"),
    Lexicon.KEYWORD_WHILE: re.compile(rf"동안"),
    Lexicon.KEYWORD_EACH: re.compile(rf"각"),
    Lexicon.KEYWORD_HAYEO: re.compile(rf"하여"),
    Lexicon.KEYWORD_BREAK: re.compile(rf"그만하기"),
    Lexicon.KEYWORD_CONTINUE: re.compile(rf"넘어가기"),
    Lexicon.KEYWORD_END: re.compile(rf"하기"),
    Lexicon.KEYWORD_DOING: re.compile(rf"하는"),
    Lexicon.KEYWORD_RECEIVING: re.compile(rf"받고"),
    Lexicon.KEYWORD_OF: re.compile(rf"의"),
    Lexicon.KEYWORD_BEING: re.compile(rf"인"),
    Lexicon.KEYWORD_FUNCTION: re.compile(rf"함수"),
    Lexicon.KEYWORD_STRUCT: re.compile(rf"묶음"),
    Lexicon.OPERATION_PLUS: re.compile(rf"더하기"),
    Lexicon.OPERATION_MINUS: re.compile(rf"빼기"),
    Lexicon.OPERATION_TIMES: re.compile(rf"곱하기"),
    Lexicon.OPERATION_OVER: re.compile(rf"나누기"),
    Lexicon.OPERATION_MODULO: re.compile(rf"나머지"),
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


OPENING_CODES = [
    Lexicon.KEYWORD_THEN,
    Lexicon.KEYWORD_WHILE,
    Lexicon.KEYWORD_HAYEO,
]
CLOSING_CODES = [
    Lexicon.KEYWORD_END,
]


class Papara:
    class SyntaxError(Exception):
        pass

    class NameError(Exception):
        pass

    class InvalidBlock(Exception):
        pass

    class ParseError(Exception):
        pass


def parse_sentences(lexicons):
    sentences = list()
    buffer = list()
    stacks = 0

    for code, content in lexicons:
        buffer.append((code, content))

        if code in CLOSING_CODES:
            stacks -= 1
            continue

        if code in OPENING_CODES:
            stacks += 1
            continue

        if code == Lexicon.PUNCTUATION_DOT:
            if stacks != 0:
                continue

            sentences.append(buffer)
            buffer = list()

    if stacks or buffer:
        raise Papara.SyntaxError("열린 블럭이 닫히지 않았습니다.")

    return sentences


JOSAS = {
    "를": ["을", "를"],
    "로": ["으로", "로"],
    "에": ["에"],
    "가": ["이", "가"],
    "와": ["와", "과"],
    "보다": ["보다"],
    "의": ["의"],
}

BUILTIN_FUNCTIONS = {
    "선언": [JOSAS["를"], JOSAS["로"]],
    "대입": [JOSAS["에"], JOSAS["로"]],
    "출력": [JOSAS["를"]],
    "같음": [JOSAS["가"], JOSAS["와"]],
    "작음": [JOSAS["가"], JOSAS["보다"]],
    "묶음": [JOSAS["의"]],
}


class BlockType:
    NONE = 0
    IF = 1
    WHILE = 2
    EACH = 3
    FUNCTION = 4
    SENTENCE = 10
    LITERAL = 20
    NAME = 21
    MULTIPLE = 22
    COMPLEX = 23


def parse_if(lexicons):
    # -- parse condition
    condition = list()
    lexicons.pop(0)
    while lexicons:
        left = lexicons.pop(0)

        if left[0] == Lexicon.KEYWORD_THEN:
            break

        condition.append(left)
    condition = parse(condition)

    # -- parse sentences
    raw_sentences = parse_sentences(lexicons[:-2])
    sentences = list()
    for raw_sentence in raw_sentences:
        sentences.append(parse(raw_sentence))

    return {
        "type": BlockType.IF,
        "condition": condition,
        "sentences": sentences,
    }


def parse_while(lexicons):
    # -- parse condition
    condition = list()
    while lexicons:
        left = lexicons.pop(0)

        if left[0] == Lexicon.KEYWORD_BEING:
            lexicons.pop(0)
            break

        condition.append(left)
    condition = parse(condition)

    # -- parse sentences
    raw_sentences = parse_sentences(lexicons[:-2])
    sentences = list()
    for raw_sentence in raw_sentences:
        sentences.append(parse(raw_sentence))

    return {
        "type": BlockType.WHILE,
        "condition": condition,
        "sentences": sentences,
    }


def parse_each(lexicons):
    # TODO
    return {
        "type": BlockType.EACH,
        "lexicons": lexicons,
    }


def parse_function(lexicons):
    # TODO
    return {
        "type": BlockType.FUNCTION,
        "lexicons": lexicons,
    }


def parse_int(raw):
    letters = list(raw)

    negative = False
    if letters[0] == "-":
        negative = True
        letters.pop(0)

    result = 0
    for letter in letters:
        result *= 10
        result += ord(letter) - ord("0")

    if negative:
        result *= -1

    return result


def parse_float(raw):
    letters = list(raw)

    negative = False
    if letters[0] == "-":
        negative = True
        letters.pop(0)

    dot_index = letters.index(".")

    result = 0.0
    weight = 10.0 ** (dot_index - 1)
    for i in range(len(letters)):
        if letters[i] == ".":
            continue

        result += weight * parse_int(letters[i])
        weight /= 10.0

    if negative:
        result *= -1

    return result


def get_precision(operator):
    if operator[0] in [
        Lexicon.OPERATION_TIMES,
        Lexicon.OPERATION_OVER,
        Lexicon.OPERATION_MODULO,
    ]:
        return 2

    if operator[0] in [Lexicon.OPERATION_PLUS, Lexicon.OPERATION_MINUS]:
        return 1

    return 0


def parse_value(lexicons):
    if isinstance(lexicons, dict):
        return lexicons
    if isinstance(lexicons, tuple):
        return parse_value([lexicons])

    if not lexicons:
        return {}

    if len(lexicons) == 1:
        lexicon = lexicons[0]
        if lexicon[0] == Lexicon.LITERAL_INTEGER:
            return {
                "type": BlockType.LITERAL,
                "class": lexicon[0],
                "value": parse_int(lexicon[1]),
            }

        if lexicon[0] == Lexicon.LITERAL_FLOAT:
            return {
                "type": BlockType.LITERAL,
                "class": lexicon[0],
                "value": parse_float(lexicon[1]),
            }

        if lexicon[0] == Lexicon.LITERAL_STRING:
            return {
                "type": BlockType.LITERAL,
                "class": lexicon[0],
                "value": lexicon[1],
            }

        return {
            "type": BlockType.NAME,
            "name": lexicon[1],
        }

    # if value is special case that made with OF or BEING
    if lexicons[-2][0] in [Lexicon.KEYWORD_OF, Lexicon.KEYWORD_BEING]:
        class_ = lexicons.pop()[1]
        lexicons.pop()
        return {
            "type": BlockType.COMPLEX,
            "class": class_,
            "content": parse(lexicons, True),
        }

    value_stack = list()
    operator_stack = list()
    for lexicon in lexicons:
        precision = get_precision(lexicon)

        if precision == 0:
            value_stack.append(lexicon)
            continue

        if not operator_stack:
            operator_stack.append(lexicon)
            continue

        that_precision = get_precision(operator_stack[-1])
        if that_precision > precision:
            while operator_stack:
                new_precision = get_precision(operator_stack[-1])
                if new_precision != that_precision:
                    break

                a = parse_value(value_stack.pop())
                b = parse_value(value_stack.pop())
                operator = operator_stack.pop()[0]
                value_stack.append({"operator": operator, "a": a, "b": b})

        operator_stack.append(lexicon)

    while len(value_stack) > 1:
        a = parse_value(value_stack.pop())
        b = parse_value(value_stack.pop())
        operator = operator_stack.pop()[0]
        value_stack.append({"operator": operator, "a": a, "b": b})

    return value_stack[0]


def parse(lexicons, enable_multiple=False):
    # -- sentence with nothing
    if len(lexicons) < 2:
        return parse_value(lexicons)

    # -- sentence with block
    if lexicons[-2][0] == Lexicon.KEYWORD_END:
        # check block type
        block_type = BlockType.NONE
        for lexicon in lexicons:
            if lexicon[0] == Lexicon.KEYWORD_IF:
                block_type = BlockType.IF
                break
            if lexicon[0] == Lexicon.KEYWORD_WHILE:
                block_type = BlockType.WHILE
                break
            if lexicon[0] == Lexicon.KEYWORD_EACH:
                block_type = BlockType.EACH
                break
            if lexicon[0] == Lexicon.KEYWORD_FUNCTION:
                block_type = BlockType.FUNCTION
                break
        if block_type == BlockType.NONE:
            raise Papara.InvalidBlock("블럭이 올바르지 않습니다.")

        # parse according to block type
        if block_type == BlockType.IF:
            return parse_if(lexicons)
        if block_type == BlockType.WHILE:
            return parse_while(lexicons)
        if block_type == BlockType.EACH:
            return parse_each(lexicons)
        if block_type == BlockType.FUNCTION:
            return parse_function(lexicons)

    # -- multiple sentence connected with ','
    if enable_multiple and any(
        map(lambda x: x[0] == Lexicon.PUNCTUATION_COMMA, lexicons)
    ):
        sentences = list()
        buffer = list()
        for lexicon in lexicons:
            if lexicon[0] == Lexicon.PUNCTUATION_COMMA:
                sentences.append(buffer)
                buffer = list()
                continue
            buffer.append(lexicon)
        if buffer:
            sentences.append(buffer)

        return {
            "type": BlockType.MULTIPLE,
            "content": sentences,
        }

    # -- single sentence
    # get action name
    if lexicons[-1][0] == Lexicon.PUNCTUATION_DOT:
        lexicons.pop()
    action = lexicons.pop()[1]

    # get available josa list
    josas = list()
    if action in BUILTIN_FUNCTIONS:
        josas = BUILTIN_FUNCTIONS[action]
    else:
        raise Papara.NameError(
            f"서술어가 발견되지 않습니다. 서술어는 '{action}'입니다.",
        )

    # parse josa tree
    now_josa = None
    previous_josa = None
    value = list()
    tree = dict()
    while lexicons:
        # pop now lexicon
        lexicon = lexicons.pop()
        this = lexicon[1]

        # check if now's josa
        is_josa = False
        for josa in josas:
            if this not in josa:
                continue

            now_josa = josa[0]
            is_josa = True
            break

        # push to tree
        if is_josa:
            tree[previous_josa] = parse_value(value[::-1])
            value = list()
        else:
            value.append(lexicon)

        previous_josa = now_josa
    tree[now_josa] = parse_value(value[::-1])
    if not tree[None]:
        del tree[None]

    return {
        "action": action,
        "tree": tree,
        "type": BlockType.SENTENCE,
    }


if __name__ == "__main__":
    from sys import argv
    from pprint import pprint

    with open(argv[1], "r", encoding="utf-8") as file:
        content = file.read()
    tokens = tokenize(content)
    lexicons = lexify(tokens)
    raw_sentences = parse_sentences(lexicons)

    for raw_sentence in raw_sentences:
        pprint(parse(raw_sentence))
