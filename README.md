# Plans – heti tervező

Egyszerű, telefonra szabott heti tervező egyetlen HTML-fájlban. Négy rész van benne: **Most**, **Későbbre**, **Ne felejtsd el** és **Az én hetem** (hétfőtől péntekig, plusz a hétvége).

**Megnyitás:** a tároló GitHub Pages oldalán (`https://<felhasználónév>.github.io/todolite/`), vagy töltsd le az `index.html`-t, és nyisd meg böngészőben. Internet nélkül is működik.

## Tudnivalók

- Az adatok csak a böngésződben (localStorage) tárolódnak. Nem kerülnek fel szerverre, nincs fiók, süti vagy követés.
- Más eszközre a menü **JSON mentése** és **JSON betöltése** gombjával viheted át az adatokat. Időnként érdemes menteni.
- A **Minden adat törlése** menüpont megerősítés után törli az összes feladatot ebben a böngészőben; előtte érdemes JSON-mentést készíteni.
- A **HTML letöltése** gomb offline példányt ad az appból.
- Telefonon a böngésző „Hozzáadás a kezdőképernyőhöz” menüjével appként is elindítható.

## Használat

- Koppints az **Új sor** gombra, írd be a feladatot. Az Enter új sort nyit, üres soron a Backspace törli a sort (a törlés visszavonható).
- A kör megérintésével kipipálod a feladatot.
- A × törli a sort; a törlés néhány másodpercig visszavonható.
- Ha a **Későbbre** listában van elem, a Most vagy egy nap új sora előbb felajánlja, hogy onnan hozz át valamit.
- A nyilakkal hetet válthatsz; a **Vissza a mai hétre** gomb visszavisz.

## Fejlesztés

Egyetlen fájl (`index.html`), külső függőség nélkül. Teszt (Playwright, Python):

```
python3 tests/test_plans.py
```

A változások listája: [CHANGELOG.md](CHANGELOG.md).

## Licenc

MIT, lásd: [LICENSE](LICENSE).

## MI-jelölés

A tárolóban minden kódot, alkalmazást és leírást teljes egészében mesterséges intelligencia készített (az első változatot ChatGPT, OpenAI; az átdolgozást, a teszteket és a leírást Claude Opus 5.5, Anthropic). Független, külön munkamenetben végzett AI-ellenőrzés 2026-11-24-én történt (Mistral Vibe / GLM); az 1.1.1-es javításokat a tulajdonos kérésére ugyanez a munkamenet készítette.

All code, apps and documentation in this repository were created entirely by AI (first version: ChatGPT, OpenAI; rework, tests and documentation: Claude Opus 5.5, Anthropic). An independent AI review in a separate session was done on 2026-11-24 (Mistral Vibe / GLM); the 1.1.1 fixes were made by the same session at the owner's request.
