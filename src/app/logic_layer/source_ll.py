from app.logic_layer.logic import Logic


class SourceLogic(Logic):
    def __init__(self):
        super().__init__()

    def get_source_by_id(self, _id):
        return self.get(_id)

    def get_source_name_by_id(self, _id):
        return self.get(_id).name

    def get_source_by_name(self, name):
        for source in self.get_all():
            if source.name == name:
                return source
        return None

    def jsonify(self, models):
        json_list = []
        if not models:
            return []

        if type(models) != list:
            models = [models]
        for model in models:
            source = model.name
            json_list.append(source)
        if len(json_list) == 1:
            return json_list[0]

        return json_list


if __name__ == '__main__':
    pass
