# forms.py
from django import forms
from .models import PopulationData

def get_state_choices():
    states = PopulationData.objects.values_list('name', flat=True).distinct().order_by('name')
    return [(state, state) for state in states]

def get_year_choices():
    years = PopulationData.objects.values_list('year', flat=True).distinct().order_by('year')
    return [(year, year) for year in years]

ELECTION_YEAR_CHOICES = [
    ('2000', '2000'),
    ('2004', '2004'),
    ('2008', '2008'),
    ('2012', '2012'),
    ('2016', '2016'),
    ('2020', '2020'),
]

class PopulationForm(forms.Form):
    state = forms.ChoiceField(
        choices=get_state_choices, 
        label="Select State", 
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    year = forms.ChoiceField(
        choices=get_year_choices, 
        label="Select Year", 
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class ElectionYearForm(forms.Form):
    year = forms.ChoiceField(
        choices=ELECTION_YEAR_CHOICES,
        label="Select Election Year",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
