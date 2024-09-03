# VNULib-OCR-Scraper

## ABOUT

This repository provides a set of Python scripts to scrape images from a specified URL on VNULib and convert them into a single PDF file. It also includes a script to perform Optical Character Recognition (OCR) on the generated PDF.

## USAGE

### Installation

Before you start, ensure you have the following tools and libraries installed on your system:

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract): An OCR engine used for text extraction from images.
- [ImageMagick](https://imagemagick.org/): A software suite for manipulating and converting images, with the 'install legacy utilities' option enabled.
- [Ghostscript](https://www.ghostscript.com/): A powerful interpreter for the PostScript language and PDF files.
- [Python](https://www.python.org/) version 3.x

Make sure to add Tesseract to your system's PATH variable during installation.

### Procedure

#### Step 1: Scrape Images and Convert to PDF

1. Run the `vnulib_scraper.py` script with the following arguments:
   - `<URL>`: The URL of the content/book on VNULib that you want to scrape.
   - `<Number of Pages>`: The number of images/pages to scrape.
   - `<Output Directory>`: The folder where you want to save the resulting PDF.

   Example:
   ```bash
   python vnulib_scraper.py 'https://ir.vnulib.edu.vn/flowpaper/...' 100 /path/to/save
   ```

   The script will scrape images from the specified URL and convert them into a single PDF file saved in the provided folder.

#### Step 2: Perform OCR on the PDF

1. Run the `ocr.py` script with the following argument:
   - `<Input Directory>`: The folder path containing the PDF file generated in step 1.
   - `<Languages>`: Specify the language(s) you want to OCR. You can specify multiple languages or just one.
   - `<DPI>`: Specify the DPI (Dots Per Inch) for the OCR process. Higher DPI provides more detail; typically, values between 150 and 300 are used."

   Example:
   ```bash
   python ocr.py /path/to/save vie+eng 150
   ```

   The script will perform OCR on the generated PDF in the specified folder and create an OCR-enabled PDF in the same directory.

### Example

Here's a sample workflow:

1. Clone this repository to your local machine.

2. Install Tesseract, ImageMagick (with legacy utilities), Ghostscript, and Python 3.x.

3. Navigate to the directory containing `vnulibscraper.py` and `ocr.py`.

4. Run `vnulib_scraper.py` to scrape images from a VNULib content URL and generate a PDF file.

   ```bash
   python vnulib_scraper.py 'https://ir.vnulib.edu.vn/flowpaper/...' 100 /path/to/save
   ```

5. Run `ocr.py` to perform OCR on the generated PDF in the specified folder.

   ```bash
   python ocr.py /path/to/save vie+eng 150
   ```

6. You can now access the final PDF file with searchable text content.
