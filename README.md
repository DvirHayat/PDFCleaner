# PDFCleaner: Python-based PDF Color Removal Tool

PDFCleaner is a Python-based project that allows users to selectively remove specific colors (red, blue, or yellow) from a PDF file. The tool utilizes various libraries, including Tkinter for the graphical user interface, PIL (Pillow) for image processing, fitz for PDF handling, cv2 for computer vision tasks, and numpy for numerical operations.

## Dependencies
Ensure you have the following Python libraries installed before running PDFCleaner:
- Tkinter
- PIL (Pillow)
- fitz
- cv2
- numpy

You can install these dependencies using the following command:
```bash
pip install tk pillow PyMuPDF opencv-python numpy
```
## Usage

1. Run the Display.py script.
2. Use the graphical user interface to:
   - Select the PDF file you want to clean.
   - Choose the destination folder to save the cleaned PDF as "output.pdf."
   - Specify the color (red, blue, or yellow) to remove.
3. Click the "Create file" button to initiate the color removal process.
4. Once the process is complete, find the cleaned PDF named "output.pdf" in the specified destination folder.

## Note

- PDFCleaner is designed for basic color removal purposes and may not cover all edge cases.
- Ensure that the selected PDF file is not password-protected or encrypted.
