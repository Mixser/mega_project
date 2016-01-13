from struct import pack, unpack
from binascii import hexlify

import socket


NEW_USER = 0x01
NEW_MESSAGE = 0x02
LEAVE_USER = 0x03

class UnicodeMixin(object):
    def __str__(self):
        return unicode(self).encode('utf-8')

class Event(UnicodeMixin):
    def __init__(self, type, source, data):
        self._type = type
        self._data = data
        self._source = source

    @property
    def event_type(self):
        return self._type

    @property
    def data(self):
        return self._data

    @property
    def source(self):
        return self._source

    @classmethod
    def get_from_bytes(cls, raw_data):
        header_length = 8
        header_raw = raw_data[:header_length]
        header = unpack('!BBHI', header_raw)
        event_type = header[1]
        event_source = header[2]
        data_length = header[3]

        data = raw_data[header_length:header_length + data_length]
        event = Event(event_type, event_source, data)

        return event

    def pack(self):
        type = self._type
        source = self._source
        data_length = len(self._data)
        data = self._data

        package_format = '!BBHI%ss' % data_length

        return pack(package_format, 0, type, source, data_length, data)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"{}: {}".format(hex(self._type), self._data)


server = socket.socket()
server.connect(('127.0.0.1', 8000))

events = [
    Event(NEW_USER, 0, 'Mike'),
    Event(NEW_MESSAGE, 1, 'gfwegwegweg'),
    Event(NEW_USER, 1, 'fewefewf'),
    Event(NEW_USER, 1, 'qwfqwf'),
    Event(NEW_USER, 1, 'Hello'),
    Event(LEAVE_USER, 2, 'Mike'),
]

for event in events:
    server.send(event.pack())
    print Event.get_from_bytes(server.recv(1024))
    raw_input()