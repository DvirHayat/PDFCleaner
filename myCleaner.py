import fitz
from PIL import Image
import os
from time import sleep 
import cv2
import numpy as np
colors={"Red":[np.array([200, 0, 0]),np.array([255, 254, 254])],
        "Blue":[np.array([0, 0, 200]),np.array([254, 254, 255])], "Yellow":[np.array([0, 200, 200]),np.array([254, 255, 255])]}

def clean_color_to_white(input_image_path, output_image_path,color_to_remove):
    # Read the image
    image = cv2.imread(input_image_path)

    # Convert BGR image to RGB (OpenCV uses BGR by default)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Define the range for chosen color pixels
    lower_red = colors[color_to_remove][0]  # Adjust the values based on your requirement
    upper_red = colors[color_to_remove][1]  # Adjust the values based on your requirement

    # Create a mask for the red regions
    red_mask = cv2.inRange(rgb_image, lower_red, upper_red)

    # Change the red regions to white
    rgb_image[red_mask != 0] = [255, 255, 255]  # Set to white where the mask is non-zero

    # Convert back to BGR (if needed) and save the result
    result_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(output_image_path, result_image)

def remove_color_from_pdf(input_path, output_path,color_to_remove):
    # Open the PDF file
    pdf = fitz.open(input_path)

    # Create a new PDF document
    output_pdf = fitz.open()

    # Iterate over each page in the PDF
    for page_number in range(len(pdf)):
        page = pdf.load_page(page_number)

        # Get the page dimensions
        mediabox = page.mediabox
        page_width = int(mediabox[2])
        page_height = int(mediabox[3])

        # Render the page as a Pixmap
        pixmap = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))

        # Convert the Pixmap to a PIL Image
        img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)

        # Save the modified image as a temporary file
        temp_image_path = f"temp_image_{page_number}.png"
        img.save(temp_image_path)
        
        clean_color_to_white(temp_image_path, temp_image_path,color_to_remove)

        # Create a new blank page with the same dimensions
        new_page = output_pdf.new_page(width=page_width, height=page_height)

        # Draw the modified image onto the new page
        new_page.insert_image(fitz.Rect(0, 0, page_width, page_height), filename=temp_image_path)
        print("inserting page number:",page_number)
        
        # Remove temporary image file
        os.remove(temp_image_path)

    print("FINISHED CLEANING FILE")
    # Save the modified PDF
    print(output_path)
    sleep(5)
    output_pdf.save(output_path)
    output_pdf.close()
    pdf.close()

