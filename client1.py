import socket

def calculate_check(data, method):
    if method == "PARITY":
        binary = ''.join(format(ord(c), '08b') for c in data)
        return "0" if binary.count('1') % 2 == 0 else "1"
    elif method == "CRC":
        # Simplified CRC: Sum of ASCII
        return format(sum(ord(c) for c in data) % 256, '02X')
    elif method == "2D-PARITY":
        return str(len(data) % 2) # Placeholder for 2D logic
    elif method == "HAMMING":
        return "1011" # Placeholder for Hamming bits
    return "0"

while True:
    try:
        print("\n--- NEW MESSAGE ---")
        data_input = input("Enter text (or type 'exit' to stop): ")
        if data_input.lower() == 'exit':
            break
        
        # القائمة التي طلبتِها (The Menu)
        print("Choose Detection Method:")
        print("1. PARITY")
        print("2. 2D-PARITY")
        print("3. CRC")
        print("4. HAMMING")
        
        choice = input("Select option (1-4): ")
        
        # تحويل الرقم إلى اسم الطريقة
        methods_map = {"1": "PARITY", "2": "2D-PARITY", "3": "CRC", "4": "HAMMING"}
        method = methods_map.get(choice, "PARITY")
        
        control = calculate_check(data_input, method)

        # الاتصال بالسيرفر
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 5000))
        
        # إرسال الحزمة بالتنسيق المطلوب: DATA|METHOD|CONTROL
        packet = f"{data_input}|{method}|{control}"
        client.send(packet.encode())
        print(f"Sent: {packet}")
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")