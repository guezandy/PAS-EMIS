import logging
import os

class AppDebugFilter():
    def __init__(self, app_debug):
        self._app_debug = app_debug
    
    def filter(self, record):
        return self._app_debug


class EmisLogger:

    def get_config(self):
        return self._config
    
    def __init__(self, app_debug: bool, log_dev: bool, log_file_dir: str):

        self._app_debug = app_debug
        self._log_dev = log_dev

        self._log_file_dir = log_file_dir
        if not os.path.isdir(self._log_file_dir):
            # Throw OSError if the configured directory cannot be created
            os.mkdir(self._log_file_dir)

        self._log_file_path = os.path.join(self._log_file_dir, 'emis-pas.log')

        app_level_str = 'DEBUG' if self._app_debug else 'INFO'
        
        # NOTE/TODO: potentially an email handler could be added to this.
        # TODO: consider RotatingFileHandler or similar
        self._config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'main': {
                    'format': '{levelname} {asctime} - {message}',
                    'style': '{',
                },
                'request': {
                    'format': '{levelname} {asctime} - USER {request.user.username}: {message}',
                    'style': '{',
                },
            },
            'filters': {
                'app_debug': {
                    '()': AppDebugFilter,
                    'app_debug': self._app_debug
                },
            },
            'handlers': {
                'console': {
                    'level': app_level_str,
                    'filters': [ 'app_debug' ],
                    'class': 'logging.StreamHandler',
                    'formatter': 'main',
                },
                'console-request': {
                    'level': 'INFO',
                    'filters': [ 'app_debug' ],
                    'class': 'logging.StreamHandler',
                    'formatter': 'request',

                },
                'file': {
                    'level': app_level_str,
                    'class': 'logging.FileHandler',
                    'formatter': 'main',
                    'filename': self._log_file_path,
                },
                'file-request': {
                    'level': 'INFO',
                    'class': 'logging.FileHandler',
                    'formatter': 'request',
                    'filename': self._log_file_path,
                },
            },
            'loggers': {
                'django': {
                    'handlers': [ 'console' ],
                    'propagate': True,
                },
                'django.request': {
                    'handlers': ['console-request', 'file-request'],
                    'level': 'WARNING',
                    'propagate': False,
                },
                'emis-pas': {
                    'handlers': [ 'console', 'file' ],
                    'level': 'DEBUG',
                },
            }
        }