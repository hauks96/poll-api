import json
import os
from app.data_layer.models.candidate_model import CandidateModel
from app.data_layer.models.election_model import ElectionModel
from app.data_layer.models.election_region_model import ElectionRegionModel
from app.data_layer.models.election_candidate_model import ElectionCandidateModel
from app.data_layer.models.poll_model import PollModel
from app.data_layer.models.poll_vote_model import PollVoteModel
from app.data_layer.models.region_model import RegionModel
from app.data_layer.models.source_model import SourceModel


class Data:
    def __init__(self):
        self.idf = 0  # The current largest ID in the list
        self.data_path = "path/to/json_data.json"

    def __next_idf(self):
        """Gets the next identifier to use"""
        return self.idf + 1

    @staticmethod
    def get_filepath(relative_file_location):
        """Gets absolute file path"""
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, relative_file_location)
        return filename

    def get_idf(self):
        """Gets the current largest identifier of the class"""
        with open(self.data_path) as file:
            data = json.load(file)
            if len(data) == 0:
                return 1
        return data[-1]["id"]

    def __write_data(self, data):
        """Writes new dataset to file, overwriting all previous content"""
        with open(self.data_path, 'w') as file:
            json.dump(data, file, indent=2)

    def save(self, data):
        """WARNING. Saving data to database will overwrite all current data"""
        self.__write_data(data)

    def __get_data(self):
        """Fetches all data for this class"""
        with open(self.data_path) as file:
            data = json.load(file)
        return data

    def __get_model_from_json_data(self, json_model):
        """Fetches this class's corresponding model class and returns the json as a model"""
        new_model_cls = globals()[self.__get_model_class_name()]
        model_instance_from_json = new_model_cls.as_model(json_model)
        return model_instance_from_json

    @classmethod
    def __get_model_class_name(cls):
        """Returns this class's corresponding model class name"""
        class_name = cls.__name__
        return class_name.replace("Data", "Model", 1)

    def add(self, model_object):
        """Add a model object to the database"""
        next_idf = self.__next_idf()
        model_object.id = next_idf
        self.idf = next_idf
        data = self.__get_data()
        data.append(model_object.in_json())
        self.__write_data(data=data)

        created_object = self.get(next_idf)
        if created_object:
            return created_object
        return

    def get(self, _id: int):
        """Get model data by id"""
        data = self.__get_data()
        for instance in data:
            if instance["id"] == _id:
                return self.__get_model_from_json_data(json_model=instance)
        return None

    def get_all(self):
        """Get all model data"""
        data = self.__get_data()
        model_data = []
        for instance in data:
            model_data.append(self.__get_model_from_json_data(json_model=instance))
        return model_data

    def delete(self, _id: int):
        """Remove model data by id"""
        data = self.__get_data()
        removed = None
        for i in range(len(data)):
            if data[i]["id"] == _id:
                removed = data.pop(i)
                break

        self.__write_data(data)
        return removed

    def update(self, model_object):
        """Update a model. Fetch the model with get, and pass the modified model back in here. DO NOT CHANGE THE ID"""
        _id = model_object.id
        data = self.__get_data()
        for instance in data:
            if instance["id"] == _id:
                instance = model_object.in_json()
                self.__write_data(data)
                return instance
        return None
