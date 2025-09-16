from django import forms
from django.forms import inlineformset_factory
from .models import TripRequest, Traveler


class FreePlanForm(forms.ModelForm):
    class Meta:
        model = TripRequest
        fields = [
            'origin', 'destination', 'start_date', 'end_date'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'input'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'input'}),
            'origin': forms.TextInput(attrs={'class': 'input'}),
            'destination': forms.TextInput(attrs={'class': 'input'}),
        }

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('start_date')
        end = cleaned.get('end_date')
        if start and end and end < start:
            raise forms.ValidationError('End date must be on or after start date.')
        return cleaned

    # Revert: no class injection


class PaidPlanForm(FreePlanForm):
    BUDGET_CHOICES = [
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('JOD', 'JOD'),
    ]
    TRANSPORT_CHOICES = [
        ('Walk', 'Walk'),
        ('Public transit', 'Public transit'),
        ('Taxi/Rideshare', 'Taxi/Rideshare'),
        ('Rental car', 'Rental car'),
        ('Bike/Scooter', 'Bike/Scooter'),
    ]

    budget_amount = forms.DecimalField(required=False)
    budget_currency = forms.ChoiceField(choices=BUDGET_CHOICES, required=False)
    transport_prefs = forms.MultipleChoiceField(
        choices=TRANSPORT_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    taxi_airport_to_hotel = forms.BooleanField(required=False)

    class Meta(FreePlanForm.Meta):
        fields = FreePlanForm.Meta.fields + [
            'budget_amount', 'budget_currency', 'transport_prefs', 'taxi_airport_to_hotel'
        ]

    def clean(self):
        cleaned = super().clean()
        transports = cleaned.get('transport_prefs') or []
        cleaned['transport_prefs'] = ','.join(transports)
        return cleaned

    # Revert: no class injection


class TravelerForm(forms.ModelForm):
    class Meta:
        model = Traveler
        fields = ['age', 'gender', 'interests', 'disabilities_allergies']
        labels = {
            'disabilities_allergies': 'Disabilities / allergies (optional)'
        }
        widgets = {
            'disabilities_allergies': forms.Textarea()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure the field is optional on the form regardless of model constraints
        self.fields['disabilities_allergies'].required = False

    # Revert: default model choices (Male/Female/Other) and no size overrides


TravelerFormSet = inlineformset_factory(
    TripRequest,
    Traveler,
    form=TravelerForm,
    fields=['age', 'gender', 'interests', 'disabilities_allergies'],
    extra=0,
    min_num=1,
    validate_min=True,
    can_delete=True,
)


