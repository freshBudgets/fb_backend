# src/settings.py

import os

if os.environ.get('PRODUCTION') == True:
    from .production import *
elif os.environ.get('STAGING') == True:
    from .production import *
else:
    from .development import * 
