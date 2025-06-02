import easyocr
import cv2

def extract_text(image_path):
    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en'])
    
    # Read image
    image = cv2.imread(image_path)
    
    # Perform OCR
    results = reader.readtext(image)
    
    # Extract text from results
    extracted_text = ' '.join([text[1] for text in results])
    
    return extracted_text
