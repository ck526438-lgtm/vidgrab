# VidGrab

Téléchargeur de vidéos par lien, en ligne de commande. Fonctionne sur **Termux**, **Windows** et **Kali Linux**. Basé sur [yt-dlp](https://github.com/yt-dlp/yt-dlp).

## Fonctionnalités

- Télécharge depuis plus de 1000 sites supportés par yt-dlp
- Choix de la qualité (1080, 720, 480, 360 ou meilleure)
- Extraction audio en MP3
- Liste de liens depuis un fichier, playlists, mode interactif
- Reprise des téléchargements et nouvelles tentatives automatiques
- Cookies et proxy pour les contenus nécessitant une connexion

## Installation

### Termux (Android)
```bash
pkg update && pkg install python ffmpeg git -y
termux-setup-storage
git clone https://github.com/ck526438-lgtm/vidgrab.git
cd vidgrab
pip install -r requirements.txt
```

### Windows (PowerShell)
```powershell
winget install Python.Python.3.12
winget install Gyan.FFmpeg
git clone https://github.com/ck526438-lgtm/vidgrab.git
cd vidgrab
pip install -r requirements.txt
```

### Kali Linux
```bash
sudo apt update && sudo apt install -y python3 python3-venv ffmpeg git
git clone https://github.com/ck526438-lgtm/vidgrab.git
cd vidgrab
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

## Utilisation

```bash
python vidgrab.py "https://lien-de-la-video"
python vidgrab.py "LIEN" -q 720
python vidgrab.py "LIEN" --audio
python vidgrab.py -l liens.txt
python vidgrab.py "LIEN_PLAYLIST" --playlist
python vidgrab.py                      # mode interactif
```

| Option | Description |
|---|---|
| `-q`, `--qualite` | `best`, `1080`, `720`, `480`, `360` |
| `-a`, `--audio` | Extraire l'audio en MP3 |
| `-l`, `--liste` | Fichier texte, un lien par ligne |
| `-o`, `--dossier` | Dossier de destination |
| `--playlist` | Télécharger la playlist entière |
| `--cookies` | Fichier `cookies.txt` |
| `--navigateur` | Lire les cookies depuis chrome, firefox, edge ou brave |
| `--proxy` | Proxy, ex. `socks5://127.0.0.1:9050` |

## Mise à jour

Si un site cesse de fonctionner, mets à jour yt-dlp :
```bash
pip install -U yt-dlp
```

## Avertissement légal

Cet outil est destiné au téléchargement de contenus pour lesquels tu disposes des droits (tes propres vidéos, contenus libres, ou autorisés par le site). L'utilisateur est seul responsable du respect des droits d'auteur et des conditions d'utilisation des plateformes.

## Licence

MIT

