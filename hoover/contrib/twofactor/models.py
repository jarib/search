import random
import math
from django.conf import settings
from django.db import models

VOCABULARY = u'abcdefghijklmnopqrstuvwxyz0123456789'
REQUIRED_ENTROPY = 40

def random_code():
    entropy_per_char = math.log(len(VOCABULARY), 2)
    chars = int(math.ceil(REQUIRED_ENTROPY / entropy_per_char))
    urandom = random.SystemRandom()
    return ''.join(urandom.choice(VOCABULARY) for _ in range(chars))

class Invitation(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    code = models.CharField(max_length=200, default=random_code)
    generated = models.DateTimeField()