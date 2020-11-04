import json
import os


class Creator:
    def __init__(self):
        self.arg_name = ""
        self.data_path = "relative_path_to_data"
        self.max_creations = 5

    @staticmethod
    def get_filepath(relative_file_location):
        """Gets absolute file path"""
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, relative_file_location)
        return filename

    def write_data(self, data):
        """Writes new dataset to file, overwriting all previous content"""
        with open(self.data_path, 'w') as file:
            json.dump(data, file, indent=2)

    def get_data(self):
        """Fetches all data for this class"""
        with open(self.data_path) as file:
            data = json.load(file)
        return data

    def get_idf(self):
        """Gets the current largest identifier of the class"""
        with open(self.data_path) as file:
            data = json.load(file)
            if len(data) == 0:
                return 1
        return data[-1]["id"]

    def new_instance(self, user_id: int, arg_val: int):
        return {
            "user_id": user_id,
            self.arg_name: [arg_val]
        }

