# CLIENT_ID = 'YOUR_CLIENT_ID"
CLIENT_ID = ''
# CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
CLIENT_SECRET = ''

try:
   from dev_settings import *
except ImportError:
   pass
