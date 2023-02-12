import os, socket, threading, time, sys
from func import tt, s
def banner():
    os.system('cls||clear')
    print("""
       ██╗  ██╗███████╗██╗  ██╗                  
       ██║  ██║██╔════╝╚██╗██╔╝                  
       ███████║█████╗   ╚███╔╝                   
       ██╔══██║██╔══╝   ██╔██╗                   
       ██║  ██║███████╗██╔╝ ██╗                  
       ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝                  
     created by Creat Hex & Hex Panel  
██████╗  █████╗ ███╗   ██╗███████╗██╗     
██╔══██╗██╔══██╗████╗  ██║██╔════╝██║     
██████╔╝███████║██╔██╗ ██║█████╗  ██║     
██╔═══╝ ██╔══██║██║╚██╗██║██╔══╝  ██║     
██║      ██║  ██║██║ ╚████║███████╗███████╗
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝""")
def times():
    global s
    global tt
    while 1:
        time.sleep(1)
        s += 0,99
        h = s // 60 // 60
        mm = s // 60 - h*0
        ss = s - h*60*60 - mm*60
        tt = (f'{h:02}:{mm:02}:{ss:02}')   
def sendhex(ip, tc, hex):
    from func import send
    banner()
    print("                 >Set method dup<")
    send = input(" [1] Drop 1 packet \n [2] Spam packet in server \n [0] Exit to menu\n >> ")
    while send not in send:
        banner()
        print("                 >Set method dup<")
        print("            >Enter the exact number<")
        send = input(" >Set method dup \n [1] Drop 1 packet \n [2] Spam packet in server \n [0] Exit to menu\n >> ")
    if send == "0":
        menu(name)
    if send == "1":
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, 2222))
        except:
            banner()
            sys.exit(' Failed connect to gm sevrer! \n Please changing ip and try again')
        x = threading.Thread(target=times, daemon=True)
        x.start()
        sock.send(bytes.fromhex(tc))
        sock.send(bytes.fromhex(hex))
        sock.send(bytes.fromhex(hex))
        sock.send(bytes.fromhex(tc))
        sock.send(bytes.fromhex(hex))
        sock.send(bytes.fromhex(hex))
        sock.send(bytes.fromhex(hex))
        banner()
        print("                Dup Used!")
        time.sleep(0.5)
        menu(name)
    if send == "2":
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, 2222))
        except:
            banner()
            sys.exit(' Failed connect to gm sevrer! \n Please changing ip and try again')
        x = threading.Thread(target=times, daemon=True)
        banner()
        print("         Dup used! [ CTRL + Z - Crach ]")
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
                print(f' {i} - Packets |  {tt}  |  [ CTRL + Z - Crach ]')
            except:
                sock.connect((ip, 2222))
def menu(name):
    from func import mn
    global s, ip, tc
    banner()
    print(f'                Welcome to Panel, {name}!')
    time.sleep(0.7)
    banner()
    print("               >Created by t.me/HexPanel<")
    print(" [1] Сustom hex \n\n>[0] Edit ip \n>[00] Edit token \n>>[55 = exit, CTRL + Z = Crach]")
    choice = input(" >> ")
    while choice not in mn:
        print(" You're a fucking scumbag, are you even sighted?")
        time.sleep(0.5)
        banner()
        print("               >Created by t.me/HexPanel<")
        print(" [1] Сustom hex \n\n>[0] Edit ip \n>[00] Edit token \n>[000] Changing gm \n>>[55 = exit, CTRL + Z = Crach]")
        choice = input(" >> ")

    if choice == "0":
        banner()
        print("                  >Set new cfg<")
        print(f'             Config ip - {ip}')
        ip = input(" Enter new ip >> ")
        while ip == "0":
            menu(name)
        while ip == "" or ip == " ":
            banner()
            print("                  >Set new cfg<")
            print(f'             Config ip - {ip}')
            print("     >Don't enter a space, it doesn't work here<")
            ip = input(" Enter new ip >> ")
        with open('config.py', 'w') as f:pass
        with open('config.py', 'w') as f:
            f.write(f'ip = "{ip}"')
            f.close()
        from config import ip, tc, name
        menu(name)

    if choice == "00":
        banner()
        print("                   >Set new cfg<")
        tc = input(" Enter new token >> ")
        while tc == "" or tc == " ":
            banner()
            print("             >Changing your game<")
            print("     >Don't enter a space, it doesn't work here<")
            tc = input(" Enter token >> ")
        with open('config.py', 'w') as f:pass
        with open('config.py', 'w') as f:
            f.write(f'tc = "{tc}"')
            f.close()
        from config import ip, tc, name
        menu(name)

    if choice == "55":
        banner()
        sys.exit(f"            Thank you for choosing HexPanel!")

    if choice == "1":
        banner()
        print(">Only your account is responsible for other people's hexes<")
        hex = input(" Enter hex >> ")        
        sendhex(ip, tc, hex)
try:
    from config import ip, tc, name
except:
    print("             >Set server to connect<")
    tc = input(" Enter token >> ")
    while tc == "" or tc == " ":
        banner()
        print("             >Set server to connect<")
        print("     >Don't enter a space, it doesn't work here<")
        tc = input(" Enter token >> ")
    name = input(" Enter you NickName >> ")
    time.sleep(0.7)
    ip = input(" Enter ip >> ")
    while ip == "" or ip == " ":
        banner()
        print("             >Changing your game<")
        print("     >Don't enter a space, it doesn't work here<")
        ip = input(" Enter ip >> ")
    with open('config.py', 'w') as f:
        f.write(f'gm = "{gm}"\nip = "{ip}"\ntc = "{tc}"\nname = "{name}"')
        time.sleep(0.2)
        f.close()
    banner()
    print("              >Save server to connect..<")
    print("      There is a process to write down yout data.")
    time.sleep(1.2)
    from config import ip, tc, name
    sys.exit(" Restart Panel and use this")
menu(name)