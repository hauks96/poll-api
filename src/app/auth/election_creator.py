from app.auth.creator import Creator


class ElectionCreator(Creator):
    def __init__(self):
        super().__init__()
        self.data_path = self.get_filepath("data/auth_creator/election_creator.json")
        self.arg_name = "election_ids"
        self.max_creations = 5

