from PIL import Image
import json
import os
import img2pdf

Image.MAX_IMAGE_PIXELS = None
background = Image.open("temp.png")

with open("circle_data.json", "r") as json_file:
    circle_data = json.load(json_file)

matrix_folder = "matrix"
output_pdf = "output.pdf"
image_paths = []

for circle in circle_data["circles"]:
    x = int(int(circle["x"])*17-1210)
    y = int((circle["y"]+(734-int(circle["y"]))*2)*16.62-11350)
    image_files = os.listdir(matrix_folder)

    if image_files:
        image_path = os.path.join(matrix_folder, image_files[0])
        overlay = Image.open(image_path)

        background.paste(overlay, (x, y), overlay)

        image_paths.append(image_path)

background.save("temp_with_images.png", dpi=(1200, 1200))

pdf_options = {
    "dpi": (1200, 1200),
    "quality": 100,
}

with open("temp_with_images.png", "rb") as img_file:
    pdf_bytes = img2pdf.convert(img_file.read(), **pdf_options)

with open(output_pdf, "wb") as pdf_file:
    pdf_file.write(pdf_bytes)

os.remove("temp_with_images.png")