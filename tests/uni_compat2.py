# encoding: utf-8

__all__ = ['uchar', 'path_cases']

def uchar():
    return u'ü'

path_cases = [
        ('/', "/"),
        (u'/©', u'/©'),
        (u'/©/™', u'/©/™'),
        (u'/©/™/', u'/©/™/'),
        ((u'¡', ), u'¡'),
        (('foo', u'¡'), u'foo/¡')
    ]
