from django.shortcuts import render
from .forms import PopulationForm, ElectionYearForm
import io
import base64
import matplotlib.pyplot as plt
from .models import PopulationData
from .visualize_election import generate_election_map

# Create your views here.
def us_election(request):
    select1_value = None
    select2_value = None
    updated_data = None
    bar_chart_url = None
    pie_chart_url = None
    selected_election_year = None
    election_map_url = None

    form = PopulationForm(initial={'state': 'default_state', 'year': 'default_year'})
    year_form = ElectionYearForm()

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'population_form':
            form = PopulationForm(request.POST)
            if form.is_valid():
                select1_value = form.cleaned_data['state']
                select2_value = form.cleaned_data['year']
                updated_data = f"Updated data based on selections: {select1_value}, {select2_value}"
                # Fetch data from the database
                data = PopulationData.objects.filter(name=select1_value, year=select2_value).first()
                if data:
                    # Create bar chart
                    fig, ax = plt.subplots()
                    age_groups = ['0-4', '5-17', '18-24', '25-44', '45-64', '65+']
                    population_values = [
                        data.population_0_4, data.population_5_17, data.population_18_24,
                        data.population_25_44, data.population_45_64, data.population_65_plus
                    ]
                    ax.bar(age_groups, population_values)
                    ax.set_xlabel('Age Groups')
                    ax.set_ylabel('Population')
                    ax.set_title(f'Population Distribution in {select1_value} for {select2_value}\nTotal Population: {data.total_population:,}')

                    # Save bar chart to a BytesIO object
                    buf = io.BytesIO()
                    plt.savefig(buf, format='png')
                    buf.seek(0)
                    bar_chart_url = 'data:image/png;base64,' + base64.b64encode(buf.read()).decode('utf-8')
                    buf.close()

                    # Create pie chart
                    fig, ax = plt.subplots()
                    labels = 'Male', 'Female'
                    sizes = [data.male_population, data.female_population]
                    colors = ['blue', 'red']
                    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
                    ax.axis('equal')  
                    ax.set_title(f'Male vs Female Population in {select1_value} for {select2_value}')

                    # Save pie chart to a BytesIO object
                    buf = io.BytesIO()
                    plt.savefig(buf, format='png')
                    buf.seek(0)
                    pie_chart_url = 'data:image/png;base64,' + base64.b64encode(buf.read()).decode('utf-8')
                    buf.close()
        elif form_type == 'election_year_form':
            year_form = ElectionYearForm(request.POST)
            if year_form.is_valid():
                selected_election_year = year_form.cleaned_data['year']
                # Generate the election map
                buf = generate_election_map(selected_election_year)
                election_map_url = 'data:image/png;base64,' + base64.b64encode(buf.read()).decode('utf-8')
                buf.close()

    context = {
        'form': form,
        'year_form': year_form,
        'select1_value': select1_value,
        'select2_value': select2_value,
        'updated_data': updated_data,
        'bar_chart_url': bar_chart_url,
        'pie_chart_url': pie_chart_url,
        'selected_election_year': selected_election_year,
        'election_map_url': election_map_url,
    }
    return render(request, 'projects/us_election.html', context)



