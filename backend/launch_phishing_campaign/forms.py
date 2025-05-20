from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now
from shared_models.models import Campaign, Target

class LaunchPhishingCampaign(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter campaign name'
        }),
        label='Campaign Name',
        required=True
    )
    type = forms.ChoiceField(
        choices=Campaign.CAMPAIGN_TYPES,
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        label="Campaign Type",
        required=True
    )
    expected_signaling = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a percentage value between 0 and 100'
        }),
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        label='Expected Signaling (%)',
        required=True
    )
    compromise_type = forms.ChoiceField(
        choices=Campaign.COMPROMISE_TYPES,
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        label="Compromise Type",
        required=True
    )
    start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        label="Start Date",
        required=True,
        initial=now
    )
    end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        label="End Date",
        required=True
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a brief description of the campaign',
            'rows': 4
        }),
        label='Description',
        required=False
    )
    targets = forms.ModelMultipleChoiceField(
        queryset=Target.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        label="Select Targets",
        required=False
    )
