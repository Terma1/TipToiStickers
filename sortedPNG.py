import os
from PIL import Image
import glob
Image.MAX_IMAGE_PIXELS = None

input_folder = 'matrix'
png_files = glob.glob(os.path.join(input_folder, "*.png"))

for index, png_file in enumerate(png_files):
    if "START" in os.path.basename(png_file):
        new_file_name = os.path.join(input_folder, "0001.png")
        os.rename(png_file, new_file_name)

png_files = glob.glob(os.path.join(input_folder, "*.png"))

png_files.sort(key=lambda x: (not x.startswith("START"), x))

for png_file in png_files:
    original_image = Image.open(png_file)

    new_filename = f"{os.path.splitext(os.path.basename(png_file))[0]}.png"
    new_filepath = os.path.join(input_folder, new_filename)

    original_image.save(new_filepath)

for filename in os.listdir(input_folder):
    if filename.endswith(".png") and ("STOP" in filename or "REPLAY" in filename):
        os.remove(os.path.join(input_folder, filename))
