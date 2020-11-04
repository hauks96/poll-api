import copy

from app.data_layer.models.poll_vote_model import PollVoteModel
from app.logic_layer.election_candidate_ll import ElectionCandidateLogic
from app.logic_layer.election_region_ll import ElectionRegionLogic
from app.logic_layer.candidate_ll import CandidateLogic
from app.logic_layer.logic import Logic


class PollVoteLogic(Logic):
    def __init__(self):
        super().__init__()
        self.candidate_logic = CandidateLogic()
        self.election_candidate_logic = ElectionCandidateLogic()
        self.election_region_logic = ElectionRegionLogic()

    def vote(self, region_id, poll_id, electable_id) -> None:
        new_model = PollVoteModel(id=None, region_id=region_id, poll_id=poll_id, candidate_id=electable_id)
        self.add(new_model)

    def delete_poll_votes(self, poll_id) -> None:
        data = self.get_all()
        new_data = []
        for i in range(len(data)):
            if data[i].poll_id != poll_id:
                new_data.append(data[i])

        self.save(new_data)
        return

    def get_vote_option(self, vote_id):
        """Return the choice of the voter"""
        data = self.get_all()
        for vote in data:
            if vote.id == vote_id:
                return vote.candidate_id
        return None

    def get_poll_from_vote(self, vote_id):
        data = self.get_all()
        for vote in data:
            if vote.id == vote_id:
                return vote.region_id
        return None

    def get_all_by_poll(self, poll_id, _count=False):
        """Returns all vote objects on specific poll"""
        poll_votes = []
        data = self.get_all()
        for vote in data:
            if vote.poll_id == poll_id:
                poll_votes.append(vote)
        if _count:
            return len(poll_votes)
        return poll_votes

    def get_all_by_election_and_region(self, region_id, election_id):
        """Returns the votes in a election for candidates in the given region"""
        vote_list = {}
        data = self.get_all()
        candidate_data = self.election_candidate_logic.get_candidates_in_election(election_id)
        for vote in data:
            if vote.region_id == region_id and self.candidate_logic.get(vote.candidate_id) in candidate_data:
                if vote.candidate_id not in vote_list:
                    vote_list[vote.candidate_id] = 1
                else:
                    vote_list[vote.candidate_id] += 1
        return vote_list

    def get_all_votes_on_poll_candidate(self, poll_id, candidate_id, _count=False):
        """Returns all votes on a poll on a specific Candidate"""
        poll_votes_on_candidate = []
        data = self.get_all()
        for vote in data:
            if vote.poll_id == poll_id and vote.candidate_id == candidate_id:
                poll_votes_on_candidate.append(vote)

        if _count:
            return len(poll_votes_on_candidate)
        return poll_votes_on_candidate

    def get_votes_in_election_per_region(self, regions, election_id):
        """Returns a dictionary with votes for each candidate in the region """
        region_votes = {}
        for i in regions:
            if i not in region_votes:
                region_votes[i] = self.get_all_by_election_and_region(i, election_id)
        return region_votes

    def get_all_poll_votes_in_region(self, poll_id, region_id, _count=False):
        """Returns all votes on a poll for a specific region"""
        poll_votes_on_region = []
        data = self.get_all()
        for vote in data:
            if vote.poll_id == poll_id and vote.region_id == region_id:
                poll_votes_on_region.append(vote)
        if _count:
            return len(poll_votes_on_region)
        return poll_votes_on_region

    def get_all_poll_votes_on_candidate_in_region(self, poll_id, candidate_id, region_id, _count=False):
        """Returns all votes in a poll that were on a specific candidate in a specific region"""
        poll_votes_on_region_candidate = []
        data = self.get_all()
        for vote in data:
            if vote.poll_id == poll_id and vote.region_id == region_id and vote.candidate_id == candidate_id:
                poll_votes_on_region_candidate.append(vote)
        if _count:
            return len(poll_votes_on_region_candidate)
        return poll_votes_on_region_candidate

    def jsonify(self, poll_model):
        """Enter a poll model. This returns the equivalent of regionPoll in the interface"""
        models = self.get_all_by_poll(poll_model.id)
        json_list = []
        if not models:
            return []

        if type(models) != list:
            models = [models]

        poll_candidates = self.election_candidate_logic.get_candidates_in_election(election_id=poll_model.election_id)
        poll_regions = self.election_region_logic.get_election_regions(_id=poll_model.election_id)

        hash_bucket_counter = {}
        candidate_dicts = {}
        # building a candidate dictionary to put into hack bucket
        for candidate in poll_candidates:
            candidate_dicts[candidate.id] = {"candidate": self.election_candidate_logic.jsonify(candidate), "votes": 0}

        # Building a has bucket
        for region in poll_regions:
            hash_bucket_counter[region.id] = copy.deepcopy(candidate_dicts)

        # Iterating only once over all votes to distribute them into the correct region / candidate
        for model in models:
            # If not all poll id's are the same
            if model.poll_id != poll_model.id:
                raise KeyError("ALL VOTES ENTERED IN THE VOTE JSONIFY MUST HAVE SAME POLL ID")

            try:
                # Count vote for desired region and candidate
                hash_bucket_counter[model.region_id][model.candidate_id]["votes"] += 1
            except KeyError:
                # If vote data is flawed raise error
                for region in poll_regions:
                    if model.region_id == region.id:
                        raise KeyError("The election for which vote " + str(model.id) + " is, does not contain candidate "
                                       + str(model.candidate_id))

                raise KeyError("The election for which vote " + str(model.id) + " is, does not contain region "
                               + str(model.region_id))

        # Set it up into the requested format
        for region in poll_regions:
            poll_vote_data_array = {
                'region': self.election_region_logic.jsonify(region),
                'data': self.create_data_array(hash_bucket_counter[region.id])
            }
            json_list.append(poll_vote_data_array)
        if len(json_list) == 1:
            return json_list[0]

        return json_list

    @staticmethod
    def create_data_array(hash_bucket_region):
        data = []
        for key in hash_bucket_region:
            data.append(hash_bucket_region[key])
        return data


if __name__ == '__main__':
    pass
