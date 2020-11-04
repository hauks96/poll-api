class Model:
    def __init__(self, id=None):
        self.id = id

    @staticmethod
    def as_model(_model_as_json):
        return None

    def __repr__(self):
        return str(self.id)



