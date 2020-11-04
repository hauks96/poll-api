import unittest
from app.logic_layer.election_candidate_ll import ElectionCandidateLogic
from app.logic_layer.candidate_ll import CandidateLogic
from app.logic_layer.election_ll import ElectionLogic
from app.data_layer.models.election_candidate_model import ElectionCandidateModel
from app.data_layer.models.election_model import ElectionModel
from app.data_layer.models.candidate_model import CandidateModel


class TestElectionCandidateLogic(unittest.TestCase):
    def setUp(self):
        self.election = ElectionLogic()
        self.candidate = CandidateLogic()
        self.election_can = ElectionCandidateLogic()
        self.model_candidate1 = self.candidate.add(CandidateModel(None, 'Peter', 'URL', 'Vote for me'))
        self.model_candidate2 = self.candidate.add(CandidateModel(None, 'Gigi', 'URL', 'I rock'))
        self.model_election = self.election.add(ElectionModel(None, 'Election test'))
        self.model_election_can = self.election_can.add(
            ElectionCandidateModel(None, self.model_candidate1.id, self.model_election.id))
        self.model_election_can2 = self.election_can.add(ElectionCandidateModel(
            None, self.model_candidate2.id, self.model_election.id))

    def test_get_candidates_in_poll(self):
        candidates_in_poll = self.election_can.get_candidates_in_election(self.model_election.id)
        self.assertEqual(type(candidates_in_poll), list)
        id_lst = []
        for candidate in candidates_in_poll:
            id_lst.append(candidate.id)

        if self.model_candidate1.id not in id_lst:
            self.assertEqual(True, False)
        if self.model_candidate2.id not in id_lst:
            self.assertEqual(True, False)

    def test_get_error_candidates_in_poll(self):
        candidates_in_poll = self.election_can.get_candidates_in_election(0)
        self.assertEqual(candidates_in_poll, [])

    def tearDown(self):
        self.candidate.delete(self.model_candidate1.id)
        self.candidate.delete(self.model_candidate2.id)
        self.election.delete(self.model_election.id)
        self.election_can.delete(self.model_election_can.id)
        self.election_can.delete(self.model_election_can2.id)


if __name__ == '__main__':
    unittest.main()
