class Location:
    def __init__(self, filename: str, source: str, start: int, end: int) -> None:
        """
        filename: 파일 이름
        source: 코드
        start: 시작 부분 위치
        end: 끝 부분 위치
        """

        self.filename = filename
        self.source = source
        self.start = start
        self.end = end
