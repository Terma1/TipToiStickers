import os
import random
import subprocess
import shutil

def generate_random_product_id():
    return random.randint(400, 900)

def generate_random_start_id():
    return random.randint(5000, 13000)

def generate_script(audio_files, start_index=0):
    script = {}

    sorted_audio_files = sorted(audio_files, key=lambda x: int(x.split('_')[1].split('.')[0]))
    random_id = generate_random_start_id()
    for i, audio_file in enumerate(sorted_audio_files[start_index:], start=start_index):
        script[random_id + i] = f'P({os.path.splitext(audio_file)[0]})'

    return script

product_id = generate_random_product_id()
audio_folder = 'tttool/audio'
audio_files = [filename for filename in os.listdir(audio_folder) if filename.endswith('.wav') and filename.startswith('audio_')]

start_index = 1
data = {
    'product-id': product_id,
    'media-path': 'audio/%s',
    'init': '$mode:=1',
    'welcome': 'audio_1',
    'scripts': generate_script(audio_files, start_index),
}
yaml_filename = f'{product_id}.yaml'

script_path = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(script_path, 'tttool', yaml_filename), 'w') as yaml_file:
    yaml_file.write('product-id: {}\n'.format(data['product-id']))
    yaml_file.write('media-path: "{}"\n'.format(data['media-path']))
    yaml_file.write('init: {}\n'.format(data['init']))
    yaml_file.write('welcome: {}\n'.format(data['welcome']))
    yaml_file.write('scripts:\n')
    for key, value in data['scripts'].items():
        yaml_file.write('  {}: {}\n'.format(key, value))

current_dir = os.path.dirname(os.path.abspath(__file__))
tttool_path = os.path.join(current_dir, "tttool", "tttool.exe")
output_path = os.path.join(current_dir, "gme")
yaml_filename = os.path.join(current_dir, "tttool", f'{product_id}.yaml')

tttool_command1 = "assemble"
tttool_command2 = yaml_filename
subprocess.run([tttool_path, tttool_command1, tttool_command2], check=True)
tttool_command3 = "oid-codes"
subprocess.run([tttool_path, tttool_command3, tttool_command2], check=True)
source_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)))
destination_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "oid-codes")
for filename in os.listdir(source_directory):
    if filename.endswith('.png'):
        source_file = os.path.join(source_directory, filename)
        destination_file = os.path.join(destination_directory, filename)
        shutil.move(source_file, destination_file)