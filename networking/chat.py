from datetime import datetime
from struct import pack, unpack
from binascii import hexlify


class UnicodeMixin(object):
    def __str__(self):
        return unicode(self).encode('utf-8')


class UserManager(object):
    def __init__(self):
        self._users = []

    def get_user_by_id(self, id):
        filter_result = filter(lambda user: user._id == id, self._users)
        if not filter_result:
            raise AttributeError('User with id %s does\'t exist.')
        return filter_result[0]

    def create(self, *args, **kwargs):
        new_user = User(*args, **kwargs)
        self._users.append(new_user)

        return new_user


class User(UnicodeMixin):
    _id = 0
    objects = UserManager()

    def __init__(self, nickname):
        self._nickname = nickname
        self._messages = []
        self._id = ++User._id

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
        raw_data = pack('!BBHI%ss' % len(self._data), 0, self._type, self._source, len(self._data), self._data)
        return raw_data

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"{}: {}".format(hex(self._type), hexlify(self._data))


class EventHandler(UnicodeMixin):
    def __init__(self):
        self._callbacks = {}

    def handle(self, raw_data):
        event = Event.get_from_bytes(raw_data)

        if event.event_type in self._callbacks:
            print 'Received: ', event
            return self._callbacks[event.event_type](event)
        raise ValueError('Unknown event type %s' % event.event_type)

    def register_handler(self, type, callback):
        if not callable(callback):
            raise AttributeError("You must to pass a function.")

        if type in self._callbacks:
            raise AttributeError("Callback with this type has already exist.")
        self._callbacks[type] = callback


class MessageServer(EventHandler):

    def __init__(self):
        super(MessageServer, self).__init__()

        self._messages = []

        self.register_handler(0x01, self.__new_user_callback)
        self.register_handler(0x02, self.__new_message_callback)
        self.register_handler(0x03, self.__leave_user_callback)

    def __new_user_callback(self, event):
        User.objects.create(event.data)

    def __new_message_callback(self, event):
        new_message = Message()

    def __leave_user_callback(self, event):
        pass

    def loop(self):
        events = [Event(0x01, 0, 'Mike').pack(),
                  Event(0x02, 1, 'Hello, From mike').pack(),
                  Event(0x03, 1, 'Mike').pack()
                  ]

        for event in events:
            self.handle(event)

    def __unicode__(self):
        return u'Users: {}\n\rMessages: {}'.format(len(self._users), len(self._messages))



if __name__ == '__main__':
    server = MessageServer()

    server.loop()

    print server