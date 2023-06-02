import os, socket, threading, time, sys
from func import tt, s
def banner():
    os.system('cls||clear')
    print("""                  Build v2.38T0 & SUIUS
                HH   █H  E████EE  █   █X
                ██   ██  ██       X█ ██
                ███H███  ██E█      XXX
                ██   ██  ██       ██ █X
                H█   HH  E███EE  X█   ██
               your eternal Creat Hex Team  
       P███P█   A█████   ██N    █N  E███EE  █L
       ██   ██  ██   █A  ████   ██  ██      ██
       █P███P   ███A███  ██ █   ██  ██E█    ██
       ██       ██   ██  ██   █ ██  ██      ██
       P█       █A   ██  █N   █N██  E███EE  L████L
       """)

def times():
    global s
    global tt
    while 1:
        time.sleep(1)
        s += 1
        h = s // 60 // 60
        mm = s // 60 - h*0
        ss = s - h*60*60 - mm*60
        tt = (f'{h:02}:{mm:02}:{ss:02}')   

def sendhex(ip, tc, hex):
    banner()
    print("                 >Set method dupe<")
    send = input(" [1] Custom spam \n [2] Drop 1 packet \n [3] Spam packet in server \n\n >[0] Exit to menu\n >> ")
    while send not in send:
        banner()
        print("                 >Set method dupe<")
        print("            >Enter the exact number<")
        send = input(" [1] Custom spam \n [2] Drop 1 packet \n [3] Spam packet in server \n\n >[0] Exit to menu\n >> ")
    
    if send == "1":
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, 2222))
        except:
            banner()
            sys.exit(' Failed connect to game sevrer! \n Please change ip and try again')
        time.sleep(0.5)
        i = 0
        banner()
        b = int(input(" Number of hexes per token >> "))
        a = int(input(" The number of sending dupes >> "))
        time.sleep(0.4)
        for i in range(a):
            try:
                sock.send(bytes.fromhex(tc))
                for j in range(b):
                    sock.send(bytes.fromhex(hex))
                    i += 1
                    time.sleep(0.2)
                    print(f' {i} - Packets |  {tt}  |  [ CTRL + Z - Crash ]')
            except:
                sock.connect((ip, 2222))
        banner()
        print("Сделай чтоб в менюшку вышло")
        time.sleep(5)
        menu(name)

    if send == "2":
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, 2222))
        except:
            banner()
            sys.exit(' Failed connect to game sevrer! \n Please change ip and try again')
        x = threading.Thread(target=times, daemon=True)
        x.start()
        sock.send(bytes.fromhex(tc))
        sock.send(bytes.fromhex(hex))
        sock.send(bytes.fromhex(tc))
        sock.send(bytes.fromhex(hex))
        sock.send(bytes.fromhex(tc))
        sock.send(bytes.fromhex(hex))
        banner()
        print("                Dupe Used!")
        time.sleep(0.5)
        menu(name)

    if send == "3":
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, 2222))
        except:
            banner()
            sys.exit(' Failed connect to game sevrer! \n Please change ip and try again')
        x = threading.Thread(target=times, daemon=True)
        time.sleep(0.5)
        i = 0
        x.start()
        while 1:
            try:
                i += 1
                time.sleep(0.2)
                sock.send(bytes.fromhex(tc))
                for _ in range(2):
                   sock.send(bytes.fromhex(hex))
                banner("""         Dupe used! [ CTRL + Z - Crash ]""")
                print("")
                print(f' {i} - Packets |  {tt}  |  [ CTRL + Z - Crash ]')
            except:
                sock.connect((ip, 2222))
                menu(name)

    if send == "0":
        menu(name)

def menu(name):
    from func import mq
    global s, ip, tc
    banner()
    print(f'                Welcome to Panel, {name}!')
    time.sleep(0.7)
    banner()
    print("               >Created by t.me/HexPanel<")
    print(" [1] Сustom hex \n\n>[0] Edit ip \n>[00] Edit token \n>>[55 = exit, CTRL + Z = Crash]")
    choice = input(" >> ")
    while choice not in mq:
        print(" You're a fucking scumbag, are you even sighted?")
        time.sleep(0.5)
        banner()
        print("               >Created by t.me/HexPanel<")
        print(" [1] Сustom hex \n\n>[0] Edit ip \n>[00] Edit token \n>>[55 = exit, CTRL + Z = Crash]")
        choice = input(" >> ")

    if choice == "0":
        banner()
        print("                  >Set new config<")
        print(f'               Config ip - {ip}')
        from config import ip, tc, name
        ip = input(" Enter new ip >> ")
        while ip == "" or ip == " ":
            ip = "18.157.144.214"
        with open('config.py', 'w') as f:pass
        with open('config.py', 'w') as f:
            f.write(f'ip = "{ip}"\ntc = "{tc}"\nname = "{name}"')
            f.close()
        from config import ip, tc, name
        menu(name)

    if choice == "00":
        banner()
        print("                   >Set new cfg<")
        from config import ip, tc, name
        tc = input(" Enter new token >> ")
        while tc == "" or tc == " ":
            banner()
            print("             >change your game<")
            print("     >Don't enter a space, it doesn't work here<")
            tc = input(" Enter token >> ")
        with open('config.py', 'w') as f:pass
        with open('config.py', 'w') as f:
            f.write(f'ip = "{ip}"\ntc = "{tc}"\nname = "{name}"')
            f.close()
        from config import ip, tc, name
        menu(name)

    if choice == "55":
        banner()
        sys.exit(f"            Thank you for choosing HexPanel!")

    if choice == "1":
        banner()
        hex = input(" Enter hex >> ")        
        sendhex(ip, tc, hex)

try:
    time.sleep(0.7)
    from config import ip, tc, name
except:
    banner()
    ip = input(" Enter ip >> ")
    while ip == "" or ip == " ":
        print("         SETTING DEFAULT IP (MAYBE NO WORK!)")
        ipallow = input(" >Press 1 to apply >> ")
        if ipallow == "1":
            banner()
            ip = "18.157.144.214"
            print("                Set default ip setting")
        else:
            ip = input(" Enter ip >> ")
    tc = input(" Enter token >> ")
    while tc == "" or tc == " ":
        banner()
        print("             >Set server to connect<")
        print("     >Don't enter a space, it doesn't work here<")
        tc = input(" Enter token >> ")
    name = input(" Enter you NickName >> ")
    time.sleep(0.7)
    with open('config.py', 'w') as f:
        f.write(f'ip = "{ip}"\ntc = "{tc}"\nname = "{name}"')
        banner()
        print("              >Save server to connect..<")
        print("      It is a process to write down your data.")
        time.sleep(0.2)
        os.system('cls||clear')
        f.close()
        banner()
        print("                 Write successful!")
    time.sleep(1.2)
menu(name)