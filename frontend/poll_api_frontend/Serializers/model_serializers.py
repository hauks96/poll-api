from BackendCommunicationGateway.poll_api_gateway import PollApiGateway


class Manifest:
    """
    attributes: dictionary contain the attribute as key and the type as value
    """
    attributes = {'attribute': type}


class RegionManifest(Manifest):
    attributes = {'id': int, 'name': str, 'registered_voters': int, 'population': int}


class ElectableManifest(Manifest):
    attributes = {'id': int, 'name': str, 'description': str, 'image': str}


class OrganizationManifest(Manifest):
    attributes = {'name': str}


class ElectionManifest(Manifest):
    attributes = {'id': int, 'name': str, 'regions': list, 'candidates': list}


class RegionVoteManifest(Manifest):
    attributes = {'region': dict, 'electable_votes': list}


class ElectableVoteManifest(Manifest):
    attributes = {'candidate': dict, 'votes': int}


class PollManifest(Manifest):
    attributes = {'id': int, 'election': dict, 'organization': str,'region_votes': list, 'start_date': str, 'end_date': str}


class Model:
    def __init__(self):
        pass


class ModelFactory:
    @staticmethod
    def create_model(adapter_data, manifest: Manifest):
        ret_models = []
        if type(adapter_data) is not list:
            adapter_data = [adapter_data]

        # Get the new class name
        class_name = manifest.__name__.replace("Manifest", "Model", 1)

        for model_data in adapter_data:
            # Initialize new class
            new_class = type(class_name, (Model,), manifest.attributes)

            # Set the values to the given attributes
            new_class = ModelFactory.set_attribute_values(new_model=new_class, model_data=model_data,
                                                          attributes=manifest.attributes)
            # Append to returned model list
            ret_models.append(new_class)

        if len(ret_models) == 1:
            return ret_models[0]

        return ret_models

    @staticmethod
    def set_attribute_values(new_model, model_data, attributes):
        # For each attribute in the model
        for attr in attributes.keys():
            # Set the value of the class attribute
            setattr(new_model, attr, model_data[attr])

        return new_model
