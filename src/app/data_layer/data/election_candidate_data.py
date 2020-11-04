from app.data_layer.data.candidate_data import CandidateData
from app.data_layer.data.data import Data
from app.data_layer.models.election_candidate_model import ElectionCandidateModel


class ElectionCandidateData(Data):
    def __init__(self):
        super().__init__()
        self.data_path = self.get_filepath("../json_data/election_candidate_data.json")
        self.idf = self.get_idf()


if __name__ == '__main__':
    pass

