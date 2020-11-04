from app.data_layer.models.model import Model


# The poll on a specific election, from a specific source e.g "US Presidential election 2020 poll by fox news"
class PollModel(Model):
    def __init__(self, id: None, election_id: int, source_id: int, start_date: str, end_date: str):
        super().__init__(id)
        self.source_id = source_id
        self.election_id = election_id
        self.start_date = start_date
        self.end_date = end_date

    def in_json(self):
        return {
            "id": self.id,
            "source_id": self.source_id,
            "election_id": self.election_id,
            "start_date": self.start_date,
            "end_date": self.end_date
        }

    @staticmethod
    def as_model(_model_as_json):
        return PollModel(id=_model_as_json["id"],
                         source_id=_model_as_json["source_id"],
                         election_id=_model_as_json["election_id"],
                         start_date=_model_as_json["start_date"],
                         end_date=_model_as_json["end_date"])

    def __str__(self):
        return "Poll ID: " + str(self.id)
