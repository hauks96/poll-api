import unittest
from app.auth.auth import Auth
from app.auth.exceptions.auth_exception import AuthenticationFailed, InvalidUserCreation, AuthRelationCreationFailed, \
    VoteFailed
from app.interface_layer.candidate_interface import CandidateInterface
from app.interface_layer.election_interface import ElectionInterface
from app.interface_layer.poll_interface import PollInterface, PollVoteInterface
from app.interface_layer.region_interface import RegionInterface
from app.logic_layer.region_ll import RegionLogic


class TestAuthentication(unittest.TestCase):
    def setUp(self) -> None:
        self.auth = Auth()
        self.user_credentials = {"username": "usertest69", "password": "usertest69", "firstName": "Peter",
                                 "lastName": "Tester", "ssn": "88888888", "regionID": "1"}
        self.auth.createUser(self.user_credentials)
        self.region_logic = RegionLogic()

    def test_login(self):
        self.auth.login(self.user_credentials["username"], self.user_credentials["password"])
        self.assertEqual(self.auth.logged_in, True)

    def test_error_login(self):
        with self.assertRaises(AuthenticationFailed):
            self.auth.login("definitely not a username",
                            "definitely not a password")

    def test_error_createUser(self):
        with self.assertRaises(InvalidUserCreation):
            self.auth.createUser(self.user_credentials)

    def test_logout(self):
        self.auth.login(self.user_credentials["username"], self.user_credentials["password"])
        self.auth.logout()
        self.assertEqual(False, self.auth.logged_in)

    def test_create_election_relation(self):
        self.auth.login(self.user_credentials["username"], self.user_credentials["password"])
        self.auth.create_auth_relation(ElectionInterface, 1)  # Doesn't throw error means it works.
        self.assertEqual(len(self.auth.user_creations(ElectionInterface)), 1)
        # Raises AuthRelationCreationFailed error since relation already exists
        with self.assertRaises(AuthRelationCreationFailed):
            self.auth.create_auth_relation(ElectionInterface, 1)

    def test_create_poll_relation(self):
        self.auth.login(self.user_credentials["username"], self.user_credentials["password"])
        self.auth.create_auth_relation(PollInterface, 1)  # Doesn't throw error means it works.
        self.assertEqual(len(self.auth.user_creations(PollInterface)), 1)
        # Raises AuthRelationCreationFailed error since relation already exists
        with self.assertRaises(AuthRelationCreationFailed):
            self.auth.create_auth_relation(PollInterface, 1)

    def test_create_candidate_relation(self):
        self.auth.login(self.user_credentials["username"], self.user_credentials["password"])
        self.auth.create_auth_relation(CandidateInterface, 1)  # Doesn't throw error means it works.
        self.assertEqual(len(self.auth.user_creations(CandidateInterface)), 1)
        # Raises AuthRelationCreationFailed error since relation already exists
        with self.assertRaises(AuthRelationCreationFailed):
            self.auth.create_auth_relation(CandidateInterface, 1)

    def test_create_region_relation(self):
        self.auth.login(self.user_credentials["username"], self.user_credentials["password"])
        self.auth.create_auth_relation(RegionInterface, 1)  # Doesn't throw error means it works.
        self.assertEqual(len(self.auth.user_creations(RegionInterface)), 1)
        # Raises AuthRelationCreationFailed error since relation already exists
        with self.assertRaises(AuthRelationCreationFailed):
            self.auth.create_auth_relation(RegionInterface, 1)

    def test_create_vote_relation(self):
        self.auth.login(self.user_credentials["username"], self.user_credentials["password"])
        self.auth.create_auth_relation(PollVoteInterface, 1)  # Doesn't throw error means it works.
        self.assertEqual(len(self.auth.user_creations(PollVoteInterface)), 1)
        # Raises AuthRelationCreationFailed error since relation already exists
        with self.assertRaises(VoteFailed):
            self.auth.create_auth_relation(PollVoteInterface, 1)

    def test_remove_election_relation(self):
        self.auth.login(self.user_credentials["username"], self.user_credentials["password"])
        self.auth.create_auth_relation(ElectionInterface, 1)
        self.auth.remove_auth_relation(ElectionInterface, 1)
        self.assertEqual(len(self.auth.user_creations(ElectionInterface)), 0)

    def test_remove_poll_relation(self):
        self.auth.login(self.user_credentials["username"], self.user_credentials["password"])
        self.auth.create_auth_relation(PollInterface, 1)
        self.auth.remove_auth_relation(PollInterface, 1)
        self.assertEqual(len(self.auth.user_creations(PollInterface)), 0)

    def test_remove_candidate_relation(self):
        self.auth.login(self.user_credentials["username"], self.user_credentials["password"])
        self.auth.create_auth_relation(CandidateInterface, 1)
        self.auth.remove_auth_relation(CandidateInterface, 1)
        self.assertEqual(len(self.auth.user_creations(CandidateInterface)), 0)

    def test_remove_region_relation(self):
        self.auth.login(self.user_credentials["username"], self.user_credentials["password"])
        self.auth.create_auth_relation(RegionInterface, 1)
        self.auth.remove_auth_relation(RegionInterface, 1)
        self.assertEqual(len(self.auth.user_creations(RegionInterface)), 0)

    def test_remove_poll_vote_relation(self):
        self.auth.login(self.user_credentials["username"], self.user_credentials["password"])
        self.auth.create_auth_relation(PollVoteInterface, 1)
        self.auth.remove_auth_relation(PollVoteInterface, 1)
        self.assertEqual(len(self.auth.user_creations(PollVoteInterface)), 0)

    def test_authorize_update_election(self):
        self.auth.login(self.user_credentials["username"], self.user_credentials["password"])
        self.auth.create_auth_relation(ElectionInterface, 1)
        # If doesn't raise error, then ok
        self.auth.authorize_modification(ElectionInterface, 1)

        # Testing the error case of authorizing modification
        self.auth.remove_auth_relation(ElectionInterface, 1)
        with self.assertRaises(AuthenticationFailed):
            self.auth.authorize_modification(ElectionInterface, 1)

    def test_authorize_update_candidate(self):
        self.auth.login(self.user_credentials["username"], self.user_credentials["password"])
        self.auth.create_auth_relation(CandidateInterface, 1)
        # If doesn't raise error, then ok
        self.auth.authorize_modification(CandidateInterface, 1)

        # Testing the error case of authorizing modification
        self.auth.remove_auth_relation(CandidateInterface, 1)
        with self.assertRaises(AuthenticationFailed):
            self.auth.authorize_modification(CandidateInterface, 1)

    def test_authorize_update_poll(self):
        self.auth.login(self.user_credentials["username"], self.user_credentials["password"])
        self.auth.create_auth_relation(PollInterface, 1)
        # If doesn't raise error, then ok
        self.auth.authorize_modification(PollInterface, 1)

        # Testing the error case of authorizing modification
        self.auth.remove_auth_relation(PollInterface, 1)
        with self.assertRaises(AuthenticationFailed):
            self.auth.authorize_modification(PollInterface, 1)

    def test_authorize_update_region(self):
        self.auth.login(self.user_credentials["username"], self.user_credentials["password"])
        self.auth.create_auth_relation(RegionInterface, 1)
        # If doesn't raise error, then ok
        self.auth.authorize_modification(RegionInterface, 1)

        # Testing the error case of authorizing modification
        self.auth.remove_auth_relation(RegionInterface, 1)
        with self.assertRaises(AuthenticationFailed):
            self.auth.authorize_modification(RegionInterface, 1)

    def tearDown(self) -> None:
        self.auth.login(self.user_credentials["username"], self.user_credentials["password"])
        self.auth.removeAccount(self.user_credentials["username"], self.user_credentials["password"])


if __name__ == '__main__':
    unittest.main()
