import re

NAME_RE = rf'[ㄱ-ㅎㅏ-ㅣ가-힣a-zA-Z]+'
EXPRESSION_RE = rf'[0-9]+'
SUBSTITUTION_RE = rf'({NAME_RE}) [을를] ({EXPRESSION_RE}) 으?로 선언.'
SUBSTITUTION = re.compile(SUBSTITUTION_RE)


def main():
    message = '스치 를 123 으로 선언. 세디유 를 321 로 선언.'

    matches = SUBSTITUTION.findall(message)

    print(list(matches))


if __name__ == '__main__':
    main()