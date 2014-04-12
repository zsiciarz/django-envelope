========
Cookbook
========

Categorized contact form
------------------------

Although the ``category`` field was removed from the default form class in
1.0, you can bring it back to your form using the following subclass::

    from envelope.forms import ContactForm

    from django import forms
    from django.utils.translation import ugettext_lazy as _


    class CategorizedContactForm(ContactForm):
        CATEGORY_CHOICES = (
            ('', _("Choose")),
            (10, _("A general question regarding the website")),
            # ... any other choices you can imagine
            (None, _("Other")),
        )
        category = forms.ChoiceField(label=_("Category"), choices=CATEGORY_CHOICES)

        def __init__(self, *args, **kwargs):
            """
            Category choice will be rendered above the subject field.
            """
            super(CategorizedContactForm, self).__init__(*args, **kwargs)
            self.fields.keyOrder = [
                'sender', 'email', 'category', 'subject', 'message',
            ]

        def get_context(self):
            """
            Adds full category description to template variables in order
            to display the category in email body.
            """
            context = super(CategorizedContactForm, self).get_context()
            context['category'] = self.get_category_display()
            return context

        def get_category_display(self):
            """
            Returns the displayed name of the selected category.
            """
            try:
                category = int(self.cleaned_data['category'])
            except (AttributeError, ValueError, KeyError):
                category = None
            return dict(self.CATEGORY_CHOICES).get(category)
