from django import forms

from weather.models import Weather, City


class AddForm(forms.ModelForm):
    city = forms.CharField(max_length=100, label='City')  # Use ModelChoiceField for cities.

    class Meta:
        model = City
        fields = ['city']
