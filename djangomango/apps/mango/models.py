from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from imagekit.models import ImageSpecField

from .utils import get_mugshots_path


class BaseModel(models.Model):
    """ Base model with simple auditing fields. """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    mugshot = models.ImageField(upload_to=get_mugshots_path)
    mugshot_thumbnail = ImageSpecField(image_field='mugshot',
                                       format='JPEG',
                                       options={'quality': 90})

    def __unicode__(self):
        return self.user.get_full_name()


def create_user_profile(sender, instance, created, **kwargs):
    """ Create a profile for each user created. """
    if created:
        UserProfile.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)
