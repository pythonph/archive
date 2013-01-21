from django import forms
from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe


class ThumbnailImageWidget(forms.ClearableFileInput):
    """
    Image widget that knows how to display thumbnail when one is present.
    """

    template_with_clear = u"""
        <label class="checkbox" for="%(clear_checkbox_id)s">
            %(clear)s %(clear_checkbox_label)s
        </label>"""
    template_with_initial = u"""
        <div class="thumbnail">%(initial)s</div>
        <div class="clear-field">%(clear_template)s</div>
        <div class="clear-field">%(input)s</div>"""

    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = u'%(input)s'
        substitutions['input'] = super(forms.ClearableFileInput,
                                       self).render(name, value, attrs)

        if self.thumbnail:
            template = self.template_with_initial
            substitutions['initial'] = '<img src="%s">' % self.thumbnail.url

            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(
                    checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(
                    checkbox_id)
                substitutions['clear'] = forms.CheckboxInput().render(
                    checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = \
                    self.template_with_clear % substitutions

        return mark_safe(template % substitutions)
