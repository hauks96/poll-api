from app.logic_layer.candidate_ll import CandidateLogic
from app.logic_layer.logic import Logic


class ElectionCandidateLogic(Logic):

    def __init__(self):
        super().__init__()
        self.candidates = CandidateLogic()

    def safe_delete_candidate(self, candidate_id: int) -> None:
        data = self.get_all()
        new_data = []
        for el_candidate in data:
            if el_candidate.candidate_id != candidate_id:
                new_data.append(el_candidate)
        self.save(new_data)
        self.candidates.delete(candidate_id)

    def delete_election_candidates(self, election_id):
        """Delete candidates in election"""
        data = self.get_all()
        new_data = []
        for i in range(len(data)):
            if data[i].election_id != election_id:
                new_data.append(data[i])

        self.save(new_data)

    def get_candidates_in_election(self, election_id):
        """Returns all candidates in a specific election"""
        candidate_ids = []
        all_candidates = []
        # Fetch all candidate id's for given election_id
        for x in self.get_all():
            if x.election_id == election_id:
                candidate_ids.append(x.candidate_id)

        # Fetch all candidate models for candidate id's
        # Það væri betra að fetcha all einu sinni hér ertu að ýtra yfir alla kandídata aftur og aftur
        for _id in candidate_ids:
            all_candidates.append(self.candidates.get(_id))
        return all_candidates

    def jsonify(self, models):
        if models:
            return self.candidates.jsonify(models)
        return []

    def jsonify_with_candidate_image(self, models):
        if models:
            return self.candidates.jsonify_with_image(models)
        return []


if __name__ == '__main__':
    pass
