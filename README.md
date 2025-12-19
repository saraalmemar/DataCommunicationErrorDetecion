# Data Communication: Error Detection & Correction System

This project is a Python simulation of a network communication system. It demonstrates how data travels through a network, how errors occur, and how they are detected.

## Project Structure
- **Client 1 (Sender):** Takes user input and calculates control information (Parity, CRC).
- **Server (Intermediate Node):** Simulates network noise by injecting random errors.
- **Client 2 (Receiver):** Receives data, recalculates control bits, and alerts the user.

## How to Run
1. Start the Server: `python server.py`
2. Start the Receiver: `python client2.py`
3. Start the Sender: `python client1.py`