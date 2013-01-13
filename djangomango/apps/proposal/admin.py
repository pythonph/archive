from django.contrib import admin

from .models import ProposalType, AudienceLevel, Category, Proposal


admin.site.register(ProposalType)
admin.site.register(Category)
admin.site.register(AudienceLevel)
admin.site.register(Proposal)
