class ChildModel:
    def __init__(self):
        self.name = "CHILD_MODEL"

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @staticmethod
    def return_input(_input: int):
        return _input


class Parent:
    def __init__(self, id=None):
        self.id = id

    @classmethod
    def new_model_class_object(cls):
        new_cls = globals()[cls.__name__+"Model"]
        new_instance = new_cls()
        return new_instance

    @classmethod
    def return_child_model_method(cls, _input):
        new_cls = globals()[cls.__name__ + "Model"]
        data = new_cls.return_input(_input)
        return data


class Child(Parent):
    def __init__(self, id):
        super().__init__(id)


if __name__ == '__main__':
    child = Child(1)
    child_model = child.new_model_class_object()
    print(child_model)
    print(Child.return_child_model_method(5))
