from app.data_layer.models.model import Model


class PollVoteModel(Model):
    def __init__(self, id: None, poll_id: int, candidate_id: int, region_id: int):
        super().__init__(id)
        self.poll_id = poll_id
        self.candidate_id = candidate_id
        self.region_id = region_id

    def in_json(self):
        return {
            "id": self.id,
            "poll_id": self.poll_id,
            "candidate_id": self.candidate_id,
            "region_id": self.region_id
        }

    @staticmethod
    def as_model(_model_as_json):
        return PollVoteModel(id=_model_as_json["id"],
                             poll_id=_model_as_json["poll_id"],
                             candidate_id=_model_as_json["candidate_id"],
                             region_id=_model_as_json["region_id"])

    def __str__(self):
        return "Poll ID: " + str(self.poll_id) + ", Candidate: " + str(self.candidate_id) + ", Region: " + str(
            self.region_id)
