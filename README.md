# brudilabs Releases

Öffentliche Builds der brudilabs-Apps und der Katalog für den **brudilabs Launcher**.
Der Quellcode liegt privat auf git.brudilabs.com (gespiegelt in private GitHub-Repos); zu jedem Release gehört ein Quellpaket (`…_quellcode.tar.gz`, AGPL-3.0).

## Launcher herunterladen

- Linux: [core-launcher.AppImage](https://github.com/brudilabs/releases/releases/download/launcher/core-launcher.AppImage)
  – ausführbar machen (`chmod +x`) und starten; er legt sich selbst einen Startmenü-Eintrag an.
- macOS: [core-launcher.dmg](https://github.com/brudilabs/releases/releases/download/launcher/core-launcher.dmg)
  – noch nicht notarisiert: beim ersten Öffnen *Systemeinstellungen → Datenschutz & Sicherheit → Trotzdem öffnen*.

## Aufbau

| Release        | Inhalt                                                              |
|----------------|---------------------------------------------------------------------|
| `katalog`      | `catalog.json` + `catalog.json.sig` (wird bei jedem App-Release überschrieben) |
| `launcher`     | `latest.json` (Tauri-Updater) und feste Download-Dateien des Launchers |
| `<app>-vX.Y.Z` | AppImage, `.app.tar.gz`, (Launcher: `.dmg`), Quellpaket             |
| `content-server` | `install.sh` und `version.txt` (neueste Server-Version von contentCore) |

`content-core-vX.Y.Z` enthält zusätzlich den Server: `content-core-server_X.Y.Z_linux-x86_64.image.tar.gz`
(Docker-Image für `docker load`), `…_deploy.tar.gz` (Compose, Caddy, Skripte) und `…_SHA256SUMS`.

`apps/<id>.json` enthält Name, Beschreibung und das private Quell-Repo `brudilabs/<id>`; `apps/<id>.png` das Symbol im Launcher.

### App-Eintrag: `id` und `name`

| Feld | Beispiel | Bedeutung |
|---|---|---|
| `id` | `financial-core` | technisch: Programmname, Wayland-App-ID, Name des Desktop-Eintrags, Release-Präfix, Quell-Repo. **Nie ändern** – sonst gilt die App als neu und Installationen verwaisen. |
| `name` | `financialCore` | Anzeigename im Launcher und im Startmenü. Der Teil nach der letzten Binnenmajuskel bzw. dem letzten `-` erscheint in Lime. |
| `beschreibung` | `Buchhaltung für …` | Untertitel der Kachel |
| `quelle` | `brudilabs/financial-core` | privates GitHub-Repo, aus dem gebaut wird |

Änderungen an `apps/<id>.json` landen erst mit dem **nächsten Release dieser App** im Katalog: Nur der Workflow
kann den Katalog signieren, und er übernimmt den Eintrag dabei neu.

### Katalog (`catalog.json`, Schema 1)

```json
{ "schema": 1, "erstellt": "2026-10-17T18:38:31Z",
  "apps": [{ "id": "financial-core", "name": "financialCore", "beschreibung": "…", "icon": "https://…/apps/financial-core.png",
    "version": "0.1.1", "notizen": "…",
    "plattformen": {
      "linux-x86_64":     { "url": "…/financial-core_0.1.1_linux-x86_64.AppImage", "signatur": "<base64 .sig>", "groesse": 103545336 },
      "darwin-universal": { "url": "…/financial-core_0.1.1_darwin-universal.app.tar.gz", "signatur": "…", "groesse": 46857935 } } }] }
```

Der Launcher lehnt Katalog und Downloads ab, wenn die Minisign-Signatur nicht zum eingebauten Schlüssel passt
(Schlüssel-ID `EF5232272258720C`). Ohne Netz nutzt er den zuletzt geprüften Katalog, nie aber einen mit falscher
Signatur.

## Einrichtung (einmalig)

1. Auf GitHub Organisation `brudilabs` und dieses Repo **öffentlich** anlegen, Inhalt pushen.
2. Signaturschlüssel erzeugen (im Repo core-launcher): `ui/node_modules/.bin/tauri signer generate -w ~/.tauri/brudilabs.key`
   – privaten Schlüssel und Passwort im Passwortmanager sichern. Öffentlichen Teil eintragen:
   `./scripts/schluessel-eintragen.sh ~/.tauri/brudilabs.key.pub` (core-launcher), committen.
3. Der Quellcode bleibt privat. git.brudilabs.com ist für GitHub nicht erreichbar (Authentik-Anmeldung), daher
   wird jedes Quell-Repo beim lokalen `git push` zusätzlich in ein **privates** GitHub-Repo gleichen Namens
   gepusht (`brudilabs/financial-core`, `brudilabs/core-launcher`):
   ```sh
   git remote set-url --add --push origin https://git.brudilabs.com/andreas/<app>.git
   git remote set-url --add --push origin git@github.com:brudilabs/<app>.git
   ```
4. Fine-grained Personal Access Token auf GitHub: Ressourcen-Eigentümer `brudilabs`, nur die privaten Quell-Repos,
   Berechtigung *Contents: Read-only*.
5. Unter *Settings → Secrets and variables → Actions → Repository secrets* anlegen:
   - `QUELLCODE_TOKEN` – das Token aus Schritt 4
   - `TAURI_SIGNING_PRIVATE_KEY` – Inhalt von `~/.tauri/brudilabs.key`
   - `TAURI_SIGNING_PRIVATE_KEY_PASSWORD` – das Passwort

## Neue Version veröffentlichen

1. Im Quell-Repo `version` in `Cargo.toml` erhöhen, committen, Tag `vX.Y.Z` setzen und pushen.
2. Hier *Actions → Release → Run workflow*: App, Tag und Neuigkeiten angeben.
3. Der Workflow baut Linux + macOS, signiert, legt das Release an und aktualisiert den Katalog
   (bzw. für den Launcher `latest.json`). Installierte Launcher zeigen das Update beim nächsten Start.
4. Bei `content-core` baut er auch den Server und setzt `content-server/version.txt` auf den Tag (nur
   vorwärts, keine Vorabversionen). Admins sehen das Update danach im Client unter *Server*.
   **Nur Server** anhaken, um einen Server-Fix ohne Client-Builds und ohne Katalog-Update zu veröffentlichen
   (eigene Patch-Version, der Client bleibt auf seiner).

### contentCore-Server installieren (VPS)

```sh
mkdir -p ~/repo/content-core/deploy && cd ~/repo/content-core/deploy
# .env mit CC_GEHEIMNIS_SCHLUESSEL und CC_OIDC_AUSSTELLER anlegen (siehe contentCore-README)
curl -fsSLO https://github.com/brudilabs/releases/releases/download/content-server/install.sh
sh install.sh               # neueste Version
sh install.sh --einrichten  # Updates aus dem Client (Cronjob)
```

## Fehlersuche

| Symptom | Ursache / Abhilfe |
|---|---|
| *Quellcode holen*: `unable to update url base from redirection` | Checkout zeigt auf git.brudilabs.com (Authentik-SSO). Der Workflow muss aus dem privaten GitHub-Spiegel bauen; Push-Ziel und `QUELLCODE_TOKEN` prüfen. |
| *Quellcode holen*: `not found` / 401 | Tag nicht gepusht (`git push origin vX.Y.Z`) oder Token ohne Zugriff auf das Repo. |
| *Version prüfen* schlägt fehl | `version` in `Cargo.toml` passt nicht zum Tag. |
| *Einsammeln und signieren* schlägt fehl | Secrets `TAURI_SIGNING_PRIVATE_KEY` / `…_PASSWORD` fehlen oder passen nicht zusammen. |
| Launcher: „Signatur ungültig …“ | Datei beschädigt oder mit anderem Schlüssel signiert; wird verworfen, die installierte Version bleibt. |
| Launcher zeigt Name/Beschreibung alt | Katalog noch nicht neu signiert → Release der App laufen lassen (siehe oben). |
| App startet nicht (Linux, distrobox) | ohne FUSE: der Launcher setzt `APPIMAGE_EXTRACT_AND_RUN=1`; Details in `~/.local/share/brudilabs/logs/launcher.log`. |

Lokal prüfen, ob Katalog und Downloads zum Schlüssel passen: Katalog von
`https://github.com/brudilabs/releases/releases/download/katalog/catalog.json` laden und mit
`launcher_core::katalog::laden` / `signatur::pruefen` gegen `OEFFENTLICHER_SCHLUESSEL` prüfen (so am 2026-10-17 geschehen).

## Weitere App aufnehmen

Privates Repo `brudilabs/<id>` anlegen (Push-Ziel wie oben), `apps/<id>.json` und `apps/<id>.png` anlegen, das Token um das Repo erweitern, `<id>` in `.github/workflows/release.yml` unter `options` ergänzen.
Die `id` muss dem Programmnamen der App entsprechen (Wayland-App-ID, Desktop-Eintrag).
