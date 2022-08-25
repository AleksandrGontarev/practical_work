from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext_lazy
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=gettext_lazy("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email']


class ContactFrom(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def clean_from_email(self):
        data = self.cleaned_data['from_email']

        if data.strip().endswith("mail.ru"):
            raise ValidationError(_("We can't send email on mail.ru emails"))

        return data

    def clean(self):
        email = self.cleaned_data['from_email']
        subject = self.cleaned_data['subject']

        if email.endswith("gmail.com") and "spam" in subject.lower():
            self.add_error(None, "Can't send spam emails")
