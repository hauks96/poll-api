from BackendCommunicationGateway.poll_api_gateway import Response
from Serializers.model_serializers import *


class DataAdapters:
    # TODO: Add docstrings to all methods
    @staticmethod
    def poll_adapter(data):
        manifest = PollManifest
        key_ref = {'id': 'pollID', 'election': 'election', 'organization': 'organization',
                   'region_votes': 'dataArray', 'start_date': 'startDate', 'end_date': 'endDate'}
        attributes = manifest.attributes
        adapt = {'election': DataAdapters.election_adapter, 'organization': DataAdapters.organization_adapter,
                 'region_votes': DataAdapters.region_vote_adapter}
        adapter_data = DataAdapters.transformed_dict_or_error(attributes, key_ref, data, adapt)
        return ModelFactory.create_model(adapter_data, manifest)

    @staticmethod
    def election_adapter(data):
        manifest = ElectionManifest
        key_ref = {'id': 'electionID', 'name': 'name', 'regions': 'regions', 'candidates': 'candidates'}
        attributes = manifest.attributes
        adapt = {'regions': DataAdapters.region_adapter, 'candidates': DataAdapters.electable_adapter}
        adapter_data = DataAdapters.transformed_dict_or_error(attributes, key_ref, data, adapt)
        return ModelFactory.create_model(adapter_data, manifest)

    @staticmethod
    def organization_adapter(data):
        new_data = []
        if type(data) == list:
            for organization in data:
                new_data.append({'name': organization})
            data = new_data
        else:
            data = {'name': data}

        manifest = OrganizationManifest
        key_ref = {'name': 'name'}
        attributes = manifest.attributes
        adapter_data = DataAdapters.transformed_dict_or_error(attributes, key_ref, data)
        return ModelFactory.create_model(adapter_data, manifest)

    @staticmethod
    def electable_adapter(data):
        manifest = ElectableManifest
        key_ref = {'id': 'electableID', 'name': 'name', 'description': 'description', 'image': 'image'}
        attributes = manifest.attributes
        adapter_data = DataAdapters.transformed_dict_or_error(attributes, key_ref, data)
        return ModelFactory.create_model(adapter_data, manifest)

    @staticmethod
    def region_adapter(data):
        """
        Adapts region data to wanted standards and returns a model.

        :param data: PollAPI region data
        :return: RegionModel or [RegionModel]
        """
        manifest = RegionManifest
        key_ref = {'id': 'regionID', 'name': 'name',
                   'registered_voters': 'registeredVoters', 'population': 'population'}
        attributes = manifest.attributes
        adapter_data = DataAdapters.transformed_dict_or_error(attributes, key_ref, data)
        return ModelFactory.create_model(adapter_data, manifest)

    @staticmethod
    def region_vote_adapter(data):
        manifest = RegionVoteManifest
        key_ref = {'region': 'region', 'electable_votes': 'data'}
        attributes = manifest.attributes
        adapt = {'region': DataAdapters.region_adapter, 'electable_votes': DataAdapters.electable_vote_adapter}
        adapter_data = DataAdapters.transformed_dict_or_error(attributes, key_ref, data, adapt)
        return ModelFactory.create_model(adapter_data, manifest)

    @staticmethod
    def stats_adapter(data):
        return data

    @staticmethod
    def message_adapter(data):
        try:
            return str(data)
        except ValueError:
            raise AdapterError("Failed to parse response message to string.")

    @staticmethod
    def electable_vote_adapter(data):
        manifest = ElectableVoteManifest
        key_ref = {'candidate': 'candidate', 'votes': 'votes'}
        attributes = manifest.attributes
        adapt = {'candidate': DataAdapters.electable_adapter}
        adapter_data = DataAdapters.transformed_dict_or_error(attributes, key_ref, data, adapt)

        return ModelFactory.create_model(adapter_data, manifest)

    @staticmethod
    def transformed_dict_or_error(attributes: dict, key_ref: dict, dataset, adapt=None):
        """
        Call this method to transform the incoming data to the specification format.

        :param attributes: The new attribute names of the incoming dataset
        :type attributes: dict
        :param key_ref: The current attribute names of the incoming dataset
        :type key_ref: dict
        :param dataset: The content data received from the PollApiGateway
        :type dataset: dict
        :param adapt: Set this parameter if there are adaptable attributes within the dataset.
        :type adapt: dict
        :return: A list of dictionaries, or just a dictionary if there is only one element
        """
        if type(dataset) is not list:
            dataset = [dataset]

        new_list = []
        # For each future model in the dataset
        for data in dataset:
            new_dict = {}
            # key is the new attribute name
            for key in attributes.keys():
                key_ref_attribute = key_ref[key]  # The key from the original data source
                key_val_type = attributes[key]  # The new type the value should be cast to
                data_value = DataAdapters.get_key(data, key_ref_attribute)  # The data to set in the new attribute

                # if the current key's data should be transformed with it's own adapter method
                if adapt and key in adapt.keys():
                    transformed_val = adapt[key](data_value)

                else:
                    try:
                        transformed_val = key_val_type(data_value)
                    except TypeError:
                        print(data_value)
                        raise AdapterError("Value of key '%s' not convertible to type %s" % (key_ref_attribute,
                                                                                             str(key_val_type)))
                    except ValueError:
                        print(data_value)
                        raise AdapterError("Value of key '%s' not convertible to type %s" % (key_ref_attribute,
                                                                                             str(key_val_type)))
                new_dict[key] = transformed_val

            new_list.append(new_dict)

        if len(new_list) == 1:
            return new_list[0]
        return new_list

    @staticmethod
    def get_key(data, key: str):
        try:
            if key == "image":
                if "image" not in data.keys():
                    data[key] = ""
                    return data[key]
            return data[key]
        except (KeyError, ValueError):
            print(data, key)
            raise AdapterError("Missing key '%s' from data." % key)


class AdapterError(Exception):
    pass


class Adapter:
    # TODO: Create tests for adapter using all data types

    method_mapper = {
        'getPoll': DataAdapters.poll_adapter,
        'getAllPolls': DataAdapters.poll_adapter,
        'getElectables': DataAdapters.electable_adapter,
        'getElectableDetails': DataAdapters.electable_adapter,
        'getRegionDetails': DataAdapters.region_adapter,
        'getAllRegions': DataAdapters.region_adapter,
        'getElection': DataAdapters.election_adapter,
        'getElections': DataAdapters.election_adapter,
        'getAllSources': DataAdapters.organization_adapter,
        'getSource': DataAdapters.organization_adapter,
        'getPollsBySourceName': DataAdapters.poll_adapter,
        'getPollsByTimeframe': DataAdapters.poll_adapter,
        'getHistoricalPollsForElection': DataAdapters.poll_adapter,
        'getOverallElectionPoll': DataAdapters.poll_adapter,
        'getElectionStatistics': DataAdapters.stats_adapter,
        'getAveragePoll': DataAdapters.poll_adapter,
        'login': DataAdapters.message_adapter,
        'logout': DataAdapters.message_adapter,
        'vote': DataAdapters.message_adapter,
        'createUser': DataAdapters.message_adapter,
        'createPoll': DataAdapters.poll_adapter,
        'createElection': DataAdapters.election_adapter,
        'createElectable': DataAdapters.electable_adapter,
        'createParty': DataAdapters.electable_adapter,
        'createCandidate': DataAdapters.electable_adapter,
        'createRegion': DataAdapters.region_adapter,
        'deletePoll': DataAdapters.message_adapter,
        'deleteElection': DataAdapters.message_adapter,
        'deleteRegion': DataAdapters.message_adapter,
        'addElectionRegion': DataAdapters.message_adapter,
        'addElectionElectable': DataAdapters.message_adapter,
        'getUserPolls': DataAdapters.poll_adapter,
        'getUserElections': DataAdapters.election_adapter,
        'getUserElectables': DataAdapters.electable_adapter,
        'getUserRegions': DataAdapters.region_adapter,
        'getPollWithImageSource': DataAdapters.poll_adapter,
    }

    @staticmethod
    def get_method(operation: str):
        """
        Fetch method from mapper. The method returned is the method needed to transform the received data to
        required form.

        :param operation: The operation to map
        :return: Returns the method required
        :raises AdapterError: If the operation doesn't exist.
        """
        try:
            return Adapter.method_mapper[operation]
        except KeyError:
            raise AdapterError("Method mapper not found for operation %s" % operation)

    @staticmethod
    def adaptContent(response: Response):
        """
        Maps data to models. For reference on the model's attributes check out the manifests.

        :param response: Response object, containing status, operation and content.
        :return: Defined Model, list of defined Models or string
        """
        if response.status != 0:
            return DataAdapters.message_adapter(response.content)

        return Adapter.get_method(response.operation)(response.content)


if __name__ == '__main__':
    pass
