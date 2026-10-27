"""scripts/record_demo.py with a fake browser and a fake image library: no Playwright, no Chromium, no Pillow.

The fakes log every step, so the test checks the recording script itself: which page it opens, what it clicks and
types, how many frames it keeps and for how long each is shown, and where the GIF goes (tmp_path, never docs/).
"""
import importlib.util
import io
import pathlib
import sys
import types

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]


class FakeFrame:
    def __init__(self, log):
        self.log = log

    def convert(self, mode):
        self.log.append(("convert", mode))
        return self

    def quantize(self, colors, method):
        self.log.append(("quantize", colors, method))
        return self

    def save(self, out, save_all, append_images, duration, loop, optimize):
        self.log.append(("save", out, save_all, len(append_images), list(duration), loop, optimize))
        pathlib.Path(out).write_bytes(b"GIF89a" + b"\0" * 2048)


class FakePage:
    def __init__(self, log):
        self.log = log
        self.mouse = types.SimpleNamespace(move=lambda x, y: log.append(("move", round(x), round(y))))

    def goto(self, url):
        self.log.append(("goto", url))

    def evaluate(self, script, arg=None):
        self.log.append(("click", arg) if arg is not None else ("js", script))

    def wait_for_timeout(self, ms):
        self.log.append(("wait", ms))

    def screenshot(self):
        self.log.append(("screenshot",))
        return b"\x89PNG fake"

    def locator(self, sel):
        self.log.append(("locator", sel))
        return types.SimpleNamespace(bounding_box=lambda: {"x": 100, "y": 50, "width": 766, "height": 300})

    def fill(self, sel, value):
        self.log.append(("fill", sel, value))

    def select_option(self, sel, value):
        self.log.append(("select", sel, value))


@pytest.fixture
def recorder(tmp_path, monkeypatch):
    """The script loaded against the fakes, writing to tmp_path, and the log of what it did."""
    log = []
    page = FakePage(log)

    class Browser:
        def new_page(self, **kw):
            log.append(("new_page", kw))
            return page

        def close(self):
            log.append(("close",))

    class Playwright:
        chromium = types.SimpleNamespace(launch=lambda: log.append(("launch",)) or Browser())

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            log.append(("exit",))

    def open_image(buf):
        assert isinstance(buf, io.BytesIO) and buf.getvalue() == b"\x89PNG fake"     # the screenshot itself
        return FakeFrame(log)

    image = types.SimpleNamespace(open=open_image, Quantize=types.SimpleNamespace(MEDIANCUT="median-cut"))
    pil = types.ModuleType("PIL")
    pil.Image = image
    api = types.ModuleType("playwright.sync_api")
    api.sync_playwright = Playwright
    monkeypatch.setitem(sys.modules, "PIL", pil)
    monkeypatch.setitem(sys.modules, "PIL.Image", image)
    monkeypatch.setitem(sys.modules, "playwright", types.ModuleType("playwright"))
    monkeypatch.setitem(sys.modules, "playwright.sync_api", api)
    spec = importlib.util.spec_from_file_location("record_demo", ROOT / "scripts" / "record_demo.py")
    rd = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rd)
    assert rd.OUT == ROOT / "docs" / "demo.gif"                         # the real target, replaced below
    monkeypatch.setattr(rd, "OUT", tmp_path / "demo.gif")
    return rd, log


def test_the_demo_is_recorded_frame_by_frame_into_one_gif(recorder, tmp_path, capsys):
    rd, log = recorder
    rd.main()
    assert log[0] == ("launch",)
    assert log[1] == ("new_page", {"viewport": {"width": 960, "height": 600}, "device_scale_factor": 1, "color_scheme": "dark"})
    assert log[2] == ("goto", (ROOT / "docs" / "app" / "index.html").as_uri())
    clicks = [arg for kind, *arg in log if kind == "click"]
    assert clicks == [['[data-preset="ipo"]'], ['[data-preset="memo"]'], ["#t-size"], ["#t-check"],
                      ['[data-load="good"]'], ['[data-load="ev"]'], ['[data-load="rating"]']]
    assert [e for e in log if e[0] == "fill"] == [("fill", "#stop", s) for s in ("47", "48", "49")]
    assert ("select", "#conv", "High") in log and ("locator", "#fan svg") in log
    moves = [e for e in log if e[0] == "move"]                         # the crosshair walks right across the chart
    assert [m[1] for m in moves[:3]] == [154 + round(600 * f) for f in (0.25, 0.45, 0.65)] and moves[3] == ("move", 0, 0)
    assert all(m[2] == 200 for m in moves[:3])
    shots = [e for e in log if e[0] == "screenshot"]
    assert len(shots) == 13 and log.count(("convert", "RGB")) == 13 and log.count(("quantize", 128, "median-cut")) == 13
    assert log.index(("close",)) < log.index(("exit",)) < next(i for i, e in enumerate(log) if e[0] == "quantize")
    save = next(e for e in log if e[0] == "save")
    assert save == ("save", tmp_path / "demo.gif", True, 12,
                    [1800, 700, 700, 700, 1900, 1400, 1100, 1100, 1100, 1600, 1500, 1900, 2200], 0, True)
    assert f"{tmp_path / 'demo.gif'} (2 KB, 13 frames)" in capsys.readouterr().out
    assert (tmp_path / "demo.gif").read_bytes().startswith(b"GIF89a")
