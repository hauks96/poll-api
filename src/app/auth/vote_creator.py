from app.auth.creator import Creator


class PollVoteCreator(Creator):
    def __init__(self):
        super().__init__()
        self.data_path = self.get_filepath("data/auth_creator/vote_creator.json")
        self.arg_name = "poll_ids"

    @staticmethod
    def new_voter(user_id: int, poll_id: int):
        return {
            "user_id": user_id,
            "poll_ids": [poll_id]
        }

