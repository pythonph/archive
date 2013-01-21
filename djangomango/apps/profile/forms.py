from django import forms
from django.contrib.auth.models import User

from .models import UserProfile
from ..mango.widgets import ThumbnailImageWidget


class UserProfileForm(forms.ModelForm):
    mugshot = forms.ImageField(widget=ThumbnailImageWidget)
    first_name = forms.CharField()
    last_name = forms.CharField()

    def __init__(self, *args, **kwargs):
        form = super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['mugshot'].widget.thumbnail = self.instance.mugshot_thumbnail

    class Meta:
        model = UserProfile
        fields = ('mugshot', 'first_name', 'last_name', 'bio',)
