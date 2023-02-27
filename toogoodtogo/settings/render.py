import os

os.environ['ALLOWED_HOSTS'] = os.environ['RENDER_EXTERNAL_HOSTNAME']

from production import *
