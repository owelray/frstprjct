from django import forms


class ReviewForm(forms.Form):
    title = forms.CharField(required=True, max_length=128, widget=forms.TextInput(attrs={
                                                           'placeholder': 'Enter game title',
                                                           'autocomplete': 'off', 'maxlength':'128',
                                                           'contenteditable': 'true', 'spellcheck': 'false'}))
    review = forms.CharField(required=True, max_length=450, widget=forms.Textarea(attrs={'autocomplete': 'off',
                                                           'placeholder': 'Write your review (450 symbols max)',
                                                           'maxlength': '450', 'name': 'textarea', 'id': 'textarea'}))
