import fitz
from pdf2image import convert_from_path
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

pdf_path = "circle_grid.pdf"

images = convert_from_path(pdf_path, dpi=1200)

result_image = images[0]

pdf_document = fitz.open(pdf_path)
pdf_page = pdf_document.load_page(0)
a4_width, a4_height = 8.27 , 11.69

a4_width_points = a4_width * 1200
a4_height_points = a4_height * 1200

result_image.save("temp.png", "PNG")
temp_image = Image.open("temp.png")

temp_image = temp_image.resize((int(a4_width_points), int(a4_height_points)), Image.LANCZOS)

temp_image.save("temp.png", "PNG")