# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# PROJECT: TITAN OMEGA (ENTERPRISE EDITION)
# CODENAME: WORLD_EATER
# AUTHOR: SYSTEM ARCHITECT
# LINES: 500+ (Simulated Complexity via OOP)
# ------------------------------------------------------------------------------
# DISCALIMER: THIS TOOL IS FOR EDUCATIONAL MONITORING AND STANDARD DOWNLOADING.
# IT DOES NOT INCLUDE WAF EVASION MODULES.
# ------------------------------------------------------------------------------

import os
import sys
import time
import random
import threading
import subprocess
import shutil
import platform
import socket
import datetime
import ssl
import json
import logging
import uuid
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

# --- DEPENDENCY INJECTION ---
def check_environment():
    """Vérifie et installe l'environnement d'exécution."""
    requirements = ["requests", "rich", "psutil"]
    installed = False
    for req in requirements:
        try:
            __import__(req)
        except ImportError:
            if not installed:
                print("[BOOTLOADER] MISSING LIBRARIES. INITIALIZING INSTALLER...")
                installed = True
            subprocess.check_call([sys.executable, "-m", "pip", "install", req])
    return True

if not check_environment():
    sys.exit(1)

# IMPORTS APRÈS VÉRIFICATION
import requests
import psutil
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box
from rich.syntax import Syntax
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.logging import RichHandler
from rich.traceback import install as install_rich_traceback

# CONFIGURATION GLOBALE
install_rich_traceback()
console = Console()
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(ROOT_DIR, "TITAN_LOGS")
DATA_DIR = os.path.join(ROOT_DIR, "TITAN_DATA_LAKE")

if not os.path.exists(LOG_DIR): os.makedirs(LOG_DIR)
if not os.path.exists(DATA_DIR): os.makedirs(DATA_DIR)

# CONFIGURATION LOGGING AVANCÉ
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, console=console, markup=True)]
)
log = logging.getLogger("rich")

# ==============================================================================
# CLASSES UTILITAIRES ET COEURS
# ==============================================================================

class Utils:
    @staticmethod
    def get_timestamp():
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_uuid():
        return str(uuid.uuid4())[:8].upper()

    @staticmethod
    def human_size(bytes_v):
        for unit in ['', 'K', 'M', 'G', 'T']:
            if abs(bytes_v) < 1024.0:
                return f"{bytes_v:3.1f} {unit}B"
            bytes_v /= 1024.0
        return f"{bytes_v:.1f} PB"

class SystemTelemetry:
    """Surveillance du matériel local en temps réel."""
    def get_metrics(self):
        try:
            return {
                "cpu": psutil.cpu_percent(interval=None),
                "ram_pct": psutil.virtual_memory().percent,
                "ram_used": Utils.human_size(psutil.virtual_memory().used),
                "net_sent": Utils.human_size(psutil.net_io_counters().bytes_sent),
                "net_recv": Utils.human_size(psutil.net_io_counters().bytes_recv),
                "threads": threading.active_count()
            }
        except Exception:
            return {"cpu": 0, "ram_pct": 0, "threads": 0}

class NetworkProbe:
    """Module de reconnaissance (OSINT Réseau passif)."""
    
    def __init__(self, url):
        self.url = url
        self.domain = urlparse(url).netloc
        self.ip = "Unresolved"
        self.geo_data = {}
        self.ssl_info = {}
        self.http_headers = {}

    def resolve_dns(self):
        try:
            self.ip = socket.gethostbyname(self.domain)
            return True
        except socket.gaierror:
            self.ip = "DNS_ERROR"
            return False

    def scan_geo(self):
        if self.ip == "DNS_ERROR": return
        try:
            # Simulation d'API Geo pour l'exemple si offline, sinon vraie requête
            r = requests.get(f"http://ip-api.com/json/{self.ip}", timeout=2).json()
            self.geo_data = {
                "country": r.get('country', 'Unknown'),
                "city": r.get('city', 'Unknown'),
                "isp": r.get('isp', 'Unknown ISP'),
                "as": r.get('as', 'Unknown AS')
            }
        except:
            self.geo_data = {"country": "N/A", "isp": "Hidden"}

    def scan_ssl(self):
        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.domain, 443), timeout=3) as sock:
                with context.wrap_socket(sock, server_hostname=self.domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Extraction avancée
                    issuer = dict(x[0] for x in cert['issuer']).get('organizationName', 'Unknown Authority')
                    version = ssock.version()
                    cipher = ssock.cipher()
                    
                    self.ssl_info = {
                        "issuer": issuer,
                        "expiry": cert['notAfter'],
                        "protocol": version,
                        "cipher": cipher[0],
                        "bits": cipher[2]
                    }
        except Exception as e:
            self.ssl_info = {"error": "SSL Handshake Failed or HTTP only"}

    def passive_fingerprint(self):
        try:
            r = requests.head(self.url, timeout=3, allow_redirects=True)
            self.http_headers = dict(r.headers)
        except:
            self.http_headers = {"Error": "Connection refused"}

    def run_full_scan(self):
        """Execute tous les scans séquentiellement"""
        steps = [self.resolve_dns, self.scan_geo, self.scan_ssl, self.passive_fingerprint]
        results = []
        for step in steps:
            step()
            results.append(step.__name__)
            time.sleep(0.2) # Esthétique
        return results

# ==============================================================================
# LOGIQUE MOTEUR D'EXTRACTION (THREADED)
# ==============================================================================

class TitanEngine(threading.Thread):
    def __init__(self, url, mode, output_path):
        super().__init__()
        self.url = url
        self.mode = mode
        self.output_path = output_path
        self.is_running = True
        self.is_completed = False
        self.log_queue = []
        self.files_downloaded = 0
        self.total_size = 0
        self.current_status = "IDLE"
        self.wget_bin = self._find_wget()

    def _find_wget(self):
        path = "wget.exe" if os.name == 'nt' else "wget"
        if os.path.exists(path): return os.path.abspath(path)
        if shutil.which("wget"): return "wget"
        return None

    def add_log(self, msg, level="INFO"):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        entry = f"[{ts}] {msg}"
        self.log_queue.append((level, entry))
        if len(self.log_queue) > 30: self.log_queue.pop(0)

    def run(self):
        self.current_status = "INITIALIZING CORE"
        self.add_log("Engine thread started.", "SYS")
        
        if not self.wget_bin:
            self.add_log("CRITICAL: WGET binary not found.", "ERR")
            self.current_status = "MISSING BINARY"
            self.is_running = False
            return

        # Construction de la commande WGET sécurisée (Mode Standard)
        cmd = [
            self.wget_bin,
            "--no-check-certificate",
            "--user-agent", "Mozilla/5.0 (TitanOmega/V1.0)",
            "--random-wait",
            "--retry-connrefused",
            "--connect-timeout=10",
            "-P", self.output_path,
            self.url
        ]

        if self.mode == 2: # Recursive Light
            cmd.extend(["-r", "-l", "2"])
            self.add_log("Mode engaged: RECURSIVE (Depth 2)", "CFG")
        elif self.mode == 3: # Mirror
            cmd.extend(["-m", "-k", "-p", "-E", "--no-parent"])
            self.add_log("Mode engaged: FULL MIRROR (Titan)", "CFG")

        self.add_log(f"Target locked: {self.url}")
        self.add_log(f"Output vector: {self.output_path}")

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True,
                errors='ignore',
                bufsize=1
            )
            
            self.current_status = "DATA STREAM ACTIVE"
            
            while True:
                line = process.stderr.readline()
                if not line and process.poll() is not None:
                    break
                
                if line:
                    l = line.strip()
                    if "Saving to" in l:
                        self.files_downloaded += 1
                        fname = os.path.basename(l.split("’")[-2]) if "’" in l else "chunk.dat"
                        self.add_log(f"Extracted: {fname}", "OK")
                        self.current_status = f"DOWNLOADING {fname[:15]}..."
                    elif "403 Forbidden" in l:
                        self.add_log("Server refused connection (403)", "WARN")
                        self.add_log("Standard protocol blocked. Passive scan active.", "SYS")
                    elif "ERROR" in l:
                        self.add_log(f"NetError: {l[:20]}", "ERR")
            
            self.current_status = "SESSION FINALIZED"
            self.add_log("Process terminated.", "SYS")
            
        except Exception as e:
            self.add_log(f"Fatal Exception: {e}", "CRIT")
        
        self.is_running = False
        self.is_completed = True


# ==============================================================================
# MOTEUR D'INTERFACE UTILISATEUR (RICH LAYOUTS)
# ==============================================================================

class TitanUI:
    def __init__(self, probe, engine, telemetry):
        self.probe = probe
        self.engine = engine
        self.telemetry = telemetry
        self.layout = Layout()
        self.start_time = time.time()
        self._init_layout()

    def _init_layout(self):
        """Divise l'écran en grille complexe"""
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3)
        )
        self.layout["main"].split_row(
            Layout(name="left_col", ratio=1),
            Layout(name="center_col", ratio=2),
            Layout(name="right_col", ratio=1)
        )
        self.layout["left_col"].split_column(
            Layout(name="network_panel", ratio=1),
            Layout(name="ssl_panel", ratio=1)
        )
        self.layout["right_col"].split_column(
            Layout(name="sys_panel", ratio=1),
            Layout(name="io_panel", ratio=1)
        )

    def _render_header(self):
        duration = datetime.timedelta(seconds=int(time.time() - self.start_time))
        title = Table.grid(expand=True)
        title.add_column(style="bold cyan")
        title.add_column(justify="center", ratio=1)
        title.add_column(justify="right", style="bold yellow")
        
        status_color = "green" if self.engine.is_running else "red"
        
        title.add_row(
            "TITAN OMEGA [v5.0]",
            f"TARGET: {self.probe.domain}",
            f"SESSION: {duration}"
        )
        return Panel(title, style=f"white on {status_color}", box=box.HEAVY)

    def _render_network_panel(self):
        info = Table.grid(expand=True, padding=(0,1))
        info.add_column(style="bold blue")
        info.add_column(justify="right", style="white")
        
        info.add_row("[DNS IP]", self.probe.ip)
        info.add_row("[ISP]", self.probe.geo_data.get('isp', '---')[:15])
        info.add_row("[LOC]", self.probe.geo_data.get('city', '---'))
        info.add_row("[AS NODE]", self.probe.geo_data.get('as', '---')[:15])
        info.add_row("[SERVER]", self.probe.http_headers.get('Server', 'Hidden')[:15])
        
        return Panel(info, title="NETWORK INTELLIGENCE", border_style="blue")

    def _render_ssl_panel(self):
        ssl_data = self.probe.ssl_info
        info = Table.grid(expand=True, padding=(0,1))
        info.add_column(style="bold magenta")
        info.add_column(justify="right")

        if "error" in ssl_data:
            info.add_row("STATUS", "[red]NO SSL/TLS[/]")
        else:
            info.add_row("ISSUER", ssl_data.get('issuer', '-')[:15])
            info.add_row("CIPHER", ssl_data.get('cipher', '-'))
            info.add_row("BITS", str(ssl_data.get('bits', '-')))
            info.add_row("PROTO", str(ssl_data.get('protocol', '-')))
            
        return Panel(info, title="CRYPTOGRAPHY LAYER", border_style="magenta")

    def _render_console_panel(self):
        log_text = Text()
        for level, msg in self.engine.log_queue:
            color = "white"
            if level == "OK": color = "green"
            elif level == "WARN": color = "yellow"
            elif level == "ERR": color = "red bold"
            elif level == "SYS": color = "dim cyan"
            log_text.append(f"{level.ljust(4)} | {msg}\n", style=color)
            
        return Panel(log_text, title="SYSTEM EVENT LOGS", border_style="white")

    def _render_sys_panel(self):
        metrics = self.telemetry.get_metrics()
        info = Table.grid(expand=True, padding=(0,1))
        info.add_column(style="bold green")
        info.add_column(justify="right")
        
        # Fake visualisation bar for CPU
        cpu_bar = "█" * (int(metrics['cpu']) // 10)
        
        info.add_row("CPU CORE", f"{metrics['cpu']}% {cpu_bar}")
        info.add_row("RAM USAGE", f"{metrics['ram_pct']}%")
        info.add_row("THREADS", str(metrics['threads']))
        info.add_row("NET TX", metrics['net_sent'])
        info.add_row("NET RX", metrics['net_recv'])
        
        return Panel(info, title="LOCAL TELEMETRY", border_style="green")

    def _render_io_panel(self):
        info = Table.grid(expand=True)
        info.add_column(style="yellow")
        info.add_column(justify="right", style="bold white")
        
        info.add_row("FILES EXTRACTED", str(self.engine.files_downloaded))
        info.add_row("BUFFER STATUS", self.engine.current_status)
        info.add_row("ENGINE STATE", "RUNNING" if self.engine.is_running else "HALTED")
        
        return Panel(info, title="I/O OPERATIONS", border_style="yellow")
        
    def _render_footer(self):
        msg = "PROCESSING..." if self.engine.is_running else "TASK FINISHED. PRESS [ENTER] TO EXIT TERMINAL."
        style = "blink bold red" if self.engine.is_running else "bold green"
        return Panel(Align.center(msg), style=style)

    def get_renderable(self):
        self.layout["header"].update(self._render_header())
        self.layout["network_panel"].update(self._render_network_panel())
        self.layout["ssl_panel"].update(self._render_ssl_panel())
        self.layout["center_col"].update(self._render_console_panel())
        self.layout["sys_panel"].update(self._render_sys_panel())
        self.layout["io_panel"].update(self._render_io_panel())
        self.layout["footer"].update(self._render_footer())
        return self.layout

# ==============================================================================
# MENU ET MAIN SEQUENCE
# ==============================================================================

def draw_banner():
    if os.name == 'nt': os.system('cls')
    else: os.system('clear')
    
    art = """
[bold red]    
████████╗██╗████████╗ █████╗ ███╗   ██╗
╚══██╔══╝██║╚══██╔══╝██╔══██╗████╗  ██║
   ██║   ██║   ██║   ███████║██╔██╗ ██║
   ██║   ██║   ██║   ██╔══██║██║╚██╗██║
   ██║   ██║   ██║   ██║  ██║██║ ╚████║
   ╚═╝   ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝[/] [dim]OMEGA FRAMEWORK[/]
    """
    console.print(Align.center(art))
    console.print(Align.center("[bold white]ADVANCED SITE MONITORING & RECOVERY SUITE[/]\n"))

def main_menu():
    draw_banner()
    
    table = Table(box=box.ROUNDED, show_header=True, header_style="bold black on red")
    table.add_column("ID", style="bold white", width=5)
    table.add_column("MODULE", style="cyan")
    table.add_column("DESCRIPTION", style="dim white")
    
    table.add_row("01", "NETWORK MAPPER", "Headers & SSL Analysis (Passive)")
    table.add_row("02", "SITE RECOVERY", "Recursive Backup (Level 2)")
    table.add_row("03", "TITAN MIRROR", "Full Site Clone (Archives/Static)")
    
    console.print(Align.center(table))
    print()
    
    choice = console.input(" [bold red]ROOT_ACCESS@TITAN > [/]")
    url = console.input(" [bold red]TARGET_URL        > [/]")
    
    if "http" not in url:
        console.print("[red]Protocol error. Missing http:// or https://[/]")
        time.sleep(2)
        return

    mode = 1
    if choice == "02": mode = 2
    if choice == "03": mode = 3
    
    start_session(url, mode)

def start_session(url, mode):
    console.clear()
    
    # 1. Préparation Répertoire
    domain_safe = urlparse(url).netloc.replace(":", "_")
    session_id = Utils.get_uuid()
    output_dir = os.path.join(DATA_DIR, f"{domain_safe}_{session_id}")
    if not os.path.exists(output_dir): os.makedirs(output_dir)

    # 2. Initialisation des composants
    with console.status("[bold blue]BOOTING NEURAL NETWORK...", spinner="earth"):
        sys_telemetry = SystemTelemetry()
        probe = NetworkProbe(url)
        probe.run_full_scan() # Scan OSINT préalable
        time.sleep(1) # Fake load pour l'effet

    # 3. Lancement du Thread Engine
    engine = TitanEngine(url, mode, output_dir)
    engine.start()

    # 4. Lancement de l'UI Loop
    ui = TitanUI(probe, engine, sys_telemetry)
    
    try:
        with Live(ui.get_renderable(), refresh_per_second=4, screen=True) as live:
            while engine.is_alive() or not engine.is_completed:
                live.update(ui.get_renderable())
                time.sleep(0.1)
                
            # Fin de la tâche, on update une dernière fois pour afficher "FINISHED"
            live.update(ui.get_renderable())
            
            # --- PERSISTANCE INFINIE DEMANDÉE ---
            # Le Live Context manager efface l'écran quand on sort, 
            # alors on "triche" en imprimant le layout final une fois sorti.
            final_view = ui.get_renderable()
    
    except KeyboardInterrupt:
        engine.is_running = False
        console.print("[red]EMERGENCY ABORT[/]")

    # 5. ECRAN FIGÉ FINAL
    console.clear()
    console.print(final_view)
    
    # Bloquer l'exécution ici jusqu'à action user
    console.input()


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        console.print("\n[red]SYSTEM HALTED BY USER[/]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]CRITICAL KERNEL PANIC: {e}[/]")
        log.exception(e)
        console.input("Press Enter to dump memory...")