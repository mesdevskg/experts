from django import forms

from items.models import Book


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = 'name',
