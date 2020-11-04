from app.data_layer.models.election_candidate_model import ElectionCandidateModel
from app.data_layer.models.election_region_model import ElectionRegionModel
from app.data_layer.models.candidate_model import CandidateModel
from app.data_layer.models.poll_vote_model import PollVoteModel
from app.data_layer.models.election_model import ElectionModel
from app.data_layer.models.region_model import RegionModel
from app.data_layer.models.source_model import SourceModel
from app.data_layer.models.poll_model import PollModel
from app.logic_layer.poll_vote_ll import PollVoteLogic
from app.logic_layer.poll_ll import PollLogic
import unittest


class TestPoll(unittest.TestCase):
    def setUp(self) -> None:
        self.poll_logic = PollLogic()
        self.poll_vote_logic = PollVoteLogic()
        self.region_1 = self.poll_logic.region_logic.add(
            RegionModel(id=None, name="Alabama", population=2550000, registeredVoters=1400000))
        self.region_2 = self.poll_logic.region_logic.add(
            RegionModel(id=None, name="Alaska", population=2550000, registeredVoters=1400000))
        self.source = self.poll_logic.source_logic.add(
            SourceModel(id=None, name="Santa's elves", info="Lots of data"))
        self.candidate_1 = self.poll_logic.candidate_logic.add(
            CandidateModel(id=None, name="Santa", image_url="https://santa.com/img-1", info="I'm nice"))
        self.candidate_2 = self.poll_logic.candidate_logic.add(
            CandidateModel(id=None, name="Clause", image_url="http://clause.com/img-2", info="I'm evil"))
        self.election = self.poll_logic.election_logic.add(
            ElectionModel(id=None, name="Santa Clause's 'good boy this year' election"))
        self.poll = self.poll_logic.add(
            PollModel(id=None, election_id=self.election.id, source_id=self.source.id,
                      start_date="2020-12-24", end_date="2020-12-27"))
        self.election_region_1 = self.poll_logic.election_region_logic.add(
            ElectionRegionModel(id=None, election_id=self.election.id, region_id=self.region_1.id))
        self.election_region_2 = self.poll_logic.election_region_logic.add(
            ElectionRegionModel(id=None, election_id=self.election.id, region_id=self.region_2.id))
        self.election_candidate_1 = self.poll_logic.election_candidate_logic.add(
            ElectionCandidateModel(id=None, election_id=self.election.id, candidate_id=self.candidate_1.id))
        self.election_candidate_2 = self.poll_logic.election_candidate_logic.add(
            ElectionCandidateModel(id=None, election_id=self.election.id, candidate_id=self.candidate_2.id))
        self.poll_vote_1 = self.poll_logic.poll_vote_logic.add(
            PollVoteModel(id=None, poll_id=self.poll.id, candidate_id=self.candidate_1.id, region_id=self.region_1.id))
        self.poll_vote_2 = self.poll_logic.poll_vote_logic.add(
            PollVoteModel(id=None, poll_id=self.poll.id, candidate_id=self.candidate_2.id, region_id=self.region_1.id))
        self.poll_vote_3 = self.poll_logic.poll_vote_logic.add(
            PollVoteModel(id=None, poll_id=self.poll.id, candidate_id=self.candidate_1.id, region_id=self.region_2.id))
        self.poll_vote_4 = self.poll_logic.poll_vote_logic.add(
            PollVoteModel(id=None, poll_id=self.poll.id, candidate_id=self.candidate_2.id, region_id=self.region_2.id))

    def test_get_all_polls(self):
        json_poll_data = self.poll_logic.get_polls()
        self.assertEqual(type(json_poll_data), list)
        self.assertEqual(type(json_poll_data[0]), dict)
        poll_exists = False
        test_poll = None
        for json_poll in json_poll_data:
            if json_poll["pollID"] == str(self.poll.id):
                poll_exists = True
                test_poll = json_poll
        self.assertEqual(poll_exists, True)

        if test_poll:
            # Not really great testing, try not to do this :)
            self.assertEqual(test_poll["organization"], "Santa's elves")
            self.assertEqual(test_poll["election"]["electionID"], str(self.election.id))
            self.assertEqual(test_poll["election"]["name"], "Santa Clause's 'good boy this year' election")
            self.assertEqual(test_poll["election"]["regions"][0]["regionID"], str(self.region_1.id))
            self.assertEqual(test_poll["dataArray"][0]["region"]["regionID"], str(self.region_1.id))
            self.assertEqual(test_poll["dataArray"][0]["region"]["name"], self.region_1.name)
            self.assertEqual(test_poll["dataArray"][0]["data"][0]["votes"], 1)
            self.assertEqual(test_poll["dataArray"][0]["data"][0]["candidate"]["name"], self.candidate_1.name)

    def test_safe_delete_election(self):
        self.poll_logic.safe_delete_election(self.election.id)
        none_vote = self.poll_vote_logic.get(self.poll_vote_1.id)
        none_poll = self.poll_logic.get(self.poll.id)
        none_election_region = self.poll_logic.election_region_logic.get(self.election_region_1.id)
        none_election_candidate = self.poll_logic.election_candidate_logic.get(self.election_candidate_1.id)
        self.assertEqual(none_vote, None)
        self.assertEqual(none_poll, None)
        self.assertEqual(none_election_region, None)
        self.assertEqual(none_election_candidate, None)

    def test_get_poll(self):
        poll_id = self.poll.id
        test_poll = self.poll_logic.get_poll(poll_id)
        self.assertEqual(type(test_poll), dict)
        self.assertEqual(test_poll["pollID"], str(poll_id))

    def test_error_get_poll(self):
        test_poll = self.poll_logic.get_poll(0)
        self.assertEqual(test_poll, None)

    def test_get_poll_end_date(self):
        end_date = self.poll_logic.get_poll_end_date(self.poll.id)
        self.assertEqual(end_date["end_date"], self.poll.end_date)

    def test_get_overall_election(self):
        overall_data = self.poll_logic.get_overall_election_poll(self.election.id)
        self.assertEqual(overall_data[self.candidate_1.name], 2)
        self.assertEqual(overall_data[self.candidate_2.name], 2)

    def test_get_election_statistics(self):
        statistics = self.poll_logic.get_election_statistics(self.election.id)
        self.assertEqual(statistics[self.candidate_1.name], '50.0%')
        self.assertEqual(statistics[self.candidate_2.name], '50.0%')

    def test_get_polls_in_election(self):
        election_id = self.election.id
        polls = self.poll_logic.get_polls_in_election(election_id=election_id)
        self.assertEqual(len(polls), 1)
        self.assertEqual(type(polls), list)
        self.assertEqual(type(polls[0]), PollModel)
        poll_in_election = True
        for poll in polls:
            if poll.election_id != election_id:
                poll_in_election = False
        self.assertEqual(poll_in_election, True)

    def test_get_polls_from_source_name(self):
        polls = self.poll_logic.get_polls_from_source_name(self.source.name)
        self.assertEqual(polls["pollID"], str(self.poll.id))

    def test_error_get_polls_from_source_name(self):
        polls = self.poll_logic.get_polls_from_source_name("DefinitelyNotASourceName")
        self.assertEqual(polls, None)

    def test_error_get_polls_in_election(self):
        polls = self.poll_logic.get_polls_in_election(election_id=0)
        self.assertEqual(polls, None)

    def test_get_polls_from_specific_time_frame(self):
        polls = self.poll_logic.get_polls_from_specific_time_frame(self.poll.start_date, self.poll.end_date)
        if type(polls) == dict:
            self.assertEqual(polls["pollID"], str(self.poll.id))
        else:
            self.assertEqual(type(polls), list)
            poll_exists = False
            for poll in polls:
                if poll["pollID"] == str(self.poll.id):
                    poll_exists = True
            self.assertEqual(poll_exists, True)

    def test_get_all_votes_on_poll_candidate(self):
        votes = self.poll_vote_logic.get_all_votes_on_poll_candidate(self.poll.id, self.candidate_1.id, _count=True)
        self.assertEqual(votes, 2)

    def test_get_all_poll_votes_in_region(self):
        votes = self.poll_vote_logic.get_all_poll_votes_in_region(self.poll.id, self.region_1.id, _count=True)
        self.assertEqual(votes, 2)

    def test_get_all_poll_votes_on_candidate_in_region(self):
        votes = self.poll_vote_logic.get_all_poll_votes_on_candidate_in_region(poll_id=self.poll.id, candidate_id=
                                                                               self.candidate_1.id, region_id=
                                                                               self.region_1.id, _count=True)
        self.assertEqual(votes, 1)

    def test_get_vote_option(self):
        vote_option = self.poll_vote_logic.get_vote_option(self.poll_vote_1.id)
        self.assertEqual(vote_option, self.poll_vote_1.candidate_id)

    def test_get_poll_per_region(self):
        poll_id = self.poll.id
        test_poll = self.poll_logic.get_poll_per_region(self.election, self.region_1)
        self.assertEqual(type(test_poll), dict)
        self.assertEqual(test_poll["pollID"], str(poll_id))

    def test_get_average_poll(self):
        average_poll = self.poll_logic.get_average_poll(self.election)
        self.assertEqual(type(average_poll), dict)
        self.assertEqual(average_poll.get('dataArray')[0].get('data')[0].get('votes'), 1.0)

    def test_get_votes_in_election_per_region(self):
        regions = [self.region_1.id, self.region_2.id]
        votes = self.poll_vote_logic.get_votes_in_election_per_region(regions, self.election.id)
        self.assertEqual(type(votes), dict)
        self.assertEqual(votes.get(self.region_1.id).get(self.candidate_1.id), 1)
        self.assertEqual(votes.get(self.region_2.id).get(self.candidate_2.id), 1)

    def test_get_all_by_election_and_region(self):
        votes = self.poll_vote_logic.get_all_by_election_and_region(self.region_1.id, self.election.id)
        self.assertEqual(type(votes), dict)
        self.assertEqual(votes.get(self.candidate_1.id), 1)
        self.assertEqual(votes.get(self.candidate_2.id), 1)

    def tearDown(self) -> None:
        self.poll_logic.region_logic.safe_delete(_id=self.region_1.id)
        self.poll_logic.region_logic.safe_delete(_id=self.region_2.id)
        self.poll_logic.source_logic.safe_delete(_id=self.source.id)
        self.poll_logic.candidate_logic.safe_delete(_id=self.candidate_1.id)
        self.poll_logic.candidate_logic.safe_delete(_id=self.candidate_2.id)
        # Replaces old delete methods for election_region, election_candidate,
        # poll and poll_vote when deleting an election
        self.poll_logic.safe_delete_election(self.election.id)


if __name__ == '__main__':
    unittest.main()
