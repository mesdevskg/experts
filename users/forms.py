from django import forms
from django.contrib.auth.forms import UsernameField
from django.utils.translation import gettext_lazy as _

from items.models import Book
from users.models import User


class UserForm(forms.Form):
    TYPE_CHOICES = (
        ('', '---------'),
        ('илимий', 'илимий'),
        ('илимий-педагогикалык', 'илимий-педагогикалык'),
        ('антидискриминациялык жана гендердик', 'антидискриминациялык жана гендердик')
    )
    book = forms.ModelChoiceField(queryset=Book.objects.all(), label=_('book'))
    type = forms.ChoiceField(choices=TYPE_CHOICES, label=_('type'))

    okuu_kitep = forms.CharField(max_length=255, label=_('Okuu Kitep'))
    okuu_kitep_password = forms.CharField(widget=forms.PasswordInput(), label=_('PWD of Okuu Kitep'))

    sector_knigi = forms.CharField(max_length=255, label=_('Sector knigi'))
    sector_knigi_password = forms.CharField(widget=forms.PasswordInput(), label=_('PWD of Sector knigi'))


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    class Meta:
        model = User
        fields = 'email',
        field_classes = {'email': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

        return user
