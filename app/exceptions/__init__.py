class WrongStudyEntityKindError(BaseException):
    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code  

    def __str__(self):
        return f"{self.code}: {super().__str__()}" if self.code else super().__str__()

class StudyEntityNotFoundError(BaseException):
    def __init__(self, message, code=None):
        super().__init__(message)  
        self.code = code 

    def __str__(self):
        return f"{self.code}: {super().__str__()}" if self.code else super().__str__()

class StudyEntityNotSelectedError(BaseException):
    def __init__(self, message, code=None):
        super().__init__(message)  
        self.code = code 

    def __str__(self):
        return f"{self.code}: {super().__str__()}" if self.code else super().__str__()

class AdminLevelError(BaseException):
    def __init__(self, message, code=None):
        super().__init__(message)  
        self.code = code  

    def __str__(self):
        return f"{self.code}: {super().__str__()}" if self.code else super().__str__()
