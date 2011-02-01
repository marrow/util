# encoding: utf-8

__all__ = ['Pipe', 'pipe']


class Pipe(object):
    """An OS independent asynchronous pipe."""
    
    def __init__(self):
        # Based on Zope async.py: http://svn.zope.org/zc.ngi/trunk/src/zc/ngi/async.py
        
        self.writer = socket.socket()
        self.writer.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        
        count = 0
        while 1:
            count += 1
            a = socket.socket()
            a.bind(("127.0.0.1", 0))
            connect_address = a.getsockname()
            a.listen(1)
            
            try:
                self.writer.connect(connect_address)
                break
            
            except socket.error:
                detail = exception().exception
                
                if detail[0] != errno.WSAEADDRINUSE:
                    raise
                
                if count >= 10:
                    a.close()
                    self.writer.close()
                    raise socket.error("Cannot bind trigger!")
                
                a.close()
        
        self.reader, addr = a.accept()
        self.reader.setblocking(0)
        self.writer.setblocking(0)
        a.close()
        
        self.writer_fd = self.writer.fileno()
        self.reader_fd = self.reader.fileno()
    
    def read(self):
        """Emulate a file descriptors read method"""
        try:
            return self.reader.recv(1)
        except socket.error:
            ex = exception().exception
            if ex.args[0] == errno.EWOULDBLOCK:
                raise IOError
            raise
    
    def write(self, data):
        """Emulate a file descriptors write method"""
        return self.writer.send(data)


def pipe():
    """Return the optimum pipe implementation for the capabilities of the active system."""
    
    try:
        from os import pipe
        return pipe()
    
    except:
        pipe = Pipe()
        return pipe.reader_fd, pipe.writer_fd
