import socket

def recalculate(data, method):
    if method == "PARITY":
        binary = ''.join(format(ord(c), '08b') for c in data)
        return "0" if binary.count('1') % 2 == 0 else "1"
    return format(sum(ord(c) for c in data) % 256, '02X')

receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver.bind(('127.0.0.1', 6000))
receiver.listen(1)
print("--- CLIENT 2 IS WAITING ---")

while True:
    conn, addr = receiver.accept()
    packet = conn.recv(1024).decode()
    data, method, sent_ctrl = packet.split("|")
    
    calc_ctrl = recalculate(data, method)
    
    print("\n" + "="*30)
    print(f"DATA RECEIVED  : {data}")
    print(f"SENT CONTROL   : {sent_ctrl}")
    print(f"CALC CONTROL   : {calc_ctrl}")
    
    if sent_ctrl == calc_ctrl:
        print("RESULT: DATA CORRECT")
    else:
        print("RESULT: DATA CORRUPTED (ALERT!)")
    print("="*30)
    conn.close()