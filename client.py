import ast
import threading
import socket
from datetime import datetime
import os
from tkinter import *
from tkinter import simpledialog, messagebox, filedialog


# def find_function(input_syntax):
#
#     global client_folder
#     clientStatus = ClientStatus()
#
#     func = input_syntax[0]
#
#     if func == '/join':
#         try:
#             host = str(input_syntax[1])
#             port = int(input_syntax[2])
#             client.connect((host, port))
#             res = client_receive()
#             ClientStatus.joined = True
#             print(res)
#         except TimeoutError:
#             #Error checking for wrong IP Address or Port Number
#             print('Error: Connection to the Server has timed out! Please check the IP Address and Port Number.')
#         except ConnectionRefusedError:
#             #Error checking for wrong IP Address or Port Number
#             print('Error: Connection to the Server has failed! Please check the IP Address and Port Number.')
#         except socket.error as e:
#             #Error checking for client already connected to the server
#             if e.errno == 11001:
#                 print('Error: Connection to the Server has failed! Please check the IP Address.')
#             else:
#                 print(f'Error: Connection is already established.')
#         except IndexError:
#             #Error checking for missing IP Address or Port Number
#             print('Error: Command parameters do not match or is not allowed.')
#         except:
#             #Other errors
#             print('Error: Connection to the Server has failed! Please check the IP Address and Port Number.')
#
#     elif func == '/leave':
#         if clientStatus.joined == False:
#             print('Error: Connection to the Server has failed! Please connect to the server first.')
#             return False
#         else:
#             try:
#                 ClientStatus.request = 'getLeave'
#                 client_send()
#                 message = client_receive()
#                 print(message)
#                 return True
#             except:
#                 print('Error: Disconnection failed. Please connect to the server first.')
#
#     elif func == '/register':
#
#         if clientStatus.joined == False:
#             print('Error: Registration to the Server has failed! Please connect to the server first.')
#             return False
#         else:
#             ClientStatus.request = 'getAlias'
#             client_send()
#             message = client_receive()
#             if message == "alias?":
#                 try:
#                     alias = str(input_syntax[1])
#                     ClientStatus.alias = alias
#                     client.send(alias.encode('utf-8'))
#
#                     client_folder = os.path.join("client_files", alias)
#                     if not os.path.exists(client_folder):
#                         os.makedirs(client_folder)
#
#                     res = client_receive()
#                     ClientStatus.registered = True
#                     print(res)
#                 except socket.error as e:
#                     #Error checking for client not connected to the server
#                     print('Error: Connection to the Server has failed! Please connect to the server first.')
#                 except IndexError:
#                     #Error checking for missing alias
#                     client.send('error'.encode('utf-8'))
#                     res = client_receive()
#                     print(res)
#                 except:
#                     #Error checking for existing alias
#                     res = client_receive()
#                     print(res)
#
#     elif func == '/store':
#
#         foundError = False
#         if clientStatus.joined == False:
#             print('Error: Storing to the Server has failed! Please connect to the server first.')
#             return False
#         else:
#             if clientStatus.registered == True:
#                 ClientStatus.request = 'getStore'
#                 client_send()
#                 message = client_receive()
#
#                 if message == "store?":
#
#                     try:
#                         #Check file if it exists
#                         filename = str(input_syntax[1])
#                         storedClientFolder = os.path.join(client_folder, filename.split('.')[0] + '.' + filename.split('.')[1])
#                         file = open(filename, "rb")
#                         file.close()
#
#                     except IndexError:
#                         # Error checking for missing filename
#                         client.send('fileError'.encode('utf-8'))
#                         res = client_receive()
#                         print(res)
#                         foundError = True
#                     except FileNotFoundError as e :
#                         # Error checking for file not found
#                         client.send('fileError1'.encode('utf-8'))
#                         res = client_receive()
#                         print(res)
#                         foundError = True
#
#                     if foundError == False:
#                         #Send Original File Name
#
#                         client.send(filename.encode('utf-8'))
#
#                         file = open(filename, "rb")
#
#                         #Store a file to the server. Add '-store' as suffix to the filename
#                         storedFilename = filename.split('.')[0] + '.' + filename.split('.')[1]
#                         client.send(storedFilename.encode())
#
#                         #Current timestamp
#                         curr = datetime.now()
#                         currTime = curr.strftime("%Y-%m-%d %H:%M:%S")
#                         client.send(currTime.encode('utf-8'))
#
#                         data = file.read()
#                         client.sendall(data)
#
#                         client.send(b"<END>")
#
#                         #Receive feedback from server
#                         res = client_receive()
#                         print(res)
#
#                         file.close()
#
#             else:
#                 print('Error: Unregistered Client!')
#
#
#     elif func == '/dir':
#         if clientStatus.joined == False:
#             print('Error: Requesting for directories to the Server has failed! Please connect to the server first.')
#             return False
#         else:
#             if clientStatus.registered == True:
#                 try:
#                     ClientStatus.request = 'getDir'
#                     client_send()
#                     res = client_receive()
#                     message = 'Server Directory: ' + res
#                     print(message)
#                 except:
#                     print('Error: Requesting for directories to the Server has failed! Please connect to the server first.')
#                     client.close()
#                     return True
#             else:
#                 print('Error: Unregistered Client!')
#
#     elif func == '/get':
#
#         invalidFileName = False
#         foundError = False
#
#         if clientStatus.joined == False:
#             print('Error: Fetching files from the Server has failed! Please connect to the server first.')
#             return False
#         else:
#             if clientStatus.registered == True:
#                 ClientStatus.request = 'getRetrieve'
#                 client_send()
#                 res = client_receive()
#
#                 if res == "retrieve?":
#                     try:
#                         filename = str(input_syntax[1])
#                         client.send(filename.encode('utf-8'))
#                     except IndexError:
#                         print('Error: Command parameters do not match or is not allowed.')
#                         client.send('error'.encode('utf-8'))
#                         invalidFileName = True
#
#                     if invalidFileName == False:
#                         retrievedFileName = os.path.join(client_folder, filename)
#
#                         if retrievedFileName == 'error':
#                             print('Error: File not found in the server.')
#                             foundError = True
#                         else:
#                             if foundError == False:
#                                 file = open(retrievedFileName, "wb")
#                                 file_bytes = b""
#
#                                 done = False
#
#                                 while not done:
#                                     data = client.recv(1024)
#                                     file_bytes += data
#
#                                     if b"<END>" in file_bytes:
#                                         done = True
#
#                                 file.write(file_bytes[:-5])
#
#                                 print(f'File received from Server: {retrievedFileName}')
#
#                                 file.close()
#
#             else:
#                 print('Error: Unregistered Client!')
#
#     elif func == '/?':
#         print('\n/join <server IP address> <server port number> - Connect to the server application')
#         print('/leave - Disconnect from the server application')
#         print('/register <handle> - Register a unique handle or alias')
#         print('/store <filename> - Send a file to the server')
#         print('/dir - Request directory file list from a server')
#         print('/get <filename> - Fetch a file from the server')
#         print('/chat - Join the chat server that supports Unicast and Broadcast feature')
#         print('. . . . . /leavechat - To leave the chat server')
#         print('/? - Request command help to output all Input Syntax commands for references\n')
#
#
#
#     elif func == '/chat':
#
#         if clientStatus.registered == True:
#
#             print('You have joined the chat server.')
#
#             ClientStatus.request = 'getChat'
#             client_send()
#
#             ClientStatus.inBroadcast = True
#
#             #Overall communication with Server in Broadcast Mode
#             broadcast_receive_thread = threading.Thread(target = client_recieveBroadMode)
#             broadcast_send_thread = threading.Thread(target = client_sendBroadMode)
#
#             broadcast_receive_thread.start()
#             broadcast_send_thread.start()
#
#             broadcast_receive_thread.join()
#             broadcast_send_thread.join()
#
#             return True
#         else:
#            print('Error: Unregistered Client!')
#
#     else:
#         print('Error: Command not found.')

class ClientStatus:
    joined = False
    registered = False
    request = ""
    alias = ""
    inBroadcast = False


class BroadcastServer:
    started = False
    receiveThread = threading.Thread()
    sendThread = threading.Thread()


# Function for sending messages to the Server
def client_send():
    try:
        message = ClientStatus.request
        client.send(message.encode('utf-8'))
    except:
        print('Error: Connection to the Server has failed! Please connect to the server first.')


# Function for receiving messages from the Server
def client_receive():
    try:
        message = client.recv(1024).decode('utf-8')
        return message
    except:
        print('Error: Connection to the Server has failed! Please connect to the server first.')


# Function to recieve messages while in Broadcast mode
def client_recieveBroadMode():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == '' or message == 'leavechat':
                ClientStatus.inBroadcast = False
                start()
                break
            else:
                print(message)
        except Exception as e:
            print(f'Error: {e}')
            break


def client_sendBroadMode():
    clientStatus = ClientStatus()
    alias = clientStatus.alias

    while True:
        try:
            if clientStatus.inBroadcast == True:
                message = f'{alias}: {input("")}'
                client.send(message.encode('utf-8'))
            else:
                break
        except Exception as e:
            print(f'Error: {e}')
            break

        # Overall communication with Server


receive_thread = threading.Thread(target=client_receive)
send_thread = threading.Thread(target=client_send)


# -------------------- CONNECT TO SERVER -------------------- #
def connect_to_server():
    global clientStatus
    if clientStatus.joined == False:
        host = simpledialog.askstring("Server Connection", "Enter server IP address:")
        port = simpledialog.askinteger("Server Connection", "Enter server port:")

        # TODO: Remove Later!!!
        # host = "127.0.0.1"
        # port = 12345
        try:
            client.connect((host, port))
            joined = True
            connect_button.config(state=DISABLED)
            register_button.config(state=NORMAL)
            res = client_receive()
            messagebox.showinfo("Connection", "Connection to the server successful!")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Error: {e}")
    else:
        messagebox.showinfo("Info", "Already connected to the server!")

# -------------------- REGISTER ALIAS -------------------- #
def register_alias():
    global clientStatus, client_folder
    ClientStatus.request = "getAlias"
    client_send()
    message = client_receive()
    # print(message)

    if message == "alias?":
        try:
            alias = simpledialog.askstring("Register Alias", "Enter your alias:")

            # TODO: Remove Later!!!
            # alias = "Alice"

            ClientStatus.alias = alias
            client.send(alias.encode('utf-8'))

            client_folder = os.path.join("client_files", alias)
            if not os.path.exists(client_folder):
                os.makedirs(client_folder)

            res = client_receive()
            ClientStatus.registered = True
            messagebox.showinfo(res)

            # enable buttons and disable register button
            register_button.config(state=DISABLED)
            store_button.config(state=NORMAL)
            retrieve_button.config(state=NORMAL)
            dir_button.config(state=NORMAL)
            leave_button.config(state=NORMAL)

        except socket.error as e:
            # Error checking for client not connected to the server
            print('Error: Connection to the Server has failed! Please connect to the server first.')
        except IndexError:
            # Error checking for missing alias
            client.send('error'.encode('utf-8'))
            res = client_receive()
            print(res)
        except:
            # Error checking for existing alias
            res = client_receive()
            print(res)

# -------------------- STORE FILE -------------------- #
def store_file():
    global clientStatus
    foundError = False
    filename = ""

    if clientStatus.registered == True:
        ClientStatus.request = "getStore"
        client_send()
        message = client_receive()

        if message == "store?":
            try:
                filename = filedialog.askopenfilename(title="Select a file to store")
                filename = os.path.basename(filename)
                # print(filename)
                file = open(filename, "rb")
                file.close()
            except IndexError:
                # Error checking for missing filename
                client.send('fileError'.encode('utf-8'))
                res = client_receive()
                print(res)
                foundError = True
            except FileNotFoundError as e :
                # Error checking for file not found
                client.send('fileError1'.encode('utf-8'))
                res = client_receive()
                print(res)
                foundError = True

            if foundError == False:
                # Send Original File Name

                client.send(filename.encode('utf-8'))

                file = open(filename, "rb")

                storedFilename = filename.split('.')[0] + '.' + filename.split('.')[1]
                client.send(storedFilename.encode())

                # Current timestamp
                curr = datetime.now()
                currTime = curr.strftime("%Y-%m-%d %H:%M:%S")
                client.send(currTime.encode('utf-8'))

                data = file.read()
                client.sendall(data)

                client.send(b"<END>")

                # Receive feedback from server
                res = client_receive()
                print(res)

                file.close()

# -------------------- RETRIEVE FILE -------------------- #
def retrieve_file():
    invalidFileName = False
    foundError = False
    filename = ""

    ClientStatus.request = "getRetrieve"
    client_send()
    res = client_receive()

    if res == "retrieve?":
        try:
            filename = simpledialog.askstring("Retrieve File", "Enter the filename to retrieve:")
            client.send(filename.encode('utf-8'))
        except IndexError:
            print('Error: Command parameters do not match or is not allowed.')
            client.send('error'.encode('utf-8'))
            invalidFileName = True

        if invalidFileName == False:
            fromServerFileName = client.recv(1024).decode('utf-8')
            retrievedFileName = os.path.join(client_folder, fromServerFileName)

            if retrievedFileName == 'error':
                print('Error: File not found in the server.')
                foundError = True
            else:
                if foundError == False:
                    file = open(retrievedFileName, "wb")
                    file_bytes = b""

                    done = False

                    while not done:
                        data = client.recv(1024)
                        file_bytes += data

                        if b"<END>" in file_bytes:
                            done = True

                    file.write(file_bytes[:-5])

                    print(f'File received from Server: {retrievedFileName}')

                    file.close()

# -------------------- SHOW SERVER FILES -------------------- #
def show_server_files():
    ClientStatus.request = 'getDir'
    client_send()
    res = client_receive()
    files = ast.literal_eval(res)
    # message = 'Server Directory: ' + files
    show_files_window(files)


def show_files_window(files):
    files_window = Toplevel(window)
    files_window.title("Server Files")

    files_listbox = Listbox(files_window)
    for file in files:
        files_listbox.insert(END, file)

    files_listbox.pack(padx=10, pady=10)


# -------------------- LEAVE SERVER -------------------- #
def leave_server():
    try:
        ClientStatus.request = 'getLeave'
        client_send()
        message = client_receive()
        print(message)

        messagebox.showinfo(message)
        window.destroy()

        return True
    except:
        print('Error: Disconnection failed. Please connect to the server first.')


# -------------------- UI SETUP -------------------- #
window = Tk()
window.title("File Exchange Client")
window.geometry("300x400")

clientStatus = ClientStatus()

connect_button = Button(window, text="Connect to Server", command=connect_to_server)
connect_button.pack(pady=10)

register_button = Button(window, text="Register Alias", command=register_alias,
                         state=DISABLED)
register_button.pack(pady=10)

store_button = Button(window, text="Store File", command=store_file, state=DISABLED)
store_button.pack(pady=10)

retrieve_button = Button(window, text="Retrieve File", command=retrieve_file,
                         state=DISABLED)
retrieve_button.pack(pady=10)

dir_button = Button(window, text="Dir", command=show_server_files, state=DISABLED)
dir_button.pack(pady=10)

leave_button = Button(window, text="Leave Server", command=leave_server, state=DISABLED)
leave_button.pack(pady=10)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_folder = ""


def start():
    global client_folder
    window.mainloop()



if __name__ == "__main__":
    start()
    receive_thread.start()
    send_thread.start()
    receive_thread.join()
    send_thread.join()
