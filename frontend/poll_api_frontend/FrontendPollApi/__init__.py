from Mappers.mappers import TemplateMapper, FormArgumentMapper, ChartSerializer
from Serializers.form_serializer import FormSerializer


# This is a bit hacky but it works...
class ServerUser:
    def __init__(self):
        self.is_authenticated = False


template_mapper = TemplateMapper()
form_argument_mapper = FormArgumentMapper()
chart_data_serializer = ChartSerializer()
form_model_serializer = FormSerializer()
user = ServerUser()


SUPPORTED_METHODS = [
    'getPoll',
    'getAllPolls',
    'getElectables',
    'getElectableDetails',
    'getRegionDetails',
    'getAllRegions',
    'getElection',
    'getElections',
    'getSource',
    'getAllSources',
    'getPollsBySourceName',
    'getPollsByTimeframe',
    'getHistoricalPollsForElection',
    'getOverallElectionPoll',
    'getElectionStatistics',
    'getAveragePoll',
    'login',
    'logout',
    'vote',
    'createUser',
    'createPoll',
    'createElection',
    'createElectable',
    'createParty',
    'createCandidate',
    'createRegion',
    'deletePoll',
    'deleteElection',
    'deleteElectable',
    'deleteRegion',
    'addElectionRegion',
    'addElectionElectable',
    'getUserPolls',
    'getUserElections',
    'getUserElectables',
    'getUserRegions',
    'getPollWithImageSource',
]
