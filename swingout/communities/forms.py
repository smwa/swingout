from django import forms
from django.utils.translation import gettext as _, pgettext as _p

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Row

from .models import Style, Community

CONTACT_TYPES = (
    ('emailAddress', 'Email'),
    ('phoneNumber', 'Phone'),
    ('url', 'URL, such as a Facebook page'),
)

STYLES_SORTED = list(Style.STYLES)
STYLES_SORTED.sort(key=lambda x:x[1])
STYLES_SORTED = tuple(STYLES_SORTED)

class AddCommunityForm(forms.Form):
    label = forms.CharField(label=_('Name'), max_length=512, widget=forms.TextInput(attrs={'placeholder': _("Lovely Band o' Pirates")}))
    structure = forms.ChoiceField(label=_p("Financial structure, like non-profit, business, or unincorporated.", "Type"), choices=Community.STRUCTURES, initial=Community.NON_PROFIT)
    latitude = forms.FloatField(max_value=90.0, min_value=-90.0, widget=forms.HiddenInput())
    longitude = forms.FloatField(max_value=80.0, min_value=-180.0, widget=forms.HiddenInput())
    url = forms.URLField(label=_('Website'), max_length=512, widget=forms.TextInput(attrs={'placeholder': "https://www.facebook.com/groups/42"}))
    styles = forms.MultipleChoiceField(label=_("Dance Styles"), choices=STYLES_SORTED)

    # These fields are referenced in index.css. If you update the field names, update those references.
    contactOneType = forms.ChoiceField(label=_("Type"), choices=CONTACT_TYPES)
    contactOne = forms.CharField(label=_("Information"), max_length=512, widget=forms.TextInput(attrs={'placeholder': "sofia@gmail.com"}))
    contactTwoType = forms.ChoiceField(label=_("Type"), choices=CONTACT_TYPES, required=False, initial=CONTACT_TYPES[1])
    contactTwo = forms.CharField(label=_("Information"), max_length=512, required=False, widget=forms.TextInput(attrs={'placeholder': "1-972-098-4242"}))

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
                '{} - <small>{}</small>'.format(_('Contacts'), _('This will not be shown publicly. We will use this information to contact you and verify or request details.')),
                Row('contactOneType', 'contactOne'),
                Row('contactTwoType', 'contactTwo'),
            ),
            ButtonHolder(
                Submit('submit', _('Submit'), css_class='btn btn-outline-primary btn-lg')
            ),
        )

class RequestCommunityUpdateForm(forms.Form):
    message = forms.CharField(label=_('Message'), widget=forms.Textarea(attrs={'placeholder': _("What do you want changed?")}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                _('Request Update'),
                'message',
            ),
            ButtonHolder(
                Submit('submit', _('Submit'), css_class='btn btn-outline-primary btn-lg')
            ),
        )