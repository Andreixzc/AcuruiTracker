import pandas as pd
from datetime import datetime

# Function to calculate age from birthdate
def calculate_age(birthdate):
    today = datetime.today()
    birthdate = datetime.strptime(birthdate, '%Y-%m-%d')
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

# Read the CSV file
input_file = '../data/planilhaTratada.csv'
df = pd.read_csv(input_file)

# Calculate age and add it as a new column
df['AGE'] = df['DATA NASCIMENTO'].apply(calculate_age)

# Save the updated CSV
output_file = '../data/planilhaTratada1.csv'
df.to_csv(output_file, index=False)

print("Updated CSV file with ages has been saved.")
