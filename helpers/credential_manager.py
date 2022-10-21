import querylib

class GetCredentials:

    def __init__(self, username: str) -> None:
        self.username = username

    def get(self) -> list:
        credman = querylib.Credentials(self.username)
        data = credman.get()

        return data
