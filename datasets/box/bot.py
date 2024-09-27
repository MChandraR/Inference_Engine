import os
import glob

# Fungsi untuk mengganti karakter di dalam file
def replace_characters_in_file(file_path, target_char, replacement_char):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_contents = file.read()

    # Ganti karakter yang ditargetkan
    new_contents = file_contents.replace(target_char, replacement_char)

    # Simpan kembali file dengan perubahan
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_contents)

# Fungsi untuk memproses semua file .txt di folder
def process_text_files_in_folder(folder_path, target_char, replacement_char):
    # Dapatkan semua file .txt di dalam folder
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))

    for txt_file in txt_files:
        print(f'Processing file: {txt_file}')
        replace_characters_in_file(txt_file, target_char, replacement_char)

# Contoh penggunaan:
folder_path = 'train/labels'  # Ganti dengan path folder yang sesuai
target_char = '1'  # Karakter yang akan diganti
replacement_char = '2'  # Karakter pengganti

process_text_files_in_folder(folder_path, target_char, replacement_char)