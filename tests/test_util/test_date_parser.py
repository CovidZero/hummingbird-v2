from unittest import TestCase
from util import date_parser
from datetime import date


class TestDateParser(TestCase):

    def test_if_convert_date_object_to_string(self):
        result = date_parser.datetime_to_str(date(2020, 4, 2))
        self.assertEqual(result, '2020-04-02')
