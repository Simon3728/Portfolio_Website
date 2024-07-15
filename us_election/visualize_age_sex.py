"""
This script reads population data from a Django database, processes it, and displays it using a GUI.
It provides visualizations of population distribution by age and gender.
"""

import os
import django
import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Tk, StringVar, OptionMenu, Frame, BOTH, HORIZONTAL, IntVar, Scale, Label

# Set up Django environment
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myportfolio.settings')
django.setup()

from us_election.models import PopulationData

def fetch_population_data():
    """
    Fetch population data from the Django database and return it as a pandas DataFrame.
    """
    queryset = PopulationData.objects.all().values(
        'name', 'year', 'total_population', 'population_0_4', 'population_5_17', 'population_18_24',
        'population_25_44', 'population_45_64', 'population_65_plus', 'male_population', 'female_population'
    )
    return pd.DataFrame.from_records(queryset)

def plot_population_data(df, state_name, year):
    """
    Plot the population data for a specific state and year.
    """
    result = df[(df['name'] == state_name) & (df['year'] == year)]

    if result.empty:
        raise ValueError(f"No data found for the year {year} and state {state_name}")

    result = result.iloc[0]

    name = result['name']
    total_population = result['total_population']
    age_groups = [
        result['population_0_4'], result['population_5_17'], result['population_18_24'],
        result['population_25_44'], result['population_45_64'], result['population_65_plus']
    ]
    gender_population = [result['male_population'], result['female_population']]

    age_labels = ['0-4', '5-17', '18-24', '25-44', '45-64', '65+']
    gender_labels = ['Male', 'Female']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Plot age group distribution
    bars = ax1.bar(age_labels, age_groups)
    ax1.set_title('Population Distribution by Age')
    ax1.set_ylabel('Population')

    # Plot gender distribution
    gender_bars = ax2.bar(gender_labels, gender_population)
    ax2.set_title('Population Distribution by Gender')
    ax2.set_ylabel('Population')

    fig.suptitle(f'{name} (Total Population: {total_population}) - Year {year}', fontsize=16)

    return fig, bars, gender_bars, name, total_population, year

def update_plot(*args):
    """
    Update the plot based on the selected state and year.
    """
    state_name = selected_state.get()
    year = selected_year.get()
    fig, bars, gender_bars, name, total_population, year = plot_population_data(df, state_name, year)
    
    # Update the figure in the canvas
    canvas.figure = fig
    canvas.draw()

def on_closing():
    """
    Handle the GUI closing event.
    """
    root.quit()
    root.destroy()

def main():
    """
    Set up and run the GUI for displaying population data.
    """
    global selected_state, selected_year, df, bars, gender_bars, fig, canvas

    df = fetch_population_data()

    state_names = sorted(df['name'].unique())

    global root
    root = Tk()
    root.title("Population Data Viewer")
    root.geometry("1200x800")
    root.protocol("WM_DELETE_WINDOW", on_closing)

    selected_state = StringVar(root)
    selected_state.set(state_names[0])
    selected_state.trace_add('write', update_plot)

    selected_year = IntVar(root)
    selected_year.set(2019)
    selected_year.trace_add('write', update_plot)

    controls_frame = Frame(root)
    controls_frame.pack()

    # Dropdown for selecting state
    dropdown_state = OptionMenu(controls_frame, selected_state, *state_names)
    dropdown_state.grid(row=0, column=0, padx=5, pady=5)

    year_label = Label(controls_frame, text="Year:")
    year_label.grid(row=0, column=1, padx=5, pady=5)

    # Slider for selecting year
    year_slider = Scale(controls_frame, from_=2000, to=2019, orient=HORIZONTAL, variable=selected_year)
    year_slider.grid(row=0, column=2, padx=5, pady=5)

    plot_frame = Frame(root)
    plot_frame.pack(fill=BOTH, expand=True)

    # Initial plot
    fig, bars, gender_bars, name, total_population, year = plot_population_data(df, selected_state.get(), selected_year.get())

    # Create canvas to display the plot in the Tkinter GUI
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
