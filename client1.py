import socket

def calculate_check(data, method):
    if method == "PARITY":
        binary = ''.join(format(ord(c), '08b') for c in data)
        return "0" if binary.count('1') % 2 == 0 else "1"
    return format(sum(ord(c) for c in data) % 256, '02X')

while True: # loop لضمان عدم انقطاع الاتصال
    try:
        data_input = input("\nEnter text to send (or 'exit' to quit): ")
        if data_input.lower() == 'exit': break
        
        method = input("Choose method (PARITY/CRC): ").upper()
        control = calculate_check(data_input, method)

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 5000))
        
        packet = f"{data_input}|{method}|{control}"
        client.send(packet.encode())
        print(f"Packet sent successfully!")
        client.close() # نغلق السوكيت للرسالة الحالية ونفتحه للجديدة
    except Exception as e:
        print(f"Connection error: {e}")