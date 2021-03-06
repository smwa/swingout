from django import forms
from i18n_discoverer.translation import gettext as _, pgettext as _p
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, HTML, ButtonHolder, Submit, Row

from .models import Style, Community

CONTACT_TYPES = (
    ('emailAddress', 'Email'),
    ('phoneNumber', 'Phone'),
    ('url', 'Website'),
)

STYLES_SORTED = list(Style.STYLES)
STYLES_SORTED.sort(key=lambda x:x[1])
STYLES_SORTED = tuple(STYLES_SORTED)

STRUCTURES = [('', '')]
STRUCTURES.extend(Community.STRUCTURES)

_label_help_text = "{}: {}".format(_('Example'), _p("Community name example", "Lovely Band o' Pirates"))
_url_help_text = "{}: {}".format(_('Example'), _p("Community URL example", "https://www.facebook.com/groups/42"))
_email_contact_example = _p("Contact information example for email address", "sofia@gmail.com")
_phone_contact_example = _p("Contact information example for phone number", "+1-972-867-5309")
_url_contact_example = _p("Contact information example for URL", "https://www.facebook.com/john")
_contact_help_text = "{}: {}, {}, {}".format(_('Examples'), _email_contact_example, _phone_contact_example, _url_contact_example)
_contact_disclaimer = _('This will not be shown publicly. We will use this information to contact you and verify or request details.')

class AddCommunityForm(forms.Form):
    label = forms.CharField(label=_('Name'), max_length=512, help_text=_label_help_text)
    structure = forms.ChoiceField(label=_("Organization Type"), choices=STRUCTURES)
    latitude = forms.FloatField(max_value=90.0, min_value=-90.0, widget=forms.HiddenInput())
    longitude = forms.FloatField(max_value=80.0, min_value=-180.0, widget=forms.HiddenInput())
    url = forms.URLField(label=_('Website'), max_length=512, help_text=_url_help_text)
    styles = forms.MultipleChoiceField(label=_("Dance Styles"), choices=STYLES_SORTED, widget=forms.SelectMultiple(attrs={'style': 'width: 100%'}))

    contactOneType = forms.ChoiceField(label=_p("Contact type", "Type"), choices=CONTACT_TYPES)
    contactOne = forms.CharField(label=_p("Contact information", "Information"), max_length=512, help_text=_contact_help_text)
    contactTwoType = forms.ChoiceField(label=_p("Contact type", "Type"), choices=CONTACT_TYPES, required=False, initial=CONTACT_TYPES[1])
    contactTwo = forms.CharField(label=_p("Contact information", "Information"), max_length=512, required=False, help_text=_contact_help_text)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                _('Details'),
                'label',
                'structure',
                'url',
                'styles',
            ),
            Fieldset(
                '{} - <small>{}</small>'.format(_('Contacts'), _contact_disclaimer),
                Row('contactOneType', 'contactOne'),
                Row('contactTwoType', 'contactTwo'),
            ),
            ButtonHolder(
                Submit('submit', _('Preview'), css_class='btn-lg'),
                HTML('<a class="btn btn-secondary btn-lg" href="{}">{}</a>'.format(reverse('communities:map'), _("Cancel")))
            ),
        )

class UpdateCommunityForm(forms.Form):
    label = forms.CharField(label=_('Name'), max_length=512, help_text=_label_help_text)
    structure = forms.ChoiceField(label=_("Organization Type"), choices=STRUCTURES)
    url = forms.URLField(label=_('Website'), max_length=512, help_text=_url_help_text)
    styles = forms.MultipleChoiceField(label=_("Dance Styles"), choices=STYLES_SORTED, widget=forms.SelectMultiple(attrs={'style': 'width: 100%'}))
    latitude = forms.FloatField(max_value=90.0, min_value=-90.0)
    longitude = forms.FloatField(max_value=80.0, min_value=-180.0)

    contactOneType = forms.ChoiceField(label=_p("Contact type", "Type"), choices=CONTACT_TYPES)
    contactOne = forms.CharField(label=_p("Contact information", "Information"), max_length=512, help_text=_contact_help_text)
    contactTwoType = forms.ChoiceField(label=_p("Contact type", "Type"), choices=CONTACT_TYPES, required=False, initial=CONTACT_TYPES[1])
    contactTwo = forms.CharField(label=_p("Contact information", "Information"), max_length=512, required=False, help_text=_contact_help_text)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                _('Details'),
                'label',
                'structure',
                'url',
                'styles',
                'latitude',
                'longitude',
            ),
            Fieldset(
                '{} - <small>{}</small>'.format(_('Contacts'), _contact_disclaimer),
                Row('contactOneType', 'contactOne'),
                Row('contactTwoType', 'contactTwo'),
            ),
            ButtonHolder(
                Submit('submit', _('Save'), css_class='btn-lg'),
                HTML('<a class="btn btn-secondary btn-lg" href="{}">{}</a>'.format(reverse('communities:map'), _("Cancel")))
            ),
        )

class RequestCommunityUpdateForm(forms.Form):
    help_text = _("Tell us what you want changed, or if this community should be removed. "
              + "Providing a reason may help us make changes sooner. "
              + "You may put your contact information so we can ask you further questions. ")
    message = forms.CharField(label=_('Message'), help_text=help_text, widget=forms.Textarea())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                _('Request Update'),
                'message',
            ),
            ButtonHolder(
                Submit('submit', _('Submit'), css_class='btn-lg')
            ),
        )
