from cmd import Cmd


class Converter(object):
    pass


class ConverterUnity(object):
    def do_convert(self, another_unity):
        if self._type != another_unity._type:
            raise ValueError("Must be a same type")


class LengthUnity(ConverterUnity):
    _type = 'LENGTH'
    __units__ = {
        'm': 1.0,
        'miles': 1.0 / 1609.344,
        'km': ''
    }



class UnityConverter(Cmd):
    def do_convert(self, unity):
        print unity * 10

    def do_EOF(self, line):
        return True

    def postloop(self):
        print

if __name__ == "__main__":
    cmd = UnityConverter()
    cmd.prompt = "(Conv) "
    cmd.cmdloop("CONVERT")
