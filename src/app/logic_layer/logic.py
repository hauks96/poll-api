from app.data_layer.data.election_candidate_data import ElectionCandidateData
from app.data_layer.data.election_region_data import ElectionRegionData
from app.data_layer.data.candidate_data import CandidateData
from app.data_layer.data.election_data import ElectionData
from app.data_layer.data.poll_vote_data import PollVoteData
from app.data_layer.data.region_data import RegionData
from app.data_layer.data.source_data import SourceData
from app.data_layer.data.poll_data import PollData
import json


class Logic:
    def __init__(self):
        self.data_layer = self.__get_data_class_object()

    def __get_data_class_object(self):
        """Returns data layer instance of the child class that calls the method"""
        obj = globals()[self.__get_data_classname()]
        obj_instance = obj()
        return obj_instance

    @classmethod
    def __get_data_classname(cls):
        """Replaces 'Logic' with 'Data' to get the data class name"""
        class_name = cls.__name__.replace("Logic", "Data", 1)
        return class_name

    def get(self, _id):
        """Returns model object of current class with id=_id"""
        return self.data_layer.get(_id=_id)

    def get_all(self):
        return self.data_layer.get_all()

    def add(self, model):
        """Add an instance of a particular model to the database"""
        return self.data_layer.add(model_object=model)

    def update(self, model):
        """Update an instance of a particular model. The ID cannot be changed. To use this method,
        you must first fetch the model instance with get methods."""
        return self.data_layer.update(model_object=model)

    def delete(self, _id):
        """Deletes an instance of the current model with id=_id"""
        return self.data_layer.delete(_id=_id)

    def safe_delete(self, _id: int):
        return self.delete(_id=_id)

    def save(self, models):
        """Save models to database. WARNING: Overwrites all current data."""
        data = []
        for model in models:
            data.append(model.in_json())

        self.data_layer.save(data)

    def jsonify(self, models):
        """Returns the current models data in json format"""
        # THIS DEFAULT SHOULD BE IN ALL DATA CLASSES
        json_list = []
        if type(models) != list:
            models = [models]
        for model in models:
            pass
            # ...
            # ...
            # ...
        # ...
        if len(json_list) == 1:
            return json_list[0]

        return None

