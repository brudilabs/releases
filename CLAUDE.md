# releases – Arbeitsnotizen für Claude Code

Öffentliches GitHub-Repo `brudilabs/releases`: Workflow „Release“ baut die privaten brudilabs-Apps, signiert sie
und pflegt den Katalog für den brudilabs Launcher (`~/Repository/brudilabs/core-launcher`). Sprache: **Deutsch**.
Ablauf, Secrets, Katalogformat und Fehlersuche stehen im README.

## Entscheidungen (nicht erneut abfragen)
- Quellcode bleibt privat auf git.brudilabs.com (fremd gehostet). Gebaut wird aus privaten GitHub-Spiegeln
  `brudilabs/<id>`, die lokal per zweitem Push-Ziel mitgepusht werden (Authentik sperrt Runner aus).
- Repository-Secrets: `QUELLCODE_TOKEN` (fine-grained, Contents read-only), `TAURI_SIGNING_PRIVATE_KEY`,
  `TAURI_SIGNING_PRIVATE_KEY_PASSWORD`. Den privaten Schlüssel nie ansehen oder ins Repo legen.
- Linux auf ubuntu-22.04 (AppImage), macOS auf macos-15 (universal, unsigniert – kein Apple-Account).
- Windows auf windows-2022, nur für Apps mit `"windows": true` in `apps/<id>.json` (Job `plan` baut die Matrix):
  Apps als einzelne exe (`tauri build --no-bundle`), der Launcher als NSIS-Setup (currentUser). Unsigniert
  (SmartScreen), Minisign wie überall. Seit 2026-11: content-core und core-launcher, financial-core ab v0.21.0.
- Katalog-`id` = Programmname, nie ändern; `name` ist Anzeigename (financial-core → „financialCore“).
- content-core-Releases enthalten auch den Server (Image-Tarball, Deploy-Dateien, SHA256SUMS). Der feste Release
  `content-server` hält `install.sh` und `version.txt`, die `deploy/install.sh` von contentCore auf dem VPS liest.
  Dateinamen nicht ändern, ohne `install.sh` anzupassen. Eingabe `nur_server` überspringt Client und Katalog.
- Server-Releases sind signiert (seit 2026-11-17, Schritt „Server signieren“ in `veroeffentlichen`): `…_SHA256SUMS.sig`
  im Versions-Release, `install.sh.sig` im festen Release. `install.sh` (ab contentCore 0.15.0) bricht ohne gültige
  Signatur ab und prüft `file:` im trusted comment – Signaturdateien nie umbenennen.

## Stand (2026-10-19)
- financial-core v0.1.0 veröffentlicht (2026-10-17), Signaturen mit dem echten Schlüssel geprüft.
- Getaggt, Push + Workflow-Lauf beim Nutzer: financial-core v0.1.1, core-launcher v0.2.0/v0.2.1.
- macOS-Builds gebaut, aber auf keinem Mac getestet.

## Hinweise
- Claude darf pushen und den Workflow per `gh` starten (seit 2026-10-27), je Release vorher kurz fragen.
- Signierschlüssel nur in den Jobs `signieren` und `veroeffentlichen` (Katalog), beide mit der gepinnten CLI aus
  `signer/` (`npm ci --ignore-scripts`); nie im Build-Job, wo `npm ci` und der Build der App laufen (seit 2026-11-06).
  Rechte je Job, nur `veroeffentlichen` hat `contents: write`.
- `scripts/katalog.py` nur mit Standardbibliothek; kurz testbar mit Dummy-Dateien + `.sig`.
