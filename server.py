import socket
import random

def inject_advanced_error(data):
    if not data: return data
    chars = list(data)
    # اختيار نوع الخطأ عشوائياً في كل مرة لضمان عدم التكرار
    error_type = random.choice(['bit_flip', 'shuffle', 'random_char'])
    
    if error_type == 'bit_flip':
        # 1. قلب بت عشوائي (تغيير شكل الحرف تماماً)
        idx = random.randint(0, len(chars)-1)
        b = list(format(ord(chars[idx]), '08b'))
        bit = random.randint(0, 7)
        b[bit] = '1' if b[bit] == '0' else '0'
        chars[idx] = chr(int("".join(b), 2))
        print(f"Action: Bit Flip at index {idx}")
    
    elif error_type == 'shuffle':
        # 2. إعادة ترتيب الحروف (مثل HELLO تصبح LEOHL)
        if len(chars) > 1:
            random.shuffle(chars)
            print("Action: Character Shuffle")
            
    elif error_type == 'random_char':
        # 3. وضع رموز غريبة متنوعة (ليس فقط &)
        idx = random.randint(0, len(chars)-1)
        chars[idx] = random.choice('!@#$%^*()_+/?<>')
        print(f"Action: Random Symbol at index {idx}")
            
    return "".join(chars)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('127.0.0.1', 5000))
server.listen(5)
print("--- PERSISTENT RANDOM SERVER START ---")

while True:
    conn, addr = server.accept()
    packet = conn.recv(1024).decode()
    if not packet: continue
    
    data, method, control = packet.split("|")
    
    # تطبيق العشوائية القصوى
    corrupted = inject_advanced_error(data)
    print(f"Original: {data} -> Corrupted: {corrupted}")
    
    forward_packet = f"{corrupted}|{method}|{control}"
    
    try:
        c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c2.connect(('127.0.0.1', 6000))
        c2.send(forward_packet.encode())
        c2.close()
    except: pass
    conn.close()