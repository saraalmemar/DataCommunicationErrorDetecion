import socket

def calculate_check(data, method):
    if method == "PARITY":
        binary = ''.join(format(ord(c), '08b') for c in data)
        return "0" if binary.count('1') % 2 == 0 else "1"
    return format(sum(ord(c) for c in data) % 256, '02X')

receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
receiver.bind(('127.0.0.1', 6000))
receiver.listen(5)
print("--- RECEIVER IS PERSISTENT AND WAITING ---")

while True:
    conn, addr = receiver.accept()
    packet = conn.recv(1024).decode()
    if not packet: continue
    
    data, method, sent_ctrl = packet.split("|")
    calc_ctrl = calculate_check(data, method)
    
    status = "DATA CORRECT" if sent_ctrl == calc_ctrl else "DATA CORRUPTED"
    print(f"\n[NEW MESSAGE] Data: {data} | Status: {status}")
    conn.close()