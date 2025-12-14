import os
import sys
import subprocess
import time
import pkg_resources

TARGET_SCRIPT = "Downloader.py"

def install(package):
    try:
        dist = pkg_resources.get_distribution(package)
        print('{} ({}) est déjà installé'.format(dist.key, dist.version))
    except pkg_resources.DistributionNotFound:
        print(f'Installation de {package}...')
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"--- INSTALLATION & RÉPARATION ({TARGET_SCRIPT}) ---")
    
    # 1. Installation des modules
    try:
        install("requests")
        install("colorama")
        print(">> Modules OK.")
    except Exception as e:
        print(f"!! Erreur PIP : {e}")

    # 2. Vérification du fichier
    if not os.path.exists(TARGET_SCRIPT):
        print(f"\n[ERREUR] Le fichier '{TARGET_SCRIPT}' est introuvable !")
        print(f"Vérifiez que le fichier s'appelle bien {TARGET_SCRIPT}")
        input("Appuyez sur Entrée pour fermer...")
        sys.exit()

    # 3. Lancement
    print(f"\n>> Lancement de {TARGET_SCRIPT}...")
    time.sleep(1)
    
    try:
        subprocess.run([sys.executable, TARGET_SCRIPT])
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Erreur critique au lancement : {e}")
        input()

if __name__ == "__main__":
    main()