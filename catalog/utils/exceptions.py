
class RequestResponse404(Exception):
    """Exception raised when request response returns 404"""

    def __init__(self):
        self.message = "404 error - the request could not be completed"
        super().__init__(self.message)
