from app.data_layer.data.data import Data
from app.data_layer.data.election_region_data import ElectionRegionData
from app.data_layer.data.poll_data import PollData
from app.data_layer.data.poll_vote_data import PollVoteData

from app.data_layer.models.election_model import ElectionModel
from app.data_layer.data.election_candidate_data import ElectionCandidateData


# ELECTION IS FOR EXAMPLE US PRESIDENTIAL ELECTION 2020
class ElectionData(Data):
    def __init__(self):
        super().__init__()
        self.data_path = self.get_filepath("../json_data/election_data.json")
        self.idf = self.get_idf()


if __name__ == '__main__':
    pass
