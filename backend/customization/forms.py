from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.core.validators import FileExtensionValidator, EmailValidator
from shared_models.models import PlaceOfWork, JobType, Interest

class AddInterestForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        max_length=250,
        label='Name of interest',
        required=True,
    )
    # color = forms.CharField(
    #     label='Color',
    #     widget=forms.TextInput(attrs={
    #         'type': 'color',
    #         'class': 'form-control',
    #     })
    # )

class AddCsvForm(forms.Form):
    file = forms.FileField(
        label='',
        required=True,
        validators=[FileExtensionValidator(['csv'])]
    )
    keep_data = forms.BooleanField(
        label='Do not overwrite data',
        required=False
    )

class AddPlaceOfWorkForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Name of place of work',
        required=True
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control w-full max-w-30rem', 'style': 'box-sizing: border-box', 'rows': 3}),
        label='Address',
        required=False
    )
    country = forms.ChoiceField(
        choices=[(country.code, country.name) for country in CountryField().countries],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Country',
        required=True
    )

class AddTargetForm(forms.Form):
    firstname = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter first name'
        }),
        label='Firstname',
        required=True
    )
    lastname = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter last name'
        }),
        label='Lastname',
        required=True
    )
    email = forms.EmailField(
        validators=[EmailValidator()],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email address'
        }),
        label='Email',
        required=True
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter phone number'
        }),
        label='Phone',
        required=False
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control w-full max-w-30rem',
            'style': 'box-sizing: border-box',
            'rows': 3,
            'placeholder': 'Enter address (optional)'
        }),
        label='Address',
        required=False
    )
    country = CountryField().formfield(
        widget=CountrySelectWidget(attrs={
            'class': 'form-control',
        }),
        label='Country',
        required=True
    )
    places_of_work = forms.ModelChoiceField(
        queryset=PlaceOfWork.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Place of Work',
        required=True
    )
    job_type = forms.ModelChoiceField(
        queryset=JobType.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Job Type',
        required=True
    )
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        label='Interests',
        required=False
    )

    def clean_email(self):
        """Custom validation for email."""
        email = self.cleaned_data.get('email')
        if "example.com" in email:
            raise forms.ValidationError("Emails from 'example.com' are not allowed.")
        return email
