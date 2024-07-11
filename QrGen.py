import qrcode
from PIL import Image

def generate_qr_code(name, code, filename):
    # Concatenate name and code to form the QR code content
    qr_content = f"Name: {name}\nCode: {code}"
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_content)
    qr.make(fit=True)
    
    # Create an image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save the image to a file
    img.save(filename)

if __name__ == "__main__":
    name = "John Doe"
    code = "12345"
    filename = "qrcode.png"
    generate_qr_code(name, code, filename)
    print(f"QR code generated and saved as {filename}")
