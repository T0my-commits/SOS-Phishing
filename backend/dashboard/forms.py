from django import forms

class CampaignNotesForm(forms.Form):
    notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full p-3 mb-3 surface-100',
            'style': 'height: 80vh; box-sizing: border-box; font-family: Monospace;',
            'placeholder': 'Your notes here',
        }),
        label='',
        required=False,
    )
