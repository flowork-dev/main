# dev :  awenk audico & Gemini Partner
# EMAIL SAHIDINAOLA@GMAIL.COM
# WEBSITE WWW.TEETAH.ART
# File NAME : main.py

import os
import sys
import logging
import datetime
import argparse
import queue
from io import StringIO
import importlib.util
from importlib.machinery import SourcelessFileLoader
import subprocess
import pkg_resources

# ==============================================================================
# BLOK KODE PINTAR UNTUK PATH & DEPENDENSI (TAMBAHAN)
# ==============================================================================

def get_base_dir():
    """
    Menentukan base path yang benar, baik saat dijalankan normal maupun dari .exe.
    Ini adalah kunci agar .exe bisa menemukan semua folder data.
    """
    if getattr(sys, 'frozen', False):
        # Jika berjalan dari .exe (dibekukan oleh PyInstaller/Nuitka)
        return sys._MEIPASS
    else:
        # Jika berjalan normal sebagai skrip .py
        return os.path.dirname(os.path.abspath(__file__))

# Mendefinisikan base directory di awal
basedir = get_base_dir()

def install_requirements():
    """
    Membaca requirements.txt dari base directory dan menginstal paket yang belum ada.
    """
    requirements_path = os.path.join(basedir, 'requirements.txt')
    try:
        with open(requirements_path, 'r') as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

        print("Mengecek dan memasang dependensi dari requirements.txt...")

        # Mendapatkan daftar paket yang sudah terpasang
        installed_packages = {pkg.key for pkg in pkg_resources.working_set}

        missing_packages = []
        for req in requirements:
            try:
                # Memeriksa apakah paket sudah terpasang
                pkg_resources.require(req)
            except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
                # Jika tidak ditemukan atau versi salah, tambahkan ke daftar yang akan diinstal
                missing_packages.append(req)

        if missing_packages:
            print(f"Dependensi yang hilang atau versi salah: {', '.join(missing_packages)}")
            print("Memulai instalasi...")
            # Menjalankan pip untuk menginstal semua yang ada di requirements.txt
            # Menggunakan sys.executable memastikan kita memakai pip dari interpreter yang benar
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_path])
            print("Instalasi dependensi selesai.")
        else:
            print("Semua dependensi sudah terpasang.")

    except FileNotFoundError:
        print(f"PERINGATAN: File '{requirements_path}' tidak ditemukan. Melewati pengecekan dependensi.")
    except Exception as e:
        print(f"Terjadi kesalahan saat memasang dependensi: {e}")

# ==============================================================================
# AKHIR BLOK KODE PINTAR
# ==============================================================================

try:
    from importlib.abc import MetaPathFinder
    print("Main: Menggunakan importlib.abc (Python 3.10+)")
except ImportError:
    from _frozen_importlib_external import MetaPathFinder
    print("Main: Menggunakan _frozen_importlib_external (Fallback untuk Python < 3.10)")

class TeetahFinder(MetaPathFinder):
    """
    Finder kustom yang akan kita sisipkan ke sistem impor Python.
    Tugasnya adalah mencari file .teetah kita.
    """
    def __init__(self, root_path):
        self.root_path = root_path
        self._failed_imports = set()

    def find_spec(self, fullname, path, target=None):
        if not fullname.startswith('flowork_kernel'):
            return None

        if fullname in self._failed_imports:
            return None

        module_path_part = fullname.replace('.', os.sep)
        potential_path = os.path.join(self.root_path, f"{module_path_part}.teetah")

        if os.path.exists(potential_path):
            loader = SourcelessFileLoader(fullname, potential_path)
            return importlib.util.spec_from_loader(fullname, loader)
        else:
            self._failed_imports.add(fullname)
            return None

class ConsoleOutputInterceptor(StringIO):
    """
    Objek yang meniru file yang akan menangkap semua yang ditulis
    dan memasukkannya ke dalam sebuah queue.
    """
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def write(self, s):
        if s.strip():
            self.log_queue.put(s)
        # Tetap tampilkan output ke konsol asli
        sys.__stdout__.write(s)

    def flush(self):
        sys.__stdout__.flush()

# Menggunakan 'basedir' untuk menentukan path log
log_dir = os.path.join(basedir, 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"flowork_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

def run_gui_mode(kernel_instance):
    """Fungsi ini berisi semua logika untuk menjalankan aplikasi dengan antarmuka grafis."""
    from flowork_kernel.ui_shell.main_window import MainWindow

    kernel_instance.write_to_log("Memulai aplikasi Flowork dalam mode GUI...", "INFO")

    root = MainWindow(kernel_instance)
    kernel_instance.set_root(root)

    kernel_instance.check_for_updates()

    root.after(100, kernel_instance.trigger_module_ui_hooks)

    def on_closing_app():
        kernel_instance.write_to_log("Mendeteksi penutupan aplikasi. Menghentikan semua layanan...", "INFO")
        kernel_instance.stop_observer()
        root.destroy()
        kernel_instance.write_to_log("Aplikasi Flowork ditutup.", "INFO")

    root.protocol("WM_DELETE_WINDOW", on_closing_app)
    root.mainloop()

def run_headless_mode(kernel_instance, preset_to_run):
    """Fungsi untuk menjalankan workflow dari command line tanpa GUI."""
    kernel_instance.write_to_log(f"Memulai aplikasi Flowork dalam mode HEADLESS untuk preset: '{preset_to_run}'", "INFO")
    kernel_instance.run_preset_headless(preset_to_run)
    kernel_instance.write_to_log("Eksekusi headless selesai. Aplikasi akan ditutup.", "INFO")
    kernel_instance.stop_observer()

if __name__ == "__main__":
    # Panggil fungsi instalasi dependensi di awal
    install_requirements()

    parser = argparse.ArgumentParser(description="Flowork - Universal Workflow Orchestrator.")
    parser.add_argument(
        '--run-preset',
        type=str,
        help='Menjalankan preset tertentu dalam mode headless (tanpa GUI) dan kemudian keluar.'
    )
    args = parser.parse_args()

    # Menggunakan 'basedir' sebagai project_root_path yang konsisten
    project_root_path = basedir

    print("Main: Memasang 'Teetah Import Hook'...")
    sys.meta_path.insert(0, TeetahFinder(project_root_path))
    print("Main: Import Hook terpasang.")

    from flowork_kernel.kernel import Kernel

    # Mengirimkan project_root_path yang sudah benar ke Kernel
    kernel = Kernel(project_root_path)

    console_interceptor = ConsoleOutputInterceptor(kernel.cmd_log_queue)
    sys.stdout = console_interceptor
    sys.stderr = console_interceptor

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logging.info("Memulai aplikasi Flowork...")

    kernel.start_services()

    if args.run_preset:
        run_headless_mode(kernel, args.run_preset)
    else:
        run_gui_mode(kernel)