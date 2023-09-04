import sys
import os
import time
import calendar
from PyPDF2 import PdfMerger

if len(sys.argv) != 4:
    print("Usage: python ocr.py <Input Directory> <Languages> <DPI>")
    sys.exit(1)

input_directory = sys.argv[1]  # Specify the input directory
languages = sys.argv[2] # Example: vie+eng
dpi = sys.argv[3] # Example: 150

if not os.path.exists(input_directory):
    print("Input directory does not exist.")
    sys.exit(1)

# List files in the input directory
dir_files = [f for f in os.listdir(input_directory) if os.path.isfile(os.path.join(input_directory, f))]
epoch_time = int(calendar.timegm(time.gmtime()))

for file in dir_files:
    if file.endswith('.pdf'):
        print('Working on converting: ' + file)

        # Setup
        file_without_extension = os.path.splitext(file)[0]
        folder = str(int(epoch_time)) + '_' + file_without_extension
        combined = os.path.join(input_directory, folder, file_without_extension)

        # Create folder
        if not os.path.exists(os.path.join(input_directory, folder)):
            os.makedirs(os.path.join(input_directory, folder))

        # Convert PDF to PNG(s)
        magick = 'convert -density ' + dpi + ' "' + os.path.join(input_directory, file) + '" "' + os.path.join(input_directory, folder, file_without_extension) + '-%04d.png"'
        print(magick)
        os.system(magick)

        # Convert PNG(s) to PDF(s) with OCR data
        pngs = [f for f in os.listdir(os.path.join(input_directory, folder)) if os.path.isfile(os.path.join(input_directory, folder, f))]
        for pic in pngs:
            if pic.endswith('.png'):
                combined_pic = os.path.join(input_directory, folder, pic)
                print(combined_pic)
                tesseract = 'tesseract "' + combined_pic + '" "' + combined_pic + '-ocr" -l ' + languages + ' PDF'
                print(tesseract)
                os.system(tesseract)

        # Combine OCR'd PDFs into one
        ocr_pdfs = [f for f in os.listdir(os.path.join(input_directory, folder)) if os.path.isfile(os.path.join(input_directory, folder, f))]

        merger = PdfMerger()
        for pdf in ocr_pdfs:
            if pdf.endswith('-ocr.pdf'):
                merger.append(os.path.join(input_directory, folder, pdf))

        merger.write(os.path.join(input_directory, file_without_extension + '-ocr-combined.pdf'))
        merger.close()