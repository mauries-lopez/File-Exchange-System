import tkinter as tk
import threading
from tkinter import messagebox  # Import the messagebox module
import socket
import os


class ServerGUI:

    def __init__(self):
        self.server_folder = "server_files"
        self.clients = []

        self.root = tk.Tk()
        self.root.title("File Exchange Server")
        self.root.geometry("400x300")

        self.start_server_button = tk.Button(self.root, text="Start Server", command=self.start_server)
        self.start_server_button.pack(pady=20)

        self.add_client_button = tk.Button(self.root, text="Add Client", command=self.add_client)
        self.add_client_button.pack(pady=20)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def start_server(self):
        # Implement your server logic here
        # You can use the existing server.py code or modify it as needed
        # For simplicity, I'll just print a message for demonstration purposes
        print("Server started")
        try:
            host = '127.0.0.1'
            port = 12345
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((host, port))
            self.server.listen()

            self.receive_thread = threading.Thread(target=self.receive)
            self.receive_thread.start()

        except Exception as e:
            messagebox.showerror("Error", "Failed to start server: {}".format(str(e)))

    def add_client(self):
        # Implement your logic to add a new client here
        # You can use the existing client.py code or modify it as needed
        # For simplicity, I'll just print a message for demonstration purposes
        print("Client added")

    def on_close(self):
        # Implement cleanup logic here if needed
        if hasattr(self, 'server'):
            self.server.close()
        self.root.destroy()

    def receive(self):
        while True:
            print('Server is running and listening...')
            client, address = self.server.accept()
            print(f'Connection established on {address}')
            client.send(f'Connection to the File Exchange Server is successful!'.encode('utf-8'))
            self.clients.append(client)
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

    def handle_client(self, client):
        # Implement your existing handle_client logic here
        # You can copy the existing server.py handle_client code

        while True:
            try:
                signal = client.recv(1024).decode('utf-8')

                if signal == 'getAlias':
                    client.send('alias?'.encode('utf-8'))
                    alias = client.recv(1024).decode('utf-8')
                    if alias == 'error':
                        client.send('Error: Command parameters do not match or is not allowed.'.encode('utf-8'))
                        print(f'Error: Registration failed. Command parameters do not match or is not allowed.'.encode(
                            'utf-8'))
                    else:
                        if alias not in aliases:
                            aliases.append(alias)
                            client.send(f'Welcome {alias}!'.encode('utf-8'))
                            print(f'Alias for a client is set to {alias}!'.encode('utf-8'))
                        else:
                            client.send('Error: Registration failed. Handle or alias already exists.'.encode('utf-8'))
                            print(f'Unsuccessful registration. Handle or alias already exists!')

                elif signal == 'getLeave':
                    index = clients.index(client)
                    message = 'Connection closed. Thank you!'
                    client.send(message.encode('utf-8'))
                    clients.remove(client)
                    client.close()

                    # If client has an alias (registered), remove it from the list
                    if alias in aliases:
                        print(f'{alias} connection closed.'.encode("utf-8"))
                        alias = aliases[index]
                        aliases.remove(alias)


                elif signal == 'getStore':
                    client.send('store?'.encode('utf-8'))
                    res = client.recv(1024).decode('utf-8')
                    if res == 'fileError':
                        client.send('Error: Command parameters do not match or is not allowed.'.encode('utf-8'))
                        print(
                            f'Error: Upload failed. Command parameters do not match or is not allowed.'.encode('utf-8'))
                    elif res == 'fileError1':
                        client.send('Error: File not found'.encode('utf-8'))
                        print(f'Error: Upload failed. File not found.'.encode('utf-8'))
                    else:
                        origFileName = res
                        storeFileName = os.path.join(server_folder, client.recv(1024).decode('utf-8'))
                        timeStamp = client.recv(1024).decode('utf-8')

                        print(f'{alias}<{timeStamp}>: Uploaded {origFileName}')

                        file = open(storeFileName, "wb")
                        file_bytes = b""

                        done = False

                        while not done:
                            data = client.recv(1024)
                            file_bytes += data

                            if b"<END>" in file_bytes:
                                done = True

                        file.write(file_bytes[:-5])

                        client.send(f'{alias}<{timeStamp}>: Uploaded {origFileName}'.encode('utf-8'))
                        file.close()

                elif signal == 'getRetrieve':

                    foundError = False

                    print(f'{alias} requested for a file in the server'.encode('utf-8'))
                    client.send('retrieve?'.encode('utf-8'))

                    getFileName = os.path.join(server_folder, client.recv(1024).decode('utf-8'))

                    if getFileName == 'error':
                        print(f'Error: Download failed. Command parameters do not match or is not allowed.'.encode(
                            'utf-8'))
                        foundError = True
                    else:
                        try:
                            file = open(getFileName, "rb")
                            file.close()
                        except Exception as e:
                            foundError = True
                            client.send('error'.encode('utf-8'))
                            print(f'Error: {e}')

                        if foundError == False:
                            file = open(getFileName, "rb")

                            storedFilename = os.path.basename(getFileName)
                            # storedFilename = getFileName.split('.')[0] + '.' + getFileName.split('.')[1]
                            client.send(storedFilename.encode())

                            data = file.read()
                            client.sendall(data)

                            client.send(b"<END>")
                            file.close()

                            print(f'{alias}: Downloaded {storedFilename} from the server.')

                elif signal == 'getDir':
                    print(f'{alias} requested for the list of files in the directory.'.encode('utf-8'))
                    files = [file for file in os.listdir(server_folder) if not file.endswith(".py")]
                    client.send(str(files).encode('utf-8'))
                    print(files)

                elif signal == 'getChat':
                    print(f'{alias} joined the chat server.')
                    while True:
                        try:
                            broadcastMessage = client.recv(1024)
                            tempMessage = broadcastMessage.decode('utf-8')
                            splitMessage = tempMessage.split(':')[1].strip()
                            if splitMessage == '/leavechat':
                                print(f'{alias} has left the chat server.')
                                broadcast(f'{alias} has left the chat.'.encode('utf-8'), client)
                                client.send('leavechat'.encode('utf-8'))
                                break
                            else:
                                broadcast(broadcastMessage, client)
                        except:
                            index = clients.index(client)
                            broadcast(f'{alias} has left the chat.'.encode('utf-8'), client)
                            clients.remove(client)
                            client.close()
                            alias = aliases[index]
                            aliases.remove(alias)
                            break
            except:
                break

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    server_gui = ServerGUI()
    server_gui.run()