from django import forms

class UrlForm(forms.Form):
    url = forms.URLField(required=True, widget=forms.URLInput(attrs={
                                            'placeholder': 'Enter your url',
                                            'autocomplete': 'off',
                                            'max-length': '252'}))
    shortening_method = forms.BooleanField(required=False)
