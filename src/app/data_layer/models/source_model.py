# The source of a poll e.g FoxNews/Govt
from app.data_layer.models.model import Model


# The source of a poll e.g FoxNews/Govt
class SourceModel(Model):
    def __init__(self, id: None, name: str, info: str):
        super().__init__(id)
        self.name = name
        self.info = info

    def in_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "info": self.info
        }

    @staticmethod
    def as_model(_model_as_json):
        return SourceModel(id=_model_as_json["id"],
                           name=_model_as_json["name"],
                           info=_model_as_json["info"])

    def __str__(self):
        return self.name
