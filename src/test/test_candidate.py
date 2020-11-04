import unittest
from app.logic_layer.candidate_ll import CandidateLogic
from app.data_layer.models.candidate_model import CandidateModel


class TestCandidateLogic(unittest.TestCase):
    def setUp(self):
        self.candidate = CandidateLogic()
        self.model1 = CandidateModel(None, 'Peter', 'URL', 'Vote for me')
        self.model2 = CandidateModel(None, 'John', 'URL', 'I am the greatest')
        self.candidate.add(self.model1)
        self.candidate.add(self.model2)

    def test_get_candidates(self):
        candidates = self.candidate.get_candidates()
        self.assertEqual(type(candidates), list)
        self.assertGreaterEqual(len(candidates), 2)

    def test_get_candidate_by_id(self):
        candidate = self.candidate.get_candidate_by_id(self.model1.id)
        self.assertEqual(candidate, self.candidate.jsonify(self.model1))
        self.assertNotEqual(candidate, self.candidate.jsonify(self.model2))

    def test_get_error_candidate_by_id_(self):
        candidate = self.candidate.get_candidate_by_id(850000)
        self.assertEqual(candidate, None)

    def test_get_candidate_by_name(self):
        candidate = self.candidate.get_candidate_by_name("John")
        self.assertEqual(candidate, self.candidate.jsonify(self.model2))
        self.assertNotEqual(candidate, self.candidate.jsonify(self.model1))

    def test_get_error_candidate_by_name(self):
        candidate = self.candidate.get_candidate_by_name("")
        self.assertEqual(candidate, None)

    def tearDown(self):
        self.candidate.delete(self.model1.id)
        self.candidate.delete(self.model2.id)


if __name__ == '__main__':
    unittest.main()
