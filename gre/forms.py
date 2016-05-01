from django import forms

class SearchForm(forms.Form):
    commenter = forms.CharField(label='Enter search words separated by comma', max_length = 100)
