import hashlib


class Serializer:
    def __init__(self, username: str, password: str):
        self.username = username
        self.__password = self.__sha256_credentials(username, password)

    @staticmethod
    def __sha256_credentials(username: str, password: str) -> str:
        cred_str = username + password
        cred_str = cred_str.encode("utf-8")
        return hashlib.sha256(cred_str).hexdigest()

    def serialize(self):
        return self.__password

    def __str__(self):
        return self.username


if __name__ == '__main__':
    pass
