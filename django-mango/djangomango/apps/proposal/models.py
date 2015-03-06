from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from autoslug import AutoSlugField

from ..mango.models import BaseModel


PENDING = 'pending'
APPROVED = 'approved'
DECLINED = 'declined'

PROPOSAL_STATUS = (
    (PENDING, _(u'Pending')),
    (APPROVED, _(u'Approved')),
    (DECLINED, _(u'Declined'))
)


class ProposalType(models.Model):
    """ Talks, Tutorials or Posters """
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    """ Cloud, Education, Databases, etc. """
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = _(u'Categories')

    def __unicode__(self):
        return self.name


class AudienceLevel(models.Model):
    """ Novice, Intermediate or Experienced """
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Proposal(BaseModel):
    speaker = models.ForeignKey(User, related_name='proposals')
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', unique=True)
    type = models.ForeignKey(ProposalType)
    audience = models.ForeignKey(AudienceLevel)
    category = models.ForeignKey(Category)
    description = models.TextField()
    abstract = models.TextField()
    duration = models.TimeField()
    status = models.CharField(max_length=10, choices=PROPOSAL_STATUS,
                              default='pending')

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('proposal_details', [self.slug])
