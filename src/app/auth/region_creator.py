from app.auth.creator import Creator


class RegionCreator(Creator):
    def __init__(self):
        super().__init__()
        self.data_path = self.get_filepath("data/auth_creator/region_creator.json")
        self.arg_name = "region_ids"
        self.max_creations = 10
