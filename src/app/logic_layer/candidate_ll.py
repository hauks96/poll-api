from app.logic_layer.logic import Logic


class CandidateLogic(Logic):
    def __init__(self):
        super().__init__()

    def get_candidates(self):
        """Returns all candidates that exist"""
        return self.jsonify(self.get_all())

    def get_candidate_by_id(self, _id):
        """Returns a specific candidate"""
        candidate = self.get(_id)
        if candidate:
            return self.jsonify(candidate)
        return None

    def get_candidate_by_name(self, name):
        """Filters out candidates by name"""
        for x in self.get_all():
            if x.name == name:
                return self.jsonify(x)
        return None

    def jsonify(self, models):
        json_list = []
        if not models:
            return json_list

        if type(models) != list:
            models = [models]

        for model in models:
            candidate = {
                'electableID': str(model.id),
                'name': model.name,
                'description': model.info
            }
            json_list.append(candidate)

        if len(json_list) == 1:
            return json_list[0]

        return json_list

    def jsonify_with_image(self, models):
        json_list = []
        if not models:
            return json_list

        if type(models) != list:
            models = [models]

        for model in models:
            candidate = {
                'electableID': str(model.id),
                'name': model.name,
                'description': model.info,
                'image': model.image
            }
            json_list.append(candidate)

        if len(json_list) == 1:
            return json_list[0]

        return json_list


if __name__ == '__main__':
    pass
