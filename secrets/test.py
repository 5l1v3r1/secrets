import os.path
from secrets.storage import Storage

class File(object):

    def __init__(self, filename, contents):
        self.filename = filename
        self.contents = contents

    def save(self, path, fname):
        with open(os.path.join(path, fname), 'w') as f:
            f.write(self.contents)

st = Storage('data')
