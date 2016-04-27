
class NoInternet(Exception):
    def __init__(self,message='There is no internet connection '):
        super().__init__(message)
        self.message = message
   
class NoSentenceInJson(Exception):
    def __init__(self,message='There is no sentence in the received json'):
        super().__init__(message)
        self.message = message

class NoWordInInternet(Exception):
    def __init__(self,message='No such word is found in internte'):
        super().__init__(message)
        self.message = message


class NoSentenceInJsos(Exception):
    def __init__(self,message):
        super().__init__(message)
        self.message = message


class NoSentenceInJssn(Exception):
    def __init__(self,message):
        super().__init__(message)
        self.message = message


