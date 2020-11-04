class FormSerializer:
    @staticmethod
    def model_form(attributes: dict, values=None) -> list:
        """
        Takes two dictionaries. Creates a list of models from form data which can be used in templates. Each object in
        the list represents one attribute and contains attributes: name, type, value

        :param attributes: dictionary with key [attribute name], and value [type of input]
        :param values: dictionary with key [attribute name], and value as [value of the input]
        :return: list of form models
        """
        if not values or values == {}:
            new_vals = {}
            for key in attributes.keys():
                new_vals[key] = ""
            values = new_vals

        return FormFactory.create_form_models(attributes, values)


class FormFactory:
    @staticmethod
    def create_form_models(attributes, values):
        # Get the new class name
        class_name = "FormModel"

        ret_models = []
        models_required = attributes.keys()
        for attribute in models_required:
            # Initialize new class
            new_class = type(class_name, (), {'name': str, 'value': str, 'type': str})

            # Set the values to the given attributes
            new_class = FormFactory.set_attribute_values(new_model=new_class, value=values[attribute],
                                                         name=attribute, v_type=attributes[attribute])
            # Append to returned model list
            ret_models.append(new_class)

        return ret_models

    @staticmethod
    def set_attribute_values(new_model, value, name, v_type):
        # For each attribute in the model

        # Set the value of the class attribute
        setattr(new_model, 'name', name)
        setattr(new_model, 'value', value)
        setattr(new_model, 'type', v_type)

        return new_model
