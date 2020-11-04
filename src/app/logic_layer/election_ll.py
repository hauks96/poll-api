from app.logic_layer.election_region_ll import ElectionRegionLogic
from app.logic_layer.logic import Logic
from app.logic_layer.election_candidate_ll import ElectionCandidateLogic


class ElectionLogic(Logic):
    def __init__(self):
        super().__init__()
        self.election_candidate = ElectionCandidateLogic()
        self.election_region_logic = ElectionRegionLogic()

    def get_election(self, _id):
        """Returns the election with given id. Uses the ElectionData instance to utilize it's get method"""
        election1 = self.get(_id)
        if election1:
            return self.jsonify(election1)
        return None

    def get_elections(self):
        """Returns all elections and uses the ElectionData instance to utilize it's get_all method"""
        elections = self.get_all()
        return self.jsonify(elections)

    def get_election_by_name(self, name):
        """Returns an election with given name, if not found returns none"""
        election = next((e for e in self.get_all() if e.name == name), None)
        if election:
            election = self.jsonify(election)
        return election

    def jsonify(self, models):
        json_list = []
        if not models:
            return json_list

        if type(models) != list:
            models = [models]

        for model in models:
            election_candidates = self.election_candidate.get_candidates_in_election(model.id)
            iter_election = {
                'electionID': str(model.id),
                'name': model.name,
                'candidates': self.election_candidate.jsonify(election_candidates),
                'regions': self.election_region_logic.jsonify(self.election_region_logic.get_election_regions(model.id))
            }
            json_list.append(iter_election)

        if len(json_list) == 1:
            return json_list[0]

        return json_list

    def jsonify_with_candidate_image(self, models):
        json_list = []
        if not models:
            return json_list

        if type(models) != list:
            models = [models]

        for model in models:
            election_candidates = self.election_candidate.get_candidates_in_election(model.id)
            iter_election = {
                'electionID': str(model.id),
                'name': model.name,
                'candidates': self.election_candidate.jsonify_with_candidate_image(election_candidates),
                'regions': self.election_region_logic.jsonify(self.election_region_logic.get_election_regions(model.id))
            }
            json_list.append(iter_election)

        if len(json_list) == 1:
            return json_list[0]

        return json_list

if __name__ == '__main__':
    pass
