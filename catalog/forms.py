from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime  # for checking renewal date range.

from django import forms
from .models import Comment, Basket, BookSearch, Profile, Genre, Language
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SearchBookForm(forms.ModelForm):
    name = forms.CharField(max_length=100, widget = forms.TextInput(attrs={"class": "form-control m-2", "placeholder": "Enter book name",}))

    class Meta:
        model = BookSearch
        fields = ['name',]


class RenewBookForm(forms.Form):
    """Form for a librarian to renew books."""
    renewal_date = forms.DateField(
            help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check date is not in past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
        # Check date is in range librarian allowed to change (+4 weeks)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['create_at', 'book']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'name'}),
            'email':forms.EmailInput(attrs={'placeholder': 'email'}),
            'website':forms.TextInput(attrs={'placeholder': 'website'}),
            'message': forms.Textarea(attrs={'placeholder': 'message'})
        }

class AddToBasketForm(forms.ModelForm):
    class Meta:
        model = Basket
        fields = ['book']
        widgets = {
            'book': forms.HiddenInput(),
        }

class ProfileForm(forms.ModelForm):
    preferred_genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    preferred_languages = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Profile
        fields = ['preferred_genres', 'preferred_languages']


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']