import os
import sys
import subprocess
import time
import platform

# --- Configuration ---
# Nom EXACT du fichier cible (comme demandé, on ne change rien)
TARGET_SCRIPT = "Your.Website.Downloader.py"

# Modules requis (installés automatiquement si requirements.txt est absent)
REQUIRED_MODULES = [
    "colorama",
    "requests"
]

def clear_console():
    """Nettoie la console selon l'OS"""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def install_package(package):
    """Tente d'installer un paquet proprement"""
    print(f" > Vérification / Installation de : {package}")
    try:
        # Tentative standard
        subprocess.check_call([sys.executable, "-m", "pip", "install", package],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        try:
            # Tentative mode user (souvent requis sur Linux/Mac)
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", package],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception as e:
            print(f" [X] Erreur d'installation pour {package}: {e}")
            return False

def main():
    clear_console()
    print("==========================================")
    print("   INSTALLATION - YOUR WEBSITE DOWNLOADER ")
    print("==========================================")
    print("")

    # 1. Mise à jour de pip (bonne pratique)
    try:
        print(" [1/3] Mise à jour du gestionnaire de paquets...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass # Pas grave si ça échoue

    # 2. Gestion des dépendances
    print(" [2/3] Installation des modules...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    requirements_path = os.path.join(script_dir, "requirements.txt")
    
    if os.path.exists(requirements_path):
        # Priorité au fichier requirements.txt s'il existe
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("  -> Dépendances installées via requirements.txt")
        except:
            # Fallback manuel si erreur
            for module in REQUIRED_MODULES:
                install_package(module)
    else:
        # Installation manuelle si pas de fichier (pas de création de fichier)
        for module in REQUIRED_MODULES:
            install_package(module)

    print("  -> Modules prêts.")

    # 3. Lancement du script principal
    print(f" [3/3] Lancement de {TARGET_SCRIPT}...")
    time.sleep(1)

    target_path = os.path.join(script_dir, TARGET_SCRIPT)

    if not os.path.exists(target_path):
        print(f"\n [ERREUR] Le fichier '{TARGET_SCRIPT}' est introuvable !")
        print(f" Assurez-vous que '{TARGET_SCRIPT}' est dans ce dossier :")
        print(f" {script_dir}")
        input("\nAppuyez sur Entrée pour quitter...")
        sys.exit(1)

    try:
        # Nettoyage avant lancement
        clear_console()
        # Lancement avec le même interpréteur python
        subprocess.run([sys.executable, target_path])
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Erreur critique lors du lancement : {e}")
        input("Appuyez sur Entrée pour fermer...")

if __name__ == "__main__":
    main()