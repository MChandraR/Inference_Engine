import os
import cv2

def create_folder_in_public(public_dir='public/captures'):
    # Jika direktori 'public' belum ada, buat terlebih dahulu
    if not os.path.exists(public_dir):
        os.makedirs(public_dir)

    # Ambil semua item yang ada di direktori 'public' dan filter hanya folder
    existing_folders = [name for name in os.listdir(public_dir) if os.path.isdir(os.path.join(public_dir, name))]
    
    # Tentukan nomor folder baru berdasarkan jumlah folder yang ada + 1
    new_folder_number = len(existing_folders) + 1
    new_folder_name = str(new_folder_number)
    
    # Buat folder baru dengan nama yang sudah ditentukan
    new_folder_path = os.path.join(public_dir, new_folder_name)
    os.makedirs(new_folder_path)

    return new_folder_path

# Fungsi untuk menyimpan gambar di folder yang sudah dibuat
def save_image_to_folder(image, folder_path, image_id):
    # Path lengkap untuk menyimpan gambar
    image_filename = f"{image_id}.jpg"
    image_path = os.path.join(folder_path, image_filename)

    # Simpan gambar dengan format JPG menggunakan OpenCV
    cv2.imwrite(image_path, image)

    print(f"Gambar berhasil disimpan di: {image_path}")
    
def get_image_path(folder_id, image_id):
    folder_path = os.path.join( str(folder_id))
    image_path = os.path.join(folder_path, f"{image_id}.jpg")

    # Cek apakah file gambar ada
    if os.path.exists(image_path) and os.path.isfile(image_path):
        return image_path
    else:
        return None

