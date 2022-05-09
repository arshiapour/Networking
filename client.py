import threading
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 30522))

name = input("Choose a name: ")




def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'INTRO':
                print("P2PEM")
                client.send("P2PEM".encode('ascii'))
            if message == "NAME":
                client.send(name.encode('ascii'))
            else:
                print(message)
        except:
            print("Error. Please try again.")
            client.close()
            break


def write():
    while True:
        message = f'{name}: {input("")}'
        # if message == f'{name}: EXIT':
          #  client.close()
          #  client.send(f'{name} left.'.encode('ascii'))
        client.send(message.encode('ascii'))


threading.Thread(target=receive).start()
threading.Thread(target=write).start()
