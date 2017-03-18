import os
from secrets.app import app
import secrets.routes

# default cfg
app.config.update(
    ADMIN_PASSWORD = 'password',
    SUPER_SECRET = 'secret',
    DATA_DIR = '/var/lib/secrets',
    )

# override cfg
if 'SECRETS_CONFIG' in os.environ:
    app.config.from_envvar('SECRETS_CONFIG')
