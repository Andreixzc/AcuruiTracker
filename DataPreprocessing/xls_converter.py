import pandas as pd

def convert_xls_to_csv(input_file, output_file):
    # Read the Excel file
    try:
        if input_file.endswith('.xls'):
            df = pd.read_excel(input_file, engine='xlrd')
        elif input_file.endswith('.xlsx'):
            df = pd.read_excel(input_file, engine='openpyxl')
        else:
            raise ValueError("Unsupported file type")
        
        # Write to a CSV file
        df.to_csv(output_file, index=False)
        print(f"Successfully converted {input_file} to {output_file}")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
input_file = '../data/planilha teste Alessandro.xlsx'  # Change this to your input file path
output_file = '../data/planilha.csv'  # Change this to your desired output file path
convert_xls_to_csv(input_file, output_file)
