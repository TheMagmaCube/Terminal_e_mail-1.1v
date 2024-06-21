import socket
import time
import os
import ssl
import tempfile
# 001 = name
# 002 = password
# 003 = access got
# 004 = access don't got

# 005 = new account
# 005.1 = new account name is already in list(names) on the server
# 006 = Login

# 007 = Napisz wiadomość
# 007.1 = imię nie wystepuje
# 007.2 = imię występuje
# 008 = Odczytaj wiadomość

# 009 = Wyloguj się

cacrt = """
ca.crt from OpenSSL(same as on the server ca.crt) use Let's Encrypt to generate
"""


with tempfile.NamedTemporaryFile(delete=False) as ca_crt_file:
    ca_crt_file.write(cacrt.encode('utf-8'))
    ca_crt_path = ca_crt_file.name

HOST = 'localhost'
PORT = 49152
transmision_type = 'utf8'


context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.load_verify_locations(cafile=ca_crt_path)
context.verify_mode = ssl.CERT_REQUIRED



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


conn_sll = context.wrap_socket(client, server_hostname=HOST)


def clear_lines():
    os.system('cls' if os.name == 'nt' else 'clear')



try:
    print('Connecting...')
    conn_sll.connect((HOST,PORT))
    print(f'Successfully connected with the server.')
    time.sleep(1)
    clear_lines()
except:
    print(f'Connection with sever it is impossible\nCheck your network and PING\nYour current version is 1.0, maby the server has been changed to a newer version.')
    time.sleep(4)
    exit()


class User:
    def __init__(self, Login):
        self.Login = Login
        self.current_name = None
        self.menu_decision = None



    def login(user):
        if user.menu_decision == 'LI' and user.Login == False:
            choice = '006'
            conn_sll.send(choice.encode(transmision_type))
            while user.Login == False:
                clear_lines()
                name = str(input('Username: '))
                password = str(input('Password: '))
                conn_sll.send(name.encode(transmision_type))
                conn_sll.send(password.encode(transmision_type))
    
                feedback = conn_sll.recv(1024).decode(transmision_type)

                if feedback == '003':
                    user.Login = True
                    print('Access granted')
                    time.sleep(0.5)
                    user.current_name = name
                    clear_lines()
                    break
                if feedback == '004':
                    user.Login = False
                    print('Access denied')
                    time.sleep(0.5)


    def create_account(user):
        if user.menu_decision == 'CA' and user.Login == True:
            clear_lines()
            print('If you want create new account you must Logout.')
            time.sleep(1.5)
        if user.menu_decision == 'CA' and user.Login == False:
            choice = '005'
            conn_sll.send(choice.encode(transmision_type))
            clear_lines()
            name = str(input('New username: '))
            password = str(input('New password: '))
            password_2 = str(input('Please enter your password again: '))
            time.sleep(0.5)
            while password != password_2:
                clear_lines()
                print('The passwords do not match')
                password = str(input('New password: '))
                password_2 = str(input('Please enter your password again: '))
                time.sleep(0.5)
                if password == password_2:
                    break
            else:
                conn_sll.send(name.encode(transmision_type))
                conn_sll.send(password.encode(transmision_type))
            name_req = client.recv(1024).decode(transmision_type)
            while name_req == '005.1':
                clear_lines()
                name = str(input('Your username is already use please enter New username: '))
                conn_sll.send(name.encode(transmision_type))
                time.sleep(0.5)
                name_req = conn_sll.recv(1024).decode(transmision_type)
                if name_req == '005.2':
                    clear_lines()
                    user.Login = True
                    user.current_name = name
                    print('Successfully created account.')
                    print(f'Login on {name}')
                    time.sleep(0.5)
                    clear_lines()
                    break
            else:
                clear_lines()
                print('Successfully created account.')
                print(f'Login on {name}')
                time.sleep(0.5)
                clear_lines()
                user.Login = True
                user.current_name = name


    def reading_mail(user):
        if user.menu_decision == 'RM' and user.Login == True:
            choice = '008'
            conn_sll.send(choice.encode(transmision_type))
            clear_lines()
            list_of_messages = conn_sll.recv(1024).decode(transmision_type)
            print(list_of_messages)

    def writing_mail(user):
        if user.menu_decision == 'WM' and user.Login == True:
            choice = '007'
            conn_sll.send(choice.encode(transmision_type))
            clear_lines()
            o = str(input("Recipient's name: "))
            print(f'Sender: {user.current_name} ')
            c = user.current_name
            p = str(input('Write one-line message: '))

            conn_sll.send(o.encode(transmision_type))
            time.sleep(0.3)
            conn_sll.send(c.encode(transmision_type))
            time.sleep(0.3)
            conn_sll.send(p.encode(transmision_type))
            clear_lines()
            name_occurs = conn_sll.recv(1024).decode(transmision_type)
            while name_occurs == '007.1':
                print("This Recipient's name no occurs")
                time.sleep(0.5)
                clear_lines()
                o = str(input("Recipient's name: "))
                print(f'Sender: {user.current_name} ')
                c = user.current_name
                p = str(input('Write one-line message: '))
                conn_sll.send(o.encode(transmision_type))
                time.sleep(0.3)
                conn_sll.send(c.encode(transmision_type))
                time.sleep(0.3)
                conn_sll.send(p.encode(transmision_type))

                name_occurs = conn_sll.recv(1024).decode(transmision_type)
                
                if name_occurs == '007.2':
                    clear_lines()
                    print('Created e-mail successfully.')
                    time.sleep(0.5)
                    clear_lines()
                    break
            conn_sll.send(o.encode(transmision_type))
            time.sleep(0.3)
            conn_sll.send(c.encode(transmision_type))
            time.sleep(0.3)
            conn_sll.send(p.encode(transmision_type))
            clear_lines()
            print('Created e-mail successfully.')
            time.sleep(0.5)
            clear_lines()

    def logout(user):
        if user.menu_decision == 'LO' and user.Login == True:
            choice = '009'
            conn_sll.send(choice.encode(transmision_type))
            user.Login = False
            user.current_name = None
            clear_lines()
            print('Sucessfuly logout')
            time.sleep(0.5)
            clear_lines()


    def menu():
        user = User(False)
        user.menu_decision = None
        while True and user.Login == False:
            time.sleep(0.5)
            user.menu_decision = input(str('======Menu======\nLog in => "LI"\nCreate account => "CA"\n======Menu======: '))
            time.sleep(0.5)
            clear_lines()
            user.login()
            user.create_account()
        
        while True and user.Login == True:
            time.sleep(0.5)
            user.menu_decision = input(str('======Menu======\nWrite an e-mail => "WM"\nRead the e-mail => "RM"\nLogout => "LO"\n======Menu======: '))
            time.sleep(0.5)
            clear_lines()
            user.writing_mail()
            user.reading_mail()
            user.logout()


user = User

while True:
    user.menu()