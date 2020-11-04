from app.data_layer.data.data import Data
from app.data_layer.models.candidate_model import CandidateModel


class CandidateData(Data):
    def __init__(self):
        super().__init__()
        self.data_path = self.get_filepath("../json_data/candidate_data.json")
        self.idf = self.get_idf()


if __name__ == '__main__':
    pass
