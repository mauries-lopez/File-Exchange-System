import threading
import socket
from datetime import datetime
import os

client_folder = ""
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Client Class for knowing the status of the client
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

#Function for sending messages to the Server
def client_send():
    try:
        message = ClientStatus.request
        client.send(message.encode('utf-8'))
    except:
        print('Error: Connection to the Server has failed! Please connect to the server first.')

#Function for receiving messages from the Server
def client_receive():
    try: 
        message = client.recv(1024).decode('utf-8')
        return message
    except:
        print('Error: Connection to the Server has failed! Please connect to the server first.')

#Function to recieve messages while in Broadcast mode
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
       
            

#Overall communication with Server
receive_thread = threading.Thread(target = client_receive)
send_thread = threading.Thread(target = client_send)

#Function for starting the Client Application
def start():

    global client_folder
    while True:
        try:
            client_command = input('Input command >>> ')
            input_syntax = client_command.split()
            res = find_function(input_syntax)
            if res == True:
                break
        except IndexError:
            print('Error: Command not found.')


def find_function(input_syntax):

    global client_folder
    clientStatus = ClientStatus()

    func = input_syntax[0]

    if func == '/join':
        try: 
            host = str(input_syntax[1])
            port = int(input_syntax[2])
            client.connect((host, port))
            res = client_receive()
            ClientStatus.joined = True
            print(res)
        except TimeoutError:
            #Error checking for wrong IP Address or Port Number
            print('Error: Connection to the Server has timed out! Please check the IP Address and Port Number.')
        except ConnectionRefusedError:
            #Error checking for wrong IP Address or Port Number
            print('Error: Connection to the Server has failed! Please check the IP Address and Port Number.')
        except socket.error as e:
            #Error checking for client already connected to the server
            if e.errno == 11001:
                print('Error: Connection to the Server has failed! Please check the IP Address.')
            else:
                print(f'Error: Connection is already established.')
        except IndexError:
            #Error checking for missing IP Address or Port Number
            print('Error: Command parameters do not match or is not allowed.')
        except:
            #Other errors
            print('Error: Connection to the Server has failed! Please check the IP Address and Port Number.')

    elif func == '/leave':
        if clientStatus.joined == False:
            print('Error: Connection to the Server has failed! Please connect to the server first.')
            return False
        else:
            try:
                ClientStatus.request = 'getLeave'
                client_send()
                message = client_receive()
                print(message)
                return True
            except:
                print('Error: Disconnection failed. Please connect to the server first.')

    elif func == '/register': 

        if clientStatus.joined == False:
            print('Error: Registration to the Server has failed! Please connect to the server first.')
            return False
        else:
            ClientStatus.request = 'getAlias'
            client_send()
            message = client_receive()
            if message == "alias?":
                try:
                    alias = str(input_syntax[1])
                    ClientStatus.alias = alias
                    client.send(alias.encode('utf-8'))

                    client_folder = os.path.join("client_files", alias)
                    if not os.path.exists(client_folder):
                        os.makedirs(client_folder)

                    res = client_receive()
                    ClientStatus.registered = True
                    print(res)
                except socket.error as e:
                    #Error checking for client not connected to the server
                    print('Error: Connection to the Server has failed! Please connect to the server first.')
                except IndexError:
                    #Error checking for missing alias
                    client.send('error'.encode('utf-8'))
                    res = client_receive()
                    print(res)
                except:
                    #Error checking for existing alias
                    res = client_receive()
                    print(res)

    elif func == '/store':

        foundError = False
        if clientStatus.joined == False:
            print('Error: Storing to the Server has failed! Please connect to the server first.')
            return False
        else:
            if clientStatus.registered == True:
                ClientStatus.request = 'getStore'
                client_send()
                message = client_receive()
                
                if message == "store?":    

                    try:
                        #Check file if it exists
                        filename = str(input_syntax[1])
                        storedClientFolder = os.path.join(client_folder, filename.split('.')[0] + '-stored.' + filename.split('.')[1])
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
                        #Send Original File Name
                            
                        client.send(filename.encode('utf-8'))

                        file = open(filename, "rb")

                        #Store a file to the server. Add '-store' as suffix to the filename
                        storedFilename = filename.split('.')[0] + '-stored.' + filename.split('.')[1]
                        client.send(storedFilename.encode())

                        #Current timestamp
                        curr = datetime.now()
                        currTime = curr.strftime("%Y-%m-%d %H:%M:%S")
                        client.send(currTime.encode('utf-8'))
                                    
                        data = file.read()
                        client.sendall(data)

                        client.send(b"<END>")

                        #Receive feedback from server
                        res = client_receive()
                        print(res)

                        file.close()

            else:
                print('Error: Unregistered Client!')
            
            
    elif func == '/dir':
        if clientStatus.joined == False:
            print('Error: Requesting for directories to the Server has failed! Please connect to the server first.')
            return False
        else:
            if clientStatus.registered == True:
                try:
                    ClientStatus.request = 'getDir'
                    client_send()
                    res = client_receive()
                    message = 'Server Directory: ' + res
                    print(message)
                except:
                    print('Error: Requesting for directories to the Server has failed! Please connect to the server first.')
                    client.close()
                    return True
            else:
                print('Error: Unregistered Client!')

    elif func == '/get':

        invalidFileName = False
        foundError = False

        if clientStatus.joined == False:
            print('Error: Fetching files from the Server has failed! Please connect to the server first.')
            return False
        else:
            if clientStatus.registered == True:
                ClientStatus.request = 'getRetrieve'
                client_send()
                res = client_receive()
                
                if res == "retrieve?":
                    try:    
                        filename = str(input_syntax[1])
                        client.send(filename.encode('utf-8'))
                    except IndexError:
                        print('Error: Command parameters do not match or is not allowed.')
                        client.send('error'.encode('utf-8'))
                        invalidFileName = True
                    
                    if invalidFileName == False:
                        retrievedFileName = os.path.join(client_folder, client.recv(1024).decode('utf-8'))

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
            
            else:
                print('Error: Unregistered Client!')

    elif func == '/?':
        print('\n/join <server IP address> <server port number> - Connect to the server application')
        print('/leave - Disconnect from the server application')
        print('/register <handle> - Register a unique handle or alias')
        print('/store <filename> - Send a file to the server')
        print('/dir - Request directory file list from a server')
        print('/get <filename> - Fetch a file from the server')
        print('/chat - Join the chat server that supports Unicast and Broadcast feature')
        print('. . . . . /leavechat - To leave the chat server')
        print('/? - Request command help to output all Input Syntax commands for references\n')



    elif func == '/chat':

        if clientStatus.registered == True:

            print('You have joined the chat server.')

            ClientStatus.request = 'getChat'
            client_send()

            ClientStatus.inBroadcast = True

            #Overall communication with Server in Broadcast Mode
            broadcast_receive_thread = threading.Thread(target = client_recieveBroadMode)
            broadcast_send_thread = threading.Thread(target = client_sendBroadMode)
                
            broadcast_receive_thread.start()
            broadcast_send_thread.start()

            broadcast_receive_thread.join()
            broadcast_send_thread.join()
            
            return True     
        else:
           print('Error: Unregistered Client!')
        
    else:
        print('Error: Command not found.')

if __name__ == "__main__":
    start()
    receive_thread.start()
    send_thread.start()    
    receive_thread.join()
    send_thread.join()




#Question: 
        #1. For the alias or handles, kapag po ba may alias or handles na po ung isang client, bawal na po siya mag register ulit for a new unique alias or handles?
        #2. For the error messages naman po, dapat po ba makikita ito sa server side and client side po?
        #3. Ung sa file po since nasa localhost lang po ung pag test, pwede po ba mag lagay ng extra word sa filename if iistore na po sa server? Halimbawa po, mula sa original filename na "test.txt" magiging "test-store.txt" kapag nasa server na po. This also applies to receiving the file po.
        #4. Okay lang po ba kahit CLI lang po ung interface?
        #5. Kailangan po ba naka register po ung client bago siya mag leave? or pwede ung hindi naka register tapos makaka leave?
        #6. Habang nag tetest po ng code, dapat po ba may sample txt file na po sa folder?