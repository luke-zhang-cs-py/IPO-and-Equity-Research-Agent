"""The browser demo (docs/app/ipo-core.js) against the Python it ports: portfolio sizing and the KEY NUMBERS checks.

Runs the same inputs through both and fails on any difference, so the demo cannot drift from the bot. Needs Node
(set IPO_BOT_NODE to its path if it is not on PATH); skipped without it.
"""
import copy
import datetime as dt
import json
import os
import pathlib
import shutil
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests" / "src"))

import portfolio  # noqa: E402
import verify  # noqa: E402
from test_accuracy import BLOCK, memo_with  # noqa: E402

NODE = os.environ.get("IPO_BOT_NODE") or shutil.which("node")
pytestmark = pytest.mark.skipif(not NODE, reason="Node is not installed")
CORE = ROOT / "docs" / "app" / "ipo-core.js"
EXAMPLE = json.loads((ROOT / "portfolio.example.json").read_text(encoding="utf-8"))

DRIVER = """
const core = require(process.argv[1]);
let input = '';
process.stdin.on('data', (d) => input += d).on('end', () => {
  const job = JSON.parse(input), out = {};
  out.sizes = job.sizes.map(([pf, args]) => {
    try { return core.sizePosition(core.valued(core.validate(pf)), ...args); } catch (e) { return { error: e.message }; }
  });
  out.views = job.views.map((pf) => { const v = core.valued(core.validate(pf)); return { equity: v.equity, breaches: v.rule_breaches }; });
  out.memos = job.memos.map((m) => core.checkMemo(m));
  process.stdout.write(JSON.stringify(out));
});
"""


def run_js(job, prefix=""):
    r = subprocess.run([NODE, "-e", prefix + DRIVER, str(CORE)], input=json.dumps(job), capture_output=True, text=True,
                       encoding="utf-8", timeout=60)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def py_size(pf, args):
    try:
        return portfolio.size_position(portfolio.valued(portfolio.validate(copy.deepcopy(pf))), *args)
    except portfolio.PortfolioError as e:
        return {"error": str(e)}


SIZES = [
    (EXAMPLE, ["DDD", 50, 45, "Medium", "Energy"]), (EXAMPLE, ["DDD", 50, 45, "Low", "Energy"]),
    (EXAMPLE, ["DDD", 50, 45, "High", "Energy"]), (EXAMPLE, ["AAA", 180, 170, "High", None]),
    (EXAMPLE, ["EEE", 10, 9.9, "High", "Technology"]), ({**EXAMPLE, "cash": 600}, ["DDD", 50, 49.9, "High", "Energy"]),
    (EXAMPLE, ["DDD", 50, 55, "Medium", None]), (EXAMPLE, ["DDD", 50, 45, "Certain", None]),
    (EXAMPLE, ["BBB", 55, 44, "Medium", None]), ({**EXAMPLE, "cash": 0}, ["ZZZ", 12.5, 10, "High", "Health"]),
    (EXAMPLE, ["DDD", 50, 45, "toString", None]), (EXAMPLE, ["DDD", 50, 45, "Medium", "constructor"]),
    ({**EXAMPLE, "holdings": EXAMPLE["holdings"] + [{"symbol": "UNP", "shares": 5, "sector": "Energy"}]}, ["unp", 50, 45, "Medium", None]),
    (EXAMPLE, ["NEWCO", 20, 18, "Medium", None]),                 # not held, no sector: no sector limit
    ({"cash": 0}, ["NEWCO", 20, 18, "Medium", "Energy"]),          # an empty portfolio: nothing to risk, 0% after
    (EXAMPLE, [None, 20, 18, "Medium", None]),                    # str(None), as the Python names it
    (EXAMPLE, ["DDD", 50, 50, "Medium", None]), (EXAMPLE, ["DDD", 0, -1, "Medium", None]),
    (EXAMPLE, ["DDD", "50", 45, "Medium", None]), (EXAMPLE, ["DDD", 50, -1, "Medium", None]),
    ({**EXAMPLE, "rules": {**EXAMPLE["rules"], "conviction_scale": {"b": 1, "a": 2}}}, ["DDD", 50, 45, "Medium", None]),
    # "__proto__" as a name is a name like any other: a sector (the cap must see the 100 shares already held in it),
    # a conviction, and a rule key (which must not hand its contents to the rules as inherited settings)
    ({"cash": 1000, "holdings": [{"symbol": "AAA", "shares": 100, "price": 10, "sector": "__proto__"}], "rules": {"max_sector_pct": 30}},
     ["BBB", 10, 9, "Medium", "__proto__"]),
    ({"cash": 1000, "holdings": [{"symbol": "AAA", "shares": 100, "price": 10, "sector": "__proto__"}], "rules": {"max_sector_pct": 30}},
     ["AAA", 10, 9, "Medium", None]),
    ({**EXAMPLE, "rules": {**EXAMPLE["rules"], "conviction_scale": {"__proto__": 2, "Medium": 1}}}, ["DDD", 50, 45, "__proto__", None]),
    ({**EXAMPLE, "rules": {**EXAMPLE["rules"], "conviction_scale": {"Medium": 1}}}, ["DDD", 50, 45, "__proto__", None]),
    ({**EXAMPLE, "rules": {**EXAMPLE["rules"], "__proto__": {"max_volume_pct": 1, "max_order_value": 100}}}, ["DDD", 50, 45, "Medium", None]),
]


GUARDED = {**EXAMPLE, "day_pnl": -100.0, "rules": {**EXAMPLE["rules"], "max_daily_loss_pct": 2, "earnings_blackout_hours": 48, "max_volume_pct": 1}}
GUARD_CASES = [
    (GUARDED, ["DDD", 50, 45, "Medium", "Energy"], {"next_earnings": "2026-10-10", "avg_volume": 900_000, "now": "2026-10-07T12:00:00Z"}),
    (GUARDED, ["DDD", 50, 45, "Medium", "Energy"], {"next_earnings": "2026-10-08T20:00:00Z", "avg_volume": 900_000, "now": "2026-10-07T12:00:00Z"}),
    (GUARDED, ["DDD", 50, 45, "Medium", "Energy"], {"next_earnings": "2026-10-01", "avg_volume": 2_000, "now": "2026-10-07T12:00:00Z"}),
    (GUARDED, ["DDD", 50, 45, "Medium", "Energy"], {}),
    ({**GUARDED, "day_pnl": -400.0}, ["DDD", 50, 45, "Medium", "Energy"], {"next_earnings": "2026-12-01", "avg_volume": 900_000, "now": "2026-10-07"}),
    ({**GUARDED, "day_pnl": 250.0}, ["DDD", 50, 45, "High", "Energy"], {"avg_volume": 600, "now": "2026-10-07"}),
    ({**EXAMPLE, "rules": {**EXAMPLE["rules"], "max_order_value": 500}}, ["DDD", 50, 45, "High", "Energy"], {}),
    ({**EXAMPLE, "rules": {**EXAMPLE["rules"], "max_gross_exposure_pct": 70}}, ["DDD", 50, 45, "High", "Energy"], {}),
    ({**EXAMPLE, "equity_high": 20_000, "rules": {**EXAMPLE["rules"], "max_drawdown_pct": 8}}, ["DDD", 50, 45, "Medium", "Energy"], {}),
    ({**EXAMPLE, "rules": {**EXAMPLE["rules"], "max_drawdown_pct": 8}}, ["DDD", 50, 45, "Medium", "Energy"], {}),
    ({**EXAMPLE, "halted": True}, ["DDD", 50, 45, "Medium", "Energy"], {}),
    ({**GUARDED, "day_pnl": 0}, ["DDD", 50, 45, "Medium", "Energy"], {"avg_volume": 900_000}),          # no loss today
]
NOW = "2026-10-07T12:00:00Z"
# Earnings 47 hours away, inside the 48-hour blackout, in each form fromisoformat reads (a time with no zone is UTC, so
# "2026-10-09 11:00" must not be read in the machine's own zone); then forms it refuses, and no "now" at all.
WHEN = ["2026-10-09T11:00:00", "2026-10-09 11:00", "2026-10-09x11:00", "20261009T1100", "2026-10-09T110000",
        "2026-10-09T16:30:00.5+05:30", "2026-10-09T16:30+0530", "2026-10-09T06:59-04", "2026-10-09T11:00:00,25Z",
        "2026-10-09T12:00Z", "2026-10-10", "2026-10-09",
        "Oct 9 2026", "2026-02-30", "0", "", "2026-10-09T25:00", "2026-10-09T11:60", "2026-10-09T11:00:00+25:00",
        "2026-1009", "2026-10-09T11:0000", "0000-10-09", "2026-10-09T11:00 ", "2026-10-09T11:00:00z",
        # NOW + 48h is the edge of the blackout; these sit 1 second to 7 hours either side of it, so reading any of them in
        # the machine's own zone (the pre-fix bug), or dropping a second of offset or a digit of fraction, flips the verdict
        "2026-10-09T12:00:00", "2026-10-09 13:00", "2026-10-07 06:00", "2026-10-09T13:00:00", "2026-10-07T06:00:00", "2026-10-09T12:00:00+00:00:01",
        "2026-10-09T12:00:00-00:00:01", "2026-10-09T12:00:00.000001", "2026-10-09T12:00:00.0000009",
        "2026-10-09T12:00:00-000001", "2026-10-09T12:00-00:00:01"]
GUARD_CASES += [(GUARDED, ["DDD", 50, 45, "Medium", "Energy"], {"next_earnings": w, "avg_volume": 900_000, "now": NOW})
                for w in WHEN]
# the same instant, spelt other ways: a Z on a bare date, week dates, an offset with seconds, a "." before an offset
GUARD_CASES += [(GUARDED, ["DDD", 50, 45, "Medium", "Energy"], {"next_earnings": w, "avg_volume": 900_000, "now": NOW})
                for w in ("2026-10-09Z", "2026-W41-5", "2026W415T12", "2026-W41-5 11:59:59+00:00:01", "2026-10-09T12:00.Z", "2026-10-09T11:00:00.+00:00")]
GUARD_CASES += [(GUARDED, ["DDD", 50, 45, "Medium", "Energy"], {"next_earnings": w, "avg_volume": 900_000, **now})
                for w in ("2000-01-01", "2999-01-01") for now in ({}, {"now": ""}, {"now": None})]
GUARD_CASES += [(GUARDED, ["DDD", 50, 45, "Medium", "Energy"], {"next_earnings": NOW, "avg_volume": v, "now": NOW})
                for v in (-1, "9", 0)]
GUARD_DRIVER = """
const core = require(process.argv[1]);
let input = '';
process.stdin.on('data', (d) => input += d).on('end', () => {
  const out = JSON.parse(input).map(([pf, args, opts]) => {
    try { return core.sizePosition(core.valued(core.validate(pf)), ...args, opts); } catch (e) { return { error: e.message }; }
  });
  process.stdout.write(JSON.stringify(out));
});
"""


# A time with no zone is UTC, so the verdicts must not depend on the machine's zone. CI runs in UTC, where a local-time
# misread is invisible, so each run also sets the zone Node believes it is in (as TZ does on Linux; on Windows only
# process.env.TZ set inside the process takes effect).
ZONES = ("UTC", "America/Los_Angeles", "Asia/Tokyo")
in_zone = lambda zone: f"process.env.TZ = {json.dumps(zone)};\n"


@pytest.mark.parametrize("zone", ZONES)
def test_the_guardrails_match_the_python(zone):
    r = subprocess.run([NODE, "-e", in_zone(zone) + GUARD_DRIVER, str(CORE)], input=json.dumps(GUARD_CASES), capture_output=True, text=True,
                       env={**os.environ, "TZ": zone}, timeout=60)
    assert r.returncode == 0, r.stderr
    got_all = json.loads(r.stdout)
    assert len(got_all) == len(GUARD_CASES)
    for (pf, args, opts), got in zip(GUARD_CASES, got_all):
        view = portfolio.valued(portfolio.validate(copy.deepcopy(pf)))
        try:
            want = portfolio.size_position(view, *args, **opts)
        except portfolio.PortfolioError as e:
            assert got == {"error": str(e)}, (opts, got)
            continue
        for key in ("shares", "binding_rule", "limits_in_shares", "warnings"):
            assert got[key] == want[key], (opts, key, got[key], want[key])


# portfolio._when itself, to the microsecond, on every form the doc comment on when() names and some it must refuse. Only forms
# Python 3.12 and 3.14 read alike are here (3.12 alone reads "11.5" as a fraction of an hour, 3.14 alone reads "24:00").
WHEN_FORMS = WHEN + [
    "2026-10-09Z", "2026-10-09+05:30", "2026-W41-5", "2026W415", "2026-W41", "2026W41", "2026-W53-7", "2020-W53-7", "2025-W53",
    "2026-W00", "2026-W54", "2026-W41-0", "2026-W41-8", "2026-W415", "2026W41-5", "2026-W41-5T11:00", "2026-W41-1100", "2026-W41-11100", "2026-W41-1T1100",
    "2026W41T11:00:00+0100", "0001-W01-1", "0001-W01-1T00:00+01:00", "9999-W52-7", "9999-W52-7T23:59-23:59", "0000-W01",
    "2026-10-09T11:00:00+05:30:15", "2026-10-09T11:00:00+053015", "2026-10-09T11:00:00-05:30:15", "2026-10-09T11:00+05:60",
    "2026-10-09T11:00+05:30:60", "2026-10-09T11:00+23:59:59", "2026-10-09T11:00+23:59:60", "2026-10-09T11:00+24:00", "2026-10-09T11:00:00+05:30:1",
    "2026-10-09T11:00:00.+00", "2026-10-09T11:00:00,+00", "2026-10-09T11:00.+00", "2026-10-09T11.+00", "2026-10-09T11:00:00.Z",
    "2026-10-09T11:00:00.5,+00", "2026-10-09T11:00:00.", "2026-10-09T11:00:00,", "2026-10-09T11:00:00.5.", "2026-10-09T11:00:00+",
    "2026-10-09T11:00:00.1234567", "2026-10-09T11:00:00.123456789+01:00", "2026-10-09T11:00:00.5", "2026-10-09T11:00:00,5",
    "2024-02-29", "2026-02-29", "2100-02-29", "2000-02-29", "2026-00-10", "2026-10-00", "2026-13-01", "0001-01-01", "9999-12-31T23:59:59.999999",
    "2026-10-09T23:59:60", "2026-10-09T-01:00", "2026-10-09 +01:00", "2026-10-09T11:00:00ZZ", "２０２６-10-09", "2026-10-09\n",
]
# Forms that a Python version reads but the browser refuses on purpose (the two versions disagree, or the form is a quirk
# of the parser), so a guess would be silent. A refusal is a failed check in the page, never a guess.
WHEN_REFUSED = ["2026-10-09T11.5", "2026-10-09T11:00.5", "2026-10-09T24:00", "2026-10-09T24:00:00", "2026-10-09T11:00:00+05:30:15.5", "2026-10-09T11:00:00+00:00:00.5",
                "2024-02-291100+00", "2026W411100"]
WHEN_DRIVER = """
const core = require(process.argv[1]);
let input = '';
process.stdin.on('data', (d) => input += d).on('end', () => {
  process.stdout.write(JSON.stringify(JSON.parse(input).map((v) => { try { return core.when(v, 'x'); } catch (e) { return { error: e.message }; } })));
});
"""


@pytest.mark.parametrize("zone", ZONES)
def test_when_reads_the_forms_python_reads_to_the_microsecond(zone):
    forms = WHEN_FORMS + WHEN_REFUSED
    r = subprocess.run([NODE, "-e", in_zone(zone) + WHEN_DRIVER, str(CORE)], input=json.dumps(forms), capture_output=True, text=True,
                       encoding="utf-8", env={**os.environ, "TZ": zone}, timeout=60)
    assert r.returncode == 0, r.stderr
    got_all = json.loads(r.stdout)
    assert len(got_all) == len(forms)
    epoch, accepted = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc), 0
    for form, got in zip(forms, got_all):
        if form in WHEN_REFUSED:
            assert got == {"error": "x must be an ISO date or date-time"}, (form, got)
            continue
        try:
            want = (portfolio._when(form, "x") - epoch) / dt.timedelta(microseconds=1) / 1000
        except portfolio.PortfolioError as e:
            assert got == {"error": str(e)}, (form, got)
            continue
        accepted += 1
        assert not isinstance(got, dict) and abs(got - want) < 1e-3, (form, got, want)
    assert 40 < accepted < len(forms) - 15       # both sides of the line are exercised


def broken_blocks():
    def edit(fn):
        b = copy.deepcopy(BLOCK)
        fn(b["key_numbers"])
        return b
    yield BLOCK
    yield edit(lambda k: k["outputs"].update(market_cap=6_000_000_000))
    yield edit(lambda k: k["outputs"].update(enterprise_value=5_000_000_000))
    yield edit(lambda k: k["outputs"]["multiples"][0].update(value=7.0))
    yield edit(lambda k: k["scenarios"]["bull"].update(prob=35))
    yield edit(lambda k: k["scenarios"]["bear"].update(value=70))
    yield edit(lambda k: k["scenarios"].update(pwv=70))
    yield edit(lambda k: k.update(rating="Equal-weight"))
    yield edit(lambda k: k.update(conviction="Low"))
    yield edit(lambda k: k["inputs"]["debt"].update(value=None))
    yield edit(lambda k: k["inputs"]["price"].update(as_of="2026-10-01"))
    yield edit(lambda k: k["inputs"]["revenue"].update(period="NTM to 2027-06-30"))
    yield edit(lambda k: k["segments"][0]["parts"][0].update(value=600_000_000))
    yield edit(lambda k: k.pop("stop_working_price"))
    yield edit(lambda k: k.update(rating="NOT RATED", scenarios=None))
    yield edit(lambda k: k.update(ipo_ratings={"at_offer": "Participate", "aftermarket": "Buy below", "buy_below": 62 / 1.15}))
    yield edit(lambda k: (k["inputs"]["revenue"].update(value=100_000_000), k["outputs"]["multiples"][0].update(value=55.0)))
    # scenario numbers go through Python's float(): null, "" and lists fail one check; numeric strings and booleans convert
    for bad in (None, "", [], {}, "80", " 8e1 ", True, "eighty"):
        yield edit(lambda k, bad=bad: k["scenarios"]["bull"].update(value=bad))
    yield edit(lambda k: k["scenarios"]["base"].pop("prob"))
    yield edit(lambda k: k["scenarios"].update(bear=35))
    # a badly shaped block is a list of failed checks, never a crash
    # a lone value in a list field is a list of one (not its characters); null, "" and {} are an empty list
    yield edit(lambda k: (k["inputs"]["price"].update(as_of="2026-10-01"), k.update(flags="stale")))
    yield edit(lambda k: (k["inputs"]["price"].update(as_of="2026-10-01"), k.update(flags="")))
    yield edit(lambda k: k.update(sources="the S-1"))
    yield edit(lambda k: k.update(sources={}))
    yield edit(lambda k: k.update(sources=0))
    yield edit(lambda k: (k["inputs"]["debt"].update(value=None), k.update(unknown="debt")))
    yield edit(lambda k: (k["inputs"]["debt"].update(value=None), k.update(unknown="de")))
    yield edit(lambda k: k.update(subject="ACME Corp"))
    yield edit(lambda k: k.update(subject=["ACME"]))
    yield edit(lambda k: k.update(subject=""))
    yield edit(lambda k: k["outputs"]["multiples"][0].update(numerator=["enterprise_value"]))
    yield edit(lambda k: k["outputs"]["multiples"][0].update(denominator={"name": "revenue"}))
    yield edit(lambda k: k["outputs"].update(multiples={"name": "EV/Revenue", "numerator": "enterprise_value", "denominator": "revenue", "value": 1.0}))
    yield edit(lambda k: k["outputs"].update(multiples="EV/Revenue"))
    yield edit(lambda k: k["segments"][0].update(total=["revenue"]))
    yield edit(lambda k: k.update(rating=["Overweight"]))
    yield edit(lambda k: k.update(conviction=["Medium"]))
    yield edit(lambda k: (k["inputs"]["price"].update(as_of="2026-10-01"), k.update(flags=[{"note": "stale price"}])))
    yield edit(lambda k: k["outputs"].update(multiples={}))
    yield edit(lambda k: k["outputs"].update(multiples=["EV/Revenue", {"name": None, "numerator": "toString", "denominator": "revenue"}]))
    yield edit(lambda k: k.update(inputs=[1, 2]))
    yield edit(lambda k: k.update(outputs="none"))
    yield edit(lambda k: k.update(segments=[{"total": "revenue", "parts": "ab"}, "x"]))
    yield edit(lambda k: k.update(scenarios=[1, 2, 3]))
    yield edit(lambda k: k.update(ipo_ratings=["Participate"]))
    yield edit(lambda k: k.update(rating="NOT RATED", scenarios={}))
    # a source is what Python's str() makes of it: {} is nothing, [" "] is the text "[' ']"
    for bad in ({}, [" "], [], " ", 0, 1.0, ["[1] quote"]):
        yield edit(lambda k, bad=bad: k["inputs"]["debt"].update(source=bad))
    # a date must be written YYYY-MM-DD: not in a list, not the compact or week forms fromisoformat also takes
    for bad in (["2026-10-06"], "20261006", "2026-W41-1", "2026-02-30", "0000-10-06", "2026-13-01", "2026-10-06T09:30:00Z",
                20261006, None, "", "0999-12-31"):
        yield edit(lambda k, bad=bad: k.update(as_of=bad))
        yield edit(lambda k, bad=bad: k["inputs"]["revenue"].update(as_of=bad))
        yield edit(lambda k, bad=bad: k["inputs"]["price"].update(as_of=bad))
    # a multiple's name is str() of whatever was written, for the period check and in every check name
    for name in ({"p": "NTM"}, ["EV/Revenue", "NTM"], 1.0, 2.5, 1e16, 1.5e-5, -0.0, 7, True, None, "",
                 ["x", 1.0, None, True, False, "it's", 'say "hi"', "both ' and \"", "a\nb\\c\t", "\xa0", "\u200b", {"a": [1.0, 2]}]):
        yield edit(lambda k, name=name: k["outputs"]["multiples"][0].update(name=name))
    # unknown holds str() of each entry: 1.0 names the input "1.0", not "1"
    yield edit(lambda k: (k["inputs"].update({"1.0": {"value": None}}), k.update(unknown=[1.0])))
    yield edit(lambda k: (k["inputs"].update({"1.0": {"value": None}}), k.update(unknown=1.0)))
    yield edit(lambda k: (k["inputs"].update({"['debt']": {"value": None}}), k.update(unknown=[["debt"]])))
    yield edit(lambda k: (k["inputs"].update({"{'a': 1.0}": {"value": None}}), k.update(unknown=[{"a": 1.0}])))
    yield edit(lambda k: (k["inputs"]["price"].update(as_of="2026-10-01"), k.update(flags=[["stale", 1.0]])))
    # keys stay in the order the block wrote them, integer-like ones too: in str() of a dict and in the per-input checks
    for name in ({"b": 1, "1": 2}, [{"z": 0, "10": 1.0, "2": None}]):
        yield edit(lambda k, name=name: k["outputs"]["multiples"][0].update(name=name))
    yield edit(lambda k: k["inputs"].update({"2": {"value": None}, "1": {"value": None}, "0": 5}))
    yield edit(lambda k: (k["inputs"].update({"{'b': 1, '1': 2}": {"value": None}}), k.update(unknown=[{"b": 1, "1": 2}])))
    # integers are printed from their digits past 2^53; one past the largest float makes the block invalid
    for name in (2**53 + 1, -(2**64), 10**400, [2**70, 1.0], {"n": 10**30}):
        yield edit(lambda k, name=name: k["outputs"]["multiples"][0].update(name=name))
    yield edit(lambda k: (k["inputs"].update({str(2**60 + 1): {"value": None}}), k.update(unknown=[2**60 + 1])))
    yield edit(lambda k: k["inputs"].update(other={"value": 10**400, "source": "S-1", "as_of": "2026-10-06"}))
    # NaN and Infinity would crash the maths (round(nan), float(10**400)): both sides refuse the block instead
    nan, inf = float("nan"), float("inf")
    for name in (nan, inf, -inf, [nan, inf], {"x": -inf}):
        yield edit(lambda k, name=name: k["outputs"]["multiples"][0].update(name=name))
    yield edit(lambda k: k["inputs"]["debt"].update(value=nan))
    yield edit(lambda k: k["inputs"]["revenue"].update(value=nan))
    yield edit(lambda k: k["inputs"].update(preferred={"value": nan, "source": "S-1", "as_of": "2026-10-06"}))
    yield edit(lambda k: k["outputs"].update(market_cap=inf))
    yield edit(lambda k: k["scenarios"].update(reference_price=nan))
    yield edit(lambda k: k["scenarios"].update(pwv=nan, expected_return_pct=-inf))
    yield edit(lambda k: k.update(stop_working_price=nan))
    yield edit(lambda k: k["scenarios"]["bull"].update(prob=nan))
    yield edit(lambda k: k["scenarios"]["bull"].update(value=10**400))
    yield edit(lambda k: k["inputs"]["price"].update(value=10**400))
    # an input named __proto__ is a name like any other: a multiple can divide by it
    proto = {"value": 1_000_000_000, "source": "S-1", "as_of": "2026-10-06"}
    yield edit(lambda k: (k["inputs"].update(__proto__=proto), k["outputs"]["multiples"][0].update(denominator="__proto__")))
    yield edit(lambda k: (k["inputs"].update(__proto__=proto), k["outputs"]["multiples"][0].update(numerator="__proto__", denominator="revenue")))
    yield edit(lambda k: k["outputs"]["multiples"][0].update(name={"__proto__": 1, "a": 2}))
    # a price with no basis is a last close, so it can be stale; an offer midpoint cannot
    yield edit(lambda k: (k["inputs"]["price"].pop("basis"), k["inputs"]["price"].update(as_of="2026-10-01")))
    yield edit(lambda k: k["inputs"]["price"].update(basis="offer midpoint", as_of="2026-10-01"))
    # empty or lone-value inputs, outputs and subject: an empty one is {}, and the detail names the type as Python does
    for bad in (None, 0, "", 5, 5.0, 2.5, True, "x", [1]):
        yield edit(lambda k, bad=bad: k.update(inputs=bad, outputs=bad, subject=bad))
    yield edit(lambda k: k["inputs"].update(preferred={"value": 100_000_000, "source": "S-1", "as_of": "2026-06-30"}))
    yield edit(lambda k: k["outputs"].update(enterprise_value=5_600_000_000))
    # revenue growth: 450% must be flagged; a prior year of 0 or below cannot be compared
    prior = {"source": "S-1", "as_of": "2025-06-30", "period": "LTM to 2025-06-30"}
    for v, flags in ((200_000_000, []), (200_000_000, ["outlier"]), (1_000_000_000, []), (0, []), (-5, [])):
        yield edit(lambda k, v=v, flags=flags: (k["inputs"].update(revenue_prior={**prior, "value": v}), k.update(flags=flags)))
    # the expected return in the rating check's detail is str() of the number as written: 24.0 stays 24.0
    for er in (24.0, 24, 24.5, -0.0, 0.0, 1e16, 1.5e-05, 10**21, -11.43):
        yield edit(lambda k, er=er: k["scenarios"].update(expected_return_pct=er))
    # an expected loss: no Overweight, whatever the conviction
    yield edit(lambda k: k["scenarios"].update(reference_price=70, expected_return_pct=-11.43))
    yield edit(lambda k: (k["scenarios"].update(reference_price=70, expected_return_pct=-11.43), k.update(rating="Underweight")))
    # a rating or conviction that is an object is printed in the detail as str() prints it, not a crash
    for bad in ({}, {"a": 1}, [{"b": 2}]):
        yield edit(lambda k, bad=bad: k.update(conviction=bad))
        yield edit(lambda k, bad=bad: k.update(rating=bad))
    # float() reads inf, infinity and nan in any case and with spaces, and digits grouped by single underscores
    for bad in ("inf", "-Infinity", "nan", " NaN ", "+inf", "1_000", "1__0", "_1"):
        yield edit(lambda k, bad=bad: k["scenarios"]["bull"].update(value=bad))
    # str() of numbers with no tag to go by (a date field): a huge integer, -0.0, a float
    for bad in (10**21, -(10**22), -0.0, 0.0, 2026.5):
        yield edit(lambda k, bad=bad: k.update(as_of=bad))
    # the multiple's name escaped as repr() escapes it: \r, non-printing characters past U+FFFF, 0.0
    for name in (["a\rb"], ["\U000e0001"], ["\U000f0000"], ["\U0001f600"], [0.0], ["\x7f", "\x85", "\u2028"]):
        yield edit(lambda k, name=name: k["outputs"]["multiples"][0].update(name=name))


# JSON written the way json.dumps never writes it, in place of the multiple's name: the browser must read it as json.loads does
RAW = ['-0', '-0.0', '1E400', '-Infinity', '1.0e2', '12345678901234567890123', '{"a": 1, "1": 0, "a": 2.0}',
       '{"__proto__": [1], "constructor": 2}', '"\\ud83d"', '"\\ud83d\\ude00"', '"\\/\\b\\f"', '"\\u00e9"',
       '9' * 4301, '9' * 4300,
       # not JSON to Python either: each makes the block invalid
       '"a\tb"', '"\\u12"', '"\\x41"', '[1,]', '01', '1.', '.5', '+1', 'nan', 'NaNx', '-NaN', 'infinity', "'a'", '{"a" 1}',
       '{1: 2}', '[1 2]', 'tru', '"open']


def raw_memos():
    b = copy.deepcopy(BLOCK)
    b["key_numbers"]["outputs"]["multiples"][0]["name"] = "@@"
    return [memo_with(b).replace('"@@"', raw) for raw in RAW]


def test_sizing_matches_the_python_to_the_cent():
    js = run_js({"sizes": SIZES, "views": [], "memos": []})["sizes"]
    assert len(js) == len(SIZES)
    for (pf, args), got in zip(SIZES, js):
        want = py_size(pf, args)
        if "error" in want:
            assert got == want, (args, got)                 # the same refusal, word for word
            continue
        for key in ("symbol", "conviction", "shares", "binding_rule", "limits_in_shares", "warnings"):
            assert got[key] == want[key], (args, key, got[key], want[key])
        for key in ("cost", "risk_budget", "loss_at_stop", "weight_after_pct", "cash_after"):
            assert abs(got[key] - want[key]) <= 0.011, (args, key, got[key], want[key])


def test_portfolio_values_and_breaches_match():
    pfs = [EXAMPLE, {**EXAMPLE, "cash": 50}, {**EXAMPLE, "rules": {**EXAMPLE["rules"], "max_sector_pct": 20}}]
    js = run_js({"sizes": [], "views": pfs, "memos": []})["views"]
    for pf, got in zip(pfs, js):
        v = portfolio.valued(portfolio.validate(copy.deepcopy(pf)))
        assert abs(got["equity"] - v["equity"]) < 1e-6
        assert got["breaches"] == v["rule_breaches"]


# Portfolio files as a person might mistype them: each is refused with the Python's own words, or read to the same view.
VALIDATE = """
const core = require(process.argv[1]);
let input = '';
process.stdin.on('data', (d) => input += d).on('end', () => {
  const out = JSON.parse(input).map((pf) => { try { return core.valued(core.validate(pf)); } catch (e) { return { error: e.message }; } });
  process.stdout.write(JSON.stringify(out));
});
"""
ONE = {"symbol": "AAA", "shares": 2, "price": 10}
PORTFOLIOS = [
    EXAMPLE, [], None, "portfolio", {}, {"cash": 0}, {"cash": 0, "holdings": [{**ONE, "shares": 0}]},
    {**EXAMPLE, "cash": 0}, {**EXAMPLE, "cash": None}, {**EXAMPLE, "cash": -5}, {**EXAMPLE, "cash": "lots"},
    {**EXAMPLE, "rules": None}, {**EXAMPLE, "rules": {"max_position_pct": 150}}, {**EXAMPLE, "rules": {"max_position_pct": "10"}},
    {**EXAMPLE, "rules": {"max_position_pct": True}}, {**EXAMPLE, "rules": {"min_cash_pct": -1}},
    {**EXAMPLE, "rules": {"max_order_value": 2e12}}, {**EXAMPLE, "rules": {"earnings_blackout_hours": 721}},
    {**EXAMPLE, "rules": {"max_volume_pct": 101}}, {**EXAMPLE, "rules": {"max_daily_loss_pct": None, "conviction_scale": None}},
    {**EXAMPLE, "rules": {"conviction_scale": {"Low": -1}}},
    {**EXAMPLE, "halted": "yes"}, {**EXAMPLE, "halted": None}, {**EXAMPLE, "halted": False},
    {**EXAMPLE, "day_pnl": "x"}, {**EXAMPLE, "day_pnl": None}, {**EXAMPLE, "day_pnl": False}, {**EXAMPLE, "day_pnl": -250.5},
    {**EXAMPLE, "equity_high": -1}, {**EXAMPLE, "equity_high": None}, {**EXAMPLE, "equity_high": 12_000},
    {"holdings": [{"shares": 1}]}, {"holdings": [{"symbol": None}]}, {"holdings": [{"symbol": "  "}]}, {"holdings": [{"symbol": 0}]},
    {"holdings": ["AAA"]}, {"holdings": [None]}, {"holdings": [["AAA"]]}, {"holdings": [{"symbol": "aaa"}, {"symbol": " AAA "}]},
    {"holdings": [{**ONE, "price": 0}]}, {"holdings": [{**ONE, "shares": None}]}, {"holdings": [{**ONE, "shares": -1}]},
    {"holdings": [{**ONE, "cost_basis": "100"}]}, {"holdings": [{**ONE, "price": "10"}]},
    {"cash": 100, "holdings": [ONE]},                                                  # no sector, date or as_of: Unknown, undated
    {"as_of": "2026-10-06", "cash": 100, "holdings": [{**ONE, "cost_basis": 0, "sector": ""}]},   # the date from as_of; no gain on 0
    {"cash": 100, "holdings": [{**ONE, "symbol": 7, "sector": [], "price_date": ["2026-10-06"]}]},   # str() of odd values
    {"cash": 100, "as_of": 20261006, "holdings": [{**ONE, "symbol": True, "sector": {"a": 1}, "price_date": 0}]},
    {"cash": 100, "holdings": [{"symbol": "AAA", "shares": 1}, {**ONE, "symbol": "BBB", "cost_basis": 8}]},   # one unpriced
    {"cash": 10, "holdings": [{**ONE, "sector": "Energy"}, {**ONE, "symbol": "BBB", "sector": "Energy"}]},     # every rule breached
]


def same(a, b, path="view"):
    """Equal, with floats compared to 1e-9 (the JS cannot tell 1.0 from 1)."""
    if isinstance(a, dict) and isinstance(b, dict):
        assert sorted(a) == sorted(b), (path, sorted(a), sorted(b))
        for k in a:
            same(a[k], b[k], f"{path}.{k}")
    elif isinstance(a, list) and isinstance(b, list):
        assert len(a) == len(b), path
        for i, (x, y) in enumerate(zip(a, b)):
            same(x, y, f"{path}[{i}]")
    elif isinstance(a, (int, float)) and not isinstance(a, bool) and isinstance(b, (int, float)) and not isinstance(b, bool):
        assert abs(a - b) <= 1e-9 * max(1, abs(a), abs(b)), (path, a, b)
    else:
        assert a == b, (path, a, b)


def test_a_portfolio_file_is_read_or_refused_as_the_python_does():
    r = subprocess.run([NODE, "-e", VALIDATE, str(CORE)], input=json.dumps(PORTFOLIOS), capture_output=True, text=True,
                       encoding="utf-8", timeout=60)
    assert r.returncode == 0, r.stderr
    got_all = json.loads(r.stdout)
    assert len(got_all) == len(PORTFOLIOS)
    for pf, got in zip(PORTFOLIOS, got_all):
        try:
            want = portfolio.valued(portfolio.validate(copy.deepcopy(pf)))
        except portfolio.PortfolioError as e:
            want = {"error": str(e)}
        same(got, want, json.dumps(pf)[:80])


def all_memos():
    return [memo_with(b) for b in broken_blocks()] + raw_memos() + ["no block here", "```json\n{oops\n```",
            '```json\n{"key_numbers": "open```', '```json\n{"key_numbers": {}} x\n```', '```json\n{"key_numbers": {}}\n```',
            memo_with(BLOCK) + "\n```json\n{oops\n```"]           # a stray invalid snippet does not hide the real block


# The parity contract for a check is its name and whether it passed. The demo also gives a detail for these, and for these
# only, word for word as the Python writes it: the type's name, the rating as written, the rating rule's "expected return
# ... -> ...; block says ..." line, and the stale price's age. The page leaves every other detail blank, and the Python's
# wording for those (recomputed figures, the scenarios as JSON) is not part of it.
TYPED = {"inputs is an object", "outputs is an object", "subject is an object"}
DETAILED = TYPED | {"rating is one of the four", "rating follows the thresholds", "stale price is flagged"}


def assert_memos_match(memos, js):
    assert len(js) == len(memos)
    for memo, got_full in zip(memos, js):
        py = verify.check_memo(memo)
        got, want = [[name, ok] for name, ok, _ in got_full], [[name, ok] for name, ok, _ in py]
        assert got == want, (memo[:80], [x for x in got if x not in want], [x for x in want if x not in got])
        assert [d for n, _, d in got_full if n in DETAILED] == [d for n, _, d in py if n in DETAILED], memo[:80]


def test_every_memo_check_matches_the_python():
    memos = all_memos()
    assert_memos_match(memos, run_js({"sizes": [], "views": [], "memos": memos})["memos"])


# Browsers before Chrome 114, Firefox 135 and Safari 18.4 give JSON.parse's reviver no source text: the checks must not
# depend on it, so the same memos run again with JSON.parse stripped of that argument.
OLD_BROWSER = """
const parse = JSON.parse;
JSON.parse = function (text, reviver) { return reviver ? parse(text, function (k, v) { return reviver.call(this, k, v); }) : parse(text); };
"""


def test_a_number_nobody_tagged_is_named_by_its_value():
    # check() called directly, not through a parsed memo: there is no record of how 2.5 or 24 was written, so a
    # non-integer is a float and an integer an int (the Python's own type names), and str() of 24 is 24
    out = json.loads(subprocess.run([NODE, "-e", """
const core = require(process.argv[1]);
const k = { inputs: 2.5, outputs: 7, subject: 0.5, rating: "Overweight", conviction: "High",
            scenarios: { bull: { value: 80, prob: 30 }, base: { value: 62, prob: 50 }, bear: { value: 35, prob: 20 }, reference_price: 50, expected_return_pct: 24.5 } };
process.stdout.write(JSON.stringify(core.check(k)));""", str(CORE)], capture_output=True, text=True, encoding="utf-8", timeout=60).stdout)
    details = {name: detail for name, _, detail in out}
    assert [details[n] for n in ("inputs is an object", "outputs is an object", "subject is an object")] == ["float", "int", "float"]
    assert details["rating follows the thresholds"] == "expected return 24.5%, conviction High -> Overweight; block says Overweight"


def test_the_checks_do_not_need_the_reviver_source_text():
    memos = all_memos()
    assert_memos_match(memos, run_js({"sizes": [], "views": [], "memos": memos}, prefix=OLD_BROWSER)["memos"])


# ----------------------------------------------------------------------------- projection charts (JS only)
PROJECT = """
const core = require(process.argv[1]);
let input = '';
process.stdin.on('data', (d) => input += d).on('end', () => {
  const job = JSON.parse(input);
  const out = {
    ratings: job.ratings.map(([er, conv]) => core.expectedRating(er, conv)),
    thresholds: core.THRESHOLDS,
    runs: job.runs.map((o) => { try { return core.project(o); } catch (e) { return { error: e.message }; } }),
  };
  process.stdout.write(JSON.stringify(out));
});
"""
SCEN = {"price": 50, "bull": {"value": 80, "prob": 30}, "base": {"value": 62, "prob": 50}, "bear": {"value": 35, "prob": 20},
        "stop": 40, "months": 12, "vol": 35, "conviction": "Medium"}


def run_project(job):
    r = subprocess.run([NODE, "-e", PROJECT, str(CORE)], input=json.dumps(job), capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def test_the_charts_rate_by_the_bots_own_thresholds():
    grid = [[er, conv] for er in (-30, -10.01, -10, -9.99, 0, 14.99, 15, 15.01, 40) for conv in ("Low", "Medium", "High")]
    out = run_project({"ratings": grid, "runs": []})
    assert out["ratings"] == [verify.expected_rating(er, conv) for er, conv in grid]
    t = out["thresholds"]                                   # the numbers the page draws its gauge and notes from
    assert (t["overweight"], t["underweight"], set(t["conviction_ok"])) == (verify.OVERWEIGHT, verify.UNDERWEIGHT, verify.CONVICTION_OK)


def test_the_projection_lands_on_the_scenarios_and_the_pwv():
    a, b, other = run_project({"ratings": [], "runs": [SCEN, SCEN, {**SCEN, "seed": 2}]})["runs"]
    assert a == b and a["bands"] != other["bands"]                        # the seed fixes the paths
    want = verify.pwv({c: SCEN[c] for c in ("bull", "base", "bear")})
    assert abs(a["pwv"] - want) < 1e-9 and abs(a["weighted"][-1] - want) < 1e-9
    assert abs(a["expected_return_pct"] - 100 * (want / 50 - 1)) < 1e-9
    assert a["rating"] == verify.expected_rating(a["expected_return_pct"], "Medium")
    for c in ("bull", "base", "bear"):
        assert abs(a["scenario"][c][0] - 50) < 1e-9 and abs(a["scenario"][c][-1] - SCEN[c]["value"]) < 1e-9
    assert abs(a["mean_end"] / want - 1) < 0.03                            # the paths average out at the PWV
    assert all(abs(n / 2000 - SCEN[c]["prob"] / 100) < 0.04 for c, n in a["picks"].items())


def test_the_bands_are_ordered_and_start_at_todays_price():
    run = run_project({"ratings": [], "runs": [SCEN]})["runs"][0]
    bands = [run["bands"][k] for k in ("p10", "p25", "p50", "p75", "p90")]
    assert all(abs(b[0] - 50) < 1e-9 for b in bands)
    for i in range(len(run["t"])):
        assert all(lo <= hi + 1e-9 for lo, hi in zip([b[i] for b in bands], [b[i] for b in bands][1:]))
    assert run["p_touch_stop"] >= run["p_end_below_stop"]                  # ending below the stop means it was touched
    assert sum(run["histogram"]["counts"]) >= 0.97 * 2000
    assert run["range80"][0] < run["pwv"] < run["range80"][1]


def test_more_volatility_widens_the_bands_and_bad_input_is_refused():
    calm, wild, *bad = run_project({"ratings": [], "runs": [
        {**SCEN, "vol": 15}, {**SCEN, "vol": 70},
        {**SCEN, "bull": {"value": 80, "prob": 35}}, {**SCEN, "bear": {"value": 70, "prob": 20}},
        {**SCEN, "price": 0}, {**SCEN, "months": 0}]})["runs"]
    width = lambda r: r["bands"]["p90"][len(r["t"]) // 2] - r["bands"]["p10"][len(r["t"]) // 2]
    assert width(wild) > width(calm) and wild["p_touch_stop"] > calm["p_touch_stop"]
    assert [("error" in r) for r in bad] == [True] * 4
    assert "100%" in bad[0]["error"] and "bear < base < bull" in bad[1]["error"]


# ----------------------------------------------------------------------------- sorting trade options (JS only)
SORT = """
const core = require(process.argv[1]);
let input = '';
process.stdin.on('data', (d) => input += d).on('end', () => {
  const job = JSON.parse(input), view = core.valued(core.validate(job.portfolio));
  const rows = job.ideas.map((i) => core.tradeMetrics(i, view));
  const out = { rows: rows.map(({ idea, ...r }) => r), sorts: {} };
  for (const key of Object.keys(core.TRADE_SORTS)) for (const dir of ['best', 'worst'])
    out.sorts[key + ':' + dir] = core.sortTrades(rows, key, dir).map((r) => r.symbol);
  try { core.sortTrades(rows, 'nonsense'); } catch (e) { out.bad = e.message; }
  out.inherited = ['toString', 'constructor', '__proto__'].map((k) => { try { core.sortTrades(rows, k); return 'sorted'; } catch (e) { return e.message; } });
  process.stdout.write(JSON.stringify(out));
});
"""
IDEAS = [
    {**SCEN, "symbol": "EXM", "sector": "Technology"},
    {**SCEN, "symbol": "NEWCO", "sector": "Technology", "price": 28, "stop": 21, "vol": 75,
     "bull": {"value": 52, "prob": 25}, "base": {"value": 31, "prob": 45}, "bear": {"value": 16, "prob": 30}},
    {**SCEN, "symbol": "UTIL", "sector": "Utilities", "price": 64, "stop": 56, "vol": 18, "conviction": "High",
     "bull": {"value": 74, "prob": 25}, "base": {"value": 68, "prob": 55}, "bear": {"value": 58, "prob": 20}},
    {**SCEN, "symbol": "NOSTOP", "stop": None},
    {**SCEN, "symbol": "ODD", "conviction": "Certain"},                      # a conviction the rules have no scale for
    {c: v for c, v in SCEN.items() if c != "conviction"},                    # no symbol, sector or conviction
    {**SCEN, "symbol": "AAA", "sector": "Technology", "price": 180, "stop": 170,   # held already
     "bull": {"value": 260, "prob": 30}, "base": {"value": 210, "prob": 50}, "bear": {"value": 150, "prob": 20}},
]


def run_sort():
    r = subprocess.run([NODE, "-e", SORT, str(CORE)], input=json.dumps({"portfolio": EXAMPLE, "ideas": IDEAS}),
                       capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def test_each_trade_option_is_projected_and_sized_by_the_same_rules():
    out = run_sort()
    rows = {r["symbol"]: r for r in out["rows"]}
    view = portfolio.valued(portfolio.validate(copy.deepcopy(EXAMPLE)))
    for idea in IDEAS[:3]:
        r = rows[idea["symbol"]]
        want = portfolio.size_position(copy.deepcopy(view), idea["symbol"], idea["price"], idea["stop"], idea["conviction"], idea["sector"])
        assert r["shares"] == want["shares"] and abs(r["loss_at_stop"] - want["loss_at_stop"]) <= 0.011
        pwv = verify.pwv({c: idea[c] for c in ("bull", "base", "bear")})
        assert abs(r["reward_risk"] - (pwv - idea["price"]) / (idea["price"] - idea["stop"])) < 1e-9
        assert r["rating"] == verify.expected_rating(100 * (pwv / idea["price"] - 1), idea["conviction"])
    assert rows["NOSTOP"]["reward_risk"] is None and rows["NOSTOP"]["shares"] is None and rows["NOSTOP"]["p_touch_stop"] is None
    # a conviction with no scale cannot be sized, but is still projected
    assert rows["ODD"]["shares"] is None and rows["ODD"]["loss_at_stop"] is None and rows["ODD"]["p_touch_stop"] is not None
    # no symbol is "NEW", sized at Medium conviction with no sector; a held stock is sized against what is held
    assert rows["NEW"]["rating"] == rows["EXM"]["rating"]
    for sym, args in (("NEW", ("NEW", 50, 40, "Medium", None)), ("AAA", ("AAA", 180, 170, "Medium", "Technology"))):
        want = portfolio.size_position(copy.deepcopy(view), *args)
        assert rows[sym]["shares"] == want["shares"] and abs(rows[sym]["loss_at_stop"] - want["loss_at_stop"]) <= 0.011


def test_trade_options_sort_best_first_with_blanks_last():
    out = run_sort()
    rows = {r["symbol"]: r for r in out["rows"]}
    for key, best in (("expected_return_pct", "high"), ("reward_risk", "high"), ("p_end_above_price", "high"),
                      ("p_touch_stop", "low"), ("shares", "high")):
        for dir in ("best", "worst"):
            order = out["sorts"][f"{key}:{dir}"]
            have = [s for s in order if rows[s][key] is not None]
            assert order[len(have):] == sorted(s for s in order if rows[s][key] is None)    # blanks last, by symbol
            values = [rows[s][key] for s in have]
            high_first = (best == "high") == (dir == "best")
            assert values == sorted(values, reverse=high_first), (key, dir, order)
    assert out["sorts"]["symbol:best"] == sorted(rows)
    rank = {"Overweight": 2, "Equal-weight": 1, "Underweight": 0}
    by_rating = out["sorts"]["rating:best"]
    assert [rank[rows[s]["rating"]] for s in by_rating] == sorted((rank[rows[s]["rating"]] for s in by_rating), reverse=True)
    assert "unknown sort" in out["bad"]
    assert [m.split(":")[0] for m in out["inherited"]] == ["unknown sort"] * 3      # a name Object.prototype has is not a measure


# ----------------------------------------------------------------------------- the page's own use (JS only)
BROWSER = """
const vm = require('vm'), fs = require('fs'), file = process.argv[1], node = require(file);
const window = {};                                 // a page: no module, a global "self" the script hangs IpoCore on
vm.runInNewContext(fs.readFileSync(file, 'utf8'), { self: window }, { filename: file });
const page = window.IpoCore;
process.stdout.write(JSON.stringify({ page: Object.keys(page), node: Object.keys(node), rating: page.expectedRating(20, 'High'),
  memo: page.checkMemo('no block here')[0][1], thresholds: page.THRESHOLDS }));
"""


def test_the_page_gets_the_same_engine_as_node():
    r = subprocess.run([NODE, "-e", BROWSER, str(CORE)], capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout)
    assert out["page"] == out["node"] and "checkMemo" in out["page"] and "sizePosition" in out["page"]
    assert out["rating"] == verify.expected_rating(20, "High") and out["memo"] is False
    assert out["thresholds"]["overweight"] == verify.OVERWEIGHT


# An unforeseen error inside the checks (forced here by breaking Math.abs) must come back as one failed check, so the
# page shows it instead of freezing; the KEY NUMBERS block itself was read.
FAULT = """
const core = require(process.argv[1]);
let input = '';
process.stdin.on('data', (d) => input += d).on('end', () => {
  Math.abs = () => { throw new Error('boom'); };
  process.stdout.write(JSON.stringify(core.checkMemo(input)));
});
"""


def test_an_error_inside_the_checks_is_a_failed_check_not_a_crash():
    r = subprocess.run([NODE, "-e", FAULT, str(CORE)], input=memo_with(BLOCK), capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout) == [["KEY NUMBERS block present and valid", True, ""], ["the block's shape can be checked", False, "boom"]]


def test_the_projection_defaults_and_a_certain_path():
    bare = {c: v for c, v in SCEN.items() if c not in ("months", "vol", "conviction")}
    certain = {**SCEN, "vol": 0, "bull": {"value": 80, "prob": 0}, "base": {"value": 62, "prob": 100}, "bear": {"value": 35, "prob": 0}}
    low = {**SCEN, "conviction": "Low"}
    a, b, c, d = run_project({"ratings": [], "runs": [bare, SCEN, certain, low]})["runs"]
    assert a == b                                          # 12 months, 35% volatility and Medium conviction by default
    assert (a["months"], a["vol"], len(a["t"])) == (12, 35, 49)
    # no volatility and one sure case: every path is that case's own line, so every band is it and the stop is never touched
    for band in c["bands"].values():
        assert all(abs(x - y) < 1e-9 * y for x, y in zip(band, c["scenario"]["base"]))
    assert c["picks"] == {"bull": 0, "base": 2000, "bear": 0} and abs(c["pwv"] - 62) < 1e-9
    assert c["p_touch_stop"] == 0 and c["p_end_below_stop"] == 0 and c["p_end_above_price"] == 1
    assert sum(c["histogram"]["counts"]) == 2000 and abs(c["histogram"]["lo"] - 62) < 1e-9 and c["histogram"]["width"] > 0
    assert a["rating"] == "Overweight" and d["rating"] == verify.expected_rating(d["expected_return_pct"], "Low") == "Equal-weight"


def test_a_projection_with_impossible_inputs_is_refused():
    bad = [{**SCEN, "bull": None}, {**SCEN, "bull": {"value": 0, "prob": 30}}, {**SCEN, "bear": {"value": 35, "prob": -5}},
           {**SCEN, "base": {"value": 62}}, {**SCEN, "vol": 250}, {**SCEN, "vol": -1}, {**SCEN, "months": 1.5}, {**SCEN, "months": 37},
           {**SCEN, "price": None}]
    runs = run_project({"ratings": [], "runs": bad})["runs"]
    assert [r.get("error") for r in runs] == [
        "bull needs a value above 0 and a probability", "bull needs a value above 0 and a probability",
        "bear needs a value above 0 and a probability", "base needs a value above 0 and a probability",
        "volatility must be 0% to 200%", "volatility must be 0% to 200%", "horizon must be 1 to 36 months",
        "horizon must be 1 to 36 months", "price must be above 0"]
