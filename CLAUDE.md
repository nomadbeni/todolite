# Plans (todolite) – szabályok AI-nak

Ez a fájl erősebb a `html-app-fejlesztes` skillnél; ahol nem tér ki valamire, a skill érvényes.

## Profil

**Nyilvános** tároló (GitHub Pages, MIT licenc). Személyes app, céges anyag nem kerül ide.

## Felépítés

- Egyetlen fájl: `index.html` (CSS + JS benne), build nincs, közvetlenül szerkeszthető.
- Nincs semmilyen hálózati kérés, külső betűtípus, kép vagy szkript. A CSP meta marad a `<meta charset>` után, változatlan szöveggel (`connect-src 'none'`).
- Mentés: `localStorage` kulcs `plans.weekly.state.v1`; JSON-fájl `app: "plans-weekly-planner"`, `schema: 1`. Sémaváltoztatás előtt szólj a tulajdonosnak.
- Téma: világos + sötét CSS változókkal (`html[data-theme]`); minden színt mindkét témában ellenőrizz, a `theme-color` meta és az `applyTheme()` színe is kövesse.

## Verzió

Minden módosítás verzióemelés (új funkció = minor, javítás = patch), három helyen:
1. lábléc (`Plans vX.Y.Z`),
2. menü „változások” lista (`<summary>` + új `<li>`),
3. `CHANGELOG.md` (dátummal, magyarul).

## Teszt

```
python3 tests/test_plans.py
```

Mind a 4 futás (390 / 1366 px × világos / sötét) legyen hibátlan („MINDEN RENDBEN”). Vizuális változásnál nézd meg a `tests/out/` képernyőképeit is. Tesztet ne gyengíts azért, hogy átmenjen.

## Git

- Új funkció külön ágra, a tulajdonos „mehet” jelzése után kerül a `main`-be. Kis javítás vagy kifejezett kérés mehet közvetlenül a `main`-be.
- Commit szerző: `nomadbeni <29810786+nomadbeni@users.noreply.github.com>`.
- Commit üzenet magyarul, első sor: `Plans heti tervező vX.Y.Z – <rövid leírás>`, a végén egyetlen jelölő sor, pl. `AI-generated: Claude (Anthropic)`. Nincs `Co-Authored-By`, munkamenet-link, e-mail.
- Élesítés: `main`-be olvasztás után a GitHub Pages néhány perc alatt frissül.

## Jelölések, adatok

- A README „MI-jelölés” szakasza (HU + EN) és a lábléc AI-szövege nem távolítható el és nem gyengíthető. A független ellenőrzésről szóló mondatot csak valóban megtörtént, külön munkamenetes ellenőrzés után frissítsd.
- Védett márkát, karaktert, logót, idegen írásjelkészletet ne használj; stílus csak általános hangulatában idézhet meg egy művet.
- Valós személyes adat, e-mail cím, chat-link nem kerül a fájlokba és a commitba; példaadat legyen kitalált.
