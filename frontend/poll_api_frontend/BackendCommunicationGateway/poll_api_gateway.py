import asyncio
import json
import websockets


class Response:
    def __init__(self, status: int, content, operation: str):
        """
        This object contains all the useful data received from the server response.

        :param status: 0 When successful, 400 something otherwise
        :param content: When stats is not 0, then string, otherwise list of dicts or dict.
        :param operation: The operation that was used to call the server
        """
        self.status = status
        self.content = content
        self.operation = operation


class ResponseObject:
    """Call ResponseObject with get_response."""

    def __init__(self, response_data):
        self.response_data = response_data

    def getResponse(self) -> Response:
        """
        Returns response and resets response data to None.\n
        Response data contains keys '**msg**' and '**status**'.

        :returns Response:
        """
        if self.response_data is None:
            return None

        data = self.response_data
        self.response_data = None
        return Response(status=data['status'], content=data['msg'], operation=data['operation'])


class PollApiGatewayError(Exception):
    pass


class PollApiGateway:
    def __init__(self, loop):
        self.loop = loop

    def __read_response(self, response_data, operation: str):
        """
        Reads and converts response of a received request. **Intended for internal usage** but can be used to read in data
        from poll api server.

        :raises PollApiGatewayError: If attributes are missing from the response
        """
        try:
            response_data = json.loads(response_data)
        except ValueError:
            return None

        ret_data = {}
        try:
            ret_data['msg'] = response_data['msg']
        except KeyError:
            raise PollApiGatewayError("Attribute 'msg' missing from response.")

        try:
            ret_data['status'] = response_data['success']
        except KeyError:
            # Removed raise error to make it more modular (usable with other implementations)
            ret_data['status'] = 0
            response_data['status'] = 0
            # raise PollApiGatewayError("Attribute 'success' missing from response.")

        if ret_data['msg'] is None and ret_data['status'] is None:
            return None

        ret_data['operation'] = operation

        response = ResponseObject(ret_data)

        return response.getResponse()

    def get_request(self, operation: str, r_args=None) -> Response:
        """
        This method is to be called to fetch a response from the poll api server.

        :arg operation: The name of the operation to perform on server.
        :type operation: str
        :arg r_args: The arguments to send with the operation.
        :type r_args: dict
        :raises PollApiGatewayError: If attributes are missing from the response
        :returns: Response object with attributes status, content and operation
        """
        if r_args is None:
            r_args = {}

        try:
            async def get_request() -> Response:
                uri = "ws://localhost:8080"
                json_payload = {'op': operation, 'data': r_args}
                async with websockets.connect(uri) as socket:
                    await socket.send(json.dumps(json_payload))
                    response = await socket.recv()

                    return self.__read_response(response, operation)

            return self.loop.run_until_complete(get_request())

        except:
            return Response(500, "Connection could not be established with the server.", operation)

    def log_in(self, auth: dict) -> Response:
        """
        This method is to be called to log in with a username and password. Fetches a response from the poll api server
        into the Response object.

        :returns Response:
        :arg auth: The arguments i.e username and password.
        :type auth: dict
        :raises PollApiGatewayError: If attributes are missing from the response
        """
        try:
            async def get_request():
                uri = "ws://localhost:8080"
                json_payload = {'op': 'login', 'data': {}, 'auth': auth}
                async with websockets.connect(uri) as socket:
                    await socket.send(json.dumps(json_payload))
                    response = await socket.recv()
                    return self.__read_response(response, 'login')

            return self.loop.run_until_complete(get_request())
        except:
            return Response(500, "Connection could not be established with the server.", 'login')


# TODO: Create a service stub for the server
# TODO: Create tests for the PollApiGateway
# TODO: Create tests for the ResponseObject
# TODO: Create tests for the Response


if __name__ == '__main__':
    pass
