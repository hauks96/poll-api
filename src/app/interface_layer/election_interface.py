from app.data_layer.models.candidate_model import CandidateModel
from app.data_layer.models.election_candidate_model import ElectionCandidateModel
from app.data_layer.models.election_model import ElectionModel
from app.data_layer.models.election_region_model import ElectionRegionModel
from app.logic_layer.election_candidate_ll import ElectionCandidateLogic
from app.logic_layer.election_ll import ElectionLogic
from app.interface_layer.interface import Interface
from app.logic_layer.election_region_ll import ElectionRegionLogic
from app.logic_layer.region_ll import RegionLogic


class ElectionInterface(Interface):
    def __init__(self):
        super().__init__()
        self.auth_methods = ["createElection", "updateElection", "addElectionRegion",
                             "addElectionElectable", "getUserElections"]
        self.election_logic = ElectionLogic()
        self.election_region_logic = ElectionRegionLogic()
        self.election_candidate_logic = ElectionCandidateLogic()
        self.region_logic = RegionLogic()

    def createElection(self, args: dict, auth) -> dict:
        desired_args = ["name"]
        try:
            args = self.get_args_or_key_error(desired_args, args)
        except KeyError as error:
            return self.set_msg_or_error(str(error), 400)

        if type(args["name"]) != str:
            return self.set_msg_or_error("Name must be string.", 400)

        new_election = self.election_logic.add(ElectionModel(id=None, name=args["name"]))
        ret_msg = self.create_relation(auth, new_election.id)
        if ret_msg == "":
            return self.set_msg_or_error(self.election_logic.jsonify(new_election), 0)
        return self.set_msg_or_error(ret_msg, 401)

    def updateElection(self, args: dict, auth) -> dict:
        desired_args = ["electionID"]
        possible_args = ["name"]
        db_translation = {"name": "name"}  # e.g election_id = electionID
        try:
            args = self.get_args_or_key_error(desired_args, args)
        except KeyError as error:
            return self.set_msg_or_error(str(error), 400)

        requested_modification = self.get_possible_args(possible_args, args)
        if requested_modification["size"] == 0:
            return self.set_msg_or_error("Editable values are: name. At least one of the editable attributes "
                                         "must be in the request.", 0)

        election_id = self.convert_id(args["electionID"])
        if election_id is None:
            return self.set_msg_or_error("electionID invalid.", 400)

        ret_msg = self.edit_related(auth, election_id)
        if ret_msg != "":
            return self.set_msg_or_error(ret_msg, 401)

        election = self.election_logic.get(election_id)
        if election is None:
            return self.set_msg_or_error("No election with requested id.", 400)

        for key in requested_modification.keys():
            if requested_modification[key] is not None:
                setattr(election, db_translation[key], requested_modification[key])

        self.election_logic.update(election)
        return self.set_msg_or_error("Successfully updated election with id: %d" % election.id, 0)

    def addElectionRegion(self, args: dict, auth) -> dict:
        desired_args = ["regionID", "electionID"]
        try:
            args = self.get_args_or_key_error(desired_args, args)
        except KeyError as error:
            return self.set_msg_or_error(str(error), 400)

        region_id = self.convert_id(args["regionID"])
        election_id = self.convert_id(args["electionID"])
        if region_id is None:
            return self.set_msg_or_error("Invalid regionID", 400)
        if election_id is None:
            return self.set_msg_or_error("Invalid electionID", 400)

        regions = self.region_logic.get_all()
        exists = False
        for region in regions:
            if region.id == region_id:
                exists = True

        if not exists:
            return self.set_msg_or_error("Region doesn't exist.", 404)

        election_regions = self.election_region_logic.get_election_regions(election_id)
        for election in election_regions:
            if election_id == election.id:
                return self.set_msg_or_error("Election already covers this region.", 0)

        ret_msg = self.edit_related(auth, election_id)
        if ret_msg != "":
            return self.set_msg_or_error(ret_msg, 401)

        self.election_region_logic.add(ElectionRegionModel(id=None, election_id=election_id, region_id=region_id))
        return self.set_msg_or_error("Region added to election.", 0)

    def addElectionElectable(self, args: dict, auth) -> dict:
        desired_args = ["electableID", "electionID"]
        try:
            args = self.get_args_or_key_error(desired_args, args)
        except KeyError as error:
            return self.set_msg_or_error(str(error), 400)

        electable_id = self.convert_id(args["electableID"])
        election_id = self.convert_id(args["electionID"])
        if electable_id is None:
            return self.set_msg_or_error("Invalid regionID", 400)
        if election_id is None:
            return self.set_msg_or_error("Invalid electionID", 400)

        electables = self.election_candidate_logic.candidates.get_all()
        exists = False
        for electable in electables:
            if electable.id == electable_id:
                exists = True

        if not exists:
            return self.set_msg_or_error("Electable doesn't exist. To create an electable use"
                                         " the operation createElectable", 404)

        election_electables = self.election_candidate_logic.get_candidates_in_election(election_id)
        for electable in election_electables:
            if election_id == electable.id:
                return self.set_msg_or_error("Election already has this electable as an option.", 400)

        ret_msg = self.edit_related(auth, election_id)
        if ret_msg != "":
            return self.set_msg_or_error(ret_msg, 401)

        self.election_candidate_logic.add(ElectionCandidateModel(id=None, election_id=election_id,
                                                                 candidate_id=electable_id))
        return self.set_msg_or_error("Candidate added to election.", 0)

    def getUserElections(self, args: dict, auth) -> dict:
        id_list = self.get_user_creations(auth)
        if not auth.logged_in:
            return self.set_msg_or_error("Authentication failed.", 401)
        elections = self.election_logic.get_all()
        ret_models = []
        for election in elections:
            if election.id in id_list:
                ret_models.append(election)

        return self.set_msg_or_error(self.election_logic.jsonify(ret_models), 0)

    def getElection(self, args: dict) -> dict:
        """Returns a single election with the given ID. Returns an empty string if no election with this ID exists."""
        desired_args = ["electionID"]
        try:
            req_args = self.get_args_or_key_error(desired_args, args)
        except KeyError as error:
            return self.set_msg_or_error(str(error), 400)

        election_id = self.convert_id(req_args['electionID'])
        if not election_id:
            return self.set_msg_or_error("electionID must be a number", 400)

        election = self.election_logic.get_election(election_id)
        if not election:
            return self.set_msg_or_error("Election does not exist", 404)
        return self.set_msg_or_error(election, 0)

    def getElections(self, args: dict) -> dict:
        """Returns all Elections existing in the system. If no Election exists, an empty array is returned."""
        return self.set_msg_or_error(self.election_logic.get_elections(), 0)

    def getCandidatesInElection(self, args: dict) -> dict:
        """Returns all candidates in a specific election. If no candidate in election, an empty array is returned"""
        desired_args = ["electionID"]
        try:
            req_args = self.get_args_or_key_error(desired_args, args)
        except KeyError as error:
            return self.set_msg_or_error(str(error), 400)
        election_id = self.convert_id(req_args['electionID'])
        election_id = self.convert_id(election_id)
        if not election_id:
            return self.set_msg_or_error("electionID must be a number.", 400)

        election_candidates = self.election_candidate_logic.get_candidates_in_election(election_id)
        return self.set_msg_or_error(self.election_candidate_logic.jsonify(election_candidates), 0)

    def getElectionByName(self, args: dict):
        """Returns all candidates in a specific election. If no candidate in election, an empty array is returned"""
        try:
            election_name = args["electionName"]
            return self.election_logic.get_election_by_name(election_name)
        except KeyError:
            return None
