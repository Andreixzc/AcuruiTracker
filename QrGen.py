import qrcode
from PIL import Image
import pandas as pd

def generate_qr_code(cpf, name,competition):
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"{cpf}/{competition}")
    # qr.add_data(cpf+'/'+competition)
    qr.make(fit=True)
    
    # Create an image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save the image to a file
    filename = f"QrCodes/{name}.png"
    img.save(filename)
    print(f"QR code for {name} generated and saved as {filename}")

if __name__ == "__main__":
    competitionName = 'Clinica_17_08_24'
    # Load the CSV file
    data = pd.read_csv('Data/planilhaTratada.csv')
    
    # Ensure the QrCodes directory exists
    import os
    if not os.path.exists('QrCodes'):
        os.makedirs('QrCodes')
    
    # Iterate over the rows in the CSV file
    for index, row in data.iterrows():
        cpf = row['CPF']
        name = row['ATLETA']
        generate_qr_code(cpf, name, competitionName)
