from app.data_layer.models.model import Model


class CandidateModel(Model):
    def __init__(self, id: None, name: str, image_url: str, info: str):
        super().__init__(id)
        self.name = name
        self.image = image_url
        self.info = info

    def in_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "info": self.info
        }

    @staticmethod
    def as_model(_model_as_json):
        return CandidateModel(id=_model_as_json["id"],
                              name=_model_as_json["name"],
                              image_url=_model_as_json["image"],
                              info=_model_as_json["info"])

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if not isinstance(other, CandidateModel):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.id == other.id and self.name == other.name and self.image == other.image and self.info == other.info
