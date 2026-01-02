import socket
import threading
from queue import Queue
import time

# Ayarlar
target = input("Taramak istediğiniz IP adresini girin: ")
queue = Queue()
open_ports = []

def port_scan(port):
    """Belirli bir portun açık olup olmadığını kontrol eder."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1) # 1 saniye bekleme süresi
        result = sock.connect_ex((target, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    except:
        pass

def fill_queue(port_list):
    """Portları kuyruğa ekler."""
    for port in port_list:
        queue.put(port)

def worker():
    """Kuyruktan port alıp tarama fonksiyonunu çağırır."""
    while not queue.empty():
        port = queue.get()
        port_scan(port)

# 0 ile 65535 arasındaki tüm portları kapsar
port_list = range(1, 65536)
fill_queue(port_list)

print(f"\n{target} üzerindeki 65535 port taranıyor. Lütfen bekleyin...\n")
start_time = time.time()

# 100 ile 500 arasında thread (iş parçacığı) sayısı belirlenebilir. 
# Çok yüksek sayı sistemi yorabilir.
thread_list = []
for t in range(200):
    thread = threading.Thread(target=worker)
    thread_list.append(thread)

for thread in thread_list:
    thread.start()

for thread in thread_list:
    thread.join()

end_time = time.time()

# Sonuçları Göster
print("-" * 30)
if open_ports:
    print(f"Açık Portlar ({len(open_ports)} adet):")
    for port in sorted(open_ports):
        print(f"Port {port}: AÇIK")
else:
    print("Hiç açık port bulunamadı.")

print(f"\nToplam Süre: {round(end_time - start_time, 2)} saniye")
print("-" * 30)