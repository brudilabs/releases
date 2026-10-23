# releases – Arbeitsnotizen für Claude Code

Öffentliches GitHub-Repo `brudilabs/releases`: Workflow „Release“ baut die privaten brudilabs-Apps, signiert sie
und pflegt den Katalog für den brudilabs Launcher (`~/Repository/brudilabs/core-launcher`). Sprache: **Deutsch**.
Ablauf, Secrets, Katalogformat und Fehlersuche stehen im README.

## Entscheidungen (nicht erneut abfragen)
- Quellcode bleibt privat auf git.brudilabs.com (fremd gehostet). Gebaut wird aus privaten GitHub-Spiegeln
  `brudilabs/<id>`, die lokal per zweitem Push-Ziel mitgepusht werden (Authentik sperrt Runner aus).
- Repository-Secrets: `QUELLCODE_TOKEN` (fine-grained, Contents read-only), `TAURI_SIGNING_PRIVATE_KEY`,
  `TAURI_SIGNING_PRIVATE_KEY_PASSWORD`. Den privaten Schlüssel nie ansehen oder ins Repo legen.
- Linux auf ubuntu-22.04 (AppImage), macOS auf macos-14 (universal, unsigniert – kein Apple-Account).
- Katalog-`id` = Programmname, nie ändern; `name` ist Anzeigename (financial-core → „financialCore“).
- content-core-Releases enthalten auch den Server (Image-Tarball, Deploy-Dateien, SHA256SUMS). Der feste Release
  `content-server` hält `install.sh` und `version.txt`, die `deploy/install.sh` von contentCore auf dem VPS liest.
  Dateinamen nicht ändern, ohne `install.sh` anzupassen. Eingabe `nur_server` überspringt Client und Katalog.

## Stand (2026-10-19)
- financial-core v0.1.0 veröffentlicht (2026-10-17), Signaturen mit dem echten Schlüssel geprüft.
- Getaggt, Push + Workflow-Lauf beim Nutzer: financial-core v0.1.1, core-launcher v0.2.0/v0.2.1.
- macOS-Builds gebaut, aber auf keinem Mac getestet.

## Hinweise
- Claude kann nicht pushen (keine Zugangsdaten); der Nutzer pusht und startet Workflows.
- `scripts/katalog.py` nur mit Standardbibliothek; kurz testbar mit Dummy-Dateien + `.sig`.
