# encoding: utf-8


class Context(object):
    """Isolate changes to the local scope to a with block.
    
    Copyright (c) 2010 Larry Haskins, released under the MIT license.
    For the full text of the license, see the LICENSE file accompanying this distribution.
    """
    
    def __enter__(self):
        globals_ = globals()
        self.__globals__ = globals_.copy()
        _ = globals_['_[1]']
        globals_.clear()
        globals_.update(self.__dict__.copy())
        globals_['_[1]'] = _
    
    def __exit__(self, *args):
        __globals__ = self.__globals__.copy()
        globals_ = globals()
        self.__dict__.clear()
        self.__dict__.update(globals_.copy())
        globals_.clear()
        globals_.update(__globals__)

if __name__ == '__main__':
    # Some tests.
    
    n = Context()
    
    with n:
        x = 5
    
    print(n.x) # 5
    print(dir()) # x not present
