from .location import *


class ErrorCode:
    """
    E0XXX: 문법 오류
    E1XXX~E9XXX: 컴파일 오류
    """

    UnexpectedChar = "E0001"
    UnterminatedComment = "E0002"
    UnterminatedString = "E0003"


class Label:
    def __init__(self, location: Location, message: str = "") -> None:
        self.location = location
        self.message = message


class Error:
    def __init__(
        self,
        code: ErrorCode,
        labels: list[Label],
        note: str = "",
        help: str = "",
    ) -> None:
        """
        code: 오류 코드
        labels: 라벨(코드 밑에 ^^^부분) 리스트.
        note: 참고 설명
        help: 도움말
        """
        self.code = code
        self.labels = labels
        self.note = note
        self.help = help
