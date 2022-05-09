import threading
import socket

host = '127.0.0.1'
port = 30522

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()


clients = []
names = []

def sendToClients(message):
    for client in clients:
        client.send(message)


def handle(client):


    while True:
        try:
            message = client.recv(1024)
            sendToClients(message)
            if message.decode('ascii')[-4:] == "EXIT":
                client.close()
                print('Client left.')
                break


        except:
            index = client.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            sendToClients(f'{name} connection closed.'.encode('ascii'))
            names.remove(name)
            break

def main():
    while True:
        client, address = server.accept()
        print(f'New connection from {str(address)}')

        client.send('INTRO'.encode('ascii'))
        intro = client.recv(1024).decode('ascii')
        if intro != "P2PEM":
            client.close()
        else:
            print("INTRO received")
            client.send('NAME'.encode('ascii'))
            name = client.recv(1024).decode('ascii')
            names.append(name)
            clients.append(client)

        print(f'Client name is {name}')
        sendToClients(f'{name} joined.'.encode('ascii'))
        client.send("Connected to the server.".encode('ascii'))
        # client.send("Welcome to P2PEM.".encode('ascii'))

        threading.Thread(target=handle, args=(client,)).start()


print("Server is listening ...")
main()