import hashlib

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from imagekit.imagecache.base import NonValidatingImageCacheBackend
from autoslug import AutoSlugField

from .utils import get_mugshots_path
from ..proposal.models import APPROVED


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    slug = AutoSlugField(
        unique=True,
        always_update=True,
        populate_from=lambda instance: instance.user.get_full_name())
    mugshot = models.ImageField(upload_to=get_mugshots_path,
                                null=True,
                                blank=True)
    mugshot_thumbnail = ImageSpecField(
        [ResizeToFill(200, 200)],
        image_field='mugshot',
        format='JPEG',
        options={'quality': 90})

    bio = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.user.get_full_name()

    def proposals(self):
        """ Return approved proposals. """
        return self.user.proposals.filter(status=APPROVED)

    def gravatar_url(self, size=200):
        """ Builds gravater request URL. """

        # NOTE: if the use of if..else between mugshot and gravater becomes
        # excessive, switch a single point of entry that knows which
        # image to return.

        hasher = hashlib.md5()
        hasher.update(self.user.email)
        hashed_email = hasher.hexdigest()
        return '%s%s?s=%s' % (settings.GRAVATAR_URL, hashed_email, str(size))

    @models.permalink
    def get_absolute_url(self):
        return ('profile_details', [self.slug])


def create_user_profile(sender, instance, created, **kwargs):
    """ Create a profile for each user created. """
    if created:
        UserProfile.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)
