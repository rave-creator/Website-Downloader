<div align="center">

# 🌐 NEXUS CORE v8.0 — SOVEREIGN EDITION

<p align="center">
    <b>Intelligence Technique Ultra-Avancée & Framework d'Archivage Profond 🚀</b>
    <br>
    Furtif. Autonome. Inarrêtable.
</p>

<p align="center">
  <a href="https://github.com/rave-creator">
    <img src="https://img.shields.io/badge/Architect-rave--creator-blueviolet?style=for-the-badge&logo=github" alt="Rave Creator">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Language-Python%203.9+-yellow?style=for-the-badge&logo=python" alt="Python">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Engine-AsyncIO%20%2B%20aiohttp-blue?style=for-the-badge&logo=python" alt="Engine">
  </a>
  <a href="#">
    <img src="https://img.shields.io/github/license/rave-creator/Website-Downloader?style=for-the-badge&color=green" alt="License">
  </a>
</p>

<p align="center">
  <a href="#-fonctionnalités-principales">Fonctionnalités</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-modules-nexus">Modules NEXUS</a> •
  <a href="#-structure-résiliente">Structure</a>
</p>

</div>

---

## ⚡ Présentation

**NEXUS CORE v8.0** n'est plus un simple aspirateur de site. Il a évolué pour devenir une véritable suite **OSINT** et un **Framework d'Archivage Profond**. Porté par un moteur AsyncIO redoutable et propulsé par une IA adaptative de bypass (WAF / CDN), NEXUS est conçu pour étudier, cloner et préserver le Web avec une précision absolue et une furtivité sans précédent. 💯

### 🎯 Pourquoi choisir NEXUS CORE ?

| 🚀 **Hypermoteur Async** | 🛡️ **Bypass WAF/CDN** | 🧠 **Intelligence OSINT** |
|:---:|:---:|:---:|
| Téléchargements massifs multi-coroutines (jusqu'à 30 workers) ⚡ | Contournement Cloudflare, Akamai, Imperva, DDoS-Guard 🎭 | DNS, GeoIP, TLS, Sous-domaines et scan de ports passif 🔍 |
| Zéro dépendance binaire externe 🔥 | Rotation automatique des Proxies, IP et User-Agents 🔄 | Génération ultra-détaillée de rapports HTML 📊 |

---

## ✨ Fonctionnalités Principales

<div align="center">

| Module | Description |
| :--- | :--- |
| **🛡️ Nexus Bypass Core v3.0** | Engine autonome détectant les challenges WAF/CAPTCHA et escaladant ses stratégies (STEALTH → SPOOF → PROXY → ROTATE) en clonant les cookies de clearance. |
| **🔎 Reconnaissance Complète** | Scan passif et profond du domaine : Headers de sécurité, Technologies, CMS, Sous-domaines, E-mails, Commentaires HTML (Leak Hunt) et Ports ouverts. |
| **📥 Archivages Asynchrones** | `SINGLE`, `SMART CRAWL` (profondeur 2), `DEEP CRAWL` (profondeur 4), `FULL MIRROR` (profondeur 6) ou encore clonage via `SITEMAP`. |
| **📈 Statistiques en Temps Réel** | Live TUI propulsée par `rich` affichant la vitesse réseau, la charge CPU/RAM, et l'état de résilience du pool de proxies. |
| **🌐 Gestionnaire de Proxies** | Scraping gratuit depuis API publiques, auto-validation (Health-check) et intégration intelligente dans l'algorithme d'évasion réseau. |
| **⚙️ Bootstrap Autonome** | Le script s'auto-répare et installe automatiquement les dépendances Python requises si elles manquent à l'initialisation. |

</div>

---

## 📥 Installation

### 1️⃣ Prérequis

- **Python 3.9+** (Assurez-vous de l'ajouter au PATH durant l'installation) 🐍
- Une connexion internet stable 🌐

### 2️⃣ Démarrage Rapide

L'outil **s'auto-configure au premier lancement**. Il n'y a plus besoin de script d'installation système.

```bash
# Clonez le repository
git clone https://github.com/rave-creator/Website-Downloader.git

# Entrez dans le dossier
cd Website-Downloader

# Lancez l'outil directement (les paquets manquants s'installeront tout seuls !)
python Downloader.py
```

---

## 🎮 Modules NEXUS

L'interface de la console **NEXUS** (Redesign 2026) vous donne accès à un panel opérationnel surpuissant :

| Touche | Commande | Description |
|:---:|:---|:---|
| `1` | **⬡ RECON — FAST** | Reconnaissance en 5 modules ultra-rapide (DNS, SSL, HTTP, WAF). |
| `2` | **⬡ RECON — DEEP** | Full OSINT passif : inclut Subdomains, Ports, Extractions d'e-mails et de commentaires. |
| `3` | **⬡ DOWNLOAD SINGLE** | Récupération chirurgicale d'une ressource unique avec hash SHA-256. |
| `4` | **⬡ SMART CRAWL** | Crawl asynchrone (Prof. 2 - 15 concurrency). Extrait les assets essentiels. |
| `5` | **⬡ DEEP CRAWL** | Crawl profond (Prof. 4 - 20 concurrency). Arborescence complète, JS, Médias. |
| `6` | **⬡ FULL MIRROR** | Clonage absolu (Prof. 6 - 30 concurrency). Copie intégrale avec préservation heuristique. |
| `7` | **⬡ SITEMAP BLAST** | Téléchargement parallèle dicté par parsing automatique du *sitemap.xml*. |
| `8` | **⬡ GENERATE REPORT** | Exporte l'intelligence OSINT de votre session en un rapport HTML *Dark Theme*. |
| `9` | **⬡ VIEW ARCHIVES** | Explorateur interne pour consulter vos archives et empreintes locales. |
| `P` | **⬡ LOAD PROXIES** | Chargement d'une liste de proxies manuelle (Fichier, liste HTTP/SOCKS). |
| `F` | **⬡ FETCH FREE PROXIES**| Moissonne et vérifie automatiquement des listes publiques de proxies. |
| `B` | **⬡ BYPASS STATUS** | Affiche en temps réel l'état du moteur IA réseau, les cookies WAF et les proxies. |

---

## 📂 Structure Résiliente

Dès le premier lancement, NEXUS organise automatiquement son propre écosystème :

```text
Website-Downloader/
├── 📁 NEXUS_ARCHIVES/                     # 💾 Vos mirroirs et crawls aboutissent ici
├── 📁 NEXUS_REPORTS/                      # 📊 Rapports HTML générés automatiquement
├── 📁 NEXUS_RESOURCES/
│   ├── 📁 logs/                           # Fichiers de journalisation (nexus.log)
│   ├── 📁 cache/                          # Cache pour l'IA d'évitement
│   ├── 📁 tmp/                            # Purges automatiques
│   └── 📁 wordlists/                      # Dictionnaires bruteforce subdomains/paths
├── 🐍 Downloader.py                       # 🚀 Cœur de NEXUS
├── 📜 LICENSE
└── 📝 README.md
```

---

## ⚠️ Disclaimer & Responsabilité

> [!CAUTION]
> **À LIRE IMPÉRATIVEMENT** 👀

Cet outil, très puissant et furtif, a été développé à des fins **éducatives**, d'**OSINT légal** et de **préservation numérique** uniquement.

- ✅ **Respectez le droit d'auteur** : Ne republiez pas le contenu d'autrui sans autorisation.
- ⚠️ **Mollo sur la force brute** : Les attaques massives (`FULL MIRROR` avec 30 coroutines) peuvent stresser les serveurs modestes. L'intelligence ne remplace pas la courtoisie numérique.
- 🔐 **Autorisation** : Pratiquez la sécurité offensive et le scraping lourd uniquement si vous en avez l'autorisation explicite !
- 📜 **Responsabilité** : **rave-creator** (et ses contributeurs) déclinent toute responsabilité en cas de mauvaise utilisation de cet équipement ou de dommages collatéraux.

---

<div align="center">

<br>

**Engineered with ❤️ by TITAN CORE TEAM / rave-creator**

<br>

<a href="https://github.com/rave-creator/Website-Downloader/issues">🐛 Signaler une anomalie</a> • <a href="https://github.com/rave-creator/Website-Downloader/pulls">🤝 Contribuer au Nexus</a>

<br><br>

<img src="https://img.shields.io/badge/2026-SOVEREIGN%20EDITION-grey?style=flat-square">

---

### ⭐ Si cet outil vous aide, n'oubliez pas de mettre une étoile sur le dépôt ! ⭐

</div>
