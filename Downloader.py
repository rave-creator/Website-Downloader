# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import shutil
import time
import datetime
import random
import threading
import re
import zipfile
import ctypes

# ----------------------------------------------------------------------
# BLOC ANTI-CRASH AU DEMARRAGE (PRIORITÉ ABSOLUE)
# ----------------------------------------------------------------------
try:
    # Force l'UTF-8 pour Windows (pour les émojis)
    if os.name == 'nt':
        os.system('color')
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')

    # Importations sécurisées
    import requests
    import colorama
    from colorama import Fore, Style, Back
    colorama.init(autoreset=True)
except Exception as e:
    # Si ça plante ici, c'est que les modules manquent ou que Windows bug
    print("\n[!!!] CRASH INITIALISATION [!!!]")
    print(f"Erreur : {e}")
    print("Astuce : Lancez 'python Setup.py' d'abord.")
    input("Appuyez sur Entrée pour quitter...")
    sys.exit()

# --- CONFIGURATION ---
VERSION = "v3.1 STABLE GOD MODE"
TITLE_APP = "Downloader Pro Ultimate"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(ROOT_DIR, "Output", "Sites")
WGET_WIN_URL = "https://eternallybored.org/misc/wget/1.21.3/64/wget.exe"

# Whitelist CDNs
CDN_WHITELIST = [
    "fonts.googleapis.com", "fonts.gstatic.com", "ajax.googleapis.com",
    "cdnjs.cloudflare.com", "unpkg.com", "cdn.jsdelivr.net",
    "code.jquery.com", "use.fontawesome.com", "kit.fontawesome.com",
    "assets.vercel.com", "cdn.shopify.com"
]

# Rotation User-Agent
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
]

HEADERS_PRO = [
    "--header=Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "--header=Accept-Language: en-US,en;q=0.5",
    "--header=Cache-Control: no-cache",
    "--header=Pragma: no-cache"
]

# --- FONCTIONS SYSTÈME ---

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def set_title(status="Idle"):
    title = f"{TITLE_APP} {VERSION} | {status}"
    if os.name == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(title)

def log(tag, msg, color=Fore.WHITE):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"{Style.DIM}{Fore.WHITE}[{ts}] {Style.BRIGHT}{color}{tag.ljust(8)} {Fore.WHITE}: {msg}{Fore.RESET}")

def check_wget():
    """Vérifie ou installe wget automatiquement sans crash"""
    local_path = os.path.join(ROOT_DIR, "wget.exe")
    
    # 1. Déjà là ?
    if os.path.exists(local_path): return local_path
    if shutil.which("wget"): return "wget"

    # 2. Téléchargement
    if os.name == 'nt':
        log("SYS", "Wget manquant. Téléchargement...", Fore.YELLOW)
        try:
            r = requests.get(WGET_WIN_URL, timeout=15)
            with open(local_path, 'wb') as f:
                f.write(r.content)
            log("SYS", "Wget installé.", Fore.GREEN)
            return local_path
        except Exception as e:
            raise Exception(f"Impossible de télécharger Wget: {e}")
    else:
        raise Exception("Sur Linux/Mac, installez wget (apt install wget)")

def zip_folder(folder_path):
    output_path = folder_path + ".zip"
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                abs_file = os.path.join(root, file)
                rel_file = os.path.relpath(abs_file, os.path.dirname(folder_path))
                zipf.write(abs_file, rel_file)
    return output_path

# --- MOTEUR DE TÉLÉCHARGEMENT ---

def run_download(url, mode):
    try:
        wget_exe = check_wget()
    except Exception as e:
        log("ERREUR", str(e), Fore.RED)
        return

    domain = url.split("//")[-1].split("/")[0]
    timestamp = int(time.time())
    folder_name = f"{domain}_{timestamp}"
    save_path = os.path.join(DOWNLOAD_DIR, folder_name)
    
    if not os.path.exists(save_path): os.makedirs(save_path)

    ua = random.choice(USER_AGENTS)
    
    # Commande de base ultra robuste
    cmd = [
        wget_exe,
        "--no-check-certificate",
        "--adjust-extension",
        "--convert-links",
        "--page-requisites",
        "--no-parent",
        "--restrict-file-names=windows",
        "--random-wait",
        "--user-agent", ua,
        "-P", save_path,
        url
    ]
    
    cmd.extend(HEADERS_PRO)
    
    mode_name = "BASIC"
    if mode >= 2: # SUPER
        mode_name = "SUPER"
        cmd.extend(["--recursive", "--level=2"])
    
    if mode >= 3: # ULTRA
        mode_name = "ULTRA"
        cmd.extend([
            "--recursive", 
            "--level=inf", 
            "--span-hosts", 
            f"--domains={domain}," + ",".join(CDN_WHITELIST)
        ])
    
    if mode == 4: # EXTREME (God Mode)
        mode_name = "GOD MODE"
        cmd.extend([
            "--mirror",
            "--auth-no-challenge",
            "--retry-connrefused",
            "--timeout=20",
            "-e", "robots=off",
            "--accept-regex", r".*\.(html|css|js|json|png|jpg|gif|svg|woff|woff2|ttf|php).*"
        ])

    clear()
    print(f"\n{Fore.GREEN}╔════════════════════════════════════════════════════╗")
    print(f"{Fore.GREEN}║ {Fore.WHITE}CIBLE   : {Fore.CYAN}{url}")
    print(f"{Fore.GREEN}║ {Fore.WHITE}MODE    : {Fore.RED}{mode_name}")
    print(f"{Fore.GREEN}║ {Fore.WHITE}DOSSIER : {Fore.YELLOW}{folder_name}")
    print(f"{Fore.GREEN}╚════════════════════════════════════════════════════╝\n")

    print(f"{Style.DIM} Initialisation du moteur Wget...{Fore.RESET}")
    time.sleep(1)

    # Lancement du processus
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        errors='ignore'
    )

    # Barre de progression simplifiée mais efficace
    start_time = time.time()
    files_dl = 0
    
    # Lecture de stderr
    while True:
        line = process.stderr.readline()
        if not line and process.poll() is not None:
            break
        if line:
            if "Saving to" in line:
                files_dl += 1
                try:
                    filename = line.split("’")[-2]
                except: 
                    try: filename = line.split("'")[-2]
                    except: filename = "fichier..."
                
                filename = os.path.basename(filename)
                if len(filename) > 40: filename = filename[:37] + "..."
                sys.stdout.write(f"\r{Fore.GREEN} > OK ({files_dl}) : {Fore.WHITE}{filename:<40}")
                sys.stdout.flush()

    duration = round(time.time() - start_time, 2)
    print(f"\n\n{Back.GREEN}{Fore.BLACK} FIN DU TÉLÉCHARGEMENT {Back.RESET} en {duration}s")
    
    # Demander Zip ou Ouvrir
    action = input(f"\n{Fore.YELLOW}[O]uvrir ou [Z]ipper ? > {Fore.RESET}").lower()
    if 'z' in action:
        print("Compression...")
        zip_file = zip_folder(save_path)
        print(f"Archive : {zip_file}")
    elif 'o' in action:
        os.startfile(save_path) if os.name == 'nt' else None

def banner():
    clear()
    logo = f"""
    {Fore.GREEN}   _______  ______    
    {Fore.GREEN}  |__   __||____  |   {Fore.WHITE}DOWNLOADER {Fore.CYAN}v3.1{Fore.WHITE}
    {Fore.GREEN}     | |     / /      {Fore.WHITE}PRO EDITION
    {Fore.GREEN}     | |    / /       
    {Fore.GREEN}     |_|   /_/        {Style.DIM}by rave-creator{Style.RESET_ALL}
    """
    print(logo)

# ----------------------------------------------------------------------
# MENU PRINCIPAL SÉCURISÉ
# ----------------------------------------------------------------------
def main():
    while True:
        try:
            banner()
            set_title("Menu")
            print(f" {Fore.WHITE}[1] Basic {Style.DIM}(Rapide){Fore.RESET}")
            print(f" {Fore.WHITE}[2] Super {Style.DIM}(Blog/Standard){Fore.RESET}")
            print(f" {Fore.WHITE}[3] Ultra {Style.DIM}(E-commerce){Fore.RESET}")
            print(f" {Fore.RED}[4] GOD MODE {Style.DIM}(Miroir complet/Hacker){Fore.RESET}")
            print(f" \n {Fore.CYAN}[Q] Quitter{Fore.RESET}")

            choix = input(f"\n {Fore.GREEN}rave> {Fore.RESET}").strip().lower()

            if choix == 'q': sys.exit()
            if choix in ['1', '2', '3', '4']:
                url = input(f" {Fore.YELLOW}URL > {Fore.RESET}").strip()
                if not url.startswith("http"):
                    print(f"{Fore.RED}Il manque http:// ou https:// !")
                    time.sleep(2)
                    continue
                
                # Petit check de connexion
                try:
                    requests.head(url, timeout=5)
                except:
                    print(f"{Fore.RED}Le site ne répond pas.")
                    if input("Essayer quand même ? (o/n) ") != 'o': continue
                
                run_download(url, int(choix))
                input(f"\n{Fore.WHITE}Appuyez sur Entrée pour revenir au menu...")

        except KeyboardInterrupt:
            sys.exit()

if __name__ == "__main__":
    try:
        # Création des dossiers nécessaires
        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)
        
        main()

    except Exception as e:
        # LE FILET DE SÉCURITÉ ULTIME
        print(f"\n\n{Back.RED}{Fore.WHITE} FATAL CRASH {Back.RESET}")
        print(f"{Fore.RED}{str(e)}")
        print("\n\nC'est la catastrophe.")
        import traceback
        traceback.print_exc()
        input("Appuyez sur une touche pour mourir...")