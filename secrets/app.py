from flask import Flask, g
from .storage import Storage

app = Flask(__name__)

def get_st():
    if not hasattr(g, 'storage'):
        g.storage = Storage(app.config['DATA_DIR'])
    return g.storage

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'storage'):
        g.storage.close()
