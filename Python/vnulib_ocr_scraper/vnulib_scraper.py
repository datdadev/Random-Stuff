import sys
import os
import requests
import img2pdf
import re
import time

# --- Initial ---

if len(sys.argv) != 4:
    print("Usage: python vnulib_scraper.py <URL> <Number of Pages> <Output Directory>")
    sys.exit(1)

url = sys.argv[1]
num_pages = int(sys.argv[2])
output_directory = sys.argv[3]
output_img_directory = f"{output_directory}\\images"

pattern = r'subfolder=([\d/]+)&doc=([\d]+)'
match = re.search(pattern, url)

if match:
    subfolder = match.group(1)
    doc_id = match.group(2)
    print("Subfolder:", subfolder)
    print("Document ID:", doc_id)
else:
    print("No match found! Please try again.")
    sys.exit(1)

# --- Initial ---

start_time = time.time()

image_format = "jpg"
url_base = "https://ir.vnulib.edu.vn/flowpaper/services/view.php"
url_params = {
    "doc": doc_id,
    "format": image_format,
    "subfolder": subfolder
}

# --- Image Fetching ---

# Create the folder if it doesn't exist
if not os.path.exists(output_img_directory):
    os.makedirs(output_img_directory)

for page in range(1, num_pages + 1):  # Download pages from 1 to 10
    url_params["page"] = page
    response = requests.get(url_base, params=url_params, verify=False)
    
    if response.status_code == 200:
        image_url = response.content  # Binary image data, not text
        
        image_filename = f"page_{page}.{image_format}"
        image_path = os.path.join(output_img_directory, image_filename)
        
        with open(image_path, "wb") as image_file:
            image_file.write(image_url)  # Writing binary image data
        
        print(f"Page {page} downloaded and saved as {image_filename}!")
    else:
        print(f"Failed to download page {page}!")

# --- Image Fetching ---

# --- Merging Images into Pdf ---

file_names = sorted(os.listdir(output_img_directory), key=lambda name: int(re.search(r'\d+', name).group()))  # Sort numerically

# Create a list of image file paths
image_files = [os.path.join(output_img_directory, file_name) for file_name in file_names if file_name.lower().endswith(f'.{image_format}')]

# Create the PDF file
pdf_filename = "book.pdf"
with open(f"{output_directory}\\{pdf_filename}", "wb") as f:
    f.write(img2pdf.convert(image_files))

print("Done!")
print(f"--- {time.time() - start_time} seconds for {num_pages} pages ---")

# --- Merging Images into Pdf ---