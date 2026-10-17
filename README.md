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

`apps/<id>.json` enthält Name, Beschreibung und das private Quell-Repo `brudilabs/<id>`; `apps/<id>.png` das Symbol im Launcher.

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

## Weitere App aufnehmen

Privates Repo `brudilabs/<id>` anlegen (Push-Ziel wie oben), `apps/<id>.json` und `apps/<id>.png` anlegen, das Token um das Repo erweitern, `<id>` in `.github/workflows/release.yml` unter `options` ergänzen.
Die `id` muss dem Programmnamen der App entsprechen (Wayland-App-ID, Desktop-Eintrag).
