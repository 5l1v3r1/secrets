import os.path
import sqlite3


class SuchSecret(Exception):

    def __init__(self, name, *args, **kwargs):
        self.name = name
        Exception.__init__(self, *args, **kwargs)


class NoSuchSecret(Exception):

    def __init__(self, name, *args, **kwargs):
        self.name = name
        Exception.__init__(self, *args, **kwargs)


class Storage():

    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.conn = sqlite3.connect(os.path.join(data_dir, 'db.sqlite'))


    def close(self):
        self.conn.close()


    def note_path(self, message_id):
        return os.path.join(self.data_dir, 'notes', str(message_id))


    def file_path(self, message_id):
        return os.path.join(self.data_dir, 'files', str(message_id))


    def file_name(self, message_id):
        filename, = next(self.conn.cursor().execute('select filename from messages where id = ?', (message_id,)))
        return filename


    def get_names(self):
        return list(map(lambda x: x[0], self.conn.cursor().execute('select name from secrets')))


    def get_secret(self, name):
        it = self.conn.cursor().execute('select id, head from secrets where name = ?', (name,))
        try:
            return next(it)
        except StopIteration:
            raise NoSuchSecret(name)


    def create_secret(self, name):
        try:
            self.get_secret(name)
            raise SuchSecret(name)
        except NoSuchSecret:
            self.conn.cursor().execute('insert into secrets (name) values (?)', (name,))
            self.conn.commit()


    def get_messages(self, name):
        id, head = self.get_secret(name)
        messages = []
        c = self.conn.cursor()
        while head is not None:
            has_note, filename, prev = next(c.execute('select has_note, filename, prev from messages where id = ?', (head,)))
            if has_note:
                with open(self.note_path(head), 'r') as f:
                    note = f.read()
            else:
                note = None
            messages.append((head, note, filename))
            head = prev
        return messages


    def update_message(self, name, note, file):
        id, head = self.get_secret(name)
        c = self.conn.cursor()
        filename = file.filename if file is not None else None
        c.execute('insert into messages (has_note, filename, prev) values (?, ?, ?)', (note is not None, filename, head))
        mid = c.lastrowid
        c.execute('update secrets set head = ? where id = ?', (mid, id))
        if note is not None:
            with open(self.note_path(mid), 'w') as f:
                f.write(note)
        if file is not None:
            file.save(os.path.join(self.data_dir, 'files', str(mid)))
        self.conn.commit()
