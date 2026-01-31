import os, socket, threading, time, sys, re
from pathlib import Path
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from colorama import init, Fore, Style

init(autoreset=True)
stop_server = False
tt = '00:00:00'
s = 0
send_options = ["1", "2", "3", "0"]
menu_options = ["1", "2", "0", "00", "55", "99"]
CURRENT_VERSION = "3.0-alpha.2"
GH_RAW_URL = "https://raw.githubusercontent.com/IPaffi/HexPanel/refs/heads/main/HexPanel.py"
SCRIPT_FILE = Path(__file__).name
FULL_RAW_URL = GH_RAW_URL
ip_status = {
    "ip": "not set",
    "reachable": False,
    "last_check": 0
}

def parse_version(ver: str):
    ver = ver.lower().replace('v', '')
    pattern = r'(\d+)\.(\d+)\.?(\d*)(?:-(alpha|beta|rc|dev)\.?(\d*))?'
    match = re.match(pattern, ver)
    if match:
        major = int(match.group(1))
        minor = int(match.group(2))
        patch = int(match.group(3)) if match.group(3) else 0
        prerelease = match.group(4) if match.group(4) else ''
        prerelease_num = int(match.group(5)) if match.group(5) else 0
        prerelease_priority = {
            '': 4,
            'rc': 3,
            'beta': 2,
            'alpha': 1,
            'dev': 0
        }.get(prerelease, 0)
        return {
            'major': major,
            'minor': minor,
            'patch': patch,
            'prerelease': prerelease,
            'prerelease_num': prerelease_num,
            'prerelease_priority': prerelease_priority,
            'original': ver
        }
    return None

def infover():
    banner()
    ver_badge = display_version_badge(CURRENT_VERSION)
    print(f"\n{Fore.CYAN}╔════════════════════════════════════════╗")
    print(f"║        H E X P A N E L  I N F O        ║")
    print(f"╚════════════════════════════════════════╝{Style.RESET_ALL}")
    print(f"Type:       {get_version_type(CURRENT_VERSION)}")
    print(f"Version:    {Fore.CYAN}v{CURRENT_VERSION}{Style.RESET_ALL}")
    print(f"GitHub:     https://github.com/IPaffi/HexPanel")
    if get_version_type(CURRENT_VERSION) in ["Alpha", "Beta"]:
        print(f"\n{Fore.YELLOW}Note: This is a {get_version_type(CURRENT_VERSION)} version")
        print("Some features may be unstable or incomplete")
    chup = input(f'\nCheck for updates?\n [1] Yes \n [2] No, Back to menu \n >> ')
    if chup == "1":
        update_flow()
    else:
        return

def is_ip_reachable(ip: str, port=2222, timeout=2):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((ip, port))
        sock.close()
        return True
    except socket.timeout:
        return False
    except ConnectionRefusedError:
        return False
    except socket.gaierror:
        return False
    except Exception:
        return False

def start_ip_monitor(ip: str):
    def monitor():
        while True:
            ip_status.update({
                "reachable": is_ip_reachable(ip),
                "ip": ip,
                "last_check": time.time()
            })
            time.sleep(15)
    t = threading.Thread(target=monitor, daemon=True)
    t.start()

def compare_versions(ver1: str, ver2: str):
    v1 = parse_version(ver1)
    v2 = parse_version(ver2)
    if not v1 or not v2:
        return 0
    for field in ['major', 'minor', 'patch']:
        if v1[field] != v2[field]:
            return -1 if v1[field] < v2[field] else 1
    if v1['prerelease_priority'] != v2['prerelease_priority']:
        return -1 if v1['prerelease_priority'] < v2['prerelease_priority'] else 1
    if v1['prerelease'] and v2['prerelease'] and v1['prerelease'] == v2['prerelease']:
        if v1['prerelease_num'] != v2['prerelease_num']:
            return -1 if v1['prerelease_num'] < v2['prerelease_num'] else 1
    return 0

def get_version_type(ver: str):
    parsed = parse_version(ver)
    if not parsed:
        return "unknown"
    prerelease = parsed['prerelease']
    if not prerelease:
        return "stable"
    type_names = {
        'alpha': "Alpha",
        'beta': "Beta", 
        'rc': "Release Candidate",
        'dev': "Development"
    }
    return type_names.get(prerelease, prerelease.capitalize())

def get_version_color(ver: str):
    parsed = parse_version(ver)
    if not parsed:
        return Fore.WHITE
    prerelease = parsed['prerelease']
    if not prerelease:
        return Fore.GREEN
    elif prerelease == 'beta':
        return Fore.YELLOW
    elif prerelease == 'alpha':
        return Fore.RED
    elif prerelease == 'rc':
        return Fore.CYAN
    else:
        return Fore.MAGENTA

def display_version_badge(ver: str):
    ver_type = get_version_type(ver)
    badges = {
        "stable": f"{Fore.GREEN}[STABLE]{Style.RESET_ALL}",
        "Beta": f"{Fore.YELLOW}{Style.BRIGHT}[BETA]{Style.RESET_ALL}",
        "Alpha": f"{Fore.RED}{Style.BRIGHT}[ALPHA]{Style.RESET_ALL}",
        "Release Candidate": f"{Fore.CYAN}{Style.BRIGHT}[RC]{Style.RESET_ALL}",
        "Development": f"{Fore.MAGENTA}[DEV]{Style.RESET_ALL}"
    }
    
    return badges.get(ver_type, f"{Fore.WHITE}[{ver_type.upper()}]{Style.RESET_ALL}")

def show_version_warning():
    ver_type = get_version_type(CURRENT_VERSION)
    if ver_type == "Alpha":
        banner()
        print(f"{Fore.RED}{Style.BRIGHT}WARNING: You are using an ALPHA version!{Style.RESET_ALL}")
        print(f"{Fore.RED}• Critical errors may occur")
        print(f"• Functionality may be incomplete")
        print(f"• Not recommended for production use")
        time.sleep(2)
    elif ver_type == "Beta":
        banner()
        print(f"{Fore.YELLOW}{Style.BRIGHT}INFORMATION: You are using a BETA version{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}• Version is almost stable, but bugs may occur")
        print(f"• Functionality is complete but requires testing")
        time.sleep(2)

def check_updates(silent=False):
    try:
        if not silent:
            print(f"{Fore.YELLOW}[*] Checking for updates...{Style.RESET_ALL}")
        with urlopen(FULL_RAW_URL, timeout=5) as script_resp:
            new_code = script_resp.read().decode('utf-8')
        ver_pattern = r"CURRENT_VERSION\s*=\s*[\"']([\w\.\-]+)[\"']"
        match = re.search(ver_pattern, new_code)
        if match:
            remote_ver = match.group(1)
            remote_type = get_version_type(remote_ver)
            comparison = compare_versions(remote_ver, CURRENT_VERSION)
            if comparison > 0:
                if not silent:
                    ver_badge = display_version_badge(remote_ver)
                    print(f"{Fore.GREEN}[+] Update available!{Style.RESET_ALL}")
                return True, remote_ver, new_code.encode(), remote_type
            else:
                if not silent:
                    ver_badge = display_version_badge(CURRENT_VERSION)
                    print(f"{Fore.GREEN}[✓] You have the lasted version v{CURRENT_VERSION} its {ver_badge}{Style.RESET_ALL}")
                return False, None, None, None
        else:
            if not silent:
                print(f"{Fore.RED}[-] Unable to determine version in remote code{Style.RESET_ALL}")
            return False, None, None, None
            
    except HTTPError as e:
        if not silent:
            if e.code == 404:
                print(f"{Fore.RED}[-] Error checking for updates: File not found on GitHub{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-] Error checking for updates: HTTP Error {e.code}{Style.RESET_ALL}")
        return False, None, None, None
    except URLError as e:
        if not silent:
            print(f"{Fore.RED}[-] Error checking for updates: No internet connection{Style.RESET_ALL}")
        return False, None, None, None
    except Exception as e:
        if not silent:
            print(f"{Fore.RED}[-] Error checking for updates: {str(e)[:80]}{Style.RESET_ALL}")
        return False, None, None, None

def check_ip(ip: str):
    if not ip or not isinstance(ip, str):
        return False
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part:
            return False
        if not part.isdigit():
            return False
        try:
            num = int(part)
            if num < 0 or num > 255:
                return False
        except ValueError:
            return False
        if len(part) > 1 and part[0] == '0':
            return False
    return True

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    ver_badge = display_version_badge(CURRENT_VERSION)
    print(f"""{Fore.CYAN}               HexPanel {ver_badge} v{CURRENT_VERSION}{Fore.CYAN}
                HH   █H  E████EE  █   █X
                ██   ██  ██       X█ ██
                ███H███  ██E█      XXX
                ██   ██  ██       ██ █X
                H█    H  E███ E  X█   ██
                 your eternal 4Ivy Team 
       P███P█   A█████   ██N    █N  E███EE  █ 
       ██   ██  ██   █A  ████   ██  ██      ██
       █ ███P   ███A███  ██ █   ██  ██ █    ██
       ██       ██   ██  ██   █ ██  ██      ██
       P█       █A   ██  █N   █N██  E█mIZa  L████L{Style.RESET_ALL}""")

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
        myport = input("> Enter port\n> Default = 2222\n>> ")
        if not myport:
            myport = "2222"
            banner()
            print(f" Using default port: {myport}")
            time.sleep(1)
            break
        if myport.isdigit():
            try:
                port_num = int(myport)
                if 1 <= port_num <= 65535:
                    banner()
                    print(f" You write: {myport}")
                    time.sleep(1)
                    break
                else:
                    banner()
                    print(" Error: Port must be between 1 and 65535")
                    time.sleep(2)
            except:
                banner()
                print(" Error: Invalid port number")
                time.sleep(2)
        else:
            banner()
            print(" Error: Port must be a number")
            time.sleep(2)
    banner()
    name = input(" Enter your name\n>> ")
    banner()
    dywtc = input(" Do you wish to enter the token now?\n [1] Yes\n [2] Maybe later\n>> ")
    if dywtc == "1":
        banner()
        tc = input("Enter token\n>> ")
        with open("config.py", "w") as f:
            f.write(f'ip = "{ip}"\ntc = "{tc}"\nname = "{name}"\nmyport = "{myport}"')
        banner()
    else:
        with open("config.py", "w") as f:
            f.write(f'ip = "{ip}"\ntc = "none"\nname = "{name}"\nmyport = "{myport}"')
        banner()
        print("Token not set")
    print("> Saved all input data...")
    time.sleep(3)
    menu(name)

def current(myport):
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
    ver_badge = display_version_badge(CURRENT_VERSION)
    print(f'{Style.RESET_ALL}   Current IP: {ip_color}{ip}:{myport}{Style.RESET_ALL} [{status}] (checked {time_str})')
    print(f'{Style.RESET_ALL}   Version: {ver_badge} {Fore.CYAN}v{CURRENT_VERSION}{Style.RESET_ALL}')

def apply_update(new_code):
    try:
        current_path = Path(__file__).resolve()
        backup_path = current_path.with_suffix('.py.bak')
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        versioned_backup = current_path.with_suffix(f'.v{CURRENT_VERSION.replace(".", "_")}.{timestamp}.bak')
        print(f"{Fore.YELLOW}[*] Creating backup v{CURRENT_VERSION}...{Style.RESET_ALL}")
        with open(current_path, 'rb') as f:
            current_data = f.read()
        with open(versioned_backup, 'wb') as f:
            f.write(current_data)
        with open(backup_path, 'wb') as f:
            f.write(current_data)
        print(f"{Fore.YELLOW}[*] Applying update...{Style.RESET_ALL}")
        with open(current_path, 'wb') as f:
            f.write(new_code)
        if os.name != 'nt':
            os.chmod(current_path, 0o755)
        print(f"{Fore.GREEN}[✓] Update Successful!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Backup save: {versioned_backup}{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}[-] Failed to apply update: {e}{Style.RESET_ALL}")
        return False

def update_flow():
    banner()
    current_badge = display_version_badge(CURRENT_VERSION)
    print(f"""{Fore.CYAN}  ╔══════════════════════════════════════════════════╗
  ║          H E X P A N E L  U P D A T E R          ║
  ╚══════════════════════════════════════════════════╝{Style.RESET_ALL}
Now:{current_badge} {Fore.CYAN}v{CURRENT_VERSION}{Style.RESET_ALL}""")
    update_available, remote_ver, new_code, remote_type = check_updates(silent=False)
    if not update_available:
        print(f"\n{Fore.YELLOW} No updates found, you are using the latest version!{Style.RESET_ALL}")
        time.sleep(2)
        return False
    remote_badge = display_version_badge(remote_ver)
    print(f"\n{Fore.YELLOW}Update from v{CURRENT_VERSION} to v{remote_ver}?{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[1]{Style.RESET_ALL} Yes, update now to {remote_badge}")
    print(f"{Fore.YELLOW}[2]{Style.RESET_ALL} Skip")
    while True:
        choice = input(f"\n>> ").strip()
        if choice == "1":
            if apply_update(new_code):
                banner()
                print(f"\n{Fore.GREEN}[✓] Update Successful!{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}[*] Reboot HexPanel...{Style.RESET_ALL}")
                time.sleep(3)
                python = sys.executable
                os.execl(python, python, *sys.argv)
            break
        elif choice == "2":
            banner()
            print(f"{Fore.YELLOW}[*] Update skipped{Style.RESET_ALL}")
            time.sleep(2)
            break
        else:
            print(f"{Fore.RED}[!] Please enter the correct command{Style.RESET_ALL}")
    return True

def auto_check_update_on_start():
    try:
        check_file = Path("last_update_check.txt")
        current_type = get_version_type(CURRENT_VERSION)
        check_intervals = {
            "stable": 0,
            "Beta": 0,
            "Alpha": 0,
            "Release Candidate": 0,
            "Development": 0
        }
        interval = check_intervals.get(current_type, 86400)
        if check_file.exists():
            with open(check_file, 'r') as f:
                try:
                    last_check = float(f.read().strip())
                    if time.time() - last_check < interval:
                        return
                except:
                    pass
        update_available, remote_ver, _, remote_type = check_updates(silent=True)
    except Exception:
        pass

def menu(name):
    try:
        time.sleep(0.2)
        from config import ip, tc, name, myport
        time.sleep(0.2)
    except ImportError:
        hello()
        return
    if get_version_type(CURRENT_VERSION) in ["Alpha", "Beta"]:
        show_version_warning()
    banner()
    current(myport)
    print(f'                Welcome to Panel, {name}!')
    print("             >Created by t.me/CreatHexPanel<")
    choice = input(f"\n[1] Custom hex \n[2] Eavesdrop server\n\n[0] Edit IP \n[00] Edit token \n[55] Exit\n{Fore.CYAN}[99]{Style.RESET_ALL} Info and Updates\n >> ")
    while choice not in menu_options:
        banner()
        current(myport)
        print(f"                Welcome to Panel, {name}!\n             >Created by t.me/CreatHexPanel<\n >Please enter the correct command<")
        choice = input(f"\n[1] Custom hex \n[2] Eavesdrop server\n\n[0] Edit IP \n[00] Edit token \n[55] Exit\n{Fore.CYAN}[99]{Style.RESET_ALL} Info and Updates\n >> ")

    if choice == "55":
        banner()
        print("            Thank you for choosing HexPanel!")
        sys.exit(0)

    if choice == "99":
        infover()
        menu(name)

    print(f"\n{Fore.YELLOW}Функционал в разработке...{Style.RESET_ALL}")
    time.sleep(2)
    menu(name)

if __name__ == "__main__":
    try:
        from config import ip, tc, name, myport
        ip_status["ip"] = ip
        start_ip_monitor(ip)
        menu(name)
    except SystemExit:
        raise
    except Exception:
        hello()
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd in ['--update', '-u', 'update', '--version', '-v', 'version']:
            infover()
            sys.exit(0)
        elif cmd in ['--check', '-c', 'check']:
            update_available, remote_ver, _, remote_type = check_updates(silent=False)
            if update_available:
                remote_badge = display_version_badge(remote_ver)
                print(f"\n{Fore.GREEN}Update available!{Style.RESET_ALL}")
                print(f"Current: {display_version_badge(CURRENT_VERSION)} v{CURRENT_VERSION}")
                print(f"Latest:  {remote_badge} v{remote_ver}")
                print(f"Type:    {remote_type}")
                print(f"\nRun: python {sys.argv[0]} --update")
            else:
                ver_badge = display_version_badge(CURRENT_VERSION)
                print(f"{Fore.GREEN}You have the latest version!{Style.RESET_ALL}")
                print(f"Version: {ver_badge} v{CURRENT_VERSION}")
            sys.exit(0)
    auto_check_update_on_start()
