__author__ = 'lian'

import hashlib
import random
from tutors.models import UserActivation
from tutors.email import send_user_account_activation_email
import logging

logger = logging.getLogger(__name__)


def create_activation_key(input_string):
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    activation_key = hashlib.sha1(salt + input_string).hexdigest()

    return activation_key


def generate_and_send_activation_email(user):
    if user:
        if user.email:
            # generate random key
            activation_key = create_activation_key(user.email)

            # remove old activation keys
            UserActivation.objects.filter(user=user).delete()

            # create new activation
            user_activate = UserActivation(user=user, activation_key=activation_key)
            user_activate.save()

            # send email
            send_user_account_activation_email(user, activation_key)
        else:
            logger.error("User %s has no email address" % user.username)
    else:
        logger.error("No user was passed into function generate_and_send_activation_email")
