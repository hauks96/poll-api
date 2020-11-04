from app.data_layer.models.model import Model


# Says what regions are included in each Election. e.g Ohio, Florida ... in US Presidential election
class ElectionRegionModel(Model):
    def __init__(self, id: None, election_id: int, region_id: int):
        super().__init__(id)
        self.election_id = election_id
        self.region_id = region_id

    def in_json(self):
        return {
            "id": self.id,
            "election_id": self.election_id,
            "region_id": self.region_id
        }

    @staticmethod
    def as_model(_model_as_json):
        return ElectionRegionModel(id=_model_as_json["id"],
                                   election_id=_model_as_json["election_id"],
                                   region_id=_model_as_json["region_id"])

    def __str__(self):
        return "Election: "+str(self.election_id)+", Region: "+str(self.region_id)
