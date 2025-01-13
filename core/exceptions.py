class NullException(Exception):
    def __init__(self, value):
        super().__init__(f"값 '{value}'가 누락되었습니다.")
        self.value = value

    def __str__(self):
        return f"NullException: 값 '{self.value}'가 누락되었습니다."