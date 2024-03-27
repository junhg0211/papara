class Location:
    def __init__(self, filename: str, source: str, start: int, end: int) -> None:
        self.filename = filename
        self.source = source
        self.start = start
        self.end = end
