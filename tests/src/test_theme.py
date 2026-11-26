"""The theming of the two public pages (docs/app/index.html and docs/index.html).

Each page keeps its tokens in its own <style>: spacing, type and shape on :root, and one colour block per theme, keyed
on a class on <html> (.theme-dark, which is also the :where(:root) fallback, and .theme-light). The page's script lists
the themes in THEMES. These tests hold that structure and WCAG AA:

- every theme in THEMES has a block setting the same tokens as the default, including the shared contract;
- every foreground/background pair the page uses meets AA in every theme (4.5:1 text, 3:1 large text and UI edges),
  read from the tokens, so pairs a DOM scan never sees (a selected row, a failed check, a hover) are covered too;
- no component rule, inline style or chart code carries a raw colour;
- the type is DESIGN.md's: the three self-hosted families from docs/fonts.css, the 3x scale, no banned font anywhere;
- the layout is DESIGN.md's: an 8px rhythm, radius 4px at most, no shadows or glows, nothing centred;
- with JavaScript off the page is dark; the toggle switches and remembers; an unknown saved theme falls back to dark;
- a scan of every visible text node (chart labels included) meets AA in both themes, with the web fonts loaded.

The first four read the files and always run. The browser checks need Playwright's Chromium and skip without it. The
pages and their self-hosted fonts are served through Playwright's routing (no socket), and any other request is answered
with an empty body, so nothing leaves the machine.
"""
import mimetypes
import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
APP = DOCS / "app" / "index.html"
WRITEUP = DOCS / "index.html"

CONTRACT = {
    "--color-bg", "--color-surface", "--color-surface-subtle", "--color-border", "--color-border-strong",
    "--color-text-primary", "--color-text-muted", "--color-text-subtle",
    "--color-accent", "--color-accent-hover", "--color-accent-subtle", "--color-text-on-accent", "--color-danger",
}

ALL_BG = ["bg", "surface", "surface-subtle", "accent-subtle"]
BOXES = ["bg", "surface", "surface-subtle"]     # every background but the chosen row, where these are swapped (see CHOSEN_ROW)
# (foreground, [backgrounds]) as each page actually uses them. "overlay" is the translucent status bar and chart
# readout, laid over the page background.
PAIRS = {
    APP: {
        "text": [
            ("text-primary", ALL_BG), ("text-strong", ALL_BG + ["overlay"]), ("text-muted", ALL_BG + ["overlay"]),
            ("text-subtle", BOXES), ("accent", BOXES + ["overlay"]), ("accent-hover", ALL_BG),
            ("gain", ALL_BG + ["overlay"]), ("loss", ALL_BG + ["overlay"]), ("series-base", ["surface", "overlay"]),
            ("series-pwv", ["surface", "overlay"]), ("warning", ["surface"]), ("danger", ALL_BG), ("code", ["bg"]),
            ("text-on-accent", ["accent", "accent-hover"]), ("text-on-accent-muted", ["accent"]),
            ("text-on-warning", ["warning-fill"]),
        ],
        "ui": [
            ("border-strong", ["bg", "surface"]), ("accent", ["bg", "surface", "surface-subtle"]),
            ("gain", ["surface"]), ("loss", ["surface"]), ("series-base", ["surface"]), ("series-pwv", ["surface"]),
            ("series-neutral", ["surface"]), ("text-strong", ["surface"]),
        ],
    },
    WRITEUP: {
        "text": [
            ("text-primary", ALL_BG), ("bg", ["text-primary"]), ("text-muted", ["bg", "surface", "surface-subtle"]),
            ("text-subtle", ["bg", "surface"]), ("accent", BOXES), ("accent-hover", ["bg"]),
            ("text-on-accent", ["accent", "accent-hover"]), ("danger", ["bg", "surface"]),
        ],
        "ui": [("border-strong", ["bg", "surface"]), ("accent", ["bg", "surface"]), ("text-primary", ["bg"])],
    },
}
# What the pairs above leave out, held by the stylesheet instead (see the end of the AA test). Controls with a
# border-strong edge are filled with bg or surface, never surface-subtle (2.8:1 there in the dark). The app's chosen row
# (accent-subtle) shows its subtle text in muted and its hovered accent in accent-hover; the write-up has no chosen row.
CHOSEN_ROW = ["#cmp tbody tr.on .rank, #cmp tbody tr.on .x { color: var(--color-text-muted); }",
              "#cmp tbody tr.on .pick:hover { color: var(--color-accent-hover); }"]
PAGES = [APP, WRITEUP]
IDS = ["app", "writeup"]
FONTS = DOCS / "fonts.css"
FONT_TOKENS = {"--font-display": '"Bricolage Grotesque", sans-serif', "--font-sans": '"IBM Plex Sans", sans-serif',
               "--font-mono": '"IBM Plex Mono", monospace'}
TYPE_SCALE = {"--text-sm": "13px", "--text-base": "16px", "--text-xl": "48px", "--text-display": "clamp(64px, 14vw, 144px)"}
BANNED = r"\b(?:Inter|Roboto|Open Sans|Arial|system-ui|-apple-system|Segoe UI|Helvetica|JetBrains)\b|fonts\.(?:googleapis|gstatic)"


def read(page):
    return page.read_text(encoding="utf-8")


def style_of(text):
    return text[text.index("<style>") + len("<style>"):text.index("</style>")]


def blocks(css):
    """{theme name: {token: value}} for every .theme-<name> block."""
    out = {}
    for m in re.finditer(r"\.theme-([a-z]+)\s*\{([^}]*)\}", css):
        body = re.sub(r"/\*.*?\*/", "", m.group(2), flags=re.S)
        out[m.group(1)] = dict((k, v.strip()) for k, v in re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", body))
    return out


def themes_of(text):
    m = re.search(r"const THEMES = \[([^\]]*)\]", text)
    assert m, "no THEMES list in the page's script"
    return re.findall(r'"([a-z]+)"', m.group(1))


def rgba(value):
    value = value.strip()
    m = re.fullmatch(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})", value)
    if m:
        h = m.group(1)
        h = "".join(c * 2 for c in h) if len(h) == 3 else h
        return [int(h[i:i + 2], 16) for i in (0, 2, 4)] + [1.0]
    m = re.fullmatch(r"rgba?\(([^)]*)\)", value)
    assert m, "not a colour: %r" % value
    parts = [float(p) for p in m.group(1).replace("/", ",").split(",")]
    return parts[:3] + [parts[3] if len(parts) > 3 else 1.0]


def over(fg, bg):
    """fg laid over an opaque bg."""
    a = fg[3]
    return [fg[i] * a + bg[i] * (1 - a) for i in range(3)] + [1.0]


def luminance(c):
    lin = [v / 255 / 12.92 if v / 255 <= 0.03928 else ((v / 255 + 0.055) / 1.055) ** 2.4 for v in c[:3]]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def ratio(a, b):
    hi, lo = sorted([luminance(a), luminance(b)], reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def colour(tokens, name):
    """A token as an opaque colour: a translucent one is laid over the page background."""
    c = rgba(tokens["--color-" + name])
    return over(c, rgba(tokens["--color-bg"])) if c[3] < 1 else c


def shortfalls(tokens, pairs):
    short = []
    for kind, need in (("text", 4.5), ("ui", 3.0)):
        for fg, bgs in pairs[kind]:
            for bg in bgs:
                r = ratio(colour(tokens, fg), colour(tokens, bg))
                if r < need:
                    short.append("%s %s on %s: %.2f < %.1f" % (kind, fg, bg, r, need))
    return short


# ----------------------------------------------------------------------------- the tokens, read from the files
@pytest.mark.parametrize("page", PAGES, ids=IDS)
def test_every_theme_in_THEMES_has_a_block_with_the_same_tokens(page):
    text = read(page)
    css, names = style_of(text), themes_of(text)
    found = blocks(css)
    assert names[0] == "dark" and "light" in names
    assert re.search(r":where\(:root\),\s*\.theme-dark\s*\{", css), "the default theme must also be the :where(:root) fallback"
    default = set(found["dark"])
    assert CONTRACT <= default, sorted(CONTRACT - default)
    for name in names:
        assert name in found, "THEMES lists %r but the stylesheet has no .theme-%s block" % (name, name)
        assert set(found[name]) == default, (name, sorted(set(found[name]) ^ default))


@pytest.mark.parametrize("page", PAGES, ids=IDS)
def test_every_pair_the_page_uses_meets_AA_in_every_theme(page):
    text = read(page)
    found = blocks(style_of(text))
    for name in themes_of(text):
        assert not shortfalls(found[name], PAIRS[page]), (name, shortfalls(found[name], PAIRS[page]))
    # the pairs the lists leave out, held by the stylesheet (see CHOSEN_ROW)
    css = re.sub(r"/\*.*?\*/", "", style_of(text), flags=re.S)
    rules = re.findall(r"([^{}]+)\{([^{}]*)\}", css)
    for sel, body in rules:
        if "var(--color-border-strong)" in body:
            assert not re.search(r"background(?:-color)?:\s*var\(--color-surface-subtle\)", body), sel
    painted = [sel.strip() for sel, body in rules if re.search(r"background(?:-color)?:\s*var\(--color-accent-subtle\)", body)]
    if page == APP:
        assert painted == ["#cmp tbody tr.on td"] and all(rule in css for rule in CHOSEN_ROW), painted
    else:
        assert painted == [] and "accent-subtle)" not in css.split(".theme-light")[1].split("}", 1)[1], painted


def test_the_contrast_check_catches_a_failing_pair():
    tokens = {"--color-bg": "#ffffff", "--color-text-primary": "#777777", "--color-overlay": "rgba(0, 0, 0, .5)"}
    assert round(ratio(rgba("#777777"), rgba("#fff")), 2) == 4.48
    assert shortfalls(tokens, {"text": [("text-primary", ["bg"])], "ui": []}) == ["text text-primary on bg: 4.48 < 4.5"]
    assert colour(tokens, "overlay")[:3] == [127.5, 127.5, 127.5]          # laid over the white page


@pytest.mark.parametrize("page", PAGES, ids=IDS)
def test_non_colour_tokens_live_on_root_and_colour_only_in_theme_blocks(page):
    css = style_of(read(page))
    root = re.search(r"(?m)^:root\s*\{([^}]*)\}", css).group(1)
    assert "--color-" not in root
    for prefix in ("--space-", "--font-display", "--font-sans", "--font-mono", "--text-", "--leading-", "--weight-", "--radius-"):
        assert prefix in root, prefix
    assert all(int(n) * 4 == int(px) for n, px in re.findall(r"--space-(\d+):\s*(\d+)px", root))
    # DESIGN.md's layout: an 8px rhythm (even N, and only defined steps), radius 4px at most, no shadow or glow, nothing
    # centred. The one exception is the app's 50% LED dot; the inset 2px bars mark a chosen row and are not shadows.
    spaces = set(re.findall(r"--space-(\d+):", root))
    assert spaces and all(int(n) % 2 == 0 for n in spaces), sorted(spaces)
    assert set(re.findall(r"var\(--space-(\d+)\)", css)) <= spaces, sorted(set(re.findall(r"var\(--space-(\d+)\)", css)) - spaces)
    radii = dict(re.findall(r"--radius-([\w-]+):\s*([^;]+);", root))
    assert all(v == "50%" or int(v.rstrip("px")) <= 4 for v in radii.values()), radii
    for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", re.sub(r"/\*.*?\*/", "", css, flags=re.S)):
        sel = sel.strip()
        if "var(--radius-full)" in body:
            assert sel == ".led", sel
        assert all(1 <= int(px) <= 4 for px in re.findall(r"border-radius:\s*(\d+)px", body)), sel
        assert not re.search(r"text-shadow|drop-shadow|(?<!backdrop-)filter:", body), sel
        assert all(s.startswith("inset 2px 0 0") for s in re.findall(r"box-shadow:\s*([^;]+)", body)), sel
        assert "text-align: center" not in body, sel
    declared = dict((k, v.strip()) for k, v in re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", re.sub(r"/\*.*?\*/", "", root, flags=re.S)))
    assert {k: declared.get(k) for k in FONT_TOKENS} == FONT_TOKENS
    assert {k: declared.get(k) for k in TYPE_SCALE} == TYPE_SCALE
    # every family a rule names is one of the three tokens, and display type is only ever 200 or 800
    families = re.findall(r"font-family:\s*([^;}]+)", css)
    assert all(f.strip() in ("var(--font-display)", "var(--font-sans)", "var(--font-mono)", "inherit") for f in families), families
    display = [body for body in re.findall(r"\{([^{}]*var\(--font-display\)[^{}]*)\}", css)]
    assert display
    for body in display:
        weights = [declared["--weight-" + w] for w in re.findall(r"var\(--weight-([\w-]+)\)", body)]
        weights += re.findall(r"font-weight:\s*(\d+)", body)
        assert weights and set(weights) <= {"200", "800"}, body
    # the fonts are self-hosted: one local stylesheet, its files and licences in the repo, and no banned font anywhere
    text = read(page)
    assert not re.findall(BANNED, text), re.findall(BANNED, text)
    href = re.findall(r'<link rel="stylesheet" href="([^"]+)">', text[:text.index("</head>")])
    assert href == [("../" if page == APP else "") + "fonts.css"], href
    assert (page.parent / href[0]).resolve() == FONTS
    faces = FONTS.read_text(encoding="utf-8")
    assert not re.findall(BANNED, faces) and "//" not in re.sub(r"/\*.*?\*/", "", faces, flags=re.S)
    assert set(re.findall(r'font-family:"([^"]+)"', faces)) == {"Bricolage Grotesque", "IBM Plex Sans", "IBM Plex Mono"}
    assert all((FONTS.parent / src).is_file() for src in re.findall(r'url\("([^"]+)"\)', faces))
    assert all((FONTS.parent / "fonts" / lic).is_file() for lic in ("OFL-Bricolage-Grotesque.txt", "OFL-IBM-Plex.txt"))


@pytest.mark.parametrize("page", PAGES, ids=IDS)
def test_components_read_tokens_not_raw_colours(page):
    text = read(page)
    css = style_of(text)
    rest = re.sub(r"(?::where\(:root\),\s*)?\.theme-[a-z]+\s*\{[^}]*\}", "", css)
    rest = re.sub(r"/\*.*?\*/", "", rest, flags=re.S)
    raw = r"#[0-9a-fA-F]{3,8}\b|\brgba?\(|\bhsla?\("
    assert not re.findall(raw, rest), "raw colour in a component rule"
    outside = text[:text.index("<style>")] + text[text.index("</style>"):]       # markup, inline styles, scripts
    assert not re.findall(raw, outside), "raw colour outside the tokens"


@pytest.mark.parametrize("page", PAGES, ids=IDS)
def test_dark_is_in_the_markup_and_the_system_setting_is_not_followed(page):
    text = read(page)
    assert re.search(r'<html lang="en" class="theme-dark">', text)
    assert "prefers-color-scheme" not in text and "data-theme" not in text
    head = text[:text.index("</head>")]
    restore = head.index('localStorage.getItem("theme")')
    assert 'classList.replace("theme-dark", "theme-" + saved)' in head and "/^[a-z]+$/.test(saved)" in head
    assert all(m.start() > restore for m in re.finditer(r'<link rel="stylesheet"|<style>', head)), "restore before the CSS"
    assert re.search(r'<button type="button" class="theme-btn" id="themeBtn" aria-label="Switch to light theme">', text)


# ----------------------------------------------------------------------------- the pages in a browser
SCAN = """() => {
  const parse = (c) => { const n = c.match(/[\\d.]+/g).map(Number); return { rgb: n.slice(0, 3).map((v) => v / 255), a: n.length > 3 ? n[3] : 1 }; };
  const lum = (c) => { const [r, g, b] = parse(c).rgb.map((v) => v <= .03928 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4);
                       return .2126 * r + .7152 * g + .0722 * b; };
  const behind = (el) => { for (let e = el; e; e = e.parentElement) { const bg = getComputedStyle(e).backgroundColor;
                           if (/\\d/.test(bg) && parse(bg).a > .5) return bg; } return getComputedStyle(document.body).backgroundColor; };
  const out = [];
  let seen = 0;
  for (const el of document.querySelectorAll('body *')) {
    if (![...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim())) continue;
    const s = getComputedStyle(el);
    if (s.visibility === 'hidden' || s.display === 'none' || !el.getClientRects().length || el.closest('[hidden]')) continue;
    const fg = el instanceof SVGElement ? s.fill : s.color;       // chart labels are painted with fill
    const size = parseFloat(s.fontSize), big = size >= 24 || (size >= 18.66 && +s.fontWeight >= 700);
    const [L1, L2] = [lum(fg), lum(behind(el))].sort((a, b) => b - a), r = (L1 + .05) / (L2 + .05);
    seen++;
    if (r < (big ? 3 : 4.5)) out.push(el.tagName + '.' + (el.getAttribute('class') || '') + ' ' + r.toFixed(2) + ' "' + el.textContent.trim().slice(0, 30) + '"');
  }
  return { seen, bad: [...new Set(out)] };
}"""
LOADED = """() => document.fonts.ready.then(() => [
  [...new Set([...document.fonts].filter((f) => f.status === 'loaded').map((f) => f.family.replace(/"/g, '')))].sort(),
  ['800 48px "Bricolage Grotesque"', '400 16px "IBM Plex Sans"', '600 16px "IBM Plex Sans"', '400 13px "IBM Plex Mono"']
    .every((f) => document.fonts.check(f))])"""
FAMILIES = ["Bricolage Grotesque", "IBM Plex Mono", "IBM Plex Sans"]
THEME = "() => (document.documentElement.className.match(/(?:^|\\s)theme-(\\S+)/) || [])[1]"
BASE = "http://ipo.test/"


@pytest.fixture(scope="module")
def browser():
    sync_api = pytest.importorskip("playwright.sync_api")
    pw = sync_api.sync_playwright().start()
    try:
        b = pw.chromium.launch()
    except Exception as e:                       # Playwright without its browser
        pw.stop()
        pytest.skip("Chromium for Playwright is not installed: %s" % str(e).splitlines()[0])
    yield b
    b.close()
    pw.stop()


def serve(route):
    url = route.request.url
    if not url.startswith(BASE):                  # nothing else is requested; if it were, nothing leaves the machine
        return route.fulfill(status=200, body="", content_type="text/plain")
    f = DOCS / url[len(BASE):].split("?")[0].split("#")[0]
    f = f / "index.html" if f.is_dir() else f
    if not f.is_file():
        return route.fulfill(status=404, body="")
    return route.fulfill(status=200, body=f.read_bytes(), content_type=mimetypes.guess_type(f.name)[0])


def open_page(browser, path, saved=None, js=True, width=1280):
    ctx = browser.new_context(java_script_enabled=js, viewport={"width": width, "height": 900}, color_scheme="light")
    ctx.route("**/*", serve)
    page = ctx.new_page()
    page.errors = []
    page.on("pageerror", lambda e: page.errors.append(str(e)))
    page.on("console", lambda m: page.errors.append(m.text) if m.type == "error" else None)
    if saved is not None:
        page.add_init_script("localStorage.setItem('theme', %r)" % saved)
    page.goto(BASE + path)
    if js and path.startswith("app"):
        page.wait_for_function("() => document.querySelector('#fan svg') && document.querySelectorAll('#nyse-list li').length > 0")
    return ctx, page


def dark_bg(page):
    return "rgb(%d, %d, %d)" % tuple(rgba(blocks(style_of(read(page)))["dark"]["--color-bg"])[:3])


@pytest.mark.parametrize("path, file", [("app/", APP), ("", WRITEUP)], ids=IDS)
def test_without_javascript_the_page_is_dark(browser, path, file):
    ctx, page = open_page(browser, path, js=False)
    seen = page.evaluate("[document.documentElement.className, getComputedStyle(document.body).backgroundColor, "
                         "getComputedStyle(document.documentElement).colorScheme, document.getElementById('themeBtn').getClientRects().length]")
    assert seen == ["theme-dark", dark_bg(file), "dark", 0]       # dark, and no toggle that could not work
    assert not page.evaluate(SCAN)["bad"]
    ctx.close()


@pytest.mark.parametrize("path, file", [("app/", APP), ("", WRITEUP)], ids=IDS)
def test_the_toggle_switches_and_remembers_and_an_unknown_theme_falls_back_to_dark(browser, path, file):
    ctx, page = open_page(browser, path)
    assert page.evaluate(THEME) == "dark" and page.get_attribute("#themeBtn", "aria-label") == "Switch to light theme"
    page.click("#themeBtn")
    page.wait_for_function(THEME.replace("() =>", "() => 'light' ===", 1))
    light = "rgb(%d, %d, %d)" % tuple(rgba(blocks(style_of(read(file)))["light"]["--color-bg"])[:3])
    assert page.evaluate("getComputedStyle(document.body).backgroundColor") == light
    assert page.get_attribute("#themeBtn", "aria-label") == "Switch to dark theme"
    assert page.evaluate("localStorage.getItem('theme')") == "light"
    page.reload()
    assert page.evaluate(THEME) == "light"
    page.click("#themeBtn")
    assert page.evaluate(THEME) == "dark" and page.evaluate("localStorage.getItem('theme')") == "dark"
    assert not page.errors, page.errors
    ctx.close()
    ctx, page = open_page(browser, path, saved="sepia")              # a theme that does not exist (or no longer does)
    assert page.evaluate("[document.documentElement.className.match(/theme-\\S+/g).join(), getComputedStyle(document.body).backgroundColor]") \
        == ["theme-dark", dark_bg(file)]
    assert page.get_attribute("#themeBtn", "aria-label") == "Switch to light theme"
    ctx.close()


def test_the_app_charts_follow_the_theme(browser):
    ctx, page = open_page(browser, "app/", saved="light")
    tokens = blocks(style_of(read(APP)))["light"]
    fills = page.evaluate("() => [...document.querySelectorAll('#fan text')].map((t) => t.getAttribute('fill'))")
    assert tokens["--color-gain"] in fills and tokens["--color-text-muted"] in fills
    page.click("#themeBtn")
    page.wait_for_function("(c) => [...document.querySelectorAll('#fan text')].some((t) => t.getAttribute('fill') === c)",
                           arg=blocks(style_of(read(APP)))["dark"]["--color-gain"])
    ctx.close()


@pytest.mark.parametrize("theme", ["dark", "light"])
def test_every_visible_text_meets_AA_in_the_app(browser, theme):
    ctx, page = open_page(browser, "app/", saved=theme)
    assert page.evaluate(THEME) == theme
    scans = {"project": page.evaluate(SCAN)}
    page.click("#tpl-fill")                                          # the TEMPLATE chip
    page.wait_for_function("() => !document.getElementById('tpl').hidden")
    scans["project, template"] = page.evaluate(SCAN)
    page.evaluate("() => document.getElementById('fan').scrollIntoView({ block: 'center' })")
    box = page.locator("#fan svg").bounding_box()                    # the readout under the pointer (a hover redraws
    page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)   # the chart, so move the mouse)
    page.wait_for_function("() => !document.querySelector('.readout span').textContent.startsWith('+12')")
    scans["project, hover"] = page.evaluate(SCAN)
    page.fill("#pj-bull-p", "40")                                    # probabilities that do not add up: an error
    page.wait_for_function("() => document.getElementById('pj-sum').classList.contains('bad') && !!document.querySelector('#fan .err')")
    scans["project, error"] = page.evaluate(SCAN)
    page.click("#t-size")
    page.fill("#entry", "40")                                        # a stop above the entry: an error message
    page.wait_for_function("() => !!document.querySelector('#result .err')")
    scans["size, error"] = page.evaluate(SCAN)
    page.fill("#entry", "50")
    page.wait_for_function("() => !!document.querySelector('#result .big')")
    scans["size"] = page.evaluate(SCAN)
    page.click("#t-check")
    page.click("[data-load=rating]")                                 # a failed check with its detail
    page.wait_for_function("() => document.getElementById('score').classList.contains('bad')")
    scans["check, failing"] = page.evaluate(SCAN)
    for name, scan in scans.items():
        assert scan["seen"] > 40 and not scan["bad"], (theme, name, scan["bad"])
    assert page.evaluate(LOADED) == [FAMILIES, True]                 # the self-hosted fonts, not a fallback
    assert not page.errors, page.errors
    ctx.close()


@pytest.mark.parametrize("theme", ["dark", "light"])
def test_every_visible_text_meets_AA_in_the_writeup(browser, theme):
    ctx, page = open_page(browser, "", saved=theme)
    assert page.evaluate(THEME) == theme
    scan = page.evaluate(SCAN)
    assert scan["seen"] > 40 and not scan["bad"], scan["bad"]
    assert page.evaluate(LOADED) == [FAMILIES, True]
    assert not page.errors, page.errors
    ctx.close()


@pytest.mark.parametrize("path", ["app/", ""], ids=IDS)
def test_no_sideways_scroll_on_a_phone(browser, path):
    ctx, page = open_page(browser, path, width=390)
    assert page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth") <= 0
    ctx.close()
