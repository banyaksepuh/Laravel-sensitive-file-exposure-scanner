# 🔐 Laravel Sensitive File Exposure Scanner

**Automated tool for detecting Laravel Framework and Sensitive File Exposure**

---

## 🧠 Overview

Tool ini digunakan untuk melakukan automated scanning terhadap aplikasi Laravel guna mengidentifikasi potensi misconfiguration dan sensitive file exposure.

Tool ini dirancang untuk:
- Security assessment
- Penetration testing (authorized scope)
- Reconnaissance awal terhadap target Laravel

Scanner bekerja dengan:
- Mendeteksi apakah target menggunakan framework Laravel
- Melakukan probing terhadap file sensitif yang umum terekspos
- Mengidentifikasi indikasi kebocoran informasi penting seperti credential atau source code

> ⚠️ Tool ini dibuat hanya untuk **educational purposes** dan **authorized security testing**

---

## 🔍 Detection Logic
1. Laravel Fingerprinting

Target akan diidentifikasi sebagai Laravel jika ditemukan indikator seperti:
- Cookie: laravel_session
- Header mengandung keyword Laravel
- Header khusus seperti X-Laravel-Cache

2. Sensitive File Scanning

Setelah terdeteksi Laravel, tool akan mengecek endpoint berikut:
- /.env → konfigurasi environment
- /storage/logs/laravel.log → log aplikasi
- /vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php → potensi RCE lama

---

## ⚙️ Features
- 🔍 Multi-threaded scanning
- ⚡ Laravel fingerprinting
- 🔐 Sensitive file exposure detection
- 🧪 Real-time progress tracking
- 🚀 Output logging otomatis

## 🛠️ Requirements

- Python 3.x
- requests
- urllib3
- colorama

Install dependencies:
```bash
pip install -r requirements.txt
```
---
USAGE
---
📌 Basic Command with list
```bash
$ python scan.py -l list.txt
```
⚡ Advanced Usage with threads
```bash
$ python scan.py -l targets.txt -t 10
```
---

