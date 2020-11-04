from app.data_layer.models.model import Model


# The election type, e.g US Presidential Election/Icelandic Parliament Election
class ElectionModel(Model):
    def __init__(self, id: None, name: str):
        super().__init__(id)
        self.name = name

    def in_json(self):
        return {
            "id": self.id,
            "name": self.name
        }

    @staticmethod
    def as_model(_model_as_json):
        return ElectionModel(id=_model_as_json["id"],
                             name=_model_as_json["name"])

    def __str__(self):
        return self.name

