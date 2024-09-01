import cv2#This imports the OpenCV library, which is used for image processing tasks
import pytesseract#This imports the pytesseract library, which provides a Python wrapper for Tesseract OCR (Optical Character Recognition), allowing you to extract text from images

# Load the image
#This loads an image from the file 'number_plate.jpg' into the image variable. The image is read as a numpy array in BGR format (Blue, Green, Red) by default.
image = cv2.imread('number_plate.jpg')

# Convert to grayscale
#Converts the loaded color image into a grayscale image. Grayscale images are simpler to process because they only have one color channel instead of three (BGR).
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Apply a bilateral filter to preserve edges while reducing noise
#Applies a bilateral filter to the grayscale image to reduce noise while preserving the edges. The parameters 11, 17, and 17 control the filter size, color space sigma, and coordinate space sigma, respectively.

gray = cv2.bilateralFilter(gray, 11, 17, 17)

# Detect edges using Canny
# Uses the Canny edge detection algorithm to detect edges in the image. The thresholds 30 and 200 determine the sensitivity of edge detection.
edges = cv2.Canny(gray, 30, 200)

# Find contours based on edges detected
#Finds contours in the edge-detected image. Contours are simply curves joining all continuous points along a boundary with the same color or intensity.
#cv2.RETR_TREE: Retrieves all of the contours and reconstructs a full hierarchy of nested contours.
#cv2.CHAIN_APPROX_SIMPLE: Compresses horizontal, vertical, and diagonal segments and leaves only their end points, thus reducing the amount of memory needed to store the contour.
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Sort the contours based on area (descending) and keep the largest one
#Sorts the contours by their area in descending order (largest first) and keeps only the top 10 largest contours. This is because the number plate is likely to be among the largest contours.
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

# Initialize a variable to hold the contour of the number plate
#: Initializes a variable to store the contour of the number plate, which will be identified in the next loop.
number_plate_contour = None

# Loop over the contours to find a rectangular contour, likely to be the number plate
# cv2.arcLength(contour, True): Calculates the perimeter (arc length) of the contour.
# cv2.approxPolyDP(contour, 0.018 * peri, True): Approximates the contour to a polygon with fewer vertices based on the perimeter. The 0.018 * peri parameter controls the approximation accuracy.
# if len(approx) == 4: Checks if the approximated contour has 4 vertices. A 4-sided polygon is likely to be a rectangle, which is the expected shape of a number plate.
# number_plate_contour = approx: If a rectangular contour is found, it is stored in number_plate_contour.
# break: Stops the loop once a likely number plate contour is found.
for contour in contours:
    # Approximate the contour
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.018 * peri, True)
    
    # If the contour has 4 points, it is likely to be the number plate
    if len(approx) == 4:
        number_plate_contour = approx
        break

if number_plate_contour is not None:
    # Mask everything except the number plate
    mask = cv2.drawContours(cv2.fillPoly(image.copy(), [number_plate_contour], (255,255,255)), [number_plate_contour], -1, (255, 255, 255), cv2.FILLED)
    mask = cv2.bitwise_and(image, mask)

    # Crop the number plate from the image
    x, y, w, h = cv2.boundingRect(number_plate_contour)
    cropped = gray[y:y + h, x:x + w]
    
    # Optional: Apply additional thresholding to clean up the cropped image
    _, cropped = cv2.threshold(cropped, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Use Tesseract to extract the text from the cropped image
#     custom_config: Configures Tesseract to use the LSTM OCR engine (--oem 3), treat the image as a single word (--psm 8), and restrict the character set to uppercase letters and digits.
# pytesseract.image_to_string(cropped, config=custom_config): Runs Tesseract OCR on the cropped image to extract the text.
    custom_config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    text = pytesseract.image_to_string(cropped, config=custom_config)
    
    # Print the detected text
    print("Detected Number Plate Text:", text)

    # Display the cropped image (optional)
    cv2.imshow("Cropped Number Plate", cropped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No number plate contour detected")
