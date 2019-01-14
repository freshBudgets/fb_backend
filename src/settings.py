# src/settings.py

import os

if os.environ.get('PRODUCTION'):
    from .production import *
elif os.environ.get('STAGING'):
    from .staging import *
else:
    from .development import * 
