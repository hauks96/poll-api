from app.data_layer.models.candidate_model import CandidateModel
from app.logic_layer.election_candidate_ll import ElectionCandidateLogic
from app.logic_layer.candidate_ll import CandidateLogic
from app.interface_layer.interface import Interface


# THIS IS WHERE WE CREATE METHODS THAT HAVE THE SAME NAMES AS GRISCHA WANTS
class CandidateInterface(Interface):
    def __init__(self):
        super().__init__()
        self.candidate_logic = CandidateLogic()
        self.election_candidate_logic = ElectionCandidateLogic()
        self.auth_methods = ["createElectable", "deleteElectable", "getUserElectables",
                             "createCandidate", "createParty"]

    def createElectable(self, args: dict, auth) -> dict:
        desired_args = ["name", "description"]
        optional_args = ["imageUrl"]
        try:
            req_args = self.get_args_or_key_error(desired_args, args)
        except KeyError as error:
            return self.set_msg_or_error(str(error), 400)

        optional_args = self.get_possible_args(optional_args, args)
        image_url = ""
        if optional_args["imageUrl"] is not None:
            image_url = optional_args["imageUrl"]

        new_electable = CandidateModel(id=None, name=req_args["name"], image_url=image_url, info=req_args["bio"])
        electable = self.candidate_logic.add(new_electable)
        ret_str = self.create_relation(auth, electable.id)
        if ret_str == "":
            return self.set_msg_or_error(self.candidate_logic.jsonify(electable), 0)
        self.candidate_logic.delete(electable)
        return self.set_msg_or_error(ret_str, 401)

    def createCandidate(self, args: dict, auth) -> dict:
        return self.createElectable(args, auth)

    def createParty(self, args: dict, auth) -> dict:
        return self.createElectable(args, auth)

    def deleteElectable(self, args: dict, auth) -> dict:
        desired_args = ["electableID"]
        try:
            req_args = self.get_args_or_key_error(desired_args, args)
        except KeyError as error:
            return self.set_msg_or_error(str(error), 400)

        electable_id = self.convert_id(req_args["electableID"])
        if electable_id is None:
            return self.set_msg_or_error("electableID invalid.", 400)

        ret_str = self.delete_relation(auth, electable_id)
        if ret_str != "":
            return self.set_msg_or_error(ret_str, 401)

        self.election_candidate_logic.safe_delete_candidate(electable_id)
        return self.set_msg_or_error("Successfully removed electable.", 0)

    def getUserElectables(self, args: dict, auth) -> dict:
        if not auth.logged_in:
            return self.set_msg_or_error("Must be logged in.", 401)
        id_list = self.get_user_creations(auth)
        electables = self.candidate_logic.get_all()
        ret_models = []
        for electable in electables:
            if electable.id in id_list:
                ret_models.append(electable)

        return self.set_msg_or_error(self.candidate_logic.jsonify(ret_models), 0)

    def getElectables(self, args: dict) -> dict:
        """Returns all candidates for a given election. Returns an empty array if no election with this ID exists,
        or the election has no candidate."""
        # Return empty array if no election with this id exists
        # return [Candidate]
        desired_args = ['electionID']
        try:
            req_args = self.get_args_or_key_error(desired_args, args)
        except KeyError as error:
            return self.set_msg_or_error(str(error), 400)

        election_id = self.convert_id(req_args['electionID'])
        if not election_id:
            return self.set_msg_or_error('electionID must be a number.', 400)

        election_candidates = self.election_candidate_logic.get_candidates_in_election(election_id)
        if not election_candidates:
            return self.set_msg_or_error([], 0)
        return self.set_msg_or_error(self.election_candidate_logic.jsonify(election_candidates), 0)

    def getElectableDetails(self, args: dict) -> dict:
        """Returns a single candidate with the given ID. Returns an empty string if no candidate with this ID exists."""
        # return Candidate
        # return empty string if no candidate
        desired_args = ['electableID']
        try:
            req_args = self.get_args_or_key_error(desired_args, args)
        except KeyError as error:
            return self.set_msg_or_error(str(error), 400)

        candidate_id = self.convert_id(req_args['electableID'])
        if not candidate_id:
            return self.set_msg_or_error('electableID must be a number.', 400)

        candidate = self.candidate_logic.get(_id=candidate_id)
        if not candidate:
            return self.set_msg_or_error("Electable does not exist.", 404)
        return self.set_msg_or_error(self.candidate_logic.jsonify(candidate), 0)

    def getAllCandidates(self, args: dict):
        candidates = self.candidate_logic.get_all()
        if not candidates:
            return self.set_msg_or_error([], 0)
        return self.set_msg_or_error(self.candidate_logic.jsonify(candidates), 0)

    def getAllParties(self, args: dict):
        # not available in our system
        return self.set_msg_or_error([], 0)
