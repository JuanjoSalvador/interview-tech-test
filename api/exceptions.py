class ValidationError(Exception):
    def __init__(self):
        self.message = "HTTP 400 BAD REQUEST - Data sent is not valid."
        super().__init__(self.message)


class NotAuthorizedException(Exception):
    def __init__(self):
        self.message = (
            "HTTP 401 NOT AUTHORIZED - User has not permissions to execute this action."
        )
        super().__init__(self.message)


class FirebaseServiceError(Exception):  # pragma: no cover
    def __init__(self, message, status):
        self.message = message
        super().__init__(self.message)

        self.status = status


class DocumentDoesNotExist(Exception):
    def __init__(self):
        self.message = "Document does not exist or has been already deleted."
        super().__init__(self.message)

        self.status = 400
