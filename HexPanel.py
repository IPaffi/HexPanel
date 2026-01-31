import os
import socket
import threading
import time
import sys
from colorama import init, Fore, Style
init(autoreset=True)
stop_server = False
tt = '00:00:00'
s = 0
send_options = ["1", "2", "3", "0"]
menu_options = ["1", "2", "0", "00", "55"]
ip_status = {"ip": "not set", "reachable": False, "last_check": 0}
CURRENT_VERSION = "3.0-beta.1"
def time_tracker():
    global s, tt
    while True:
        time.sleep(1)
        s += 1
        h = s // 3600
        m = (s % 3600) // 60
        sec = s % 60
        tt = f'{h:02}:{m:02}:{sec:02}'

threading.Thread(target=time_tracker, daemon=True).start()
def current(porti):
    ip = ip_status.get("ip", "not set")
    reachable = ip_status.get("reachable", False)
    last_check = ip_status.get("last_check", 0)
    elapsed = int(time.time() - last_check)
    if elapsed < 60:
        time_str = f"{elapsed} sec ago"
    elif elapsed < 3600:
        time_str = f"{elapsed // 60} min ago"
    elif elapsed < 86400:
        time_str = f"{elapsed // 3600} h ago"
    else:
        time_str = f"{elapsed // 86400} d ago"
    if ip == "not set":
        ip_color = Fore.YELLOW
        status = "not set"
    else:
        ip_color = Fore.GREEN if reachable else Fore.RED
        status = "online" if reachable else "offline"
    print(f'{Style.RESET_ALL}   Current IP: {ip_color}{ip}:{porti}{Style.RESET_ALL} [{status}] (checked {time_str})')
def check_ip(ip: str):
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(p) <= 255 for p in parts)
    except:
        return False

def is_ip_reachable(ip: str, port=2222, timeout=2):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((ip, port))
        sock.close()
        return True
    except:
        return False

def start_ip_monitor(ip: str):
    def monitor():
        while True:
            if check_ip(ip):
                ip_status.update({
                    "reachable": is_ip_reachable(ip),
                    "ip": ip,
                    "last_check": time.time()
                })
            time.sleep(15)
    t = threading.Thread(target=monitor, daemon=True)
    t.start()

def banner():
    os.system('cls||clear')
    print(f"""{Fore.CYAN}                       Build v3.0 - Beta 1
                HH   █H  E████EE  █   █X
                ██   ██  ██       X█ ██
                ███H███  ██E█      XXX
                ██   ██  ██       ██ █X
                H█    H  E███ E  X█   ██
               your eternal Creat Hex Team  
       P███P█   A█████   ██N    █N  E███EE  █ 
       ██   ██  ██   █A  ████   ██  ██      ██
       █ ███P   ███A███  ██ █   ██  ██ █    ██
       ██       ██   ██  ██   █ ██  ██      ██
       P█       █A   ██  █N   █N██  E█mIZa  L████L""")

def hello():
    banner()
    print("> Enter server IP")
    while True:
        ip = input(">> ")
        if check_ip(ip):
            ip_status["ip"] = ip
            start_ip_monitor(ip)
            banner()
            print("> IP correct!")
            break
        else:
            banner()
            print("> Invalid IP, try again")
    while True:
        banner()
        porti = input("> Enter port\n> Default = 2222\n>> ")
        if porti.isdigit() and len(porti) == 4 or 5:
            banner()
            print(f" You write: {porti}")
            time.sleep(1)
            break
        banner()
        print(" Error, the entered number consists of more than 4 digits.")
        time.sleep(2)
    banner()
    name = input(" Enter your name\n>> ")
    banner()
    dywtc = input(" Do you wish to enter the token now?\n [1] Yes\n [2] Maybe later\n>> ")
    if dywtc == "1":
        banner()
        tc = input("Enter token\n>> ")
        with open("config.py", "w") as f:
            f.write(f'ip = "{ip}"\ntc = "{tc}"\nname = "{name}"\nporti = "{porti}"')
        banner()
    else:
        with open("config.py", "w") as f:
            f.write(f'ip = "{ip}"\ntc = "none"\nname = "{name}"\nporti = "{porti}"')
        banner()
        print("Token not set")
    print("> Saved all input data...")
    time.sleep(3)
    menu(name)

def tryingip(ip, porti):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, porti))
    except:
        banner()
        again = input('> !!! Failed to connect to server !!!\n> Try again? \n\n [1] Yes \n [2] No \n >> ')
        if again == "1":
            try:
                banner()
                print("> Trying to reconnect...")
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ip, porti))
            except:
                banner()
                print("> Failed to connect to server \n Exit to main menu...")
                time.sleep(1)
                menu(name)
        if again == "2":
            banner()
            print("> Exit to main menu...")
            time.sleep(0.7)
            menu(name)

def send_hex(ip, tc, hex_data, porti):
    banner()
    choiceH = input(" [1] Custom spam \n [2] Drop 1 packet \n [3] Spam packets \n\n [0] Exit to menu\n >> ")
    while choiceH not in send_options:
        banner()
        choiceH = input(" [1] Custom spam \n [2] Drop 1 packet \n [3] Spam packets \n\n [0] Exit to menu\n Enter exact number >> ")

    if choiceH == "0":
        time.sleep(0.3)
        menu(name)

    if choiceH == "0":
        menu(name)

    if choiceH == "1":
        num_per_token = int(input("Number of packets per token >> "))
        total_packets = int(input("Total number of sending packets >> "))
        for i in range(total_packets):
            try:
                sock.send(bytes.fromhex(tc))
                for _ in range(num_per_token):
                    sock.send(bytes.fromhex(hex_data))
                print(f"{i+1} packets sent | {tt}")
            except:
                sock.close()
                sock.connect((ip, porti))
        banner()
        print("> Spam finished")
        time.sleep(1)
        menu(name)

    if choiceH == "2":
        sock.send(bytes.fromhex(tc))
        sock.send(bytes.fromhex(hex_data))
        banner()
        print("> Packet sent")
        time.sleep(1)
        menu(name)

    if choiceH == "3":
        i = 0
        while True:
            try:
                i += 1
                sock.send(bytes.fromhex(tc))
                sock.send(bytes.fromhex(hex_data))
                print(f"{i} packets sent | {tt}")
            except:
                sock.close()
                sock.connect((ip, porti))
                menu(name)

def handle_client(client_socket, addr):
    print(f'Client connected: {addr}')
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f'Received from {addr}: {data.decode()}')
            client_socket.sendall(f"Echo: {data.decode()}".encode())
    except:
        pass
    finally:
        client_socket.close()
        print(f'Client {addr} disconnected')

def server():
    global stop_server

    def command_input():
        global stop_server
        while True:
            cmd = input("Enter 'stop' for back to main menu: ")
            if cmd.strip().lower() == 'stop':
                stop_server = True
                break

    host_input = input("Enter host (Default 0.0.0.0): ").strip()
    HOST = host_input if host_input else '0.0.0.0'
    port_input = input("Enter port (Default 12345): ").strip()
    try:
        PORT = int(port_input) if port_input else 12345
    except ValueError:
        PORT = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f'The server is running and listening. {HOST}:{PORT}')
        threading.Thread(target=command_input, daemon=True).start()
        while not stop_server:
            try:
                s.settimeout(1.0)
                client_sock, addr = s.accept()
                threading.Thread(target=handle_client, args=(client_sock, addr), daemon=True).start()
            except socket.timeout:
                continue
        print("Stopping server...")
        time.sleep(3)
        menu(name)

def menu(name):
    global tc
    try:
        from config import ip, tc, name, porti
    except:
        hello()
        return
    from config import ip, tc, name, porti
    banner()
    current(porti)
    print(f'                Welcome to Panel, {name}!')
    print("             >Created by t.me/CreatHexPanel<")
    choice = input("\n[1] Custom hex \n[2] Eavesdrop server\n\n[0] Edit IP \n[00] Edit token \n[55] Exit\n >> ")
    while choice not in menu_options:
        banner()
        current(porti)
        print(f"                Welcome to Panel, {name}!\n             >Created by t.me/CreatHexPanel<\n >Please enter the correct command")
        choice = input("\n[1] Custom hex \n[2] Eavesdrop server\n\n[0] Edit IP \n[00] Edit token \n[55] Exit\n >> ")

    if choice == "55":
        banner()
        sys.exit("            Thank you for choosing HexPanel!")
        sys.exit(0)

    if choice == "0":
        banner()
        ip_new = input("Enter new IP >> ")
        while not check_ip(ip_new):
            banner()
            ip_new = input("Invalid IP, enter again >> ")
        ip_status["ip"] = ip_new
        start_ip_monitor(ip_new)
        banner()
        print("> Enter port")
        print("> Default = 2222")
        while True:
            banner()
            print("> Enter port")
            print("> Default = 2222")
            porti = input(">> ")
            if porti.isdigit() and len(porti) == 4 or 5:
                banner()
                print(f" You write: {porti}")
                time.sleep(1)
                break
            banner()
            print(" Error, the entered number consists of more than 4 digits.")
            time.sleep(2)
        with open("config.py", "w") as f:
            f.write(f'ip = "{ip_new}"\ntc = "none"\nname = "{name}"\nporti = "{porti}"')
        banner()
        print(f"> New IP set: {ip_new}:{porti}")
        time.sleep(3)
        menu(name)

    if choice == "00":
        banner()
        tc_new = input("Enter new token >> ").strip()
        while not tc_new:
            banner()
            tc_new = input("Token cannot be empty >> ")
        tc = tc_new
        with open("config.py", "w") as f:
            f.write(f'ip = "{ip}"\ntc = "none"\nname = "{name}"\nporti = "{porti}"')
        banner()
        sys.exit(" Please reboot HexPanel!")
        sys.exit(0)

    if choice == "1":
        from config import ip, tc, name, porti
        from config import tc
        if tc == "none":
            banner()
            print("> Token not set, returning to menu...")
            time.sleep(1)
            menu(name)
        else:
            banner()
            hex_data = input(" Enter hex >> ").strip()
            send_hex(ip_status["ip"], tc, hex_data)
            menu(name)
    if choice == "2":
        if __name__ == "__main__":
            server()
        menu(name)
try:
    from config import ip, tc, name, porti
    ip_status["ip"] = ip
    start_ip_monitor(ip)
    menu(name)
except SystemExit:
        raise
except Exception as e:
        hello()
