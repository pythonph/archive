from django import forms
from django.utils.html import escape
from django.utils.safestring import mark_safe


class ThumbnailImageWidget(forms.FileInput):
    """
    Image widget that knows how to display thumbnail when one is present.
    """

    template = '<div class="thumbnail">%(image)s</div>%(input)s'

    def render(self, name, value, attrs=None):
        input_html = super(ThumbnailImageWidget, self).render(name, value, attrs)

        if self.thumbnail:
            output = self.template % {
                'input': input_html,
                'image': '<img src="%s">' % self.thumbnail.url
            }
        else:
            output = input_html
        return mark_safe(output)
