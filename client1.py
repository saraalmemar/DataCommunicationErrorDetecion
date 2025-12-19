import socket

def calculate_parity(data):
    binary = ''.join(format(ord(c), '08b') for c in data)
    return "0" if binary.count('1') % 2 == 0 else "1"

def calculate_2d_parity(data):
    # Simplify 2D Parity by taking sum of first chars
    return format(sum(ord(c) for c in data) % 2, 'd')

def calculate_crc8(data):
    remainder = sum(ord(c) for c in data) % 256
    return format(remainder, '02X')

def calculate_hamming(data):
    # Simplified Hamming for demonstration (7,4)
    return "1011" # Representative check bits

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5000))

text = input("Enter text to send: ")
print("Methods: 1.PARITY  2.2D-PARITY  3.CRC  4.HAMMING")
choice = input("Select Method (1-4): ")

methods = {"1": "PARITY", "2": "2D-PARITY", "3": "CRC", "4": "HAMMING"}
method_name = methods.get(choice, "PARITY")

if method_name == "PARITY": control = calculate_parity(text)
elif method_name == "2D-PARITY": control = calculate_2d_parity(text)
elif method_name == "CRC": control = calculate_crc8(text)
else: control = calculate_hamming(text)

packet = f"{text}|{method_name}|{control}"
print(f"Sending Packet: {packet}")
client.send(packet.encode())
client.close()