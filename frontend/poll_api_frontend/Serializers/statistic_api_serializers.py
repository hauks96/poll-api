from Serializers.model_serializers import Model


class ChartSerializerError(Exception):
    pass


class ChartSerializer:
    @staticmethod
    def poll_pie_chart(poll_model: Model) -> dict:
        """
        Takes a single poll model as input and renders the data format required for a pie chart for each region. \n
        Format is: [{region_name: [candidate_name, votes]}, ...]

        :param poll_model:
        :return: Required data.
        :raises: ChartSerializerError: If poll_model doesn't have base class Model
        """
        if poll_model.__bases__[0] is not Model:
            raise ChartSerializerError("Poll model in chart serialization expected type Model but received type %s" %
                                       str(type(poll_model)))

        region_dict = {}
        for region_vote in poll_model.region_votes:
            region_dict[region_vote.region.name] = []
            for candid_vote in region_vote.electable_votes:
                region_dict[region_vote.region.name].append([candid_vote.candidate.name, candid_vote.votes, False, False])

        return region_dict
