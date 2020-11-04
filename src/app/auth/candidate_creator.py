from app.auth.creator import Creator


class CandidateCreator(Creator):
    def __init__(self):
        super().__init__()
        self.data_path = self.get_filepath("data/auth_creator/candidate_creator.json")
        self.arg_name = "candidate_ids"
        self.max_creations = 10
