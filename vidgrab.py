#!/usr/bin/env python3
"""
VidGrab - Téléchargeur de vidéos par lien (Termux / Windows / Kali Linux)
Basé sur yt-dlp.

Exemples :
  python vidgrab.py https://exemple.com/video
  python vidgrab.py URL -q 720
  python vidgrab.py URL --audio
  python vidgrab.py -l liens.txt
  python vidgrab.py            (mode interactif)
"""
import argparse
import os
import shutil
import sys
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    sys.exit("yt-dlp est manquant. Installe-le avec : pip install -U yt-dlp")


def dossier_par_defaut() -> Path:
    # Termux : dossier partagé Android si termux-setup-storage a été lancé
    if "com.termux" in os.environ.get("PREFIX", ""):
        partage = Path.home() / "storage" / "downloads"
        if partage.exists():
            return partage / "VidGrab"
    return Path.home() / "Downloads" / "VidGrab"


def progression(d):
    if d["status"] == "downloading":
        pct = d.get("_percent_str", "").strip()
        vit = d.get("_speed_str", "").strip()
        eta = d.get("_eta_str", "").strip()
        print(f"\r  {pct}  {vit}  ETA {eta}   ", end="", flush=True)
    elif d["status"] == "finished":
        print("\n  Téléchargement terminé, traitement en cours...")


def construire_options(args, sortie: Path) -> dict:
    opts = {
        "outtmpl": str(sortie / "%(title).150B [%(id)s].%(ext)s"),
        "noplaylist": not args.playlist,
        "progress_hooks": [progression],
        "quiet": True,
        "no_warnings": True,
        "retries": 5,
        "fragment_retries": 5,
        "continuedl": True,
        "restrictfilenames": False,
        "windowsfilenames": os.name == "nt",
    }

    if args.audio:
        opts["format"] = "bestaudio/best"
        opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    else:
        if args.qualite == "best":
            opts["format"] = "bv*+ba/b"
        else:
            h = args.qualite
            opts["format"] = f"bv*[height<={h}]+ba/b[height<={h}]/b"
        opts["merge_output_format"] = "mp4"

    if args.cookies:
        opts["cookiefile"] = args.cookies
    if args.navigateur:
        opts["cookiesfrombrowser"] = (args.navigateur,)
    if args.proxy:
        opts["proxy"] = args.proxy
    return opts


def telecharger(urls, args):
    sortie = Path(args.dossier).expanduser() if args.dossier else dossier_par_defaut()
    sortie.mkdir(parents=True, exist_ok=True)

    if not shutil.which("ffmpeg"):
        print("Attention : ffmpeg est introuvable. La fusion audio/vidéo "
              "et la conversion MP3 ne fonctionneront pas.\n")

    opts = construire_options(args, sortie)
    ok, echecs = 0, []
    with yt_dlp.YoutubeDL(opts) as ydl:
        for i, url in enumerate(urls, 1):
            print(f"[{i}/{len(urls)}] {url}")
            try:
                ydl.download([url])
                ok += 1
            except Exception as e:
                msg = str(e).splitlines()[-1] if str(e) else "erreur inconnue"
                print(f"  Échec : {msg}")
                echecs.append(url)

    print(f"\nRéussis : {ok}/{len(urls)}  |  Dossier : {sortie}")
    if echecs:
        fichier = sortie / "echecs.txt"
        fichier.write_text("\n".join(echecs), encoding="utf-8")
        print(f"Liens en échec sauvegardés dans : {fichier}")


def lire_liste(chemin):
    lignes = Path(chemin).read_text(encoding="utf-8").splitlines()
    return [l.strip() for l in lignes if l.strip() and not l.startswith("#")]


def mode_interactif(args):
    print("VidGrab - colle un lien (ou 'q' pour quitter)")
    while True:
        try:
            url = input("\nLien > ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if url.lower() in {"q", "quit", "exit"}:
            break
        if url:
            telecharger([url], args)


def main():
    p = argparse.ArgumentParser(description="Télécharge des vidéos à partir de leur lien.")
    p.add_argument("urls", nargs="*", help="Un ou plusieurs liens")
    p.add_argument("-l", "--liste", help="Fichier texte contenant un lien par ligne")
    p.add_argument("-q", "--qualite", default="best",
                   choices=["best", "1080", "720", "480", "360"],
                   help="Qualité maximale (défaut : best)")
    p.add_argument("-a", "--audio", action="store_true", help="Extraire l'audio en MP3")
    p.add_argument("-o", "--dossier", help="Dossier de destination")
    p.add_argument("--playlist", action="store_true", help="Télécharger toute la playlist")
    p.add_argument("--cookies", help="Fichier cookies.txt (contenus nécessitant une connexion)")
    p.add_argument("--navigateur", choices=["chrome", "firefox", "edge", "brave"],
                   help="Lire les cookies depuis ce navigateur (Windows/Kali)")
    p.add_argument("--proxy", help="Proxy, ex : socks5://127.0.0.1:9050")
    args = p.parse_args()

    urls = list(args.urls)
    if args.liste:
        urls += lire_liste(args.liste)

    if urls:
        telecharger(urls, args)
    else:
        mode_interactif(args)


if __name__ == "__main__":
    main()
