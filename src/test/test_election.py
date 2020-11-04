import unittest
from app.logic_layer.election_ll import ElectionLogic
from app.data_layer.data.election_data import ElectionModel, ElectionData
from app.data_layer.data.candidate_data import CandidateModel
from app.logic_layer.candidate_ll import CandidateLogic
from app.logic_layer.election_candidate_ll import ElectionCandidateLogic
from app.data_layer.models.election_candidate_model import ElectionCandidateModel


class TestElectionLogic(unittest.TestCase):
    def setUp(self):
        self.election_logic = ElectionLogic()
        self.candidate = CandidateLogic()
        self.election_can = ElectionCandidateLogic()
        self.election_data = ElectionData()
        self.model_candidate1 = CandidateModel(None, 'Peter', 'URL', 'Vote for me')
        self.model_candidate2 = CandidateModel(None, 'Gigi', 'URL', 'I rock')
        self.model_election = ElectionModel(None, 'Election test')
        self.election_logic.add(self.model_election)
        self.candidate.add(self.model_candidate1)
        self.candidate.add(self.model_candidate2)
        self.model_election_can = ElectionCandidateModel(None, self.model_candidate1.id, self.model_election.id)
        self.model_election_can2 = ElectionCandidateModel(None, self.model_candidate2.id, self.model_election.id)
        self.election_can.add(self.model_election_can)
        self.election_can.add(self.model_election_can2)
        self.model_candidate1_jsonify = self.candidate.jsonify(self.model_candidate1)
        self.model_candidate2_jsonify = self.candidate.jsonify(self.model_candidate2)

    def tearDown(self):
        self.candidate.delete(self.model_candidate1.id)
        self.candidate.delete(self.model_candidate2.id)
        self.election_logic.delete(self.model_election.id)
        self.election_can.delete(self.model_election_can.id)
        self.election_can.delete(self.model_candidate2.id)

    def test_get_election_by_id(self):
        election = self.election_logic.get_election(self.model_election.id)
        self.assertEqual(election, self.election_logic.jsonify(self.model_election))
        self.assertEqual(type(election), dict)

    def test_get_error_election(self):
        election = self.election_logic.get_election(999)
        self.assertEqual(election, None)
        election = self.election_logic.get_election('string')
        self.assertEqual(election, None)

    def test_get_all_elections(self):
        elections = self.election_logic.get_elections()
        self.assertEqual(type(elections), list)
        self.assertGreaterEqual(len(elections), 1)
        for x in elections:
            self.assertEqual(type(x), dict)

    def test_get_election_by_name(self):
        election = self.election_logic.get_election_by_name("Election test")
        self.assertEqual(type(election), dict)
        self.assertEqual(election, self.election_logic.jsonify(self.model_election))
        self.assertNotEqual(election, None)

    def test_get_error_election_by_name(self):
        election = self.election_logic.get_election_by_name("")
        self.assertEqual(election, None)
        self.assertNotEqual(type(election), dict)
        self.assertNotEqual(election, self.election_logic.jsonify(self.model_election))
        election = self.election_logic.get_election_by_name(1)
        self.assertEqual(election, None)
        self.assertNotEqual(type(election), dict)
        self.assertNotEqual(election, self.election_logic.jsonify(self.model_election))


if __name__ == '__main__':
    unittest.main()
