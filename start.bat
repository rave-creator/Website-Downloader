@echo off
setlocal EnableDelayedExpansion
title NEXUS CORE v8.0 - SOVEREIGN EDITION
color 0B

echo =======================================================
echo     NEXUS CORE v8.0 - SECURE STARTUP SEQUENCE
echo =======================================================
echo.

:: 1. Vérification de l'installation Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERREUR CRITIQUE] Python n'est pas installe ou n'est pas dans le PATH.
    echo Veuillez installer Python 3.9+ depuis python.org et cocher "Add to PATH".
    pause
    exit /b
)

:: 2. Securisation de l'environnement (Environnement Virtuel Isol)
:: Cela evite que les modules Python n'interferent avec votre systeme global.
if not exist ".venv\" (
    echo [NEXUS] Premiere utilisation detectee.
    echo [NEXUS] Creation d'un environnement virtuel securise et isole...
    python -m venv .venv
    if !errorlevel! neq 0 (
        color 0C
        echo [ERREUR] Impossible de creer l'environnement virtuel.
        pause
        exit /b
    )
    echo [NEXUS] ✓ Environnement virtuel cree avec succes.
    echo.
)

:: 3. Activation de l'environnement et Lancement
echo [NEXUS] Activation du bouclier virtuel...
call .venv\Scripts\activate.bat

echo [NEXUS] Lancement du moteur Principal...
echo.
python Downloader.py

:: 4. Maintien de la consoleouverte en cas de crash
echo.
color 07
echo [NEXUS] Session terminee. Appuyez sur une touche pour fermer...
pause >nul
