from types import FunctionType

from app.auth.exceptions.auth_exception import AuthenticationFailed, AuthRelationCreationFailed, CreationLimitReached, \
    AuthRelationDeletionFailed


class Interface:
    def __init__(self):
        self.auth_methods = []

    @staticmethod
    def convert_id(_id: str):
        try:
            converted_id = int(_id)
        except ValueError:
            return None
        except TypeError:
            return None
        return converted_id

    @classmethod
    def return_class_methods(cls):
        """Returns all method names of the class"""
        methods = [x for x, y in cls.__dict__.items() if type(y) == FunctionType]
        ret_methods = []
        for method in methods:
            if method[:2] != "__":
                ret_methods.append(method)
        return ret_methods

    @staticmethod
    def get_args_or_key_error(desired_args: list, args: dict) -> dict:
        """Raises key error with appropriate message if arg key missing."""
        # Could send in a model object to assert that the types are correct or to convert them to the correct type
        new_dict = {}
        for arg in desired_args:
            try:
                new_dict[arg] = args[arg]
            except KeyError:
                err_str = "Missing argument: %s" % arg
                raise KeyError(err_str)
        return new_dict

    @classmethod
    def create_relation(cls, auth, model_id: int) -> str:
        try:
            auth.create_auth_relation(cls, model_id)
            return ""
        except AuthenticationFailed as error:
            return str(error)
        except AuthRelationCreationFailed as error:
            return str(error)
        except CreationLimitReached as error:
            return str(error)

    @classmethod
    def delete_relation(cls, auth, model_id: int) -> str:
        try:
            auth.remove_auth_relation(cls, model_id)
            return ""
        except AuthenticationFailed as error:
            return str(error)
        except AuthRelationDeletionFailed as error:
            return str(error)

    @classmethod
    def edit_related(cls, auth, model_id: int) -> str:
        try:
            auth.authorize_modification(cls, model_id)
            return ""
        except AuthenticationFailed as error:
            return str(error)

    @staticmethod
    def get_possible_args(possible_args: list, args: dict):
        """Returns dict with possible args. If the arg didn't exist in argument dict, then the value will be None.
        The return dict has an attribute size, which can be used to check if the dict is empty. (Only None values)"""
        # Could send in a model object to assert that the types are correct or to convert them to the correct type
        ret_args = {"size": 0}
        for arg in possible_args:
            try:
                ret_args[arg] = args[arg]
                ret_args["size"] += 1
            except KeyError:
                ret_args[arg] = ""

        return ret_args

    @classmethod
    def get_user_creations(cls, auth) -> list:
        try:
            return auth.user_creations(cls)
        except AuthenticationFailed:
            return []

    @staticmethod
    def set_msg_or_error(msg, success: int) -> dict:
        return {'msg': msg, 'success': success}


if __name__ == '__main__':
    # methods = Interface().return_class_methods()
    # print(methods)
    pass
