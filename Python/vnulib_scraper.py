import os
import requests
import img2pdf
import re
import time

start_time = time.time()

image_format = "jpg"
numPages = 157
url_base = "https://ir.vnulib.edu.vn/flowpaper/services/view.php"
url_params = {
    "doc": "1122469547324222540191515350393125615",
    "format": image_format,
    "subfolder": "11/22/46/"
}

folder_path = "D:\\LTD\\E-Book\\nguyen_ly_may_bt"
images_path = f"{folder_path}\\images"

# --- Image Fetching ---

# Create the folder if it doesn't exist
if not os.path.exists(images_path):
    os.makedirs(images_path)

for page in range(1, numPages + 1):  # Download pages from 1 to 10
    url_params["page"] = page
    response = requests.get(url_base, params=url_params, verify=False)
    
    if response.status_code == 200:
        image_url = response.content  # Binary image data, not text
        
        image_filename = f"page_{page}.{image_format}"
        image_path = os.path.join(images_path, image_filename)
        
        with open(image_path, "wb") as image_file:
            image_file.write(image_url)  # Writing binary image data
        
        print(f"Page {page} downloaded and saved as {image_filename}")
    else:
        print(f"Failed to download page {page}")

# --- Image Fetching ---

# --- Merging Images into Pdf ---

file_names = sorted(os.listdir(images_path), key=lambda name: int(re.search(r'\d+', name).group()))  # Sort numerically

# Create a list of image file paths
image_files = [os.path.join(images_path, file_name) for file_name in file_names if file_name.lower().endswith(f'.{image_format}')]

# Create the PDF file
pdf_filename = "book.pdf"
with open(f"{folder_path}\\{pdf_filename}", "wb") as f:
    f.write(img2pdf.convert(image_files))

print("Done!")
print(f"--- {time.time() - start_time} seconds for {numPages} pages ---")

# --- Merging Images into Pdf ---