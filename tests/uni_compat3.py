# encoding: utf-8

__all__ = ['uchar', 'path_cases']

def uchar():
    return 'ü'

path_cases = [
        ('/', "/"),
        ('/©', '/©'),
        ('/©/™', '/©/™'),
        ('/©/™/', '/©/™/'),
        (('¡', ), '¡'),
        (('foo', '¡'), 'foo/¡')
    ]
