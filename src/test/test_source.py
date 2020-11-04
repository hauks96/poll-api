import unittest

from app.data_layer.models.source_model import SourceModel
from app.logic_layer.source_ll import SourceLogic


class TestSourceLogic(unittest.TestCase):
    def setUp(self) -> None:
        self.source_logic = SourceLogic()
        self.source_1 = self.source_logic.add(SourceModel(id=None, name="TestSource", info="Test Info"))

    def test_get_sources(self):
        sources = self.source_logic.get_all()
        if type(sources) == list:
            source_exists = False
            for source in sources:
                if source.id == self.source_1.id:
                    source_exists = True
                    break

            self.assertEqual(source_exists, True)
        else:
            self.assertEqual(sources.id, self.source_1.id)

    def test_get_source_name_by_id(self):
        source_name = self.source_logic.get_source_name_by_id(self.source_1.id)
        self.assertEqual(source_name, self.source_1.name)

    def test_get_source_by_name(self):
        source = self.source_logic.get_source_by_name(self.source_1.name)
        self.assertEqual(source.id, self.source_1.id)

    def tearDown(self) -> None:
        self.source_logic.delete(self.source_1.id)


if __name__ == '__main__':
    unittest.main()
