# encoding: utf-8

from unittest import TestCase

from pulp.util.time import delta_to_seconds, hour, map_month, map_dow



class TestTime(TestCase):
    def test_constant_and_converter(self):
        self.assertEquals(delta_to_seconds(hour), 60*60)
    
    def test_month_mapping(self):
        self.assertEquals(map_month('jan'), 1)
        self.assertEquals(map_month('Jan'), 1)
        self.assertEquals(map_month('January'), 1)
    
    def test_dow_mapping(self):
        self.assertEquals(map_dow('mon'), 1)
        self.assertEquals(map_dow('Mon'), 1)
        self.assertEquals(map_dow('Monday'), 1)
