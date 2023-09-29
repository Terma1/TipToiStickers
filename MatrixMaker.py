import os
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
input_folder = 'oid-codes'
output_folder = 'matrix'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

png_files = [filename for filename in os.listdir(input_folder) if filename.endswith(".png")]

for png_file in png_files:
    original_image = Image.open(os.path.join(input_folder, png_file))

    original_size = original_image.size
    right_half = original_image.crop(((original_size[0] // 2), 0, original_size[0], original_size[1]))

    matrix_image = Image.new('RGBA', (original_size[0] * 2, original_size[1]))

    matrix_image.paste(original_image, (0, 0))
    matrix_image.paste(right_half, (original_size[0], 0))

    bottom_third = matrix_image.crop((0, (2 * original_size[1]) // 3, matrix_image.width, matrix_image.height))

    final_image = Image.new('RGBA', (matrix_image.width, original_size[1] * 2))

    final_image.paste(matrix_image, (0, 0))
    final_image.paste(bottom_third, (0, original_size[1]))

    new_filename = f"{png_file.split('.')[0]}_matrix.png"
    new_filepath = os.path.join(output_folder, new_filename)

    final_image.save(new_filepath)
