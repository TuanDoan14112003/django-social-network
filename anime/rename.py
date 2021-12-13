from django.utils.deconstruct import deconstructible
from uuid import uuid4
import os


@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
        print('instance: ', instance)
        print('ext: ', ext)
        print('filename: ', filename)
        # return the whole path to the file
        final_image_url = os.path.join(self.path, filename)
        print(final_image_url)
        return final_image_url
