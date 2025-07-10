################ # dev :  awenk audico # ###############
# Lokasi file: /clean.py

import os
import shutil

def bersihkan_sampah():
    """
    Fungsi untuk mencari dan menghapus folder __pycache__
    dan file dengan ekstensi .pyc dan .log di dalam direktori
    tempat skrip ini dijalankan dan semua subfolder-nya.
    """
    # PERBAIKAN KODE: Gunakan os.getcwd() agar lebih tangguh.
    # Ini akan membersihkan folder tempat terminal/CMD kamu sedang aktif.
    folder_proyek = os.getcwd()

    print(f"Akan membersihkan cache dan log di dalam folder: {folder_proyek}")

    konfirmasi = input("Apakah Anda yakin ingin melanjutkan? (y/n): ")
    if konfirmasi.lower() != 'y':
        print("Pembersihan dibatalkan oleh pengguna.")
        return

    folder_dihapus = 0
    file_dihapus = 0

    for root, dirs, files in os.walk(folder_proyek, topdown=False):
        # 1. Hapus folder __pycache__
        if '__pycache__' in dirs:
            path_folder_cache = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(path_folder_cache)
                folder_dihapus += 1
                print(f"[DIHAPUS] Folder: {path_folder_cache}")
            except OSError as e:
                print(f"[ERROR] Gagal menghapus folder {path_folder_cache}: {e}")

        # 2. Hapus file .pyc dan .log
        for nama_file in files:
            if nama_file.endswith(('.pyc', '.log')):
                path_file = os.path.join(root, nama_file)
                try:
                    os.remove(path_file)
                    file_dihapus += 1
                    print(f"[DIHAPUS] File: {path_file}")
                except OSError as e:
                    print(f"[ERROR] Gagal menghapus file {path_file}: {e}")

    print("\n--- PROSES PEMBERSIHAN SELESAI ---")
    print(f"Total folder __pycache__ yang dihapus: {folder_dihapus}")
    print(f"Total file .pyc dan .log yang dihapus: {file_dihapus}")
    print("Proyek Anda sekarang lebih bersih!")

if __name__ == "__main__":
    bersihkan_sampah()