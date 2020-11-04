from app.auth.creator import Creator


class PollCreator(Creator):
    def __init__(self):
        super().__init__()
        self.data_path = self.get_filepath("data/auth_creator/poll_creator.json")
        self.arg_name = "poll_ids"

