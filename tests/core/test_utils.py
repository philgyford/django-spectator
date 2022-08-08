from django.test import TestCase

from spectator.core.factories import IndividualCreatorFactory
from spectator.core.utils import chartify


class ChartifyTestCase(TestCase):
    def setUp(self):
        super().setUp()

        self.creators = IndividualCreatorFactory.create_batch(5)
        self.creators[0].num_readings = 10
        self.creators[1].num_readings = 8
        self.creators[2].num_readings = 8
        self.creators[3].num_readings = 6
        self.creators[4].num_readings = 0

    def test_default_list(self):
        chart = chartify(self.creators, "num_readings")

        self.assertEqual(len(chart), 4)
        self.assertEqual(chart[0].chart_position, 1)
        self.assertEqual(chart[1].chart_position, 2)
        self.assertEqual(chart[2].chart_position, 2)
        self.assertEqual(chart[3].chart_position, 4)

    def test_cutoff_is_none(self):
        "Should include the 0-scoring item."
        chart = chartify(self.creators, "num_readings", cutoff=None)

        self.assertEqual(len(chart), 5)
        self.assertEqual(chart[0].chart_position, 1)
        self.assertEqual(chart[1].chart_position, 2)
        self.assertEqual(chart[2].chart_position, 2)
        self.assertEqual(chart[3].chart_position, 4)
        self.assertEqual(chart[4].chart_position, 5)

    def test_cutoff_value(self):
        "Should be possible to set a custom cutoff value."
        chart = chartify(self.creators, "num_readings", cutoff=6)

        self.assertEqual(len(chart), 3)
        self.assertEqual(chart[0].chart_position, 1)
        self.assertEqual(chart[1].chart_position, 2)
        self.assertEqual(chart[2].chart_position, 2)

    def test_ensure_chartiness(self):
        "By default list should be empty if all objects have the same score."
        creators = IndividualCreatorFactory.create_batch(3)
        for c in creators:
            c.num_readings = 10

        chart = chartify(creators, "num_readings")

        self.assertEqual(len(chart), 0)

    def test_ensure_chartiness_false(self):
        "Should be possible to disable the behaviour."
        creators = IndividualCreatorFactory.create_batch(3)

        for c in creators:
            c.num_readings = 10

        chart = chartify(creators, "num_readings", ensure_chartiness=False)

        self.assertEqual(len(chart), 3)

    def test_handle_empty_chart(self):
        "There was an error if all items in chart met the cutoff value."
        creator = IndividualCreatorFactory()
        creator.num_readings = 1

        chart = chartify([creator], "num_readings", cutoff=1)

        self.assertEqual(len(chart), 0)
