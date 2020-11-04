from app.data_layer.data.data import Data


class PollData(Data):
    def __init__(self):
        super().__init__()
        self.data_path = self.get_filepath("../json_data/poll_data.json")
        self.idf = self.get_idf()


if __name__ == '__main__':
    pass
