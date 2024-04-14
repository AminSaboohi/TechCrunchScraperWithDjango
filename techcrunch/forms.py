from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import constances


class SearchByKeywordForm(forms.Form):
    keyword = forms.CharField(label='Keyword', max_length=250)
    page_count = forms.IntegerField(
        label='Page Count',
        min_value=1,
        max_value=constances.MAXIMUM_SEARCH_PAGE_COUNT,
        initial=constances.DEFAULT_SEARCH_PAGE_COUNT,
    )
    user = forms.TextInput(
        attrs={'class': 'form-control', 'value': '',
               'id': 'elder',
               'type': 'hidden'}
    )


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1',
                  'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
