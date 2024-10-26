class WrongStudyEntityKindError(BaseException):
    def __init__(self, message, code=None):
        super().__init__(message)  # Call the base class constructor
        self.code = code  # You can add any additional attributes

    def __str__(self):
        # Customize the string representation of the exception
        return f"{self.code}: {super().__str__()}" if self.code else super().__str__()

class StudyEntityNotFoundError(BaseException):
    def __init__(self, message, code=None):
        super().__init__(message)  # Call the base class constructor
        self.code = code  # You can add any additional attributes

    def __str__(self):
        # Customize the string representation of the exception
        return f"{self.code}: {super().__str__()}" if self.code else super().__str__()

class StudyEntityNotSelectedError(BaseException):
    def __init__(self, message, code=None):
        super().__init__(message)  # Call the base class constructor
        self.code = code  # You can add any additional attributes

    def __str__(self):
        # Customize the string representation of the exception
        return f"{self.code}: {super().__str__()}" if self.code else super().__str__()
