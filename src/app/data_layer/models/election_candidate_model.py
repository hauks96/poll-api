from app.data_layer.models.model import Model


class ElectionCandidateModel(Model):
    def __init__(self, id: None, candidate_id: int, election_id: int):
        super().__init__(id)
        self.candidate_id = candidate_id
        self.election_id = election_id

    def in_json(self):
        return {
            "id": self.id,
            "candidate_id": self.candidate_id,
            "election_id": self.election_id
        }

    @staticmethod
    def as_model(_model_as_json):
        return ElectionCandidateModel(id=_model_as_json["id"],
                                      candidate_id=_model_as_json["candidate_id"],
                                      election_id=_model_as_json["election_id"])

    def __str__(self):
        return "Candidate ID: " + str(self.candidate_id) + ", Election ID: " + str(self.election_id)

    def __eq__(self, other):
        if not isinstance(other, ElectionCandidateModel):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.id == other.id and self.candidate_id == other.candidate_id and self.election_id == other.election_id
