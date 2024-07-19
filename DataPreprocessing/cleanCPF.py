import pandas as pd

def clean_and_deduplicate_cpf(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Check if 'CPF' column exists
    if 'CPF' in df.columns:
        # Remove '.' and '-' from the 'CPF' column
        df['CPF'] = df['CPF'].str.replace('.', '', regex=False).str.replace('-', '', regex=False)
        
        # Check for duplicated CPF values
        duplicates = df[df.duplicated('CPF')]
        if not duplicates.empty:
            print(f"Found duplicated CPF values:\n{duplicates}")
            
            # Drop duplicate rows based on 'CPF'
            df = df.drop_duplicates(subset='CPF')
        
        # Save the modified DataFrame to a new CSV file
        df.to_csv(output_file, index=False)
        print(f"Successfully cleaned CPF column, removed duplicates, and saved to {output_file}")
    else:
        print("Error: 'CPF' column not found in the CSV file")

# Example usage
input_file = '../data/planilha.csv'  # Change this to your input file path
output_file = '../data/planilhaTratada.csv'  # Change this to your desired output file path
clean_and_deduplicate_cpf(input_file, output_file)
