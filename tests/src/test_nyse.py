"""The NYSE list behind the demo's picker (docs/app/nyse.json) and the SIC-to-sector map that builds it."""
import json
import pathlib
import re
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import build_nyse  # noqa: E402

DATA = json.loads((ROOT / "docs" / "app" / "nyse.json").read_text(encoding="utf-8"))


def test_sic_codes_map_to_sectors():
    cases = {"2834": "Health Care", 3841: "Health Care", 8062: "Health Care", 7372: "Technology", 3674: "Technology",
             6021: "Financials", 6798: "Real Estate", 6512: "Real Estate", 1311: "Energy", 2911: "Energy", 4911: "Utilities",
             4953: "Industrials", 3711: "Consumer Discretionary", 3721: "Industrials", 2080: "Consumer Staples",
             2844: "Consumer Staples", 5411: "Consumer Staples", 5331: "Consumer Discretionary", 4813: "Communication",
             2711: "Communication", 2800: "Materials", 1040: "Materials", 9995: "Other", None: "Other", "": "Other"}
    for sic, want in cases.items():
        assert build_nyse.sic_sector(sic) == want, (sic, build_nyse.sic_sector(sic), want)


def test_industry_names_are_unescaped_and_readable():
    assert build_nyse.industry("FIRE, MARINE &amp;amp; CASUALTY INSURANCE") == "Fire, Marine & Casualty Insurance"
    assert build_nyse.industry("SERVICES-PREPACKAGED SOFTWARE") == "Services-Prepackaged Software"
    assert build_nyse.industry(None) == ""


def test_every_sector_the_map_can_give_is_a_known_one():
    assert {s for _, _, s in build_nyse.SIC_RANGES} | {"Other"} <= set(build_nyse.SECTORS)
    for code in range(0, 10000, 7):
        assert build_nyse.sic_sector(code) in build_nyse.SECTORS


def test_a_failed_lookup_is_retried_next_run_not_cached():
    calls = {}

    def lookup(cik):
        calls[cik] = calls.get(cik, 0) + 1
        if cik == 2:
            raise OSError("throttled")
        return [str(6000 + cik), "SOME INDUSTRY"]

    cache = {}
    failed = build_nyse.look_up_all([1, 2, 3], lookup, cache, interval=0, workers=2, retries=3, backoff=0)
    assert failed == [2] and set(cache) == {"1", "3"} and calls[2] == 3       # three tries, then left for the next run
    assert build_nyse.look_up_all([2], lambda cik: ["6798", "REIT"], cache, interval=0, backoff=0) == []
    assert cache["2"] == ["6798", "REIT"]


def test_rows_are_sorted_with_sector_and_readable_industry():
    fields = {"cik": 0, "name": 1, "ticker": 2}
    rows = build_nyse.rows_for([[7, "Zed Co", "ZED"], [5, "Abc Inc", "ABC"], [9, "No Sic", "NOS"]], fields,
                               {"7": ["4911", "ELECTRIC SERVICES"], "5": ["7372", "SERVICES-PREPACKAGED SOFTWARE"]})
    assert rows == [["ABC", "Abc Inc", 5, "Technology", "Services-Prepackaged Software"], ["NOS", "No Sic", 9, "Other", ""],
                    ["ZED", "Zed Co", 7, "Utilities", "Electric Services"]]


def test_the_list_is_the_whole_nyse_and_well_formed():
    rows, f = DATA["rows"], {k: i for i, k in enumerate(DATA["fields"])}
    assert DATA["fields"] == ["ticker", "name", "cik", "sector", "industry"] and DATA["as_of"]
    assert len(rows) > 2500                                    # the SEC lists about 3,300 NYSE tickers
    tickers = [r[f["ticker"]] for r in rows]
    assert tickers == sorted(tickers)
    assert all(isinstance(r[f["cik"]], int) and r[f["cik"]] > 0 and r[f["name"]] for r in rows)
    assert {r[f["sector"]] for r in rows} <= set(build_nyse.SECTORS)
    with_sector = sum(r[f["sector"]] != "Other" for r in rows)
    assert with_sector > 0.8 * len(rows)                        # nearly every operating company has a SIC code
    assert not any("&amp;" in r[f["industry"]].lower() for r in rows)
    by = {r[f["ticker"]]: r for r in rows}
    for t, sector in (("JPM", "Financials"), ("LLY", "Health Care"), ("XOM", "Energy")):
        assert t in by and by[t][f["sector"]] == sector, (t, by.get(t))


def test_requests_start_an_interval_apart(monkeypatch):
    waits = []
    monkeypatch.setattr(build_nyse.time, "sleep", waits.append)                # nothing really waits
    cache = {}
    assert build_nyse.look_up_all([1, 2, 3], lambda cik: ["7372", "X"], cache, interval=10, workers=1) == []
    assert len(waits) == 2 and 0 < waits[0] <= 10 < waits[1] <= 20       # the first starts at once, then 10 s apart
    assert set(cache) == {"1", "2", "3"}


ATOM = ("<feed><company-info><assigned-sic>4911</assigned-sic>"
        "<assigned-sic-desc> ELECTRIC SERVICES </assigned-sic-desc></company-info></feed>")


def test_sic_of_reads_the_code_and_description_from_the_edgar_header():
    seen = []

    def get(url, headers):
        seen.append((url, headers))
        return ATOM
    assert build_nyse.sic_of(1234, get, {"User-Agent": "me x@y.z"}) == ["4911", "ELECTRIC SERVICES"]
    url, headers = seen[0]
    assert "CIK=0000001234&" in url and "output=atom" in url and headers == {"User-Agent": "me x@y.z"}
    assert build_nyse.sic_of(1, lambda url, headers: "<feed></feed>", {}) == [None, None]   # no SIC on file


@pytest.fixture
def sec(tmp_path, monkeypatch):
    """main() against a fake SEC: the ticker list and EDGAR headers come from dicts, the files go to tmp_path."""
    import ipo_bot
    import tools
    monkeypatch.setattr(build_nyse, "OUT", tmp_path / "nyse.json")
    monkeypatch.setattr(build_nyse, "CACHE", tmp_path / "bench_data" / "nyse_sic.json")
    monkeypatch.setattr(build_nyse.time, "sleep", lambda s: None)
    monkeypatch.setattr(ipo_bot, "load_env", lambda: None)
    monkeypatch.setattr(tools, "_sec_headers", lambda: {"User-Agent": "Test test@example.com"})
    tickers = {"fields": ["cik", "name", "ticker", "exchange"], "data": [
        [7, "Zed Co", "ZED", "NYSE"], [5, "Abc Inc", "ABC", "NYSE"], [5, "Abc Inc", "ABC-PA", "NYSE"],
        [9, "Nas Co", "NAS", "Nasdaq"], [11, "No Ticker", "", "NYSE"], [13, "Flaky Co", "FLK", "NYSE"]]}
    state = {"down": {13}, "asked": []}

    def get(url, headers):
        assert headers == {"User-Agent": "Test test@example.com"}
        if url.endswith("company_tickers_exchange.json"):
            return json.dumps(tickers)
        cik = int(re.search(r"CIK=(\d+)", url).group(1))
        state["asked"].append(cik)
        if cik in state["down"]:
            raise tools.ToolError("HTTP 503 from www.sec.gov")
        return {7: ATOM, 5: ATOM.replace("4911", "7372").replace("ELECTRIC SERVICES", "SERVICES-PREPACKAGED SOFTWARE"),
                13: ATOM.replace("4911", "6021").replace("ELECTRIC SERVICES", "NATIONAL COMMERCIAL BANKS")}[cik]
    monkeypatch.setattr(tools, "_get", get)
    return state


def test_main_writes_the_nyse_list_and_a_rerun_retries_only_what_failed(sec, tmp_path, capsys):
    build_nyse.main()
    out = capsys.readouterr().out
    assert "4 NYSE tickers, 3 companies; 3 to look up" in out                 # Nasdaq and the blank ticker are left out
    assert "1 companies could not be looked up" in out and "CIK 13: HTTP 503" in out
    assert sorted(sec["asked"]) == [5, 7, 13, 13, 13]                          # three tries for the one that is down
    data = json.loads((tmp_path / "nyse.json").read_text(encoding="utf-8"))
    assert data["fields"] == ["ticker", "name", "cik", "sector", "industry"] and data["as_of"]
    assert data["rows"] == [["ABC", "Abc Inc", 5, "Technology", "Services-Prepackaged Software"],
                            ["ABC-PA", "Abc Inc", 5, "Technology", "Services-Prepackaged Software"],
                            ["FLK", "Flaky Co", 13, "Other", ""],
                            ["ZED", "Zed Co", 7, "Utilities", "Electric Services"]]
    cache = json.loads((tmp_path / "bench_data" / "nyse_sic.json").read_text(encoding="utf-8"))
    assert cache == {"5": ["7372", "SERVICES-PREPACKAGED SOFTWARE"], "7": ["4911", "ELECTRIC SERVICES"]}
    sec["down"].clear()
    sec["asked"].clear()
    build_nyse.main()                                                          # the rerun starts from the cache
    out = capsys.readouterr().out
    assert "1 to look up" in out and "could not be looked up" not in out and sec["asked"] == [13]
    assert "4 tickers" in out
    rows = json.loads((tmp_path / "nyse.json").read_text(encoding="utf-8"))["rows"]
    assert ["FLK", "Flaky Co", 13, "Financials", "National Commercial Banks"] in rows
