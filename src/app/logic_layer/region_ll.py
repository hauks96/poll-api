from app.logic_layer.logic import Logic


class RegionLogic(Logic):
    def __init__(self):
        super().__init__()

    def get_region(self, _id):
        """Returns the region with the given id. Uses the RegionData instance to utilize it's get method"""
        region = self.get(_id)
        if region:
            return self.jsonify(region)
        return None

    def get_region_details(self, _id):
        """ Returns the information on a specific state"""
        region = self.get_region(_id)
        region_details = {}
        if region:
            region_details['population'] = region.get('population')
            region_details['registeredVoters'] = region.get('registeredVoters')
            return region_details
        return None

    def get_regions(self):
        """Returns all regions. Uses the RegionData instance to utilize it's get_all method"""
        regions = self.get_all()
        if regions:
            return self.jsonify(self.get_all())
        else:
            return None

    def jsonify(self, models):
        json_list = []
        if not models:
            return []

        if type(models) != list:
            models = [models]
        for model in models:
            region = {
                'regionID': str(model.id),
                'name': model.name,
                'population': model.population,
                'registeredVoters': model.registeredVoters
            }
            json_list.append(region)
        if len(json_list) == 1:
            return json_list[0]

        return json_list


if __name__ == '__main__':
    pass
