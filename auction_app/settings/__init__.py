from .base import *
import os

'''settings for different environments'''

if os.environ.get("ENV_NAME") == 'Production':
    from .production import *
elif os.environ.get("ENV_NAME") == 'Staging':
    '''environment that is as identical to the production environment, simulate the Production environment'''
    from .staging import *
elif os.environ.get("ENV_NAME") == 'Integration':
    '''combine and validate the work of the entire project team'''
    from .integration import *
else:
    '''working environment for individual developers'''
    from .development import *