from django.db import models


class AuditableModel(models.Model):
    """ Base model with simple auditing fields. """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True
