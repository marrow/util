# encoding: utf-8

from unittest import TestCase

from pulp.util.time import delta_to_seconds, hour



class TestTime(TestCase):
    def test_constant_and_converter(self):
        self.assertEquals(delta_to_seconds(hour), 60*60)
