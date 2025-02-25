import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def load_and_process_data(file_path):
    # Read the raw data
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Process each line
    data = []
    for line in lines:
        # Split on first comma for DOB, then on last comma for city
        parts = line.strip().split(',', 1)
        if len(parts) < 2:
            continue
            
        dob = parts[0]
        remaining = parts[1]
        
        # Get the city (last part after last comma)
        last_comma_idx = remaining.rfind(',')
        if last_comma_idx != -1:
            street = remaining[:last_comma_idx].strip()
            city = remaining[last_comma_idx + 1:].strip()
        else:
            street = ''
            city = remaining.strip()
            
        data.append({
            'DOB': dob,
            'Street': street,
            'City': city
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Convert DOB to datetime
    df['DOB'] = pd.to_datetime(df['DOB'])
    
    # Extract year and calculate age
    df['Birth_Year'] = df['DOB'].dt.year
    current_year = 2024
    df['Age'] = current_year - df['Birth_Year']
    
    # Create age groups
    bins = [0, 20, 30, 40, 50, 60, 100]
    labels = ['0-20', '21-30', '31-40', '41-50', '51-60', '60+']
    df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
    
    # Create decade groups
    df['Decade'] = (df['Birth_Year'] // 10) * 10
    df['Decade'] = df['Decade'].astype(str) + 's'
    
    # Process Oslo migration
    df['Is_Oslo'] = df['City'].str.contains('OSLO', na=False)
    
    return df

def create_visualizations(df):
    # Set style
    plt.style.use('seaborn')
    
    # Create a figure with three subplots
    fig = plt.figure(figsize=(20, 12))
    
    # 1. Age Distribution
    plt.subplot(2, 2, 1)
    age_dist = df['Age_Group'].value_counts().sort_index()
    age_dist.plot(kind='bar')
    plt.title('Age Distribution')
    plt.xlabel('Age Groups')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    
    # 2. Oslo vs Other Cities
    plt.subplot(2, 2, 2)
    oslo_counts = df['Is_Oslo'].value_counts()
    plt.pie(oslo_counts, labels=['Other Cities', 'Oslo'], autopct='%1.1f%%', colors=['lightblue', 'darkblue'])
    plt.title('Oslo vs Other Cities Distribution')
    
    # 3. Birth Decade Distribution
    plt.subplot(2, 2, 3)
    decade_dist = df['Decade'].value_counts().sort_index()
    decade_dist.plot(kind='bar')
    plt.title('Birth Decade Distribution')
    plt.xlabel('Decade')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    
    # 4. Top 10 Cities
    plt.subplot(2, 2, 4)
    city_counts = df['City'].value_counts().head(10)
    city_counts.plot(kind='bar')
    plt.title('Top 10 Cities')
    plt.xlabel('City')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    
    # Adjust layout and display
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('demographic_analysis.png')
    
    # Print some summary statistics
    print("\nDemographic Analysis Summary:")
    print("-" * 30)
    print(f"Total number of people: {len(df)}")
    print(f"Number of people in Oslo: {df['Is_Oslo'].sum()}")
    print(f"Average age: {df['Age'].mean():.1f} years")
    print(f"Median age: {df['Age'].median():.1f} years")
    print("\nTop 5 Cities:")
    print(df['City'].value_counts().head())
    print("\nAge Group Distribution:")
    print(df['Age_Group'].value_counts().sort_index())

def main():
    try:
        # Load and process the data
        df = load_and_process_data('flyttet.txt')
        
        # Create visualizations
        create_visualizations(df)
        
        print("\nAnalysis complete! Visualizations have been saved to 'demographic_analysis.png'")
        
    except FileNotFoundError:
        print("Error: 'data.csv' file not found. Please ensure the file exists in the current directory.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()