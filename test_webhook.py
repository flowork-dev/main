# dev :  awenk audico
# EMAIL SAHIDINAOLA@GMAIL.COM
# WEBSITE WWW.TEETAH.ART
# File NAME : test_webhook.py

import requests
import json

# Nama preset yang ingin Anda panggil
nama_preset = "test-webhook"

# URL lengkap ke endpoint webhook
url = f"http://localhost:8989/webhook/{nama_preset}"

# Data yang ingin Anda kirim sebagai pemicu
payload = {
    "pesan_dari_webhook": "Halo dari skrip Python!",
    "sumber_data": "Pengujian Otomatis"
}

# Header untuk menandakan kita mengirim JSON
headers = {
    "Content-Type": "application/json"
}

try:
    print(f"Mengirim permintaan POST ke: {url}")
    print(f"Dengan data: {json.dumps(payload, indent=2)}")

    # Mengirim permintaan
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    # Mencetak hasil respons dari server
    print(f"\nStatus Kode: {response.status_code}")
    print("Respons Server:")
    print(response.json())

except requests.exceptions.ConnectionError as e:
    print(f"\n[ERROR] Gagal terhubung ke server. Pastikan aplikasi Flowork sedang berjalan.")
    print(f"Detail: {e}")