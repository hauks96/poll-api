from app.auth.user.user import User
from app.auth.vote_creator import PollVoteCreator
from app.auth.poll_creator import PollCreator
from app.auth.region_creator import RegionCreator
from app.auth.election_creator import ElectionCreator
from app.auth.candidate_creator import CandidateCreator
from app.auth.exceptions.auth_exception import AuthenticationFailed, InvalidUserCreation, AuthRelationCreationFailed, \
    AuthRelationDeletionFailed, VoteFailed, CreationLimitReached


class Auth:
    """Authentication model for Poll API"""

    def __init__(self):
        self.methods = ["login", "logout", "createUser"]
        self.__user_id = None
        self.logged_in = False

    def logout(self):
        """Logs out an active user"""
        self.__user_id = None
        self.logged_in = False

    def login(self, username: str, password: str) -> None:
        """Raises AuthenticationFailed if user is not authenticated"""
        self.logout()
        self.__authenticate(username, password)
        self.logged_in = True

    @staticmethod
    def createUser(auth: dict) -> None:
        """auth dict: { username, password, firstName, lastName, regionID, ssn } all values are string.
        Raises InvalidUserCreation if anything goes wrong.
        Constraints: [Username] ->unique length >5, [password] -> length > 5, [ssn] -> unique only numbers length>=8,
        [regionID] -> must exist"""
        try:
            username = auth["username"]
            password = auth["password"]
            fist_name = auth["firstName"]
            last_name = auth["lastName"]
            region_id = auth["regionID"]
            ssn = auth["ssn"]
        except KeyError:
            raise InvalidUserCreation("Missing attributes from auth dict in user creation")

        try:
            region_id = int(region_id)
        except ValueError:
            raise InvalidUserCreation("region id must be an integer string")

        user = User(username=username, password=password)
        user.create(_ssn=ssn, first_name=fist_name, last_name=last_name, region_id=region_id)

    def removeAccount(self, username: str, password: str) -> None:
        """Removes the account of the logged in user. Raises AuthenticationFailed"""
        if not self.logged_in:
            raise AuthenticationFailed("Must log in to remove your account")

        user = User(username, password)
        user_exists = user.exists()
        if not user_exists:
            raise AuthenticationFailed("Invalid credentials given.")

        if user.id != self.__user_id:
            print(str(user.id) + ":" + str(self.__user_id))
            raise AuthenticationFailed("Invalid credentials given.")

        creators = [CandidateCreator(), ElectionCreator(), PollVoteCreator(), PollCreator(), RegionCreator()]
        for creator in creators:
            data = creator.get_data()
            for i in range(len(data)):
                if data[i]["user_id"] == self.__user_id:
                    data.pop(i)
                    creator.write_data(data)
                    break

        user.remove()
        self.logout()
        return

    def user_region(self) -> int:
        if not self.logged_in:
            raise AuthenticationFailed("Must log in before fetching user details")
        return User.region(self.__user_id)

    def user_creations(self, interface_class) -> list:
        """Returns election id's as list"""
        if not self.logged_in:
            raise AuthenticationFailed("Must log in before fetching user creations")

        instance = self.__get_related_class_instance(interface_class)
        if not instance:
            raise AuthenticationFailed("The requested interface has no authentication standard.")

        data = instance.get_data()
        for user in data:
            if user["user_id"] == self.__user_id:
                return user[instance.arg_name]
        return []

    def authorize_modification(self, interface_class, model_id: int) -> None:
        """Call this method when an update method is called. Authorizes the modification of an object related to the
        current interface. Model id would be the id of the desired data. For example poll id or election id. Raises
        AuthenticationFailed, """
        if not self.logged_in:
            raise AuthenticationFailed("Must log in before authorizing method")

        instance = self.__get_related_class_instance(interface_class)

        if type(instance).__name__ == PollVoteCreator:
            return

        if not instance:
            raise AuthenticationFailed("The requested interface has no authentication standard.")

        data = instance.get_data()
        for user in data:
            if user["user_id"] == self.__user_id:
                for _id in user[instance.arg_name]:
                    if _id == model_id:
                        return
                break
        raise AuthenticationFailed("User is not related to requested object")

    def create_auth_relation(self, interface_class, model_id: int) -> None:
        """Call this method when a create method is called. Creates a relationship between the data object and the user.
         Method should be used AFTER an object has been successfully created by user. Raises AuthenticationFailed,
         AuthRelationCreationFailed and CreationLimitReached.
         WARNING: Only create auth relation for a NEW OBJECT."""
        if not self.logged_in:
            raise AuthenticationFailed("Must log in before creating data")

        instance = self.__get_related_class_instance(interface_class)

        if not instance:
            raise AuthenticationFailed("The requested interface has no authentication standard.")

        if type(instance).__name__ == PollVoteCreator.__name__:
            return self.__vote(instance=instance, poll_id=model_id)

        self.__create_instance(instance, model_id)

    def remove_auth_relation(self, interface_class, model_id: int) -> None:
        """Call this method when a delete/remove method is called. Delete a relationship between a model and it's
        creator. Raises AuthenticationFailed if not authorized. Raises AuthRelationDeletionFailed if relationship
         doesn't exist """
        if not self.logged_in:
            raise AuthenticationFailed("Must log in before deleting data")

        self.authorize_modification(interface_class, model_id)

        instance = self.__get_related_class_instance(interface_class)
        self.__delete_instance(instance, model_id)

    @staticmethod
    def __get_related_class_instance(interface_class):
        if_name = interface_class.__name__
        if_name = if_name.replace("Interface", "Creator", 1)
        cls_instance = globals()[if_name]
        return cls_instance()

    def __vote(self, instance: PollVoteCreator, poll_id: int) -> None:
        """Before a user vote is created here, it should be validated that the poll exists in the backend.
        RETURNS VOTE MODEL IF SUCCESSFUL. Only holds data on what poll the user has voted on."""
        # Vote creator instance
        data = instance.get_data()
        for user in data:
            if user["user_id"] == self.__user_id:
                for _id in user[instance.arg_name]:
                    if _id == poll_id:
                        raise VoteFailed("You've already voted on this poll!")

                user[instance.arg_name].append(poll_id)
                instance.write_data(data)
                return

        # Add new vote to vote creator data
        data.append(instance.new_instance(user_id=self.__user_id, arg_val=poll_id))
        instance.write_data(data)
        return

    def __authenticate(self, username: str, password: str) -> None:
        """Raises AuthenticationFailed if user is not authenticated"""
        try:
            user = User(username=username, password=password)
        except InvalidUserCreation:
            raise AuthenticationFailed("Login credentials are of length 5 or greater...")
        if user.exists():
            self.__user_id = user.id
            return
        raise AuthenticationFailed("User with these credentials does not exist")

    def __create_instance(self, instance, model_id: int) -> None:
        """Raises AuthRelationCreationFailed if model already in user's relations"""
        data = instance.get_data()
        for user in data:
            if user["user_id"] == self.__user_id:
                if len(user[instance.arg_name]) >= instance.max_creations:
                    err_str = "Creation limit has been reached. You can have at most %d of this instance. Please " \
                              "consider deleting some of your older ones." % instance.max_creations
                    raise CreationLimitReached(err_str)
                for _id in user[instance.arg_name]:
                    if _id == model_id:
                        raise AuthRelationCreationFailed("Auth relation already exists")
                user[instance.arg_name].append(model_id)
                instance.write_data(data)
                return
        data.append(instance.new_instance(user_id=self.__user_id, arg_val=model_id))
        instance.write_data(data)
        # Set new created instance as authorized for mods until another operation is performed
        self.__authorized_model_id = model_id

    def __delete_instance(self, instance, model_id: int) -> None:
        """Raises AuthRelationDeletionFailed if model doesn't exist in user's relations"""
        data = instance.get_data()
        for user in data:
            if user["user_id"] == self.__user_id:
                for i in range(len(user[instance.arg_name])):
                    if user[instance.arg_name][i] == model_id:
                        user[instance.arg_name].pop(i)
                        instance.write_data(data)

                        return

                raise AuthRelationDeletionFailed("Auth relation doesn't exists")


if __name__ == '__main__':
    pass
