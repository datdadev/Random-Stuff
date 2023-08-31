import os
import requests
from PIL import Image
from fpdf import FPDF
import re

image_format = "png"
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

for page in range(1, 157+1):  # Download pages from 1 to 10
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

pdf_filename = "book.pdf"
pdf = FPDF(unit="mm")
pdf.set_auto_page_break(0)

file_names = sorted(os.listdir(images_path), key=lambda name: int(re.search(r'\d+', name).group()))  # Sort numerically

for index, file_name in enumerate(file_names):
    print(f"Added file {file_name}!")
    f = os.path.join(images_path, file_name)
    img = Image.open(f)
    img_width, img_height = img.size
    pdf.add_page()
    pdf.image(f, 0, 0, w=float(img_width * 0.16946), h=float(img_height * 0.16946))

print("Added all files, finishing...")
pdf_path = os.path.join(folder_path, pdf_filename)
pdf.output(pdf_path)
print("Done!")

# --- Merging Images into Pdf ---