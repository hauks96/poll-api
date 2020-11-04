# This example includes some more advanced concepts.
# To start with a basic websocket implementation, try to get the basic example from
# the original documentation to run, as we did in L7:
# https://websockets.readthedocs.io/en/stable/intro.html

# asyncio is used to ensure that we can do asynchronous operations (non-blocking)
import asyncio
import json
import websockets

# We need our station code, to have actual "functionality"
# This represents our actual system.
# The code in this file represents the interface - the connection to the outside


# This class represents our technical connection to the outside.
# It allows processing of incoming text messages via WebSockets
# It is implemented as a Singleton pattern (which ensures there is only ever one instance of this class)
# Details on Singleton in the design lectures and here: https://en.wikipedia.org/wiki/Singleton_pattern
from app.auth.auth import Auth
from app.auth.exceptions.auth_exception import AuthenticationFailed, InvalidUserCreation
from app.interface_layer.candidate_interface import CandidateInterface
from app.interface_layer.poll_interface import PollInterface
from app.interface_layer.region_interface import RegionInterface
from app.interface_layer.source_interface import SourceInterface
from app.interface_layer.election_interface import ElectionInterface


class Communicator:
    # This is our (private) instance
    __instance = None

    # This is a class method - it can be called without an instance existing
    @staticmethod
    def get_instance():
        """ Static access method. """
        if Communicator.__instance is None:
            # in this particular case, the method makes sure that an instance is created if none exists
            Communicator()

            # afterwards (or if an instance did already exist), we return the instance
        return Communicator.__instance

    # The constructor throws an exception if we already have an instance - we don't want to allow any other instances
    # Note: This is actually not a nice implementation in Python. In other languages, you can actually force that
    # only one instance is created. In Python, this is more of a convention...
    def __init__(self):
        if Communicator.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            # If there is no instance, we create one
            Communicator.__instance = self
            try:
                self.authentication = Auth()  # SET NONE TO DISABLE AUTHENTICATION AND DEPENDENT METHODS ENTIRELY
            except NameError:
                self.authentication = None
            self.interfaces = [PollInterface(), RegionInterface(),
                               SourceInterface(), CandidateInterface(), ElectionInterface()]

    def auth_operation(self, operation: str, auth: dict) -> dict:
        if operation == "login":
            return self.login(auth=auth)

        if operation == "logout":
            return self.logout()

    def login(self, auth: dict) -> dict:
        try:
            password = auth["password"]
            username = auth["username"]
        except KeyError:
            return {"msg": "Missing authentication credentials for login. [username] and [password] required",
                    "success": 400}

        try:
            self.authentication.login(username, password)
            return {"msg": "Successfully logged in", "success": 0}

        except AuthenticationFailed as error:
            error_msg = str(error)
            return {"msg": error_msg, "success": 401}

    def logout(self) -> dict:
        if self.authentication.logged_in:
            self.authentication.logout()
            return {"msg": "Successfully logged out.", "success": 0}
        return {"msg": "Already logged out.", "success": 0}

    def validate_user_region(self, args: dict) -> None:
        """Call to validate that a user creation has a valid region"""
        for interface in self.interfaces:
            if type(interface).__name__ == 'RegionInterface':
                region = interface.getRegionDetails(args)
                if region == "":
                    raise InvalidUserCreation("Region doesn't exist")
                return

    def operation_processor(self, data):
        operation = self.get_operation(data)
        if operation == "":
            return {"msg": "Operation missing from request data", "success": 400}

        args = self.get_args(data)
        auth = self.get_auth(data)

        # If authentication related
        if self.authentication is not None:
            if operation in self.authentication.methods:
                if operation == "createUser":
                    try:
                        self.validate_user_region(args)
                    except InvalidUserCreation as error:
                        return {"msg": str(error), "success": 400}
                    try:
                        self.authentication.createUser(args)
                        return {"msg": "User created.", "success": 0}
                    except InvalidUserCreation as error:
                        return {"msg": str(error), "success": 400}
                else:
                    return self.auth_operation(operation, auth)

        # Otherwise
        for interface in self.interfaces:
            if operation in interface.return_class_methods():
                # If interface method requires auth
                if operation in interface.auth_methods:
                    # If logged in -> do operation
                    if self.authentication is None:
                        return {"msg": "Methods requiring authentication currently unavailable", "success": 404}
                    elif self.authentication.logged_in:
                        return getattr(interface, operation)(args, self.authentication)
                    # Not logged in -> return error
                    return {"msg": "Authentication required for operation %s" % operation, "success": 401}
                # If interface method doesn't require authentication
                else:
                    return getattr(interface, operation)(args)
        return {"msg": "Operation %s not implemented." % operation, "success": 401}

    @staticmethod
    def get_operation(data: dict) -> str:
        try:
            return data["op"]
        except TypeError:
            return ""
        except KeyError:
            return ""

    @staticmethod
    def get_args(data: dict) -> dict:
        try:
            args = data["data"]
        except KeyError:
            args = {}
        except TypeError:
            args = {}
        except ValueError:
            args = {}

        if not args:
            args = {}

        return args

    @staticmethod
    def get_auth(data: dict) -> dict:
        try:
            auth_dict = data["auth"]
            usn = auth_dict["username"]
            pw = auth_dict["password"]
            auth = {"username": usn, "password": pw}
        except KeyError:
            auth = {}
        except TypeError:
            auth = {}
        except ValueError:
            auth = {}

        if not auth:
            auth = {}

        return auth

    # This is the real WebSockets meat
    async def __msg_handler(self, websocket, path):
        # We wait until we receive a message (from a client/other system)
        msg = await websocket.recv()
        print("request received")
        invalid_format = False
        return_value = ""
        data = None
        try:
            data = json.loads(msg)  # convert msg to dict object
        except ValueError:
            invalid_format = True
            return_value = {"msg": "Invalid data format", "success": 400}
        print(data)
        if not invalid_format:
            return_value = self.operation_processor(data)
        print(return_value)
        # We return our return message (depending on the outcome a different JSON string)
        await websocket.send(json.dumps(return_value, indent=2))

    # This logic starts the websocket server and listens until we kill the application
    # In the basic example, this code is just below the actual method
    # Here, I placed it into a function so that I can just call it below in the main part
    def start(self):
        # Note here that __msg_handler is the name of the function that should be called whenever a message arrives
        # That's the function defined above (Line 65)
        start_server = websockets.serve(self.__msg_handler, "0.0.0.0", 8080)

        # Run until forever
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    # Here we get out Communicator Singleton (our single instance) and start the WebSockets server
    compPort = Communicator.get_instance()
    compPort.start()
