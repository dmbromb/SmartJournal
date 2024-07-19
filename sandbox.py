from PIL import Image
import pytesseract

# Path to tesseract executable if not in the system's PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\c-OCR\tesseract'

# Open an image file
image_path = 'static/img/notebook_picture.jpg'
img = Image.open(image_path)

# Use pytesseract to do OCR on the image
text = pytesseract.image_to_string(img)

# Print the text
print(text)
