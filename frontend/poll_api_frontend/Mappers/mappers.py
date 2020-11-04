from Serializers.statistic_api_serializers import ChartSerializer


class TemplateMapperError(Exception):
    pass


# TODO: Supporting statistic template for getOverallElectionPoll': 'stats.html'
# TODO: Supporting statistic template for getElectionStatistics': 'stats.html',
class TemplateMapper:
    def __init__(self):
        self.__mapper = {
            'getPoll': 'poll_details.html',
            'getAllPolls': 'polls.html',
            'getElectables': 'electives.html',
            'getElectableDetails': 'electives.html',
            'getRegionDetails': 'regions.html',
            'getAllRegions': 'regions.html',
            'getElection': 'elections.html',
            'getElections': 'elections.html',
            'getSource': 'organizations.html',
            'getAllSources': 'organizations.html',
            'getPollsBySourceName': 'polls.html',
            'getPollsByTimeframe': 'polls.html',
            'getHistoricalPollsForElection': 'polls.html',
            'getOverallElectionPoll': 'poll_details.html',
            'getElectionStatistics': 'message.html',
            'getAveragePoll': 'polls.html',
            'login': 'message.html',
            'logout': 'message.html',
            'vote': 'message.html',
            'createUser': 'message.html',
            'createPoll': 'polls.html',
            'createElection': 'elections.html',
            'createElectable': 'electives.html',
            'createParty': 'electives.html',
            'createCandidate': 'electives.html',
            'createRegion': 'regions.html',
            'deletePoll': 'message.html',
            'deleteElection': 'message.html',
            'deleteElectable': 'message.html',
            'deleteRegion': 'message.html',
            'addElectionRegion': 'message.html',
            'addElectionElectable': 'message.html',
            'getUserPolls': 'polls.html',
            'getUserElections': 'elections.html',
            'getUserElectables': 'electives.html',
            'getUserRegions': 'regions.html',
            'getPollWithImageSource': 'poll_details.html'
        }

    def get_template(self, operation: str):
        try:
            return self.__mapper[operation]
        except KeyError:
            raise TemplateMapperError("Argument %s not found in mapper" % operation)


class ArgumentMapperError(Exception):
    pass


# Argument mapper for form creation
class FormArgumentMapper:
    def __init__(self):
        self.__mapper = {
            'getPoll': {'pollID': 'number'},
            'getPollWithImageSource': {'pollID': 'number'},
            'getAllPolls': {},
            'getElectables': {'electionID': 'number'},
            'getElectableDetails': {'electableID': 'number'},
            'getRegionDetails': {'regionID': 'number'},
            'getAllRegions': {},
            'getElection': {'electionID': 'number'},
            'getElections': {},
            'getSource': {'sourceID': 'number'},
            'getAllSources': {},
            'getPollsBySourceName': {'sourceName': 'text'},
            'getPollsByTimeframe': {'startDate': 'date', 'endDate': 'date'},
            'getHistoricalPollsForElection': {'electionID': 'number', 'dateAfter': 'date', 'dateBefore': 'date'},
            'getOverallElectionPoll': {'electionID': 'number'},
            'getElectionStatistics': {'electionID': 'number'},
            'getAveragePoll': {'electionID': 'number'},
            'login': {'username': 'text', 'password': 'password'},
            'logout': {},
            'vote': {'pollID': 'number', 'electableID': 'number'},
            'createUser': {'username': 'text', 'password': 'password', 'firstName': 'text',
                           'lastName': 'text', 'ssn': 'tel', 'regionID': 'number'},
            'createPoll': {'electionID': 'number', 'startDate': 'date', 'endDate': 'date'},
            'createElection': {'name': 'text'},
            'createElectable': {'name': 'text', 'description': 'text', 'imageUrl': 'url'},
            'createParty': {'name': 'text', 'description': 'text', 'imageUrl': 'url'},
            'createCandidate': {'name': 'text', 'description': 'text', 'imageUrl': 'url'},
            'createRegion': {'name': 'text', 'population': 'number', 'registeredVoters': 'number'},
            'deletePoll': {'pollID': 'number'},
            'deleteElection': {'electionID': 'number'},
            'deleteElectable': {'electableID': 'number'},
            'deleteRegion': {'regionID': 'number'},
            'addElectionRegion': {'electionID': 'number', 'regionID': 'number'},
            'addElectionElectable': {'electionID': 'number', 'electableID': 'number'},
            'getUserPolls': {},
            'getUserElections': {},
            'getUserElectables': {},
            'getUserRegions': {}
        }

    def get_form_attributes(self, operation: str):
        try:
            return self.__mapper[operation]
        except KeyError:
            raise ArgumentMapperError("Argument %s not found in mapper" % operation)

