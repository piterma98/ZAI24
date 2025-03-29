class PhonebookError(Exception):
    def __init__(self, reason: str):
        super().__init__()
        self.reason = reason
