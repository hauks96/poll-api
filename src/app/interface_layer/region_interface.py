from app.data_layer.models.region_model import RegionModel
from app.logic_layer.election_region_ll import ElectionRegionLogic
from app.logic_layer.poll_vote_ll import PollVoteLogic
from app.logic_layer.region_ll import RegionLogic
from app.interface_layer.interface import Interface


# THIS IS WHERE WE CREATE METHODS THAT HAVE THE SAME NAMES AS GRISCHA WANTS
class RegionInterface(Interface):
    def __init__(self):
        super().__init__()
        self.logic = RegionLogic()
        self.auth_methods = ['createRegion', 'deleteRegion', 'getUserRegions']

    def getAllRegions(self, args: dict) -> dict:
        regions = self.logic.get_all()
        if not regions:
            return self.set_msg_or_error([], 0)
        return self.set_msg_or_error(self.logic.jsonify(regions), 0)

    def createRegion(self, args: dict, auth) -> dict:
        desired_args = ["name"]
        optional_args = ["population", "registeredVoters"]
        try:
            req_args = self.get_args_or_key_error(desired_args, args)
        except KeyError as error:
            return self.set_msg_or_error(str(error), 400)

        if type(req_args["name"]) != str:
            return self.set_msg_or_error(msg="Name must be string.", success=400)

        optional_args = self.get_possible_args(optional_args, args)
        str_population = optional_args['population']
        if str_population == "":
            population = 0
        else:
            population = self.convert_id(str_population)
            if not population:
                return self.set_msg_or_error("Population must be a number.", 400)

        str_registered_voters = optional_args['registeredVoters']
        if str_registered_voters == "":
            registered_voters = 0
        else:
            registered_voters = self.convert_id(str_registered_voters)
            if not registered_voters:
                return self.set_msg_or_error("Registered voters must be a number.", 400)

        new_region = self.logic.add(RegionModel(id=None, name=args["name"], population=population,
                                                registeredVoters=registered_voters))
        ret_msg = self.create_relation(auth, new_region.id)
        if ret_msg == "":
            return self.set_msg_or_error(self.logic.jsonify(new_region), 0)

        self.logic.delete(new_region.id)
        return self.set_msg_or_error(ret_msg, 401)

    def deleteRegion(self, args: dict, auth) -> dict:
        desired_args = ["regionID"]
        try:
            req_args = self.get_args_or_key_error(desired_args, args)
        except KeyError as error:
            return self.set_msg_or_error(str(error), 400)

        region_id = self.convert_id(req_args["regionID"])
        if region_id is None:
            return self.set_msg_or_error("regionID invalid.", 400)

        ret_str = self.delete_relation(auth, region_id)
        if ret_str != "":
            return self.set_msg_or_error(ret_str, 401)

        vote_logic = PollVoteLogic()
        election_region_logic = ElectionRegionLogic()
        votes = vote_logic.get_all()
        new_votes = []
        # Removing all votes that this region has
        for vote in votes:
            if not vote.region_id == region_id:
                new_votes.append(vote)
        vote_logic.save(new_votes)

        election_regions = election_region_logic.get_all()
        new_election_regions = []
        # Removing all connections to elections
        for region in election_regions:
            if not region.region_id == region_id:
                new_election_regions.append(region)

        election_region_logic.save(new_election_regions)
        self.logic.delete(region_id)

        return self.set_msg_or_error("Successfully removed region.", 0)

    def getUserRegions(self, args: dict, auth) -> dict:
        if not auth.logged_in:
            return self.set_msg_or_error("Must be logged in.", 401)
        id_list = self.get_user_creations(auth)
        regions = self.logic.get_all()
        ret_models = []
        for region in regions:
            if region.id in id_list:
                ret_models.append(region)

        return self.set_msg_or_error(self.logic.jsonify(ret_models), 0)

    def getRegionDetails(self, args: dict) -> dict:
        """Returns a single region with the given ID. Returns an empty string if no region with this ID exists."""
        # return Region
        # return ""
        desired_args = ["regionID"]
        try:
            req_args = self.get_args_or_key_error(desired_args, args)
        except KeyError as error:
            return self.set_msg_or_error(str(error), 400)

        region_id = self.convert_id(req_args['regionID'])
        if not region_id:
            return self.set_msg_or_error("regionID must be a number", 400)

        region = self.logic.get(region_id)
        if not region:
            return self.set_msg_or_error("Region does not exist.", 404)
        return self.set_msg_or_error(self.logic.jsonify(region), 0)
