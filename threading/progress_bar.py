import Tkinter
import io
import ttk

from tempfile import TemporaryFile

import requests

from threading import Thread


class Delegate(object):
    def __init__(self, callback=None):
        self._callback = callback

    def __call__(self, *args, **kwargs):
        return self._callback(*args, **kwargs)


class Downloader(object):

    def __init__(self, url, on_load, on_finish, chunk=8192):
        self._url = url
        self._total_size = 0
        self._loaded_size = 0
        self._chunk = chunk

        self._on_load = on_load or (lambda x, y, z: (x, y, z))
        self._on_finish = on_finish or (lambda x: x)

    def _load_data(self):
        response = requests.get(self._url, stream=True)
        self._total_size = int(response.headers['Content-Length'])

        with TemporaryFile('w+b') as temp_file:
            while True:
                chunk = response.raw.read(self._chunk)
                if not chunk:
                    break
                self._loaded_size += len(chunk)
                temp_file.write(chunk)
                self._on_load(chunk, self._loaded_size, self._total_size)

            temp_file.seek(0)

            self._on_finish(temp_file)

        response.close()

    def start(self):
        th = Thread(target=self._load_data)
        th.start()


if __name__ == '__main__':
    url = 'http://ipv4.download.thinkbroadband.com/10MB.zip'

    root = Tkinter.Tk()

    ft = ttk.Frame()

    ft.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)

    pb_hd = ttk.Progressbar(ft, orient='horizontal', mode='determinate')

    pb_hd.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)

    def callback(data, l, t):
        pb_hd['value'] = l * 100.0 / t


    def finish(file):
        print 'Download finished'

    pb_hd['value'] = 0

    Downloader(url, on_load=callback, on_finish=finish).start()

    root.mainloop()





