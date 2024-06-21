import socket
import threading
import time
from datetime import datetime
import html
import ssl
import re
import tempfile
# Odbiorca == o
# Adresat == c
# Wiadomość == p
# Data == d

# 001 = name
# 002 = password
# 003 = access got
# 004 = access don't got

# 005 = new account
# 005.1 = new account name is already on the list(names) chose other
# 006 = Login

# 007 = Napisz wiadomość
# 007.1 = imię nie występuje
# 008 = Odczytaj wiadomość

# 009 = Wyloguj się


servercrt = """
server.crt from OpenSSL use Let's Encrypt to generate
"""

serverkey = """
server.key from OpenSSL use Let's Encrypt to generate
"""

cacrt = """
ca.crt from OpenSSL use Let's Encrypt to generate
"""


with tempfile.NamedTemporaryFile(delete=False) as server_crt_file:
    server_crt_file.write(servercrt.encode('utf-8'))
    server_crt_path = server_crt_file.name

with tempfile.NamedTemporaryFile(delete=False) as server_key_file:
    server_key_file.write(serverkey.encode('utf-8'))
    server_key_path = server_key_file.name

with tempfile.NamedTemporaryFile(delete=False) as ca_crt_file:
    ca_crt_file.write(cacrt.encode('utf-8'))
    ca_crt_path = ca_crt_file.name


context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile=server_crt_path, keyfile=server_key_path)
context.load_verify_locations(cafile=ca_crt_path)
context.verify_mode = ssl.CERT_REQUIRED



now = datetime.now()
time_raport = now.strftime("%Y-%m-%d %H:%M:%S")
print(f'[{time_raport}]Server: Starting...')
HOST = 'localhost'
PORT = 49152
transmision_type = 'utf8'
now = datetime.now()
time_raport = now.strftime("%Y-%m-%d %H:%M:%S")
print(f'[{time_raport}]Server: listening at {HOST}:{PORT}.')
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST,PORT))
server.listen()

def sanitized_input(user_input):
    sanitized1 = html.escape(user_input)
    sanitized2 = re.sub(r'[^\w\s]', '', sanitized1)
    return sanitized2

class Client:
    def __init__(self,Login):
        self.Login = Login
        self.current_name = None
        self.menu_decision = None
        self.messages = []
        self.names = []
        self.passwords = []

    def login(self):        
        if client_log.menu_decision == '006' and client_log.Login == False:
            while client_log.Login == False:
                name_user = conn_ssl.recv(1024).decode(transmision_type)
                name_user = sanitized_input(name_user)
                password_user = conn_ssl.recv(1024).decode(transmision_type)
                password_user = sanitized_input(password_user)

                if name_user == '' or password_user == '':
                    now = datetime.now()
                    time_raport = now.strftime("%Y-%m-%d %H:%M:%S")
                    print(f'[{time_raport}]Server: Error occurs {address[0]}:{address[1]} raise error.')
                if name_user in client_log.names and password_user in client_log.passwords:
                    i = client_log.names.index(name_user)
                    if name_user == client_log.names[i] and password_user == client_log.passwords[i]:
                        conn_ssl.send('003'.encode(transmision_type))
                        client_log.Login = True
                        client_log.current_name = name_user
                        now = datetime.now()
                        time_raport = now.strftime("%Y-%m-%d %H:%M:%S")
                        print(f'[{time_raport}]Server: {address[0]}:{address[1]} successfully login on {name_user}.')
                    else:
                        conn_ssl.send('004'.encode(transmision_type))
                        now = datetime.now()
                        time_raport = now.strftime("%Y-%m-%d %H:%M:%S")
                        print(f'[{time_raport}]Server: {address[0]}:{address[1]} tried to login, but unsuccessfully')
                else:
                    conn_ssl.send('004'.encode(transmision_type))
                    now = datetime.now()
                    time_raport = now.strftime("%Y-%m-%d %H:%M:%S")
                    print(f'[{time_raport}]Server: {address[0]}:{address[1]} tried to login, but unsuccessfully')
        
            
    

    def create_account(self):        
        if client_log.menu_decision == '005' and client_log.Login == False:
            new_name = conn_ssl.recv(1024).decode(transmision_type)
            new_name = sanitized_input(new_name)
            new_password = conn_ssl.recv(1024).decode(transmision_type)
            new_password = sanitized_input(new_password)
            if new_name == '' or new_password == '':
                now = datetime.now()
                time_raport = now.strftime("%Y-%m-%d %H:%M:%S")
                print(f'[{time_raport}]Server: Error occurs {address[0]}:{address[1]} raise error.')
                client_log.Login = False
                client_log.current_name = None
                client.close()
                conn_ssl.close()
            while new_name in client_log.names:
                conn_ssl.send('005.1'.encode(transmision_type))
                new_name = conn_ssl.recv(1024).decode(transmision_type)
                new_name = sanitized_input(new_name)
                if new_name == '':
                    now = datetime.now()
                    time_raport = now.strftime("%Y-%m-%d %H:%M:%S")
                    print(f'[{time_raport}]Server: Error occurs {address[0]}:{address[1]} raise error.')
                    client_log.Login = False
                    client_log.current_name = None
                    conn_ssl.close()
                    client.close()
                now = datetime.now()
                time_raport = now.strftime("%Y-%m-%d %H:%M:%S")
                print(f'[{time_raport}]Server: {address[0]}:{address[1]} tried to create an account, but unsuccessfully')
                if new_name not in client_log.names:
                    conn_ssl.send('005.2'.encode(transmision_type))
                    break
                
            conn_ssl.send('005.2'.encode(transmision_type))
            client_log.current_name = new_name
            client_log.Login = True

            f_names_a = open('names.txt', 'a')
            f_names_a.write(f'{new_name}\n')
            f_passwords_a = open('passwords.txt', 'a')
            f_passwords_a.write(f'{new_password}\n')
            f_names_a.close()
            f_passwords_a.close()
            client_log.names.append(new_name)
            client_log.passwords.append(new_password)
            client_log.current_name == new_name
            client_log.Login = True
            now = datetime.now()
            time_raport = now.strftime("%Y-%m-%d %H:%M:%S")
            print(f'[{time_raport}]Server: {address[0]}:{address[1]} created successfully an account with the name {new_name}.')
        


    def creating_mail(self):        
        if client_log.menu_decision == '007' and client_log.Login == True:
            o = conn_ssl.recv(1024).decode(transmision_type)
            o = sanitized_input(o)
            time.sleep(0.3)
            c = conn_ssl.recv(1024).decode(transmision_type)
            c = sanitized_input(c)
            time.sleep(0.3)
            p = conn_ssl.recv(1024).decode(transmision_type)
            p = sanitized_input(p)
            now = datetime.now()
            time_msg = now.strftime("%Y-%m-%d %H:%M:%S")

            if o == '' or c == '' or p == '':
                now = datetime.now()
                time_raport = now.strftime("%Y-%m-%d %H:%M:%S")
                print(f'[{time_raport}]Server: Error occurs {address[0]}:{address[1]} raise error.')
                client_log.Login = False
                client_log.current_name = None
                conn_ssl.close()
                client.close()

            while o not in client_log.names:
                conn_ssl.send('007.1'.encode(transmision_type))
                o = conn_ssl.recv(1024).decode(transmision_type)
                o = sanitized_input(o)
                time.sleep(0.3)
                c = conn_ssl.recv(1024).decode(transmision_type)
                c = sanitized_input(c)
                time.sleep(0.3)
                p = conn_ssl.recv(1024).decode(transmision_type)
                p = sanitized_input(p)
                now = datetime.now()
                time_msg = now.strftime("%Y-%m-%d %H:%M:%S")
                if o == '' or c == '' or p == '':
                    now = datetime.now()
                    time_raport = now.strftime("%Y-%m-%d %H:%M:%S")
                    print(f'[{time_raport}]Server: Error occurs {address[0]}:{address[1]} raise error.')
                    client_log.Login = False
                    client_log.current_name = None
                    conn_ssl.close()
                    client.close()

                if o in client_log.names:
                    conn_ssl.send('007.2'.encode(transmision_type))
                    break
            else:
                conn_ssl.send('007.2'.encode(transmision_type))


            f_messages_a = open('messages.txt', 'a')
            f_messages_a.write(f'{o}o\n{c}c\n{p}p\n{time_msg}d\n')
            f_messages_a.close()
            now = datetime.now()
            time_raport = now.strftime("%Y-%m-%d %H:%M:%S")
            print(f'[{time_raport}]Server: {address[0]}:{address[1]} from {client_log.current_name} created an e-mail.')
        
            

            
    def reading_mail(self):        
        if client_log.menu_decision == '008' and client_log.Login == True:
            words = ''
            counter = 0
            pocket3 = []
            for char in client_log.messages:
                pocket2 = char

                if pocket2[1] == client_log.current_name:
                    pocket3.append(pocket2)
                    pocket2 = []
                            
                            
            for char in pocket3:
                for char1 in char:
                    if counter == 4:
                        words += '\n'
                        words += '\n'
                        counter = 0
                    
                    if counter == 3:
                        words += '\n'
                        words += '\n'
                        words += 'Time: ' + char1
                        counter += 1
                    
                    if counter == 2:
                        words += '\n'
                        words += '\n'
                        words += 'Message: ' + char1
                        counter += 1

                    if counter == 1:
                        words += '\n'
                        words += '\n'
                        words += 'Sender: ' + char1
                        counter += 1

                    if counter == 0:
                        words += '================'
                        words += '\n'
                        words += '\n'
                        words += "Recipient's: " + char1
                        counter += 1
                    

            if words == '':
                words = 'Nobody sent you an e-mail'
            conn_ssl.send(words.encode(transmision_type))
            now = datetime.now()
            time_raport = now.strftime("%Y-%m-%d %H:%M:%S")
            print(f'[{time_raport}]Server: {address[0]}:{address[1]} from {client_log.current_name} read e-mails.')
        


    def Logout(self):
        if client_log.menu_decision == '009' and client_log.Login == True:
            now = datetime.now()
            time_raport = now.strftime("%Y-%m-%d %H:%M:%S")
            print(f'[{time_raport}]Server: {address[0]}:{address[1]} logout from {client_log.current_name}.')
            client_log.Login = False
            client_log.current_name = None
        
              
    
        
    def menu(self):
        while True:
            client_log.synchronization()
            try:
                m_d = conn_ssl.recv(1024).decode(transmision_type)
                client_log.menu_decision = sanitized_input(m_d)
            except Exception as e:
                client_log.Login = False
                client_log.current_name = None
                conn_ssl.close()
                client.close()
                now = datetime.now()
                time_raport = now.strftime("%Y-%m-%d %H:%M:%S")
                print(f'[{time_raport}]Server: Lost connection with {address[0]}:{address[1]}.')
                print(f'{e}')
                break
            if client_log.menu_decision == '':
                client_log.Login = False
                client_log.current_name = None
                conn_ssl.close()
                client.close()
                now = datetime.now()
                time_raport = now.strftime("%Y-%m-%d %H:%M:%S")
                print(f'[{time_raport}]Server: Lost connection with {address[0]}:{address[1]}.')
                break
            client_log.login()
            client_log.create_account()
            client_log.creating_mail()
            client_log.Logout()
            client_log.reading_mail()
        
            
    
    def synchronization(self):   
        list_m_from_file = []
        addressee = ''
        recipient = ''
        message = ''
        time_msg = ''
        pocket = []
        client_log.names.clear()
        client_log.passwords.clear()
        client_log.messages.clear()
        f_names_r = open('names.txt', 'r')
        f_passwords_r = open('passwords.txt', 'r')
        f_messages_r = open('messages.txt', 'r')
        
        read_f_messages = f_messages_r.readlines()

        for line in read_f_messages:
            list_m_from_file.append(line.strip())

        for char in list_m_from_file:

            if char[-1] == 'o':
                recipient = (char[:-1])

            if char[-1] == 'c':
                addressee = (char[:-1])

            if char[-1] == 'p':
                message = (char[:-1])
            
            if char[-1] == 'd':
                time_msg = (char[:-1])


            if addressee != '' and recipient != '' and message != '' and time_msg != '':
                pocket.append(recipient)
                pocket.append(addressee)
                pocket.append(message)
                pocket.append(time_msg)
                client_log.messages.append(pocket)
                pocket = []
                
                recipient = ''
                addressee = ''
                message = ''
                time_msg = ''

        f_messages_r.close()


        read_f_names = f_names_r.readlines()
        for line in read_f_names:
            client_log.names.append(line.strip())
        f_names_r.close()

        read_f_passwords = f_passwords_r.readlines()
        for line in read_f_passwords:
            client_log.passwords.append(line.strip())

        f_passwords_r.close()
            

while True:
    client, address = server.accept()
    conn_ssl = context.wrap_socket(client, server_side=True)
    now = datetime.now()
    time_raport = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f'[{time_raport}]Server: Connected with {address[0]}:{address[1]}.')
    client_log = Client(False)
    try:
        thread = threading.Thread(target=Client.menu(self = client_log),args=(conn_ssl,client_log))
        thread.start()
    except Exception as e:
        client_log.Login = False
        client_log.current_name = None
        conn_ssl.close()
        client.close()
        now = datetime.now()
        time_raport = now.strftime("%Y-%m-%d %H:%M:%S")
        print(f'[{time_raport}]Server: Lost connection with {address[0]}:{address[1]}.')
        print(f'{e}')