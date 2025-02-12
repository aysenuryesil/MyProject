import os
import sys

from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        signal_path = os.path.join(base_dir, 'signal.py')
        sys.path.append(os.path.dirname(signal_path))
