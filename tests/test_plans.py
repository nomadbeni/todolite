"""Plans – füstteszt Playwrighttal.

Futtatás:  python3 tests/test_plans.py
Képernyőképek: tests/out/ (nem kerül a tárolóba)
"""
import json, pathlib, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
URL = (ROOT / "index.html").as_uri()
OUT = ROOT / "tests" / "out"
OUT.mkdir(exist_ok=True)
fails = []


def check(cond, msg):
    print(("OK   " if cond else "HIBA ") + msg)
    if not cond:
        fails.append(msg)


def run(p, width, height, scheme):
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": width, "height": height}, color_scheme=scheme,
                        has_touch=width < 600, accept_downloads=True)
    page = ctx.new_page()
    errors, requests = [], []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("console", lambda m: m.type == "error" and errors.append(m.text))
    page.on("request", lambda r: not r.url.startswith(("file:", "data:", "blob:")) and requests.append(r.url))
    page.goto(URL)
    tag = f"{width}-{scheme}"

    theme = page.evaluate("document.documentElement.dataset.theme")
    check(theme == scheme, f"[{tag}] téma követi a rendszert ({theme})")

    # sor hozzáadása, szöveg, Enter új sort ad
    page.click('[data-add="now"]')
    page.keyboard.type("Bevásárlás <b>x</b>")
    page.keyboard.press("Enter")
    page.keyboard.type("Edzés")
    rows = page.locator('#list-now .task-row')
    check(rows.count() == 2, f"[{tag}] Enter új sort ad ({rows.count()})")
    check(page.locator("#list-now b").count() == 0, f"[{tag}] a szöveg escape-elve")

    # kipipálás
    page.locator('#list-now .check').first.click()
    check(page.locator('#list-now .task-row.is-done').count() == 1, f"[{tag}] kipipálás működik")
    check(page.text_content('#cnt-now') == "1/2", f"[{tag}] számláló 1/2")

    # hosszú szöveg sortörése
    page.click('[data-add="remember"]')
    page.keyboard.type("Nagyon hosszú emlékeztető " * 6)
    h = page.evaluate("document.querySelector('#list-remember .task-input').offsetHeight")
    check(h > 50, f"[{tag}] hosszú szöveg több sorba tördel ({h}px)")

    # később -> most áthelyezés
    page.click('[data-add="later"]')
    page.keyboard.type("Ötlet")
    page.click('[data-add="day-2"]')
    check(page.is_visible("#laterSheet"), f"[{tag}] későbbre-választó megnyílik")
    page.click('#laterChoices .pick')
    check(page.locator('[data-scope="day-2"]').count() == 1 and page.locator('#list-later .task-row').count() == 0,
          f"[{tag}] áthelyezés a későbbre listából")

    # törlés + visszavonás
    page.locator('#list-now .task-row').nth(1).hover()
    page.locator('#list-now .remove').nth(1).click()
    check(rows.count() == 1, f"[{tag}] törlés")
    page.click("#toastUndo")
    check(rows.count() == 2, f"[{tag}] visszavonás")

    # újratöltés -> megmarad
    page.reload()
    check(page.locator('#list-now .task-row').count() == 2, f"[{tag}] újratöltés után megmarad")
    check(page.locator('#list-now .is-done').count() == 1, f"[{tag}] kész állapot megmarad")

    # hétváltás
    page.click('[data-act="next"]')
    check(page.locator('#list-now .task-row').count() == 0 and page.is_visible("#todayBtn"), f"[{tag}] következő hét üres, visszagomb látszik")
    page.click("#todayBtn")
    check(page.locator('#list-now .task-row').count() == 2, f"[{tag}] vissza a mai hétre")
    check(page.locator(".day.today").count() == 1, f"[{tag}] mai nap kiemelve")

    # vízszintes görgetés, gombok a képernyőn
    sw = page.evaluate("document.documentElement.scrollWidth")
    check(sw <= width, f"[{tag}] nincs vízszintes görgetés ({sw})")
    off = page.evaluate(f"[...document.querySelectorAll('button')].filter(b=>b.offsetParent&&(b.getBoundingClientRect().right>{width}+1||b.getBoundingClientRect().left<-1)).length")
    check(off == 0, f"[{tag}] minden gomb a képernyőn belül")
    small = page.evaluate("[...document.querySelectorAll('button')].filter(b=>b.offsetParent).map(b=>b.getBoundingClientRect()).filter(r=>r.height<36||r.width<34).length")
    check(small == 0, f"[{tag}] érintési célok elég nagyok ({small} kicsi)")
    fs = page.evaluate("parseFloat(getComputedStyle(document.querySelector('.task-input')).fontSize)")
    if width < 600:
        check(fs >= 16, f"[{tag}] mezők betűmérete ≥16px (iOS nem nagyít) ({fs})")
    page.screenshot(path=str(OUT / f"{tag}.png"), full_page=True)

    # menü + téma váltás
    page.click('[data-act="menu"]')
    page.screenshot(path=str(OUT / f"{tag}-menu.png"))
    other = "light" if scheme == "dark" else "dark"
    page.click(f'[data-theme-set="{other}"]')
    check(page.evaluate("document.documentElement.dataset.theme") == other, f"[{tag}] kézi téma")
    page.keyboard.press("Escape")
    check(not page.is_visible("#menuSheet"), f"[{tag}] Escape bezár")
    page.click('[data-act="menu"]'); page.click(f'[data-theme-set="auto"]'); page.keyboard.press("Escape")

    # JSON oda-vissza
    before = page.evaluate("localStorage.getItem('plans.weekly.state.v1')")
    page.click('[data-act="menu"]')
    with page.expect_download() as d:
        page.click('#menuSheet [data-act="export"]')
    path = d.value.path()
    payload = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    check(payload["app"] == "plans-weekly-planner" and payload["schema"] == 1, f"[{tag}] JSON fejléc")
    page.evaluate("localStorage.clear()"); page.reload()
    page.on("dialog", lambda dlg: dlg.accept())
    page.set_input_files("#importFile", path)
    page.wait_for_timeout(300)
    after = page.evaluate("localStorage.getItem('plans.weekly.state.v1')")
    check(json.loads(after)["weeks"] == json.loads(before)["weeks"], f"[{tag}] JSON mentés → betöltés azonos")

    # hibás JSON és rossz app
    bad = OUT / "bad.json"; bad.write_text("{nem json", encoding="utf-8")
    page.set_input_files("#importFile", str(bad)); page.wait_for_timeout(200)
    check(page.locator('#list-now .task-row').count() == 2, f"[{tag}] hibás JSON nem rontja el")
    evil = OUT / "evil.json"
    evil.write_text(json.dumps({"app": "plans-weekly-planner", "schema": 1, "data": {
        "weeks": {"__proto__": {"x": 1}, "2026-11-23": {"now": [{"id": "\"><img src=x onerror=alert(1)>", "text": "<img src=x onerror=alert(1)>"}]}},
        "later": [{"text": "<script>alert(1)</script>"}], "theme": "javascript:alert(1)"}}), encoding="utf-8")
    page.set_input_files("#importFile", str(evil)); page.wait_for_timeout(200)
    check(page.locator("img").count() == 0 and page.locator("main script").count() == 0, f"[{tag}] kártékony JSON nem fut")

    # sérült localStorage
    page.evaluate("localStorage.setItem('plans.weekly.state.v1','{rossz')"); page.reload()
    check(page.locator("#list-now").count() == 1, f"[{tag}] sérült mentésre nem omlik össze")

    # offline HTML: nem tartalmaz felhasználói adatot
    page.evaluate("localStorage.clear()"); page.reload()
    page.click('[data-add="later"]'); page.keyboard.type("TITKOS-SZOVEG")
    page.click('[data-act="menu"]')
    with page.expect_download() as d2:
        page.click('#menuSheet [data-act="download"]')
    html = pathlib.Path(d2.value.path()).read_text(encoding="utf-8")
    check("TITKOS-SZOVEG" not in html and '<html lang="hu">' in html, f"[{tag}] offline HTML tiszta másolat")

    check(not errors, f"[{tag}] nincs konzolhiba {errors}")
    check(not requests, f"[{tag}] nincs külső kérés {requests}")
    b.close()


with sync_playwright() as p:
    for w, h in ((390, 844), (1366, 900)):
        for s in ("light", "dark"):
            run(p, w, h, s)

print("\n" + ("MINDEN RENDBEN" if not fails else f"{len(fails)} HIBA"))
sys.exit(1 if fails else 0)
