import socket
import errno
from threading import Thread
import rsa
import json
from base64 import b64encode, b64decode
import jsonpickle
import aes256encrypt, aes256decrypt
flag=0
HEADER_LENGTH = 10
client_socket = None
other_client = ""
# Connects to the server
def connect(ip, port, my_username, error_callback):

    global client_socket

    # Create a socket
    # socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
    # socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to a given ip and port
        client_socket.connect((ip, port))
    except Exception as e:
        # Connection error
        error_callback('Connection error: {}'.format(str(e)))
        return False

    #generate the private and public keys
    global publickey, privatekey
    (publickey, privatekey) = rsa.newkeys(1024)
    json_pk = jsonpickle.encode(publickey)
    # Prepare username and header and send them
    # We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
    username = my_username.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    # client_socket.send(username_header + username + publickey)
    send(my_username)
    send(json_pk)
    # print(publickey)
    return True

# Sends a message to the server
def send(message):
    message = aes256encrypt.aes256encrypt(message)
    # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
    message = message.encode('utf-8')
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(message_header + message)

# Starts listening function in a thread
# incoming_message_callback - callback to be called when new message arrives
# error_callback - callback to be called on error
def start_listening(incoming_message_callback, error_callback):
    Thread(target=listen, args=(incoming_message_callback, error_callback), daemon=True).start()

# Listens for incomming messages
def listen(incoming_message_callback, error_callback):
    global flag
    while True:

        try:
            # Now we want to loop over received messages (there might be more than one) and print them
            while True:

                # Receive our "header" containing username length, it's size is defined and constant
                username_header = client_socket.recv(HEADER_LENGTH)

                # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
                if not len(username_header):
                    error_callback('Connection closed by the server')
                
                # cred_length = int(username_header.decode('utf-8').strip())
                # cred = client_socket.recv(cred_length)
                # print(cred)
                # clients = jsonpickle.decode(cred)
                # print(clients)
                # flag=1
                

                # Convert header to int value
                username_length = int(username_header.decode('utf-8').strip())

                # Receive and decode username
                username = client_socket.recv(username_length).decode('utf-8')
                if username_length > 128 and '{"py/b64' in username:
                    # print(username)
                    #list of public keys
                    creds = list(jsonpickle.decode(username).values())
                    for i in creds:
                        creds[creds.index(i)] = jsonpickle.decode(i)
                        if i == publickey:
                            creds.remove(i)
                    # print(creds)
                    continue
                username = aes256decrypt.aes256decrypt(username)

                # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
                message_header = client_socket.recv(HEADER_LENGTH)
                message_length = int(message_header.decode('utf-8').strip())
                message = client_socket.recv(message_length).decode('utf-8')
                # Print message
                #here decryption will be done
                message = aes256decrypt.aes256decrypt(message)
                incoming_message_callback(username, message)

        except Exception as e:
            # Any other exception - something happened, exit
            error_callback('Reading error: {}'.format(str(e)))
