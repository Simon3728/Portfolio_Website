"""
Forms for selecting the data to plot in the Election project page.

This file contains forms to allow users to select states and years for population data,
as well as election years for visualization in the Election project.
"""

from django import forms
from .models import PopulationData

def get_state_choices():
    """
    Retrieve distinct state names from PopulationData and format them as choices.
    """
    states = PopulationData.objects.values_list('name', flat=True).distinct().order_by('name')
    return [(state, state) for state in states]

def get_year_choices():
    """
    Retrieve distinct years from PopulationData and format them as choices.
    """
    years = PopulationData.objects.values_list('year', flat=True).distinct().order_by('year')
    return [(year, year) for year in years]

# Predefined choices for election years
ELECTION_YEAR_CHOICES = [
    ('2000', '2000'),
    ('2004', '2004'),
    ('2008', '2008'),
    ('2012', '2012'),
    ('2016', '2016'),
    ('2020', '2020'),
]

class PopulationForm(forms.Form):
    """
    Form for selecting state and year from PopulationData.

    Fields:
        state (ChoiceField): Dropdown for selecting a state.
        year (ChoiceField): Dropdown for selecting a year.
    """
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
    """
    Form for selecting an election year from predefined choices.

    Fields:
        year (ChoiceField): Dropdown for selecting an election year.
    """
    year = forms.ChoiceField(
        choices=ELECTION_YEAR_CHOICES,
        label="Select Election Year",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
