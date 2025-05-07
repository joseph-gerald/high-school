import matplotlib.pyplot as plt
import json

countries_emission = json.load(open("countries_emissions.json"))
countries_emissions_per_capita = json.load(open("countries_emissions_per_capita.json"))

# the format is
"""
[
    [
        "China",
        10006.343
    ],
    [
        "United States of America",
        5212.1623
    ],
    ...
    ]
"""

# i want a bar chat of the top 10 countries with the most emissions and the top 10 countries with the most emissions per capita


def plot_top_10_countries(countries_emission, countries_emissions_per_capita):
    # there should be 2 graphs one with the top 10 countries with most emissions and one with the top 10 countries with most emissions per capita they should be overlaid on top of each other
    
    # get the top 10 countries with the most emissions
    
    top_10_countries_emission = sorted(countries_emission, key=lambda x: x[1], reverse=True)[:10]
    top_10_countries_emissions_per_capita = sorted(countries_emissions_per_capita, key=lambda x: x[1], reverse=True)[:10]
    
    # get the names and values of the top 10 countries with the most emissions
    
    top_10_countries_emission_names = [x[0] for x in top_10_countries_emission]
    top_10_countries_emission_values = [x[1] for x in top_10_countries_emission]
    
    # get the names and values of the top 10 countries with the most emissions per capita
    
    top_10_countries_emissions_per_capita_names = [x[0] for x in top_10_countries_emissions_per_capita]
    top_10_countries_emissions_per_capita_values = [x[1] for x in top_10_countries_emissions_per_capita]
    
    # create a bar chart of the top 10 countries with the most emissions and the top 10 countries with the most emissions per capita
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(top_10_countries_emissions_per_capita_names, top_10_countries_emission_values, label="Most Emissions", alpha=0.5)
    ax.bar(top_10_countries_emissions_per_capita_names, top_10_countries_emissions_per_capita_values, label="Most Emissions per Capita", alpha=0.5)
    
    ax.set_xlabel("Countries")
    ax.set_ylabel("Emissions (in tons)")
    ax.set_title("Top 10 Countries with Most Emissions and Most Emissions per Capita")
    ax.legend()
    
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()
    plt.close()

if __name__ == "__main__":
    plot_top_10_countries(countries_emission, countries_emissions_per_capita)