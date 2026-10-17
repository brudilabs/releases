#!/usr/bin/env python3
"""Trägt eine neue App-Version in catalog.json ein bzw. erzeugt latest.json für den Launcher.

Nur Standardbibliothek. Die Signaturen (.sig) erzeugt `tauri build` bzw. `tauri signer sign`.

  katalog.py katalog --katalog catalog.json --app apps/financial-core.json --version 0.2.0 \
      --basis-url https://…/download/financial-core-v0.2.0 --notizen "…" \
      linux-x86_64=dist/financial-core_0.2.0_linux-x86_64.AppImage …
  katalog.py launcher --version 0.2.0 --basis-url … --notizen "…" linux-x86_64=dist/… > latest.json
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

ICON_BASIS = "https://raw.githubusercontent.com/brudilabs/releases/main/apps"
PLATTFORMEN = {"linux-x86_64", "linux-aarch64", "darwin-universal", "darwin-aarch64", "darwin-x86_64"}


def artefakte(paare, basis_url):
    ergebnis = {}
    for paar in paare:
        plattform, _, datei = paar.partition("=")
        if plattform not in PLATTFORMEN:
            sys.exit(f"unbekannte Plattform: {plattform}")
        with open(datei + ".sig", encoding="utf-8") as f:
            signatur = f.read().strip()
        ergebnis[plattform] = {
            "url": f"{basis_url.rstrip('/')}/{os.path.basename(datei)}",
            "signatur": signatur,
            "groesse": os.path.getsize(datei),
        }
    return ergebnis


def jetzt():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def katalog(args):
    with open(args.app, encoding="utf-8") as f:
        meta = json.load(f)
    try:
        with open(args.katalog, encoding="utf-8") as f:
            daten = json.load(f)
    except FileNotFoundError:
        daten = {"schema": 1, "apps": []}
    eintrag = {
        "id": meta["id"],
        "name": meta["name"],
        "beschreibung": meta.get("beschreibung", ""),
        "icon": f"{ICON_BASIS}/{meta['id']}.png",
        "version": args.version,
        "notizen": args.notizen,
        "plattformen": artefakte(args.artefakte, args.basis_url),
    }
    apps = [a for a in daten["apps"] if a["id"] != meta["id"]] + [eintrag]
    daten = {"schema": 1, "erstellt": jetzt(), "apps": sorted(apps, key=lambda a: a["name"].lower())}
    with open(args.katalog, "w", encoding="utf-8") as f:
        json.dump(daten, f, ensure_ascii=False, indent=2)
        f.write("\n")


def launcher(args):
    # Format des Tauri-Updaters; universelle macOS-Builds gelten für beide Architekturen.
    plattformen = {}
    for plattform, a in artefakte(args.artefakte, args.basis_url).items():
        wert = {"url": a["url"], "signature": a["signatur"]}
        if plattform == "darwin-universal":
            plattformen["darwin-aarch64"] = wert
            plattformen["darwin-x86_64"] = wert
        else:
            plattformen[plattform] = wert
    json.dump(
        {"version": args.version, "notes": args.notizen, "pub_date": jetzt(), "platforms": plattformen},
        sys.stdout,
        ensure_ascii=False,
        indent=2,
    )
    sys.stdout.write("\n")


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="art", required=True)
    for name in ("katalog", "launcher"):
        s = sub.add_parser(name)
        if name == "katalog":
            s.add_argument("--katalog", required=True)
            s.add_argument("--app", required=True)
        s.add_argument("--version", required=True)
        s.add_argument("--basis-url", required=True)
        s.add_argument("--notizen", default="")
        s.add_argument("artefakte", nargs="+", metavar="PLATTFORM=DATEI")
    args = p.parse_args()
    if not re.fullmatch(r"\d+\.\d+\.\d+(-[0-9A-Za-z.-]+)?", args.version):
        sys.exit(f"ungültige Version: {args.version}")
    katalog(args) if args.art == "katalog" else launcher(args)


if __name__ == "__main__":
    main()
