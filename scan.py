import requests
import urllib3
import argparse
import sys
import concurrent.futures
from colorama import Fore, Style, init

# Inisialisasi Colorama & Matikan Warning SSL
init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Global counter untuk progress
processed_count = 0
total_targets = 0

def update_progress():
    # Progress persen warna kuning tanpa bar
    if total_targets > 0:
        percent = (processed_count / total_targets) * 100
        sys.stdout.write(f"\r{Fore.YELLOW}Progress: {percent:.2f}%")
        sys.stdout.flush()

def check_target(url):
    global processed_count
    url = url.strip()
    if not url: return
    if not url.startswith('http'):
        url = 'http://' + url

    try:
        # Step 1: Deteksi Laravel
        root_res = requests.get(url, timeout=7, verify=False, allow_redirects=True)
        
        is_laravel = False
        if 'laravel_session' in root_res.cookies.get_dict():
            is_laravel = True
        elif any('Laravel' in v for v in root_res.headers.values()):
            is_laravel = True
        elif 'X-Laravel-Cache' in root_res.headers:
            is_laravel = True

        if is_laravel:
            # (Hijau) Https://domain.com -> laravel detected (Putih)
            sys.stdout.write(f"\r{Fore.GREEN}{url} -> {Fore.WHITE}laravel detected\n")
            update_progress()
            
            # Step 2: Scan File Sensitif
            paths = {
                "ENV": "/.env", 
                "LOG": "/storage/logs/laravel.log", 
                "UNIT": "/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php"
            }
            
            for name, path in paths.items():
                try:
                    target = url.rstrip('/') + path
                    res = requests.get(target, timeout=7, verify=False, allow_redirects=False)
                    # Validasi konten agar akurat
                    if res.status_code == 200 and any(x in res.text for x in ["APP_KEY", "<?php", "DB_PASSWORD", "Laravel"]):
                        # [!] ENV EXPOSED! (Putih) -> URL (Putih)
                        sys.stdout.write(f"{Fore.WHITE}    [!] {name} EXPOSED! -> {target}\n")
                        update_progress()
                        with open("hasil_tembus.txt", "a") as f:
                            f.write(f"{target}\n")
                except:
                    pass
    except:
        pass
    finally:
        processed_count += 1
        update_progress()

def main():
    global total_targets
    parser = argparse.ArgumentParser(description="Laravel & File Exposure Scanner")
    parser.add_argument("-l", "--list", help="File list target (list.txt)", required=True)
    parser.add_argument("-t", "--threads", help="Jumlah threads (default: 10)", type=int, default=10)
    args = parser.parse_args()

    try:
        with open(args.list, 'r') as f:
            targets = [line.strip() for line in f if line.strip()]
        
        total_targets = len(targets)
        print(f"{Fore.CYAN}Starting scan on {total_targets} targets with {args.threads} threads...\n")
        
        # Eksekusi dengan ThreadPool sesuai input -t
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
            executor.map(check_target, targets)

        print(f"\n\n{Fore.GREEN}Scan Selesai! Hasil sukses tersimpan di hasil_tembus.txt")

    except FileNotFoundError:
        print(f"{Fore.RED}[x] File {args.list} tidak ditemukan!")
    except Exception as e:
        print(f"{Fore.RED}[x] Error: {e}")

if __name__ == "__main__":
    main()
