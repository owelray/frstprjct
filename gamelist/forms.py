from django import forms


class ReviewForm(forms.Form):
    title = forms.CharField(required=True, max_length=128, widget=forms.TextInput(attrs={
                                                           'placeholder': 'Enter game title',
                                                           'autocomplete': 'off', 'maxlength':'128',
                                                           'contenteditable': 'true', 'spellcheck': 'false',
                                                            'class': 'search-input'}))
    review = forms.CharField(required=True, max_length=1000, widget=forms.Textarea(attrs={'autocomplete': 'off',
                                                           'placeholder': 'Write your review (1000 symbols max)',
                                                           'maxlength': '1000', 'name': 'textarea', 'id': 'textarea'}))
    game_api_id = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'autocomplete': 'off',
                                                                'class': 'hidden', 'name': 'game-id',
                                                                'id': 'gameid', 'contenteditable': 'false'}))
