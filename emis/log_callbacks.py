import logging

from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)
from django.dispatch import receiver

LOGGER = logging.getLogger("emis-pas")


@receiver(user_logged_in)
def login_callback(sender, request, user, **kwargs):
    LOGGER.info('user "{}" logged in'.format(user))


@receiver(user_logged_out)
def logout_callback(sender, request, user, **kwargs):
    LOGGER.info('user "{}" logged out'.format(user))


@receiver(user_login_failed)
def login_failed_callback(sender, credentials, **kwargs):
    LOGGER.warning("failed login attempt: {}".format(credentials))
