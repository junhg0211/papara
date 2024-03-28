from enum import Enum
from location import Location


class CompileErrorCode(Enum):
    """
    E0XXX: 문법 오류
    E1XXX~E9XXX: 컴파일 오류
    """

    UNEXPECTED_CHAR = "E0001"
    UNTERMINATED_COMMENT = "E0002"
    UNTERMINATED_STRING = "E0003"


class Label:
    def __init__(self, location: Location, message: str = "") -> None:
        self.location = location
        self.message = message


class CompileError:
    def __init__(
        self,
        code: CompileErrorCode,
        labels: list[Label],
        note: str = "",
        help_message: str = "",
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
        self.help_message = help_message
