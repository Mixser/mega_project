from datetime import datetime
from struct import pack, unpack
from binascii import hexlify

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

        self._user_manager = UserManager()
        self._message_manager = MessageManager()

        self.register_handler(NEW_USER, self.__new_user_callback)
        self.register_handler(NEW_MESSAGE, self.__new_message_callback)
        self.register_handler(0x03, self.__leave_user_callback)

    def send_message_to_user(self, user, message):
        pass

    def broadcast_event(self, event):
        print 'Broadcast event: ', event

    def __new_user_callback(self, event):
        self._user_manager.create(event.data)
        self.broadcast_event(event)

    def __new_message_callback(self, event):
        user = self._user_manager.get_user_by_id(event.source)
        self._message_manager.create(user, event.data)

    def __leave_user_callback(self, event):
        self._user_manager.delete()

    def __unicode__(self):
        user_counts = self._user_manager.count()
        message_counts = self._message_manager.count()
        return u'Users: {}\nMessages: {}'.format(user_counts, message_counts)


def loop(chat_server):
    events = [Event(NEW_USER, 0, 'Mike').pack(),
              Event(NEW_MESSAGE, 1, 'Hello, From mike').pack(),
              Event(NEW_USER, 0, 'Mike2').pack(),
              Event(NEW_USER, 2, 'Hello, From mike').pack(),
              Event(NEW_MESSAGE, 2, 'Hello, From mike').pack(),
              Event(NEW_MESSAGE, 1, 'Hello, From mike').pack(),
              ]
    import time
    for event in events:
        chat_server.handle(event)
        time.sleep(1)


if __name__ == '__main__':
    server = MessageServer()

    loop(server)

    print server
