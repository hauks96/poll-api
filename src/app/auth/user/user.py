from app.auth.exceptions.auth_exception import InvalidUserCreation
from app.auth.user.fetcher import Fetcher
from app.auth.user.serializer import Serializer
from app.auth.user.ssn import SSN


class User(Fetcher):
    def __init__(self, username: str, password: str):
        super().__init__()
        if len(username) < 5 or len(password) < 5:
            raise InvalidUserCreation("Username and password must be at least length 5")
        self.data_path = self.get_filepath("../data/auth_user/auth.json")
        self.id = None
        self.username = username
        self.__password = Serializer(username, password).serialize()
        self.__idf = self.get_idf()

    def exists(self):
        """Returns true if user with the initialized credentials exists"""
        data = self.get_data()
        for i in range(len(data)):
            if data[i]["username"] == self.username:
                if self.__password == data[i]["password"]:
                    self.id = data[i]["id"]
                    return True
                return False
        return False

    @staticmethod
    def region(user_id: int) -> int:
        user_ssn = SSN(ssn="", first_name="", last_name="", region_id=0, user_id=user_id)
        return user_ssn.region()

    def create(self, _ssn: str, first_name: str, last_name: str, region_id: int):
        """Returns true for successful creation, false otherwise. Saves self to database"""
        data = self.get_data()
        for i in range(len(data)):
            if data[i]["username"] == self.username:
                raise InvalidUserCreation("User with that username already exists.")
        next_id = self.__idf + 1

        SSN(ssn=_ssn, user_id=next_id, first_name=first_name, last_name=last_name, region_id=region_id).create()

        data.append({
            "id": next_id,
            "username": self.username,
            "password": self.__password
        })
        self.id = next_id
        self.__idf = next_id
        self.write_data(data)

    def remove(self):
        user_ssn = SSN(ssn="", first_name="", last_name="", region_id=0, user_id=self.id)
        ssn_data = user_ssn.get_data()
        for i in range(len(ssn_data)):
            if ssn_data[i]["user_id"] == self.id:
                ssn_data.pop(i)
                user_ssn.write_data(ssn_data)
                break

        data = self.get_data()
        for i in range(len(data)):
            if data[i]["id"] == self.id:
                data.pop(i)
                self.write_data(data)
                return


if __name__ == '__main__':
    user = User("Test1", password="Test1")
    print(user.exists())
    new_user = User("Test1", password="Test1")
    ssn = "00000001"
    was_created = new_user.create(ssn)
    print(was_created)
