# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import shutil
import requests
import ctypes
import time
import datetime
import random
import json
import re

# Tentative d'importation de colorama
try:
    import colorama
    colorama.init(autoreset=True)
    colorama_available = True
    color = colorama.Fore
    style = colorama.Style
except ImportError:
    colorama_available = False

# --- Configuration Visuelle ---
if colorama_available:
    GREEN = color.GREEN
    RED = color.RED
    WHITE = color.WHITE
    YELLOW = color.YELLOW
    CYAN = color.CYAN
    RESET = color.RESET
    BRIGHT = style.BRIGHT
else:
    # Codes ANSI de secours
    GREEN = '\033[92m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BRIGHT = ''

# Symboles
INFO = f'{BRIGHT}{GREEN}[{WHITE}!{GREEN}]{RESET}'
INPUT = f'{BRIGHT}{GREEN}[{WHITE}?{GREEN}]{RESET}'
ERROR = f'{BRIGHT}{RED}[{WHITE}x{RED}]{RESET}'
SUCCESS = f'{BRIGHT}{GREEN}[{WHITE}+{GREEN}]{RESET}'
WAIT = f'{BRIGHT}{YELLOW}[{WHITE}~{YELLOW}]{RESET}'

# --- Configuration Globale ---
VERSION = "v2.0 Ultimate"
TOOL_NAME = "Website Downloader Pro"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIR = os.path.join(ROOT_DIR, "Downloads")
WGET_WIN_URL = "https://eternallybored.org/misc/wget/1.21.3/64/wget.exe"

# Liste de User-Agents pour éviter la détection (Rotation)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

def clear_screen():
    if sys.platform.startswith("win"):
        os.system("cls")
    else:
        os.system("clear")

def set_title(title):
    try:
        if sys.platform.startswith("win"):
            ctypes.windll.kernel32.SetConsoleTitleW(f"{TOOL_NAME} {VERSION} - {title}")
        else:
            sys.stdout.write(f"\x1b]2;{TOOL_NAME} {VERSION} - {title}\x07")
    except:
        pass

def timestamp():
    return datetime.datetime.now().strftime('%H:%M:%S')

def print_line(msg):
    print(f"{GREEN}[{WHITE}{timestamp()}{GREEN}] {msg}")

# --- Fonctions Système ---

def get_wget_path():
    """Vérifie ou installe wget selon l'OS."""
    if sys.platform.startswith("win"):
        wget_exe = os.path.join(ROOT_DIR, "wget.exe")
        if os.path.exists(wget_exe):
            return wget_exe
        
        # Check system PATH
        if shutil.which("wget"):
            return "wget"

        print_line(f"{WAIT} Wget non trouvé, téléchargement automatique...")
        try:
            response = requests.get(WGET_WIN_URL, timeout=30)
            response.raise_for_status()
            with open(wget_exe, 'wb') as f:
                f.write(response.content)
            print_line(f"{SUCCESS} Wget installé avec succès.")
            return wget_exe
        except Exception as e:
            print_line(f"{ERROR} Impossible de télécharger wget : {e}")
            return None
    else:
        # Linux / MacOS
        if shutil.which("wget"):
            return "wget"
        else:
            print_line(f"{ERROR} 'wget' n'est pas installé sur ce système Linux/Mac.")
            print_line(f"{INFO} Installez-le via : sudo apt install wget (Debian) ou brew install wget (Mac)")
            return None

def detect_technology(url):
    """Analyse rapide des headers et du contenu HTML."""
    try:
        print_line(f"{WAIT} Analyse de la technologie du site...")
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        r = requests.get(url, headers=headers, timeout=10, verify=False)
        content = r.text.lower()
        
        techs = []
        if 'wp-content' in content: techs.append("WordPress")
        if '/_next/' in content or '__next' in content: techs.append("Next.js")
        if 'react' in content: techs.append("React")
        if 'vue' in content: techs.append("Vue.js")
        if 'shopify' in content: techs.append("Shopify")
        if 'wix' in content: techs.append("Wix")
        
        server = r.headers.get('Server', '')
        if server: techs.append(f"Server: {server}")

        tech_str = ", ".join(techs) if techs else "HTML/Standard"
        print_line(f"{SUCCESS} Technologies détectées : {WHITE}{tech_str}")
        
        return "Next.js" in techs or "React" in techs, techs
    except Exception as e:
        print_line(f"{ERROR} Erreur d'analyse : {e}")
        return False, []

# --- Moteur de Téléchargement ---

def build_wget_command(url, path, level, is_spa=False):
    """Construit la commande Wget en fonction du niveau de puissance."""
    wget = get_wget_path()
    if not wget:
        return None

    domain = url.replace("https://", "").replace("http://", "").split('/')[0]
    user_agent = random.choice(USER_AGENTS)
    
    # Options de base (Base solides)
    cmd = [
        wget,
        "--no-check-certificate", # Ignorer erreurs SSL
        "--no-hsts",
        "--restrict-file-names=windows",
        "--content-disposition",
        "--html-extension",       # Force .html
        "--convert-links",        # Transforme les liens pour lecture hors ligne
        "--page-requisites",      # CSS, Images, JS
        "--no-parent",            # Ne pas remonter dans l'arborescence
        "-e", "robots=off",       # Ignorer robots.txt
        "--random-wait",          # Éviter ban IP
        "-U", user_agent,         # User-Agent aléatoire
        "--header", "Accept-Language: fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
        "-P", path,
        url
    ]

    # Vérification si cookies.txt existe dans le dossier du script
    cookie_file = os.path.join(ROOT_DIR, "cookies.txt")
    if os.path.exists(cookie_file):
        print_line(f"{INFO} Fichier cookies.txt détecté et injecté.")
        cmd.extend(["--load-cookies", cookie_file])

    # Niveaux de puissance
    if level == 1:
        # Rapide : juste la page et assets
        pass 
        
    elif level == 2:
        # Standard : Récursif léger
        cmd.extend(["--recursive", "--level=2", "--span-hosts", "--domains=" + domain])
        
    elif level == 3:
        # Puissant : Récursif profond + Ignorer tags restrictifs
        cmd.extend([
            "--recursive", 
            "--level=5", 
            "--span-hosts", 
            "--domains=" + domain,
            "--header", "Cache-Control: no-cache",
            "--header", "Pragma: no-cache"
        ])

    elif level == 4:
        # Extrême (Clone total + tentative SPA)
        # Tente de télécharger tous les types de fichiers souvent ignorés
        cmd.extend([
            "--mirror",               # Copie miroir infinie (level inf)
            "--span-hosts",
            "--domains=" + domain,
            "--auth-no-challenge",    # Force l'auth si besoin
            "--retry-connrefused",
            "--timeout=15",
            "--tries=3",
            "--ignore-tags=area,canvas,form", # Nettoyage HTML spécifique
        ])
        
        # Ajout pour React/Next/Webpack chunks
        if is_spa:
             cmd.extend([
                "--accept-regex", r".*\.(html|css|js|json|png|jpg|jpeg|gif|svg|woff|woff2|ttf|ico|php|txt|xml|webmanifest|_next|static).*"
            ])

    return cmd

def run_download(url, level_choice):
    output_folder = os.path.join(DOWNLOADS_DIR, url.replace("https://", "").replace("http://", "").split('/')[0] + "_" + str(int(time.time())))
    
    # Détection pour avertissement
    is_spa, techs = detect_technology(url)
    
    if is_spa and level_choice < 4:
        print_line(f"{YELLOW} ATTENTION: Ce site utilise {techs[0]}. Utilisez le mode 4 (Extrême) pour de meilleurs résultats.")
        time.sleep(2)

    cmd = build_wget_command(url, output_folder, level_choice, is_spa)
    if not cmd:
        return

    print_line(f"{INFO} Démarrage du téléchargement dans : {CYAN}{output_folder}")
    print_line(f"{INFO} Mode choisi : {WHITE}{level_choice}")
    if is_spa and level_choice == 4:
        print_line(f"{INFO} Application des patterns spécifiques JS/Next.js...")
    
    print_line(f"{WAIT} Wget est en cours d'exécution... Veuillez patienter.")
    
    try:
        # Exécution silencieuse (pour pas polluer), on capture juste si ça crash grave
        start_time = time.time()
        
        # On utilise subprocess.Popen pour pouvoir l'arrêter proprement
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Petit spinner d'attente car wget est verbeux
        spinner = "|/-\\"
        idx = 0
        while process.poll() is None:
            sys.stdout.write(f"\r{CYAN}[Traitement] {spinner[idx % len(spinner)]} Téléchargement en cours... (Ctrl+C pour stopper)")
            sys.stdout.flush()
            idx += 1
            time.sleep(0.1)
            
        print() # Saut de ligne après fin loop
        
        if process.returncode in [0, 4, 8]: # 0=Ok, 4=Network Err, 8=Server Err (souvent juste des fichiers manquants, acceptable)
             elapsed = round(time.time() - start_time, 2)
             count = sum([len(files) for r, d, files in os.walk(output_folder)])
             size_bytes = sum([sum(map(lambda f: os.path.getsize(os.path.join(r, f)), files)) for r, d, files in os.walk(output_folder)])
             size_mb = round(size_bytes / (1024*1024), 2)
             
             print_line(f"{SUCCESS} Téléchargement terminé en {WHITE}{elapsed}s")
             print_line(f"{INFO} Fichiers récupérés : {WHITE}{count}")
             print_line(f"{INFO} Taille totale : {WHITE}{size_mb} MB")
             
             try:
                 if sys.platform.startswith("win"):
                     os.startfile(output_folder)
                 elif sys.platform.startswith("darwin"): # macOS
                     subprocess.Popen(["open", output_folder])
                 else: # Linux
                     subprocess.Popen(["xdg-open", output_folder])
             except:
                 pass
        else:
            _, stderr = process.communicate()
            print_line(f"{ERROR} Wget a rencontré une erreur critique.")
            print(f"{RED}Log partiel : {stderr[:500]}") # Afficher le début de l'erreur
            
    except KeyboardInterrupt:
        process.kill()
        print_line(f"\n{YELLOW} Téléchargement interrompu par l'utilisateur.")
    except Exception as e:
        print_line(f"\n{ERROR} Erreur inattendue : {e}")

    input(f"\n{INPUT} Appuyez sur Entrée pour revenir au menu...")

# --- Interface ---

def banner_art():
    grad = [GREEN, CYAN, CYAN, GREEN] # Simple dégradé
    ascii_art = r"""
 __   __              _____                         _                 _ 
 \ \ / /__  _   _ _ _|_   _|__  __ _ _ __ ___    __| | _____      ___| |
  \ V / _ \| | | | '__|| |/ _ \/ _` | '_ ` _ \  / _` |/ _ \ \ /\ / / | |
   | | (_) | |_| | |   | |  __/ (_| | | | | | || (_| | (_) \ V  V /| | |
   |_|\___/ \__,_|_|   |_|\___|\__,_|_| |_| |_(_)__,_|\___/ \_/\_/ |_|_|
    """
    lines = ascii_art.split("\n")
    for i, line in enumerate(lines):
        if line.strip():
            print(f"{grad[i % len(grad)]}{line}")
    print(f"\n{BRIGHT}{WHITE}       >> {VERSION} | Codé pour la puissance & la précision <<{RESET}\n")

def menu():
    while True:
        clear_screen()
        set_title("Menu Principal")
        banner_art()
        
        print(f" {GREEN}┌───────────────────────────────────────────────┐")
        print(f" {GREEN}│  {WHITE}[1] {CYAN}Mode Rapide (Une page)                  {GREEN}│")
        print(f" {GREEN}│  {WHITE}[2] {CYAN}Mode Standard (Structure de base)       {GREEN}│")
        print(f" {GREEN}│  {WHITE}[3] {CYAN}Mode Avancé (Profondeur & Récursivité)  {GREEN}│")
        print(f" {GREEN}│  {WHITE}[4] {CYAN}Mode Extrême (Miroir total / Anti-Bot)  {GREEN}│")
        print(f" {GREEN}│                                               │")
        print(f" {GREEN}│  {WHITE}[Q] {RED}Quitter                                 {GREEN}│")
        print(f" {GREEN}└───────────────────────────────────────────────┘")
        
        choice = input(f"\n{INPUT} Votre choix -> {WHITE}").strip().lower()
        
        if choice == 'q':
            sys.exit()
            
        if choice in ['1', '2', '3', '4']:
            url = input(f"{INPUT} Entrez l'URL du site (ex: https://site.com) -> {WHITE}").strip()
            
            if not url.startswith("http"):
                print_line(f"{ERROR} L'URL doit commencer par http:// ou https://")
                time.sleep(2)
                continue
                
            try:
                run_download(url, int(choice))
            except Exception as e:
                print_line(f"{ERROR} Crash lors de l'exécution : {e}")
                input()
        else:
            print_line(f"{ERROR} Choix invalide.")
            time.sleep(1)

if __name__ == "__main__":
    if sys.platform.startswith("win"):
        # Fix pour les couleurs ANSI sous Windows legacy console
        os.system('color')
        
    try:
        # Création du dossier output
        os.makedirs(DOWNLOADS_DIR, exist_ok=True)
        menu()
    except KeyboardInterrupt:
        print(f"\n{YELLOW} Au revoir !")
        sys.exit()