"""Proof trace: every figure in a research draft against the company's own SEC filings, exactly.

    python src/proof.py draft.json             a draft's figures (format below)
    python src/proof.py --memo memos/X.md      the SEC-sourced inputs of a memo's KEY NUMBERS block
    add --json for the results as JSON. Exit code 1 if any figure fails.

A draft names each figure by the XBRL concept and period it claims to be:

    {"cik": "320193",                               or "ticker": "AAPL"
     "metrics": [{"name": "Revenue FY2025", "value": 416161000000,
                  "concept": "RevenueFromContractWithCustomerExcludingAssessedTax",
                  "start": "2024-09-29", "end": "2025-09-27",       start only for a flow over a period
                  "unit": "USD", "accession": "0000320193-25-000079"}]}  unit and accession are optional

In a memo, an input sourced from the SEC carries the same fields under "sec":
    "revenue": {"value": 416161000000, ..., "sec": {"cik": "320193", "concept": "...", "start": "...", "end": "..."}}

Each figure is re-read from the SEC's XBRL data (data.sec.gov companyfacts) and compared with no tolerance:
any difference at all is a FAIL, as is a figure the SEC does not report (EBITDA, "adjusted" measures), a
period that matches more than one figure, and a figure filed in two versions that disagree unless the draft
names the filing. XBRL records the filing, never the page or note, so the proof gives the filing's index
link; the page and note have to be read there.
"""
import json
import pathlib
import sys
from decimal import Decimal, InvalidOperation

import common
import tools
import verify

TAXONOMIES = ("us-gaap", "ifrs-full", "dei")
PASS, FAIL = "PASS", "FAIL"
PAGE_NOTE = "not recorded in XBRL; open the filing"


class ProofError(Exception):
    """A draft that can't be checked at all (no company, no metrics)."""


def _exact(x):
    """The number as written, without float rounding: 391035000000.0 and 391035000000 are equal, 3.1 is not 3.10001."""
    try:
        return Decimal(str(x))
    except (InvalidOperation, ValueError):
        return None


def _pct(draft, official):
    if official == 0:
        return "n/a (official value is 0)"
    return f"{(draft - official) / abs(official) * 100:+.4f}%"


def resolve_cik(draft):
    if draft.get("cik"):
        return str(draft["cik"])
    ticker = str(draft.get("ticker") or "").strip()
    if not ticker:
        raise ProofError("the draft needs a cik or a ticker")
    hits = json.loads(tools.edgar_lookup(ticker))["data"]
    exact = [h for h in hits if str(h["ticker"]).upper() == ticker.upper()]
    if not exact:
        raise ProofError(f"the SEC lists no company with the ticker {ticker!r}")
    return exact[0]["cik"]


def company_facts(cik):
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{tools._cik10(cik)}.json"
    return json.loads(tools._get(url, tools._sec_headers())).get("facts", {})


def _candidates(facts, metric):
    """The SEC's facts for this concept, unit and period, from periodic reports and registration statements."""
    concept = next((facts[t][metric["concept"]] for t in TAXONOMIES if metric["concept"] in facts.get(t, {})), None)
    if concept is None:
        return None, "the SEC reports no figure under this concept (a non-GAAP or derived measure can't be proved here)"
    units = concept.get("units", {})
    unit = metric.get("unit") or (next(iter(units)) if len(units) == 1 else "USD")
    if unit not in units:
        return None, f"no figures in {unit}; the SEC has {sorted(units)}"
    rows = [v for v in units[unit] if v.get("end") == metric.get("end") and v.get("form") in tools.FACT_FORMS
            and (not metric.get("start") or v.get("start") == metric["start"])
            and (not metric.get("accession") or v.get("accn") == metric["accession"])]
    if not rows:
        return None, f"no {unit} figure for the period {metric.get('start') or ''}..{metric.get('end')}"
    if not metric.get("start") and len({v.get("start") for v in rows}) > 1:
        return None, "more than one period ends on this date (a quarter and a year to date): give its start"
    return rows, unit


def prove(cik, metric, facts):
    """One proof line: {metric, draft, official, filing, page_note, link, result, detail}."""
    line = {"metric": metric.get("name") or metric.get("concept"), "draft": metric.get("value"), "official": None,
            "filing": "", "page_note": PAGE_NOTE, "link": "", "result": FAIL, "detail": ""}
    draft = _exact(metric.get("value"))
    if draft is None:
        line["detail"] = "the draft value is not a number"
        return line
    if not metric.get("concept") or not metric.get("end"):
        line["detail"] = "the draft doesn't say which reported figure this is (concept and period end)"
        return line
    rows, unit_or_why = _candidates(facts, metric)
    if rows is None:
        line["detail"] = unit_or_why
        return line
    values = {_exact(v.get("val")) for v in rows}
    newest = max(rows, key=lambda v: (v.get("filed") or "", v.get("accn") or ""))
    official = _exact(newest.get("val"))
    line.update(official=newest.get("val"), filing=f"{newest.get('form')} filed {newest.get('filed')}, "
                f"accession {newest.get('accn')} ({newest.get('fy')} {newest.get('fp')})",
                link=tools.filing_index(cik, newest.get("accn")))
    if len(values) > 1:
        line["detail"] = (f"filed in versions that disagree ({', '.join(sorted(str(v) for v in values))}); "
                          "name the filing (accession) the draft is from")
        return line
    if draft != official:
        line["detail"] = f"off by {_pct(draft, official)} ({draft - official:+} {unit_or_why})"
        return line
    line.update(result=PASS, detail=f"exact match, {unit_or_why}")
    return line


def metrics_from_memo(memo):
    """(cik, metrics) from the inputs of a memo's KEY NUMBERS block that carry an "sec" reference."""
    k = verify.extract(memo)
    found, ciks = [], set()
    for name, v in (k.get("inputs") or {}).items():
        if isinstance(v, dict) and isinstance(v.get("sec"), dict):
            ref = v["sec"]
            ciks.add(str(ref.get("cik") or ""))
            found.append({"name": name, "value": v.get("value"), **{f: ref.get(f) for f in
                                                                     ("concept", "start", "end", "unit", "accession")}})
    if not found:
        raise ProofError("no KEY NUMBERS input carries an \"sec\" reference to prove")
    if len(ciks) != 1 or "" in ciks:
        raise ProofError(f"every \"sec\" reference needs the same cik; found {sorted(ciks)}")
    return ciks.pop(), found


def run(draft=None, memo=None):
    """(cik, lines, latest periodic filing or None)."""
    if memo is not None:
        cik, metrics = metrics_from_memo(memo)
    else:
        if not isinstance(draft, dict) or not isinstance(draft.get("metrics"), list) or not draft["metrics"]:
            raise ProofError("the draft needs a non-empty \"metrics\" list")
        cik, metrics = resolve_cik(draft), draft["metrics"]
    facts = company_facts(cik)
    return cik, [prove(cik, m, facts) for m in metrics], tools._latest_periodic_filing(cik)


def table(cik, lines, latest):
    out = [f"Proof trace for CIK {cik}, against the SEC's XBRL data (no tolerance)", "",
           "| Metric | AI draft value | Official SEC value | Filing | Page/note | Link | Result |",
           "|---|---|---|---|---|---|---|"]
    for p in lines:
        result = p["result"] + (f": {p['detail']}" if p["result"] == FAIL else "")
        out.append(f"| {p['metric']} | {p['draft']} | {p['official'] if p['official'] is not None else 'NOT AVAILABLE'} "
                   f"| {p['filing'] or '-'} | {p['page_note']} | {p['link'] or '-'} | {result} |")
    passed = sum(p["result"] == PASS for p in lines)
    out += ["", f"{passed} of {len(lines)} figures proved exactly; any other result is a failure."]
    if latest:
        form, filed, acc = latest
        out.append(f"Latest periodic report: {form} filed {filed} ({tools.filing_index(cik, acc)}).")
    return "\n".join(out)


def main(argv):
    common.utf8_console()
    args = [a for a in argv if a != "--json"]
    try:
        if args[:1] == ["--memo"] and len(args) == 2:
            cik, lines, latest = run(memo=pathlib.Path(args[1]).read_text(encoding="utf-8"))
        elif len(args) == 1:
            cik, lines, latest = run(draft=json.loads(pathlib.Path(args[0]).read_text(encoding="utf-8")))
        else:
            sys.exit(__doc__)
    except (ProofError, tools.ToolError, verify.BlockError) as e:
        sys.exit(f"Can't prove this draft: {e}")
    if "--json" in argv:
        print(json.dumps({"cik": cik, "lines": lines, "latest_periodic": latest}, indent=1, default=str))
    else:
        print(table(cik, lines, latest))
    return 1 if any(p["result"] != PASS for p in lines) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
