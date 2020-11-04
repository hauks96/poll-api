from app.logic_layer.logic import Logic
from app.logic_layer.region_ll import RegionLogic


class ElectionRegionLogic(Logic):
    def __init__(self):
        super().__init__()
        self.region_logic = RegionLogic()

    def delete_election_regions(self, election_id):
        data = self.get_all()
        new_data = []
        for i in range(len(data)):
            if data[i].election_id != election_id:
                new_data.append(data[i])

        self.save(new_data)

    def get_election_regions(self, _id: int):
        data = self.get_all()
        regions = []
        for election_region in data:
            if election_region.election_id == _id:
                region = self.region_logic.get(election_region.region_id)
                if region:
                    regions.append(region)

        return regions

    def jsonify(self, models):
        return self.region_logic.jsonify(models)

