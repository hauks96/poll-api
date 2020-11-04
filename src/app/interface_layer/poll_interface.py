import datetime
from app.auth.exceptions.auth_exception import VoteFailed, AuthenticationFailed, AuthRelationCreationFailed, \
    CreationLimitReached, AuthRelationDeletionFailed
from app.data_layer.models.poll_model import PollModel
from app.interface_layer.election_interface import ElectionInterface
from app.interface_layer.interface import Interface
from app.logic_layer.poll_ll import PollLogic


# THIS IS WHERE WE CREATE METHODS THAT HAVE THE SAME NAMES AS GRISCHA WANTS

class PollInterface(Interface):
    def __init__(self):
        super().__init__()
        self.auth_methods = ["createPoll", "deletePoll", "vote", "getUserPolls", "deleteElection"]
        self.logic = PollLogic()

    def getPoll(self, args: dict) -> dict:
        desired_args = ["pollID"]
        try:
            args = self.get_args_or_key_error(desired_args, args)
        except KeyError as error:
            return self.set_msg_or_error(str(error), 400)

        poll_id = self.convert_id(args['pollID'])
        if not poll_id:
            return self.set_msg_or_error("pollID must be a number.", 400)

        poll = self.logic.get(poll_id)
        if not poll:
            return self.set_msg_or_error("Poll with given ID does not exist.", 404)

        json_poll = self.logic.jsonify(poll)
        return self.set_msg_or_error(json_poll, 0)

    def createPoll(self, args: dict, auth) -> dict:
        desired_args = ["electionID", "startDate", "endDate"]
        try:
            args = self.get_args_or_key_error(desired_args, args)
        except KeyError as error:
            return self.set_msg_or_error(str(error), 400)

        is_date = self.logic.validate_date(args["startDate"])
        if not is_date:
            return self.set_msg_or_error("start date is not a valid in valid format: YYYY-MM-DD", 400)
        is_date = self.logic.validate_date(args["endDate"])
        if not is_date:
            return self.set_msg_or_error("end date is not a valid in valid format: YYYY-MM-DD", 400)

        election_id = self.convert_id(args["electionID"])
        new_poll = PollModel(id=None, source_id=1, election_id=election_id,
                             start_date=args["startDate"], end_date=args["endDate"])
        # Must create poll first in order to get an id
        new_poll = self.logic.add(new_poll)
        ret_msg = self.create_relation(auth=auth, model_id=new_poll.id)
        if ret_msg == "":
            return self.set_msg_or_error(self.logic.jsonify(new_poll), 0)
        self.logic.delete(new_poll.id)
        return self.set_msg_or_error(ret_msg, 401)

    def getUserPolls(self, args: dict, auth) -> dict:
        if not auth.logged_in:
            return self.set_msg_or_error("Authentication failed.", 401)
        id_list = self.get_user_creations(auth)
        polls = self.logic.get_all()
        ret_models = []
        for poll in polls:
            if poll.id in id_list:
                ret_models.append(poll)

        return self.set_msg_or_error(self.logic.jsonify(ret_models), 0)

    def deletePoll(self, args: dict, auth) -> dict:
        desired_args = ["pollID"]
        try:
            args = self.get_args_or_key_error(desired_args, args)
        except KeyError as error:
            return self.set_msg_or_error(str(error), 400)

        poll_id = self.convert_id(args["pollID"])
        if not poll_id:
            return self.set_msg_or_error("Invalid pollID. Must be a number", 400)

        ret_msg = self.delete_relation(auth, model_id=poll_id)
        if ret_msg == "":
            self.logic.safe_delete(poll_id)
            return self.set_msg_or_error("Successfully deleted poll.", 0)
        return self.set_msg_or_error(ret_msg, 401)

    def deleteElection(self, args: dict, auth) -> dict:
        desired_args = ["electionID"]
        try:
            args = self.get_args_or_key_error(desired_args, args)
        except KeyError as error:
            return self.set_msg_or_error(str(error), 400)

        election_id = self.convert_id(args["electionID"])
        if not election_id:
            return self.set_msg_or_error("Invalid electionID. Must be a number", 400)

        try:
            auth.remove_auth_relation(ElectionInterface, election_id)
        except AuthenticationFailed as error:
            return self.set_msg_or_error(str(error), 401)
        except AuthRelationDeletionFailed as error:
            return self.set_msg_or_error(str(error), 401)

        self.logic.safe_delete_election(election_id=election_id)
        return self.set_msg_or_error("Successfully deleted election.", 0)

    def vote(self, args: dict, auth) -> dict:
        desired_args = ["pollID", "electableID"]
        try:
            args = self.get_args_or_key_error(desired_args, args)
        except KeyError as error:
            return self.set_msg_or_error(str(error), 400)

        electable_id = self.convert_id(args["electableID"])
        poll_id = self.convert_id(args["pollID"])
        if not electable_id:
            return self.set_msg_or_error("Electable id must be integer string", 400)
        if not poll_id:
            return self.set_msg_or_error("Poll id must be integer string", 400)

        poll = self.logic.get(_id=poll_id)
        if not poll:
            return self.set_msg_or_error("The poll you are trying to vote on does not exist", 404)

        election = self.logic.election_logic.get(poll.election_id)
        if not election:
            return self.set_msg_or_error("Election for poll couldn't be found! Sorry for the inconvenience!", 500)

        election_regions = self.logic.election_region_logic.get_election_regions(election.id)
        user_in_region = False
        user_region = auth.user_region()
        for region in election_regions:
            if region.id == user_region:
                user_in_region = True

        if not user_in_region:
            return self.set_msg_or_error("Selected poll is not available in your region", 401)

        election_electable = self.logic.election_candidate_logic.get_candidates_in_election(election.id)
        valid_option = False
        for electable in election_electable:
            if electable.id == electable_id:
                valid_option = True

        if not valid_option:
            return self.set_msg_or_error("Vote option not recognized as an electable.", 400)

        end_date = datetime.date.fromisoformat(poll.end_date)
        start_date = datetime.date.fromisoformat(poll.start_date)
        date_today = datetime.datetime.now().date()
        if end_date < date_today:
            return self.set_msg_or_error("This poll is closed for voting as of %s." % poll.end_date, 400)
        if start_date > date_today:
            return self.set_msg_or_error("This poll opens for voting on %s." % poll.start_date, 400)

        try:
            auth.create_auth_relation(PollVoteInterface, poll_id)
        except AuthenticationFailed as error:
            return self.set_msg_or_error(str(error), 401)
        except AuthRelationCreationFailed as error:
            return self.set_msg_or_error(str(error), 401)
        except CreationLimitReached as error:
            return self.set_msg_or_error(str(error), 401)
        except VoteFailed as error:
            return self.set_msg_or_error(str(error), 401)

        self.logic.poll_vote_logic.vote(region_id=auth.user_region(), poll_id=poll_id, electable_id=electable_id)
        return self.set_msg_or_error("Vote submitted!", 0)

    def getAllPolls(self, args: dict) -> dict:
        """Returns all polls existing in the system. If no poll exists, an empty array is returned.
        If you only support one poll, it's fine to return that one poll (as the only element in an array)"""
        # return [Poll]
        # {"op": self.getAllPolls.__name__ , "data":self.logic.get_polls()}
        return self.set_msg_or_error(self.logic.get_polls(), 0)

    def getPollsBySourceName(self, args: dict) -> dict:
        try:
            source_name = args["sourceName"]
        except KeyError:
            return self.set_msg_or_error("argument sourceName not found.", 400)
        polls = self.logic.get_polls_from_source_name(source_name)
        if not polls:
            return self.set_msg_or_error([], 0)
        return self.set_msg_or_error(polls, 0)

    def getPollsByTimeFrame(self, args: dict) -> dict:
        try:
            _start_date = args["startDate"]
            _end_date = args["endDate"]
        except KeyError:
            return self.set_msg_or_error("Argument startDate and endDate required", 400)
        return_polls = self.logic.get_polls_from_specific_time_frame(_start_date, _end_date)
        if not return_polls:
            return self.set_msg_or_error([], 0)
        return self.set_msg_or_error(return_polls, 0)

    def getHistoricalPollsForElection(self, args:dict) -> dict:
        try:
            _start_date = args["dateAfter"]
            _end_date = args["dateBefore"]
            election_id = args["electionID"]
        except KeyError:
            return self.set_msg_or_error("Argument dateAfter, dateBefore and electionID required", 400)

        election_id = self.convert_id(election_id)
        if not election_id:
            return self.set_msg_or_error("electionID must be a decimal number.", 400)
        return_polls = self.logic.get_historical_polls_for_election(election_id, _start_date, _end_date)
        if not return_polls:
            return self.set_msg_or_error([], 0)
        return self.set_msg_or_error(return_polls, 0)

    def getOverallElectionPoll(self, args: dict) -> dict:
        try:
            election_id = args["electionID"]
        except KeyError:
            return self.set_msg_or_error("electionID argument required.", 400)

        election_id = self.convert_id(election_id)
        if not election_id:
            return self.set_msg_or_error("electionId must be a decimal number.", 400)

        election = self.logic.election_logic.get(_id=election_id)
        return self.set_msg_or_error(self.logic.get_overall_election_poll2(election.id), 0)

    def getElectionStatistics(self, args: dict) -> dict:
        desired_args = ["electionID"]
        try:
            req_args = self.get_args_or_key_error(desired_args, args)
        except KeyError as error:
            return self.set_msg_or_error(str(error), 400)

        election_id = self.convert_id(req_args['electionID'])
        if not election_id:
            return self.set_msg_or_error("electionID must be a decimal number.", 400)
        return self.set_msg_or_error(self.logic.get_election_statistics(election_id), 0)

    def getPollPerRegion(self, args: dict) -> dict:
        """Returns all polls for a given region and election
        (i.e, the poll needs to fit both the election and the region).
        Returns an empty array if no polls exist for the region and/or election."""
        # return [Poll]
        # return [] if no polls
        try:
            election_id = args["electionID"]
            region_id = args["regionID"]
        except KeyError:
            return self.set_msg_or_error("Arguments electionID and regionID required.", 400)

        election_id = self.convert_id(election_id)
        region_id = self.convert_id(region_id)
        if not election_id or not region_id:
            return self.set_msg_or_error("Arguments electionID and regionID must be decimal numbers", 400)

        election = self.logic.election_logic.get(_id=election_id)
        region = self.logic.region_logic.get(_id=region_id)

        if not election:
            return self.set_msg_or_error("Election with given ID doesn't exist.", 404)
        if not region:
            return self.set_msg_or_error("Region with given ID doesn't exist", 404)
        return self.set_msg_or_error(self.logic.get_poll_per_region(election, region), 0)

    def getAveragePoll(self, args: dict) -> dict:
        desired_args = ['electionID']
        try:
            req_args = self.get_args_or_key_error(desired_args, args)
        except KeyError as error:
            return self.set_msg_or_error(str(error), 400)

        election_id = self.convert_id(req_args['electionID'])
        if not election_id:
            return self.set_msg_or_error("electionID must be a decimal number.", 400)

        election = self.logic.election_logic.get(_id=election_id)

        if not election:
            return self.set_msg_or_error("Election with given ID doesn't exist", 404)
        return self.set_msg_or_error(self.logic.get_average_poll(election), 0)

    def getPollWithImageSource(self, args: dict) -> dict:
        desired_args = ["pollID"]
        try:
            args = self.get_args_or_key_error(desired_args, args)
        except KeyError as error:
            return self.set_msg_or_error(str(error), 400)

        poll_id = self.convert_id(args['pollID'])
        if not poll_id:
            return self.set_msg_or_error("pollID must be a number.", 400)

        poll = self.logic.get(poll_id)
        if not poll:
            return self.set_msg_or_error("Poll with given ID does not exist.", 404)

        json_poll = self.logic.jsonify_with_candidate_image(poll)
        return self.set_msg_or_error(json_poll, 0)


class PollVoteInterface(Interface):
    def __init__(self):
        super().__init__()
