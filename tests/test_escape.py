# encoding: utf-8

from unittest import TestCase

from marrow.util.bunch import Bunch
from marrow.util.escape import unescape


PLAYERS = Bunch(
        alice = Bunch(name="Alice", gender='female'),
        bob = Bunch(name="Bob", gender='male'),
        everyone = Bunch(name="everyone", gender='group'),
        bender = Bunch(name='Bender', gender='i', role="bending robot")
    )

CASES = [
        (None,             '%N', 'Anonymous'),
        (PLAYERS.alice,    '%N welcomes you.', 'Alice welcomes you.'),
        (PLAYERS.alice,    'The book is %a.', 'The book is hers.'),
        (PLAYERS.alice,    '%S loves coffee.', 'She loves coffee.'),
        (PLAYERS.alice,    '%s %o %p %a %S %O %P %A %N', 'she her her hers She Her Her Hers Alice'),
        (PLAYERS.bob,      '%s %o %p %a %S %O %P %A %N', 'he him his his He Him His His Bob'),
        (PLAYERS.everyone, '%s %o %p %a %S %O %P %A %N', 'they them their theirs They Them Their Theirs everyone'),
        (PLAYERS.bender,   '%s %o %p %a %S %O %P %A %N', 'it it its its It It Its Its Bender'),
    ]


def assert_expected(caller, testing, expected, obj=None):
    assert unescape(caller, testing, obj) == expected, "Expected '%s', returned '%s'." % (expected, unescape(caller, testing, obj))


def test_escapes():
    for p, i, o in CASES:
        yield assert_expected, p, i, o
