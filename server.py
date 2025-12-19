import socket
import random

def inject_advanced_error(data):
    # احتمال حدوث خطأ (مثلاً 70% من المرات يحدث خطأ)
    # إذا كان الرقم العشوائي أكبر من 0.7، تمر الرسالة "سليمة"
    if random.random() > 0.7:
        print("Network Status: Stable - Data sent WITHOUT errors.")
        return data

    if not data: return data
    chars = list(data)
    error_type = random.choice(['bit_flip', 'shuffle', 'random_char'])
    
    if error_type == 'bit_flip':
        idx = random.randint(0, len(chars)-1)
        b = list(format(ord(chars[idx]), '08b'))
        bit = random.randint(0, 7)
        b[bit] = '1' if b[bit] == '0' else '0'
        chars[idx] = chr(int("".join(b), 2))
        print(f"Action: Bit Flip at index {idx}")
    
    elif error_type == 'shuffle':
        if len(chars) > 1:
            random.shuffle(chars)
            print("Action: Character Shuffle")
            
    elif error_type == 'random_char':
        idx = random.randint(0, len(chars)-1)
        chars[idx] = random.choice('!@#$%^*()_+')
        print(f"Action: Random Symbol at index {idx}")
            
    return "".join(chars)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('127.0.0.1', 5000))
server.listen(5)
print("--- PERSISTENT SMART SERVER START ---")

while True:
    conn, addr = server.accept()
    packet = conn.recv(1024).decode()
    if not packet: continue
    
    data, method, control = packet.split("|")
    
    # هنا السيرفر يقرر: هل يخرب أم لا؟
    corrupted = inject_advanced_error(data)
    
    forward_packet = f"{corrupted}|{method}|{control}"
    print(f"Result: {data} -> {corrupted}")
    
    try:
        c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c2.connect(('127.0.0.1', 6000))
        c2.send(forward_packet.encode())
        c2.close()
    except: pass
    conn.close()