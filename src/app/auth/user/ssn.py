from app.auth.user.fetcher import Fetcher
from app.data_layer.data.region_data import RegionData
from app.auth.exceptions.auth_exception import InvalidUserCreation


class SSN(Fetcher):
    def __init__(self, ssn: str, first_name: str, last_name: str, region_id: int, user_id: int):
        super().__init__()
        self.data_path = self.get_filepath("../data/auth_user/ssn.json")
        self.id = None
        self.user_id = user_id
        self.ssn = ssn
        self.first_name = first_name
        self.last_name = last_name
        self.region_id = region_id
        self.idf = self.get_idf()

    def exists(self):
        """Returns true if self exists in database"""
        data = self.get_data()
        for ssn_model in data:
            if ssn_model["ssn"] == self.ssn:
                return True
        return False

    def region(self):
        data = self.get_data()
        for ssn_model in data:
            if ssn_model["user_id"] == self.user_id:
                return ssn_model["region_id"]
        return None

    def create(self):
        """Adds self to database"""
        if not self.ssn.isdecimal():
            raise InvalidUserCreation("SSN must be numbers only")

        if len(self.ssn) < 8:
            raise InvalidUserCreation("SSN must be at least length 8")

        data = self.get_data()

        for ssn in data:
            if ssn["ssn"] == self.ssn:
                raise InvalidUserCreation("SSN has already been signed up")
            if ssn["user_id"] == self.user_id:
                raise InvalidUserCreation("Unique constraint failed for user_id")
        self.id = self.idf + 1
        data.append({
            "id": self.id + 1,
            "user_id": self.user_id,
            "region_id": self.region_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "ssn": self.ssn
        })
        self.write_data(data)
        self.idf += 1
