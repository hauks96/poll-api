from app.data_layer.models.model import Model


class RegionModel(Model):
    def __init__(self, id: None, name: str, population: int, registeredVoters: int):
        super().__init__(id)
        self.name = name
        self.population = population
        self.registeredVoters = registeredVoters

    def in_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "registeredVoters": self.registeredVoters
        }

    @staticmethod
    def as_model(_model_as_json):
        return RegionModel(id=_model_as_json["id"],
                           name=_model_as_json["name"],
                           population=_model_as_json["population"],
                           registeredVoters=_model_as_json["registeredVoters"])

    def __str__(self):
        return self.name
