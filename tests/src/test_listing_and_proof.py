"""Identity, listing status, freshness and the proof trace, offline: SEC responses are faked at tools._get."""
import json
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))

import proof  # noqa: E402
import tools  # noqa: E402
import verify  # noqa: E402

UA = "Test test@example.com"


@pytest.fixture(autouse=True)
def sec(monkeypatch):
    monkeypatch.setenv("SEC_USER_AGENT", UA)
    monkeypatch.setitem(tools.AS_OF, "date", None)


def fake_get(monkeypatch, pages):
    """tools._get answering from {url substring: object or exception}; the URLs asked for are kept."""
    calls = []

    def get(url, headers=None):
        calls.append(url)
        for part, obj in pages.items():
            if part in url:
                if isinstance(obj, Exception):
                    raise obj
                return obj if isinstance(obj, str) else json.dumps(obj)
        raise AssertionError(f"unexpected url {url}")
    monkeypatch.setattr(tools, "_get", get)
    return calls


def recent(rows):
    """Submissions 'recent' columns from (form, filed, items) rows."""
    return {"form": [r[0] for r in rows], "filingDate": [r[1] for r in rows], "items": [r[2] for r in rows],
            "accessionNumber": [f"0000000001-26-{i:06d}" for i in range(len(rows))],
            "primaryDocument": [f"d{i}.htm" for i in range(len(rows))]}


# ----------------------------------------------------------------------------- tools: identity and listing

def test_edgar_filings_carries_the_exchanges_and_former_names(monkeypatch):
    sub = {"name": "Co", "tickers": ["CO"], "exchanges": ["NYSE"],
           "formerNames": [{"name": "Old Co", "from": "2001-01-01T00:00:00.000Z", "to": "2020-05-01T00:00:00.000Z"}, {}],
           "filings": {"recent": recent([("10-K", "2026-02-01", "")])}}
    fake_get(monkeypatch, {"CIK0000000001.json": sub})
    data = json.loads(tools.edgar_filings("1"))["data"]
    assert data["exchanges"] == ["NYSE"]
    assert data["former_names"] == [{"name": "Old Co", "from": "2001-01-01", "to": "2020-05-01"},
                                    {"name": None, "from": "", "to": ""}]


def test_edgar_listing_finds_the_last_years_listing_events_and_a_foreign_filers_adr_ratio(monkeypatch):
    monkeypatch.setattr(tools, "_now", lambda: "2026-10-15T12:00:00Z")
    rows = [("8-K", "2026-09-01", "3.01,9.01"), ("8-K", "2026-08-01", "2.02"), ("25-NSE", "2026-05-01", ""),
            ("8-A12B", "2025-01-01", ""), ("20-F", "2026-04-01", "")]        # the 8-A is more than a year old
    sub = {"name": "Foreign Co", "tickers": ["FC"], "exchanges": ["NYSE"], "filings": {"recent": recent(rows)}}
    search = {"hits": {"hits": [
        {"_id": "0000000001-24-000001:old.htm", "_source": {"form": "20-F", "file_date": "2024-04-01"}},
        {"_id": "0000000001-26-000004:f20.htm", "_source": {"form": "20-F", "file_date": "2026-04-01"}}]}}
    calls = fake_get(monkeypatch, {"CIK0000000001.json": sub, "efts.sec.gov": search})
    out = json.loads(tools.edgar_listing("1"))
    data = out["data"]
    assert data["foreign_private_issuer"] is True and data["listing_events_since"] == "2025-10-15"
    assert [(e["form"], e["filed"]) for e in data["listing_events"]] == [("8-K", "2026-09-01"), ("25-NSE", "2026-05-01")]
    assert data["listing_events"][0]["filing"].endswith("/1/000000000126000000/0000000001-26-000000-index.htm")
    assert [a["filed"] for a in data["adr_ratio_sources"]] == ["2026-04-01", "2024-04-01"]     # newest first
    assert data["adr_ratio_sources"][0]["document"] == "https://www.sec.gov/Archives/edgar/data/1/000000000126000004/f20.htm"
    assert "read each listing event" in out["note"] and "ADR ratio" in out["note"] and "ISIN" in out["note"]
    assert "ciks=0000000001" in calls[1] and "enddt" not in calls[1]


def test_edgar_listing_in_a_backtest_stops_at_its_date_and_says_when_search_fails(monkeypatch):
    tools.AS_OF["date"] = "2026-06-01"
    rows = [("25-NSE", "2026-09-01", ""), ("40-F", "2026-03-01", "")]
    sub = {"name": "Co", "filings": {"recent": recent(rows)}}
    calls = fake_get(monkeypatch, {"CIK0000000001.json": sub, "efts.sec.gov": tools.ToolError("HTTP 500")})
    out = json.loads(tools.edgar_listing("1"))
    assert out["data"]["listing_events"] == [] and out["data"]["listing_events_since"] == "2025-06-01"
    assert out["data"]["adr_ratio_sources"] == [] and "full-text search failed (HTTP 500)" in out["note"]
    assert "no delisting" in out["note"] and "enddt=2026-06-01" in calls[1]


def test_edgar_listing_for_a_domestic_filer_searches_no_adr_filings(monkeypatch):
    monkeypatch.setattr(tools, "_now", lambda: "2026-10-15T12:00:00Z")
    sub = {"name": "Us Co", "tickers": ["US"], "exchanges": ["Nasdaq"], "filings": {"recent": recent([("10-K", "2026-02-01", "")])}}
    calls = fake_get(monkeypatch, {"CIK0000000001.json": sub})
    data = json.loads(tools.edgar_listing("1"))["data"]
    assert data["foreign_private_issuer"] is False and "adr_ratio_sources" not in data and len(calls) == 1


# ----------------------------------------------------------------------------- tools: figures

def test_edgar_financials_names_the_filing_of_every_figure_and_warns_when_a_newer_report_is_missing(monkeypatch):
    vals = [{"start": "2025-01-01", "end": "2025-12-31", "val": 10, "form": "10-K", "filed": "2026-02-01",
             "accn": "0000000001-26-000007", "fy": 2025, "fp": "FY"}]
    later = recent([("10-Q", "2026-05-01", ""), ("8-K", "2026-06-01", "")])
    fake_get(monkeypatch, {"companyfacts": {"facts": {"us-gaap": {"Revenues": {"units": {"USD": vals}}}}},
                           "submissions": {"filings": {"recent": later}}})
    out = json.loads(tools.edgar_financials("1", ["Revenues"]))
    row = out["data"]["Revenues (USD)"][0]
    assert row["accession"] == "0000000001-26-000007"
    assert row["filing"] == "https://www.sec.gov/Archives/edgar/data/1/000000000126000007/0000000001-26-000007-index.htm"
    assert out["note"].startswith("STALE: the newest figures here were filed 2026-02-01, but a 10-Q was filed 2026-05-01")


def test_edgar_financials_picks_ifrs_names_for_an_ifrs_filer_and_survives_a_failed_freshness_check(monkeypatch):
    vals = [{"start": "2025-01-01", "end": "2025-12-31", "val": 7, "form": "20-F", "filed": "2026-04-01"}]
    fake_get(monkeypatch, {"companyfacts": {"facts": {"ifrs-full": {"Revenue": {"units": {"TWD": vals}}}}},
                           "submissions": tools.ToolError("HTTP 503")})
    out = json.loads(tools.edgar_financials("1"))
    assert list(out["data"]) == ["Revenue (TWD)"] and "accession" not in out["data"]["Revenue (TWD)"][0]
    assert "GrossProfit" in out["note"] and "Revenues" not in out["note"].split(";")[0]   # the IFRS set, not us-gaap
    assert "could not check for a newer report than these figures (HTTP 503)" in out["note"]


def test_latest_periodic_filing_ignores_other_forms_and_the_future_in_a_backtest(monkeypatch):
    fake_get(monkeypatch, {"submissions": {"filings": {"recent": recent([("10-K", "2026-02-01", ""), ("10-Q", "2026-08-01", "")])}}})
    assert tools._latest_periodic_filing("1")[:2] == ("10-Q", "2026-08-01")
    tools.AS_OF["date"] = "2026-03-01"
    assert tools._latest_periodic_filing("1")[:2] == ("10-K", "2026-02-01")
    tools.AS_OF["date"] = "2026-01-01"
    assert tools._latest_periodic_filing("1") is None


def test_the_listing_tool_is_offered_and_validated():
    assert tools.validate("edgar_listing", {"cik": "1"}) == ""
    assert "missing" in tools.validate("edgar_listing", {})


# ----------------------------------------------------------------------------- verify: identity against the SEC

def block(**subject):
    return {"subject": {"company": "Example Corp", "ticker": "EXM", "exchange": "NYSE", "share_class": "common",
                        "type": "listed", **subject}, "flags": []}


def src(tool, data, error=False):
    return {"tool": tool, "result": json.dumps({"data": data}), "error": error}


def rows(k, sources):
    return {n: (ok, d) for n, ok, d in verify.check_identity(k, sources)}


def test_identity_passes_when_the_sec_lists_the_ticker_on_that_exchange():
    lookup = src("edgar_lookup", [{"ticker": "EXM", "exchange": "NYSE"}, "not a record"])
    got = rows(block(exchange="New York Stock Exchange"), [lookup])
    assert got["identity: ticker is one the SEC lists"][0] and got["identity: exchange is the one the SEC lists"][0]
    assert rows(block(ticker="exm"), [src("edgar_filings", {"tickers": ["EXM"], "exchanges": ["NYSE"]})]) \
        ["identity: exchange is the one the SEC lists"][0]


def test_identity_fails_a_wrong_exchange_or_ticker_and_spells_share_classes_one_way():
    listed = [src("edgar_listing", {"tickers": ["BRK-B", "BRK-A"], "exchanges": ["NYSE", "NYSE"]})]
    got = rows(block(ticker="BRK.B", exchange="Nasdaq"), listed)
    assert got["identity: ticker is one the SEC lists"][0]
    assert got["identity: exchange is the one the SEC lists"] == (False, "memo 'Nasdaq'; SEC ['NYSE']")
    wrong = rows(block(ticker="EXMX"), listed)
    assert wrong["identity: ticker is one the SEC lists"][0] is False and "identity: exchange is the one the SEC lists" not in wrong


def test_identity_needs_an_sec_record_and_skips_unreadable_or_failed_results():
    unreadable = [{"tool": "edgar_lookup", "result": '{"data": [cut off', "error": False},
                  src("edgar_lookup", [{"ticker": "EXM"}], error=True), src("calculate", {}), "junk",
                  {"tool": "edgar_listing", "result": "[1, 2]", "error": False}, src("edgar_filings", ["not", "an object"])]
    assert verify.check_identity(block(), unreadable) == [
        ("identity checked against an SEC record", False, "no edgar_lookup, edgar_listing or edgar_filings result among the sources")]
    assert verify.check_identity({"subject": "not an object"}, [])[0][1] is False


def test_an_ipo_not_yet_trading_passes_the_ticker_check_but_still_needs_an_sec_record():
    got = rows(block(type="ipo", ticker="NEWCO"), [src("edgar_filings", {"tickers": [], "exchanges": []})])
    assert got == {"identity: ticker is one the SEC lists": (True, "an IPO's ticker is not in the SEC's lists until it trades")}
    assert "identity checked against an SEC record" in rows(block(type="ipo"), [src("edgar_lookup", [])])


def test_listing_events_must_be_flagged():
    listing = src("edgar_listing", {"tickers": ["EXM"], "exchanges": ["NYSE"],
                                    "listing_events": [{"form": "25-NSE", "filed": "2026-05-01"}, "junk"]})
    name = "listing or delisting filings in the last year are flagged"
    assert rows(block(), [listing])[name] == (False, "25-NSE filed 2026-05-01")
    flagged = dict(block(), flags=["LISTING: a 25-NSE removed the 2027 notes, not the common stock"])
    assert rows(flagged, [listing])[name][0] is True
    assert name not in rows(block(), [src("edgar_listing", {"tickers": ["EXM"], "exchanges": ["NYSE"]})])


def test_memo_checks_with_sources_add_identity_only_when_there_is_a_block_and_sources(tmp_path):
    memo = "As of: today\n```json\n" + json.dumps({"key_numbers": block()}) + "\n```"
    base = verify.check_memo(memo)
    assert verify.check_memo_with_sources(memo, None) == base
    assert len(verify.check_memo_with_sources(memo, [src("edgar_lookup", [{"ticker": "EXM", "exchange": "NYSE"}])])) == len(base) + 2
    assert verify.check_memo_with_sources("no block", []) == verify.check_memo("no block")
    path = tmp_path / "m.md"
    path.write_text(memo, encoding="utf-8")
    assert verify._sources_beside(path) is None
    (tmp_path / "m.sources.json").write_text(json.dumps([src("edgar_lookup", [{"ticker": "EXM", "exchange": "NYSE"}])]))
    assert verify._sources_beside(path)[0]["tool"] == "edgar_lookup"


def test_verify_command_line_reads_the_sources_saved_beside_a_memo(tmp_path, capsys):
    memo = "As of: today\n```json\n" + json.dumps({"key_numbers": block()}) + "\n```"
    path = tmp_path / "m.md"
    path.write_text(memo, encoding="utf-8")
    (tmp_path / "m.sources.json").write_text(json.dumps([src("edgar_lookup", [{"ticker": "EXM", "exchange": "Nasdaq"}])]))
    verify.main([str(path)])
    assert "FAIL  identity: exchange is the one the SEC lists" in capsys.readouterr().out


# ----------------------------------------------------------------------------- the proof trace

FACTS = {"facts": {"us-gaap": {
    "Revenues": {"units": {"USD": [
        {"start": "2025-01-01", "end": "2025-12-31", "val": 391035000000, "form": "10-K", "filed": "2026-02-01",
         "accn": "0000000001-26-000001", "fy": 2025, "fp": "FY"},
        {"start": "2025-01-01", "end": "2025-12-31", "val": 391035000000, "form": "10-K", "filed": "2027-02-01",
         "accn": "0000000001-27-000001", "fy": 2026, "fp": "FY"},
        {"start": "2025-10-01", "end": "2025-12-31", "val": 100000000000, "form": "10-Q", "filed": "2026-02-01",
         "accn": "0000000001-26-000001"},
        {"start": "2025-01-01", "end": "2025-12-31", "val": 1, "form": "8-K", "filed": "2026-02-01"}]}},
    "EarningsPerShareDiluted": {"units": {"USD/shares": [
        {"start": "2025-01-01", "end": "2025-12-31", "val": 6.08, "form": "10-K", "filed": "2026-02-01", "accn": "a1"},
        {"start": "2025-01-01", "end": "2025-12-31", "val": 6.11, "form": "10-K", "filed": "2027-02-01", "accn": "a2"}]}},
    "Cash": {"units": {"USD": [{"end": "2025-12-31", "val": 0, "form": "10-K", "filed": "2026-02-01", "accn": "a1"}],
                       "EUR": [{"end": "2025-12-31", "val": 5, "form": "10-K", "filed": "2026-02-01", "accn": "a1"}]}}}}}


def metric(**kw):
    return {"name": "Revenue FY2025", "value": 391035000000, "concept": "Revenues", "start": "2025-01-01",
            "end": "2025-12-31", **kw}


def test_an_exact_figure_passes_with_the_filing_that_reported_it():
    line = proof.prove("1", metric(value=391035000000.0), FACTS["facts"])
    assert line["result"] == "PASS" and line["official"] == 391035000000 and line["detail"] == "exact match, USD"
    assert "10-K filed 2027-02-01, accession 0000000001-27-000001" in line["filing"]       # the newest version
    assert line["link"].endswith("/000000000127000001/0000000001-27-000001-index.htm")
    assert line["page_note"] == proof.PAGE_NOTE


@pytest.mark.parametrize("change, why", [
    (dict(value=391000000000), "off by -0.0090%"),
    (dict(value="391bn"), "not a number"),
    (dict(concept=None), "doesn't say which reported figure"),
    (dict(concept="EBITDA"), "reports no figure under this concept"),
    (dict(unit="EUR"), "no figures in EUR"),
    (dict(end="2024-12-31"), "no USD figure for the period"),
    (dict(start=None), "more than one period ends on this date"),
    (dict(name="EPS", concept="EarningsPerShareDiluted", value=6.11), "versions that disagree (6.08, 6.11)"),
])
def test_every_other_outcome_is_a_failure(change, why):
    line = proof.prove("1", metric(**change), FACTS["facts"])
    assert line["result"] == "FAIL" and why in line["detail"], line


def test_naming_the_filing_settles_a_restated_figure_and_a_zero_has_no_percentage():
    eps = proof.prove("1", metric(concept="EarningsPerShareDiluted", value=6.08, accession="a1"), FACTS["facts"])
    assert eps["result"] == "PASS"
    cash = proof.prove("1", {"name": "Cash", "value": 3, "concept": "Cash", "end": "2025-12-31", "unit": "USD"}, FACTS["facts"])
    assert cash["result"] == "FAIL" and "n/a (official value is 0)" in cash["detail"]


def test_the_draft_names_its_company_by_cik_or_ticker(monkeypatch):
    fake_get(monkeypatch, {"company_tickers_exchange": {"fields": ["cik", "name", "ticker", "exchange"],
                                                        "data": [[9, "Exm Corp", "EXMB", "NYSE"], [7, "Exm", "EXM", "NYSE"]]}})
    assert proof.resolve_cik({"cik": 5}) == "5"
    assert proof.resolve_cik({"ticker": "exm"}) == "7"
    with pytest.raises(proof.ProofError, match="no company with the ticker"):
        proof.resolve_cik({"ticker": "ex"})
    with pytest.raises(proof.ProofError, match="needs a cik or a ticker"):
        proof.resolve_cik({})


def memo_with(inputs):
    k = {"key_numbers": dict(block(), inputs=inputs)}
    return "As of: today\n```json\n" + json.dumps(k) + "\n```"


def test_a_memos_sec_inputs_are_the_metrics():
    ref = {"cik": "1", "concept": "Revenues", "start": "2025-01-01", "end": "2025-12-31"}
    cik, found = proof.metrics_from_memo(memo_with({"revenue": {"value": 5, "sec": ref}, "price": {"value": 9}, "x": 3}))
    assert cik == "1" and found == [{"name": "revenue", "value": 5, "concept": "Revenues", "start": "2025-01-01",
                                     "end": "2025-12-31", "unit": None, "accession": None}]
    with pytest.raises(proof.ProofError, match="no KEY NUMBERS input"):
        proof.metrics_from_memo(memo_with({"price": {"value": 9}}))
    with pytest.raises(proof.ProofError, match="same cik"):
        proof.metrics_from_memo(memo_with({"a": {"value": 1, "sec": ref}, "b": {"value": 1, "sec": dict(ref, cik="2")}}))
    with pytest.raises(proof.ProofError, match="same cik"):
        proof.metrics_from_memo(memo_with({"a": {"value": 1, "sec": dict(ref, cik="")}}))


def test_run_and_table_report_every_line_and_the_latest_report(monkeypatch):
    fake_get(monkeypatch, {"companyfacts": FACTS, "submissions": {"filings": {"recent": recent([("10-K", "2026-02-01", "")])}}})
    cik, lines, latest = proof.run(draft={"cik": "1", "metrics": [metric(), metric(value=1)]})
    text = proof.table(cik, lines, latest)
    assert "| Revenue FY2025 | 391035000000 | 391035000000 |" in text and "| PASS |" in text
    assert "FAIL: off by" in text and "1 of 2 figures proved exactly" in text
    assert "Latest periodic report: 10-K filed 2026-02-01" in text
    assert "NOT AVAILABLE" in proof.table("1", [proof.prove("1", metric(concept="EBITDA"), FACTS["facts"])], None)
    with pytest.raises(proof.ProofError, match="non-empty"):
        proof.run(draft={"cik": "1", "metrics": []})
    with pytest.raises(proof.ProofError, match="non-empty"):
        proof.run(draft=["not", "a", "draft"])


def test_command_line(monkeypatch, tmp_path, capsys):
    fake_get(monkeypatch, {"companyfacts": FACTS, "submissions": {"filings": {"recent": {}}}})
    draft = tmp_path / "d.json"
    draft.write_text(json.dumps({"cik": "1", "metrics": [metric()]}))
    assert proof.main([str(draft)]) == 0 and "1 of 1 figures proved" in capsys.readouterr().out
    assert proof.main([str(draft), "--json"]) == 0 and json.loads(capsys.readouterr().out)["lines"][0]["result"] == "PASS"
    memo = tmp_path / "m.md"
    memo.write_text(memo_with({"revenue": {"value": 1, "sec": {"cik": "1", "concept": "Revenues",
                                                               "start": "2025-01-01", "end": "2025-12-31"}}}))
    assert proof.main(["--memo", str(memo)]) == 1                     # 1 is not the reported 391,035,000,000
    bad = tmp_path / "bad.json"
    bad.write_text('{"metrics": [1]}')                                 # no cik or ticker
    with pytest.raises(SystemExit, match="Can't prove this draft: the draft needs a cik or a ticker"):
        proof.main([str(bad)])
    with pytest.raises(SystemExit, match="Proof trace"):
        proof.main([])                                                 # no file: the usage text


def test_proof_runs_as_a_script(monkeypatch, tmp_path):
    import runpy
    fake_get(monkeypatch, {"companyfacts": FACTS, "submissions": {"filings": {"recent": {}}}})
    draft = tmp_path / "d.json"
    draft.write_text(json.dumps({"cik": "1", "metrics": [metric()]}))
    monkeypatch.setattr(sys, "argv", ["proof.py", str(draft)])
    with pytest.raises(SystemExit) as done:
        runpy.run_path(str(pathlib.Path(proof.__file__)), run_name="__main__")
    assert done.value.code == 0
