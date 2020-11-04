from app.logic_layer.election_candidate_ll import ElectionCandidateLogic
from app.logic_layer.candidate_ll import CandidateLogic
from app.logic_layer.election_ll import ElectionLogic
from app.logic_layer.election_region_ll import ElectionRegionLogic
from app.logic_layer.poll_vote_ll import PollVoteLogic
from app.logic_layer.region_ll import RegionLogic
from app.logic_layer.source_ll import SourceLogic
from app.logic_layer.logic import Logic
from datetime import date
import json


class PollLogic(Logic):
    def __init__(self):
        super().__init__()
        self.poll_vote_logic = PollVoteLogic()
        self.candidate_logic = CandidateLogic()
        self.election_candidate_logic = ElectionCandidateLogic()
        self.election_region_logic = ElectionRegionLogic()
        self.election_logic = ElectionLogic()
        self.source_logic = SourceLogic()
        self.region_logic = RegionLogic()

    def safe_delete_election(self, election_id):
        """Safely remove election. Removes all objects that depend on the election being deleted.
        Had to put it in logic layer because of circular import if placed in election... This would not be a
        problem if jsonify didn't need election logic...
        We should consider making jsonify a separate entity e.g Adapter"""

        election_candidate_logic = ElectionCandidateLogic()
        election_region_logic = ElectionRegionLogic()
        # Delete related election_candidate relations
        election_candidate_logic.delete_election_candidates(election_id=election_id)
        # Delete related election_region relations
        election_region_logic.delete_election_regions(election_id=election_id)
        # Delete related polls (Polls deletes votes)
        self.delete_election_polls(election_id=election_id)

        # Delete election
        removed = self.election_logic.delete(election_id)
        return removed

    @staticmethod
    def validate_date(x_date: str):
        try:
            iso_date = date.fromisoformat(x_date)
            return True
        except ValueError:
            return False

    def delete_election_polls(self, election_id):
        data = self.get_polls_in_election(election_id=election_id)
        poll_ids_in_election = []
        if not data:
            return

        for e_poll in data:
            poll_ids_in_election.append(e_poll.id)
            if e_poll.election_id == election_id:
                self.poll_vote_logic.delete_poll_votes(e_poll.id)

        polls = self.get_all()
        new_polls = []
        for e_poll in polls:
            if e_poll.id not in poll_ids_in_election:
                new_polls.append(e_poll)

        self.save(new_polls)

    def safe_delete(self, _id):
        """Safely remove object. Removes all objects that depend on the object being deleted"""
        data = self.get_all()
        removed = None
        for i in range(len(data)):
            if data[i].id == _id:
                # Deleting related poll votes
                self.poll_vote_logic.delete_poll_votes(data[i].id)
                removed = data.pop(i)
                break

        self.save(data)
        return removed

    def get_poll(self, _id):
        """Returns specific poll jsonified"""
        this_poll = self.get(_id)
        if this_poll:
            return self.jsonify(this_poll)
        return None

    def get_polls_in_election(self, election_id):
        """ Returns all the polls in the given election as models"""
        election_poll_list = []
        data = self.get_all()
        for poll in data:
            if poll.election_id == election_id:
                election_poll_list.append(poll)
        if len(election_poll_list) == 0:
            return None
        return election_poll_list

    def get_poll_end_date(self, _id):
        """Returns the end date of a specific poll as a dictionary
        {'end_date': poll_with_id.end_date} or None"""
        poll = self.get(_id)
        if poll:
            return {'end_date': poll.end_date}
        return None

    def get_poll_per_region(self, election, region):
        """ Returns all polls in the region from the given election. Gets all the polls and
         excludes the one that are not from the election and don't have any votes from the region.
         RETURNS IN JSONIFIED FORMAT"""
        all_polls = self.get_polls_in_election(election.id)
        poll_list = []
        for poll in all_polls:
            votes_in_poll = self.poll_vote_logic.get_all_by_poll(poll.id)
            for vote in votes_in_poll:
                if vote.region_id == region.id and poll not in poll_list:
                    poll_list.append(poll)
        return self.jsonify(poll_list)

    def get_polls(self):
        """Returns all polls in jsonified format"""
        return self.jsonify(self.get_all())

    def get_overall_election_poll(self, election_id):
        """Returns the overall poll result of a specific election in the form {'candidate': number of votes from all
        the polls} """
        polls_in_election = self.get_polls_in_election(election_id)
        votes_in_election = []
        if polls_in_election:
            for poll in polls_in_election:
                votes_in_poll = self.poll_vote_logic.get_all_by_poll(poll.id)
                if votes_in_poll:
                    votes_in_election.append(votes_in_poll)
            if len(polls_in_election) == 0:
                return {}

            votes_in_election = [item for elem in votes_in_election for item in elem]
            election_result = {}
            for vote in votes_in_election:
                candidate_id = self.poll_vote_logic.get_vote_option(vote.id)
                candidate = self.candidate_logic.get(candidate_id)
                if candidate:
                    if candidate.name not in election_result.keys():
                        election_result[candidate.name] = 1
                    else:
                        election_result[candidate.name] += 1
            return election_result
        return None

    def get_overall_election_poll2(self, election_id):
        """Returns the overall poll result of a specific election in the form of a poll"""
        polls_in_election = self.get_polls_in_election(election_id)
        if not polls_in_election:
            return None

        if type(polls_in_election) is not list:
            polls_in_election = [polls_in_election]

        polls_json = self.jsonify_with_candidate_image(polls_in_election)

        first_poll = polls_json[0]
        first_poll["pollID"] = 0
        for i in range(1, len(polls_json)):
            fp_data_array = first_poll["dataArray"]
            data_array = polls_json[i]['dataArray']
            for y in range(len(data_array)):
                fp_region_data = fp_data_array[y]
                region_data = data_array[y]
                data = region_data['data']
                fp_data = fp_region_data['data']
                for z in range(len(data)):
                    votes = data[z]['votes']
                    fp_data[z]['votes'] += votes

        return first_poll

    def _get_region_in_election(self, election_id):
        """Returns a list of the regions that have votes in the election"""
        regions = []
        data = self.get_all()
        for poll in data:
            if poll.election_id == election_id:
                votes = self.poll_vote_logic.get_all_by_poll(poll.id)
                for vote in votes:
                    if vote.region_id not in regions:
                        regions.append(vote.region_id)
        return regions

    def get_average_poll(self, election):
        """Returns a single poll object with the average votes on electable for the election.
         Method jsonify the poll from the election.
          gets all the votes from from each region that participated in the any poll in the election.
           divides the votes with number of polls """
        polls = self.get_polls_in_election(election.id)
        regions_in_election = self._get_region_in_election(election.id)
        votes_per_region = self.poll_vote_logic.get_votes_in_election_per_region(regions_in_election, election.id)
        polls_jsons = self.jsonify(polls)
        if type(polls_jsons) != list:
            polls_jsons = [polls_jsons]
        for model in polls_jsons:
            if model.get('dataArray'):
                for obj in model['dataArray']:
                    try:
                        region_id = obj.get('region')['regionID']
                        candidate = int(obj.get('data')[0]['candidate']['electableID'])
                        average_vote = round(votes_per_region.get(int(region_id))[candidate]/len(polls_jsons), 2)
                        obj.get('data')[0]['votes'] = average_vote
                    except:
                        pass # object is not vote related, then pass

        if type(polls_jsons) == list:
            return polls_jsons[0]
        return polls_jsons

    def get_election_statistics(self, election_id):
        """Returns how many votes, in percentage each candidate holds for a given election"""
        results = self.get_overall_election_poll(election_id)
        total_votes = 0
        election_statistics = {}
        for value in results.values():
            total_votes += value
        for key, value in results.items():
            election_statistics[key] = str(value/total_votes * 100) + '%'
        return election_statistics

    def get_polls_from_source_name(self, source_name):
        """Returns a list of polls with a given source name. Returns None if nothing found.
        Accounts for lower case name search and partial name search (using if str in target function)
        Returns jsonified polls"""
        source = self.source_logic.get_source_by_name(source_name)
        polls = []

        if not source:
            return None

        for _poll in self.get_all():
            if _poll.source_id == source.id:
                polls.append(_poll)

        if polls:
            return self.jsonify(polls)
        return None

    def get_polls_from_specific_time_frame(self, start_date, end_date):
        """"Returns polls that were performed in the time between begin_date and end_date.
        Uses the 'fromisoformat' method, requiring input to be in the format: 2020-10-25.
        Returns list of jsonified poll objects.
        Returns None if nothing found."""
        return_polls = []
        _start_date = date.fromisoformat(start_date)
        _end_date = date.fromisoformat(end_date)
        for x in self.get_all():
            if _start_date <= date.fromisoformat(x.start_date) and _end_date >= date.fromisoformat(
                    x.end_date):
                return_polls.append(x)

        if not return_polls:
            return None
        return self.jsonify(return_polls)

    def get_historical_polls_for_election(self, election_id, start_date, end_date):
        """Returns polls from a specific election in a specific time frame.
        Uses the 'fromisoformat' method, requiring input to be in the format: 2020-10-25.
        Returns list of jsonified poll objects or None if nothing found."""

        return_polls = []
        election = self.election_logic.get_election(election_id)
        designated_begin_date = date.fromisoformat(start_date)
        designated_end_date = date.fromisoformat(end_date)

        for x in self.get_all():
            if designated_begin_date <= date.fromisoformat(x.start_date) and designated_end_date >= date.fromisoformat(
                    x.end_date):
                if str(x.election_id) == str(election_id):
                    return_polls.append(x)

        if not return_polls:
            return None
        return self.jsonify(return_polls)


    def jsonify(self, models):
        json_list = []
        if not models:
            return []

        if type(models) != list:
            models = [models]

        for model in models:
            election = self.election_logic.get(model.election_id)
            source = self.source_logic.get(model.source_id)
            poll_data = {
                'pollID': str(model.id),
                'election': self.election_logic.jsonify(election),
                'organization': self.source_logic.jsonify(source),
                'startDate': model.start_date,
                'endDate': model.end_date,
                "dataArray": self.poll_vote_logic.jsonify(model)
            }
            json_list.append(poll_data)

        if len(json_list) == 1:
            return json_list[0]

        return json_list

    def jsonify_with_candidate_image(self, models):
        json_list = []
        if not models:
            return []

        if type(models) != list:
            models = [models]

        for model in models:
            election = self.election_logic.get(model.election_id)
            source = self.source_logic.get(model.source_id)
            poll_data = {
                'pollID': str(model.id),
                'election': self.election_logic.jsonify_with_candidate_image(election),
                'organization': self.source_logic.jsonify(source),
                'startDate': model.start_date,
                'endDate': model.end_date,
                "dataArray": self.poll_vote_logic.jsonify(model)
            }
            json_list.append(poll_data)

        if len(json_list) == 1:
            return json_list[0]

        return json_list


if __name__ == '__main__':
    pass
