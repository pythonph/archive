from django import forms


class ImageWidget(forms.FileInput):
    template = '%(input)s<br />%(image)s'

    def __init__(self, attrs=None, template=None, width=200, height=200):
        if template is not None:
            self.template = template
        self.width = width
        self.height = height
        self.image_url = None
        super(ImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        input_html = super(forms.FileInput, self).render(name, value, attrs)
        if self.image_url:
            output = self.template % {
                'input': input_html,
                'image': '<img src="%s" />' % self.image_url
            }
        else:
            output = input_html
        return mark_safe(output)
