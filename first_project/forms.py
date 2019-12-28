from django import forms

class ReviewForm(forms.Form):
    title = forms.CharField(required=True, max_length=60, widget=forms.TextInput(attrs={
                                                            'placeholder': 'Enter the title of the book (60 symbols max)',
                                                           'autocomplete': 'off', 'maxlength':'60',
                                                           'contenteditable':'true',}))
    author = forms.CharField(max_length=35, required=True, widget=forms.TextInput(attrs={'autocomplete': 'off',
                                                            'placeholder': 'Enter author of the book (35 symbols)',
                                                            'maxlength': '35',}))
    review = forms.CharField(max_length=450, required=True, widget=forms.Textarea(attrs={'autocomplete': 'off',
                                                            'placeholder': 'Write your review (450 symbols max)',
                                                            'maxlength': '450'}))

