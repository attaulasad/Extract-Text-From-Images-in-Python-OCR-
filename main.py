''''age segmentation modes: 
O Orientation and script detection (OSD) only
1 Automatic page segmentation with OSD. ‘
2 Automatic page segmentation, but no OSD, or OCR.
3 Fully automatic page segmentation, but no OSD. (Default)
4 Assume a single column of text of variable sizes.
5 Assume a single uniform block of vertically aligned text.
6 Assume a single uniform block of textJ
7 Treat the image as a single text line.
8 Treat the image as a single word.
9 Treat the image as a single word in a circle.
10 Treat the image as a single character.
11 Sparse text. Find as much text as possible in no particular order.
12 Sparse text with OSD.
13 Raw line. Treat the image as a single text line, bypassing hacks that are Tesseract—specific.'''
# import pytesseract
# import PIL.Image


# myconfig = r"--psm 6 --oem 3"

# # # Perform OCR on the image using the corrected config
# # text = pytesseract.image_to_string(PIL.Image.open('text.jpg'), config=myconfig)

# # print(text)
# import pytesseract
# import cv2
# from PIL import Image

# # Load the image with OpenCV
# image = cv2.imread('text.jpg')

# # Convert image to grayscale
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # Optional: Apply thresholding to clean up the image
# gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# # Save the processed image (optional)
# cv2.imwrite('processed_text.jpg', gray)

# # Convert back to PIL image for Tesseract
# pil_img = Image.fromarray(gray)

# # Set the configuration for Tesseract
# myconfig = r"--psm 6 --oem 3"

# # Perform OCR on the processed image
# text = pytesseract.image_to_string(pil_img, config=myconfig)

# print(text)



