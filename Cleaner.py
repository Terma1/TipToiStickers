import os

def clean_folder(folder_path, file_extension):
    for filename in os.listdir(folder_path):
        if filename.endswith(file_extension):
            file_path = os.path.join(folder_path, filename)
            os.remove(file_path)
            print(f"Удален файл: {file_path}")

current_directory = os.getcwd()
clean_folder(current_directory, ".yaml")
clean_folder(current_directory, ".png")

oid_codes_directory = os.path.join(current_directory, "tttool/media/oid-codes")
if os.path.exists(oid_codes_directory):
    clean_folder(oid_codes_directory, ".png")
ttool_audio_directory = os.path.join(current_directory, "tttool", "audio")
if os.path.exists(ttool_audio_directory):
    clean_folder(ttool_audio_directory, ".wav")
    clean_folder(ttool_audio_directory, ".gme")
ttool_directory = os.path.join(current_directory, "tttool")
if os.path.exists(ttool_directory):
    clean_folder(ttool_directory, ".yaml")
ttool_audio_directory = os.path.join(current_directory, "oid-codes")
if os.path.exists(ttool_audio_directory):
    clean_folder(ttool_audio_directory, ".png")
ttool_audio_directory = os.path.join(current_directory, "matrix")
if os.path.exists(ttool_audio_directory):
    clean_folder(ttool_audio_directory, ".png")