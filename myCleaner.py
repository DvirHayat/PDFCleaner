import fitz
from PIL import Image
import os
import cv2
import numpy as np
colors={"Red":[np.array([200, 0, 0]),np.array([255, 254, 254])],
        "Blue":[np.array([0, 0, 200]),np.array([254, 254, 255])], 
        "Yellow":[np.array([120, 120, 0]),np.array([255, 255, 254])]}
        
def print_colors(input_image):
    # Read the image
    image = cv2.imread(input_image)

    # Convert BGR image to RGB (OpenCV uses BGR by default)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Get the dimensions of the image
    height, width, _ = rgb_image.shape

    # Iterate over each pixel and print the RGB values
    for y in range(height):
        for x in range(width):
            pixel_color = tuple(rgb_image[y, x])
            if(pixel_color!=(255,255,255)):
                print(f"{pixel_color}")

def clean_color_to_white(input_image_path, output_image_path,color_to_remove):
    # Read the image
    image = cv2.imread(input_image_path)

    # Convert BGR image to RGB (OpenCV uses BGR by default)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Define the range for chosen color pixels
    lower = colors[color_to_remove][0]  # Adjust the values based on your requirement
    upper = colors[color_to_remove][1]  # Adjust the values based on your requirement

    # Create a mask for the colored regions
    mask = cv2.inRange(rgb_image, lower, upper)

    # Change the colored regions to white
    rgb_image[mask != 0] = [255, 255, 255]  # Set to white where the mask is non-zero


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
        print_colors(temp_image_path)
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
    output_pdf.save(output_path)
    output_pdf.close()
    pdf.close()

