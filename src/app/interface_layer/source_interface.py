from app.logic_layer.source_ll import SourceLogic
from app.interface_layer.interface import Interface

# THIS IS WHERE WE CREATE METHODS THAT HAVE THE SAME NAMES AS GRISCHA WANTS


class SourceInterface(Interface):
    def __init__(self):
        super().__init__()
        self.logic = SourceLogic()

    def getAllSources(self, args: dict) -> dict:
        # THIS IS JUST AN EXAMPLE
        sources = self.logic.get_all()
        return self.set_msg_or_error(self.logic.jsonify(sources), 0)

    def getSource(self, args: dict) -> dict:
        desired_args = ["sourceID"]
        try:
            req_args = self.get_args_or_key_error(desired_args, args)
        except KeyError as error:
            return self.set_msg_or_error(str(error), 400)
        source_id = req_args['sourceID']
        source_id = self.convert_id(source_id)
        if not source_id:
            return self.set_msg_or_error("Source ID must be a decimal number", 400)

        source = self.logic.get(source_id)
        if not source:
            return self.set_msg_or_error("Source does not exist.", 404)
        return self.set_msg_or_error(self.logic.jsonify(source), 0)

