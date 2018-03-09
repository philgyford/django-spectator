from django.test import TestCase

from spectator.core.utils import chartify
from spectator.core.factories import IndividualCreatorFactory


class ChartifyTestCase(TestCase):

    def setUp(self):
        super().setUp()

        self.creators = IndividualCreatorFactory.create_batch(5)
        self.creators[0].num_readings = 10
        self.creators[1].num_readings = 8
        self.creators[2].num_readings = 8
        self.creators[3].num_readings = 6
        self.creators[4].num_readings = 0

    def test_chart(self):
        chart = chartify(self.creators, 'num_readings')

        self.assertEqual(len(chart), 4)
        self.assertEqual(chart[0].chart_position, 1)
        self.assertEqual(chart[1].chart_position, 2)
        self.assertEqual(chart[2].chart_position, 2)
        self.assertEqual(chart[3].chart_position, 4)

    def test_chart_do_not_remove_zero_counts(self):
        chart = chartify(self.creators, 'num_readings', remove_zero_scores=False)

        self.assertEqual(len(chart), 5)
        self.assertEqual(chart[0].chart_position, 1)
        self.assertEqual(chart[1].chart_position, 2)
        self.assertEqual(chart[2].chart_position, 2)
        self.assertEqual(chart[3].chart_position, 4)
        self.assertEqual(chart[4].chart_position, 5)
