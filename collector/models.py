import hashlib
import json
from django.db import models
from django.dispatch import receiver
from django.conf import settings
from django.utils.module_loading import import_string
from . import es


class Collection(models.Model):

    title = models.CharField(max_length=2048, blank=True)
    slug = models.CharField(max_length=256, unique=True)

    public = models.BooleanField(default=False)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    loader = models.CharField(max_length=2048,
        default='collector.loaders.collectible.Loader')
    options = models.TextField(default='{}')

    def __unicode__(self):
        return self.slug

    def get_loader(self):
        cls = import_string(self.loader)
        return cls(**json.loads(self.options))

    def label(self):
        return self.title or self.slug

    @classmethod
    def objects_for_user(cls, user):
        rv = set(cls.objects.filter(public=True))
        if user.id is not None:
            rv.update(cls.objects.filter(users__id=user.id))
        return rv

    def count(self):
        return es.count(self.id)

    def access_list(self):
        return ', '.join(u.username for u in self.users.all())


@receiver(models.signals.post_save, sender=Collection)
def create_es_index(instance, created, **kwargs):
    if created:
        es.create_index(instance.id, instance.slug)
