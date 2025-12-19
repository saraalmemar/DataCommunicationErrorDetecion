import socket
import random

def inject_random_error(data):
    if not data: return data
    chars = list(data)
    # اختيار نوع الخطأ عشوائياً في كل مرة
    error_type = random.choice(['flip', 'replace', 'swap'])
    
    if error_type == 'flip':
        # قلب بت عشوائي في مكان عشوائي
        idx = random.randint(0, len(chars)-1)
        b = list(format(ord(chars[idx]), '08b'))
        bit = random.randint(0, 7)
        b[bit] = '1' if b[bit] == '0' else '0'
        chars[idx] = chr(int("".join(b), 2))
    
    elif error_type == 'replace':
        # استبدال حرف عشوائي برموز غريبة
        idx = random.randint(0, len(chars)-1)
        chars[idx] = random.choice('!@#$%^&*()_+')
        
    elif error_type == 'swap':
        # تبديل أماكن حرفين عشوائياً
        if len(chars) > 1:
            i, j = random.sample(range(len(chars)), 2)
            chars[i], chars[j] = chars[j], chars[i]
            
    return "".join(chars)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# تأكدي من إغلاق التيرمينال القديم لتجنب خطأ الـ Port
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('127.0.0.1', 5000))
server.listen(5)
print("--- RANDOM ERROR SERVER START ---")

while True:
    conn, addr = server.accept()
    packet = conn.recv(1024).decode()
    data, method, control = packet.split("|")
    
    # تخريب عشوائي 100%
    corrupted = inject_random_error(data)
    print(f"Random Corruption: {data} -> {corrupted}")
    
    forward_packet = f"{corrupted}|{method}|{control}"
    
    try:
        c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c2.connect(('127.0.0.1', 6000))
        c2.send(forward_packet.encode())
        c2.close()
    except: pass
    conn.close()