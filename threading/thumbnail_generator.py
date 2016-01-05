from os import path, listdir, mkdir

from multiprocessing.pool import Pool
from PIL import Image

import argparse

from sys import argv, exit


class ThumbnailCreator(object):

    def __init__(self, dest_path, sizes=(200, 200)):
        if not path.isdir(dest_path):
            mkdir(dest_path)


        self._dest_path = dest_path
        self._sizes = sizes

    def __call__(self, image_path):
        image = Image.open(image_path)

        image.thumbnail(self._sizes, Image.ANTIALIAS)
        image_path, extension = path.splitext(image_path)
        filename = "%s.thumb%s" % (path.basename(image_path), extension)
        dest_path = path.join(self._dest_path, filename)

        image.save(dest_path)


class ImageProcessor(object):

    def __init__(self, process_func, processes=None):
        self._pool = Pool(processes)
        self._func = process_func

    def process_folder(self, image_path):
        if not path.isdir(image_path):
            raise ValueError('%s is not directory.' % path)

        files = listdir(image_path)

        files = filter(lambda x: path.isfile(path.join(image_path, x)), files)
        files = map(lambda x: path.join(image_path, x), files)

        self._pool.map(self._func, files)

        self._pool.close()
        self._pool.join()


def parse():
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--source', help="Generate thumbs for all images from this directory.")

    parser.add_argument('-d', '--destination', help="Target directory path.")

    parser.add_argument('--size', help='Size of thumbnails', type=str, default="200x200")
    args = parser.parse_args()

    if len(argv) == 1:
        parser.print_help()
        exit(1)

    return args

if __name__ == '__main__':
    args = parse()

    thumb_creator = ThumbnailCreator(args.destination, tuple(map(int, args.size.split('x'))))
    image_processor = ImageProcessor(thumb_creator)

    image_processor.process_folder(args.source)


