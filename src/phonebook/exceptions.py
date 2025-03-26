class PhonebookError(Exception):
    def __init__(self, reason: str, **kwargs):
        super().__init__(**kwargs)
        self.reason = reason
