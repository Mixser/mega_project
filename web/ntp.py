import struct

import datetime as dt

from multiprocessing.dummy import Pool
from multiprocessing import Lock
import socket


class NTPClient(object):
    def __init__(self, ntp_host):
        self._host = ntp_host
        self._port = 123

        self._delta = int((dt.datetime(1970, 1, 1) - dt.datetime(1900, 1, 1)).total_seconds())

        self._message = '\x1b' + '\x00' * 47

    def _request(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        s.connect((self._host, self._port))
        s.send(self._message)
        s.settimeout(2)
        raw_data = s.recv(48)
        s.close()

        data = struct.unpack('!12I', raw_data)

        return data[10], data[11]

    def get_server_time(self):
        seconds, milliseconds = self._request()
        return seconds - self._delta, milliseconds


def print_message(host, message, mutex):
    with mutex:
        print message,'on', host

if __name__ == "__main__":
    import time

    hosts = ['time-c.nist.gov', 'time-d.nist.gov', 'nist1-macon.macon.ga.us', 'nist.netservicesgroup.com',
             'nist1-lnk.binary.net', 'wwv.nist.gov', 'time.nist.gov', 'utcnist.colorado.edu',
             'utcnist2.colorado.edu', 'ntp-nist.ldsbc.net', 'time-nw.nist.gov', 'nist-time-server.eoni.com',]

    mutex = Lock()

    def foo(host):
        try:
            sec, _ = NTPClient(host).get_server_time()
            message = time.ctime(sec)
        except socket.timeout as e:
            message = e.message

        print_message(host, message, mutex)


    pool = Pool()

    pool.map(foo, hosts)

    pool.close()
    pool.join()

