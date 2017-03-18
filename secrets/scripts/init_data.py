import sys
from secrets import app
from secrets.app import get_st
import os
from os.path import join, dirname, abspath

PKG_DIR = dirname(dirname(abspath(__file__)))

def main():
    os.makedirs(os.path.join(app.config['DATA_DIR'], 'notes'), exist_ok=True)
    os.makedirs(os.path.join(app.config['DATA_DIR'], 'files'), exist_ok=True)
    with app.app_context():
        st = get_st()
        with open(join(PKG_DIR, 'schema.sql'), 'r') as f:
            st.conn.cursor().executescript(f.read())
        st.conn.commit()
