from datetime import datetime
from struct import pack, unpack
from binascii import hexlify

import socket

from thread import start_new_thread

NEW_USER = 0x01
NEW_MESSAGE = 0x02
LEAVE_USER = 0x03


class UnicodeMixin(object):
    def __str__(self):
        return unicode(self).encode('utf-8')


class ObjectManager(object):
    def __init__(self, model):
        self._model = model
        self._objects = []

    def create(self, *args, **kwargs):
        new_object = self._model(*args, **kwargs)
        self._objects.append(new_object)

        return new_object

    def delete(self, id):
        pass

    def count(self):
        return len(self._objects)


class UserManager(ObjectManager):
    def __init__(self):
        super(UserManager, self).__init__(User)

    def get_user_by_id(self, id):
        filter_result = filter(lambda user: user._id == id, self._objects)
        if not filter_result:
            raise AttributeError('User with id %s does\'t exist.')
        return filter_result[0]


class MessageManager(ObjectManager):
    def __init__(self):
        super(MessageManager, self).__init__(Message)


class User(UnicodeMixin):
    _id = 0

    def __init__(self, nickname):
        self._nickname = nickname
        self._messages = []
        User._id += 1
        self._id = User._id

    def __unicode__(self):
        return u'{}: {}'.format(self._id, unicode(self._nickname))


class Message(UnicodeMixin):
    def __init__(self, user, body):
        self._user = user
        self._body = body
        self._created_at = datetime.now()


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
        if len(header_raw) != header_length:
            return None
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


class EventHandler(UnicodeMixin):
    def __init__(self):
        self._callbacks = {}
        self._connections = []

    def handle(self, raw_data):

        event = Event.get_from_bytes(raw_data)

        if not event:
            return

        if event.event_type in self._callbacks:
            print 'Received: ', event
            return self._callbacks[event.event_type](event)
        raise ValueError('Unknown event type %s' % event.event_type)

    def register_handler(self, type, callback):
        if not callable(callback):
            raise AttributeError("You must to pass a function.")

        if type in self._callbacks:
            raise AttributeError("Callback with this type has already exist.")

        def _callback_wrapper(event):
            callback(event)
            self.broadcast_event(event)

        self._callbacks[type] = _callback_wrapper

    def broadcast_event(self, event):
        for connection in self._connections:
            connection.send(event.pack())


class MessageServer(EventHandler):

    def __init__(self):
        super(MessageServer, self).__init__()

        self._messages = []

        self._user_manager = UserManager()
        self._message_manager = MessageManager()

        self.register_handler(NEW_USER, self.__new_user_callback)
        self.register_handler(NEW_MESSAGE, self.__new_message_callback)
        self.register_handler(LEAVE_USER, self.__leave_user_callback)

    def send_message_to_user(self, user, message):
        pass

    def __new_user_callback(self, event):
        self._user_manager.create(event.data)

    def __new_message_callback(self, event):
        user = self._user_manager.get_user_by_id(event.source)
        self._message_manager.create(user, event.data)

    def __leave_user_callback(self, event):
        self._user_manager.delete(event.source)

    def listen(self, conn):
        self._connections.append(conn)

        try:
            while True:
                raw_data = conn.recv(1024)
                self.handle(raw_data)
        except socket.error as err:
            self._connections.remove(conn)

    def __unicode__(self):
        user_counts = self._user_manager.count()
        message_counts = self._message_manager.count()
        return u'Users: {}\nMessages: {}'.format(user_counts, message_counts)

def client_thread(conn, server):
    server.listen(conn)

if __name__ == '__main__':
    server = MessageServer()

    sk = socket.socket()

    sk.bind(('127.0.0.1', 8000))

    sk.listen(4)

    while True:
        conn, addr = sk.accept()
        start_new_thread(client_thread, (conn, server))