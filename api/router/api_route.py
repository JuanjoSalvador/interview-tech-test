
class APIRoute():
    def __init__(self, path: str, view: any) -> None:
        self.path = path
        self.view = view
