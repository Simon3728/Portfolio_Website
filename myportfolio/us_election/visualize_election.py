import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import io
from .models import ElectionResult
from django.db.models import Sum

# Set Matplotlib backend to Agg
plt.switch_backend('Agg')

def calculate_total_results(election_df):
    """
    Calculate the total results of the election in percentages.
    """
    total_votes = election_df['total'].sum()
    total_democratic = election_df['democratic'].sum()
    total_republican = election_df['republican'].sum()
    
    democratic_percentage = (total_democratic / total_votes) * 100
    republican_percentage = (total_republican / total_votes) * 100
    
    return democratic_percentage, republican_percentage

def generate_election_map(year):
    # Load the shapefile for US states
    shapefile_path = 'us_election/shp/States_shapefile.shp'  # Update this to your shapefile path
    gdf = gpd.read_file(shapefile_path)
    
    results = ElectionResult.objects.filter(year=year).values('state', 'republican', 'democratic', 'total')
    
    results_df = pd.DataFrame(list(results))
    results_df['state'] = results_df['state'].str.upper()
    
    results_df['dominant_party'] = results_df.apply(lambda row: 'republican' if row['republican'] > row['democratic'] else 'democratic', axis=1)
    results_df['margin_of_victory'] = abs(results_df['republican'] - results_df['democratic']) / results_df['total']
    
    merged = gdf.merge(results_df, how='left', left_on='State_Name', right_on='state')  # Use the correct column name

    # Handle NaN values
    merged['dominant_party'] = merged['dominant_party'].fillna('unknown')
    merged['margin_of_victory'] = merged['margin_of_victory'].fillna(0)
    
    # Calculate total results
    democratic_percentage, republican_percentage = calculate_total_results(results_df)

    # Create the map
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    merged.boundary.plot(ax=ax, edgecolor='black')

    party_colors = {'republican': (1, 0, 0), 'democratic': (0, 0, 1), 'unknown': (0.7, 0.7, 0.7)}  # RGB values for red, blue, and grey

    merged['color'] = merged.apply(
        lambda row: (*party_colors[row['dominant_party']], min(1, max(0.4, row['margin_of_victory'] * 2))),
        axis=1
    )
    
    # Plot the map with the calculated colors
    merged.plot(ax=ax, color=merged['color'], edgecolor='black')
    
    for _, row in merged.iterrows():
        state_center = row['geometry'].centroid
        state_name = row['State_Code']
        dominant_party = row['dominant_party']
        percentage = row[dominant_party] / row['total'] * 100  # Calculate the winning party's percentage
        text = f"{state_name}\n{percentage:.1f}%"
        
        ax.text(state_center.x, state_center.y, text, horizontalalignment='center', fontsize=8, 
                bbox=dict(facecolor='white', alpha=0.5, boxstyle='round,pad=0.3'))
        
    ax.set_title(f'US Election Results by State - {year}', fontsize=15)
    plt.suptitle(f'Total Results: Democrats {democratic_percentage:.2f}%, Republicans {republican_percentage:.2f}%', fontsize=12)
    
    ax.set_axis_off()
    
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=(party_colors[party][0], party_colors[party][1], party_colors[party][2], 0.7), markersize=10, label=party.title())
               for party in party_colors]
    ax.legend(handles=handles, loc='lower left')

    # Save to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf