"""The harness's synthetic demo (demo_setup.py) and the harness checks it exists to exercise, on a small demo world and
whatever HARNESS_SETUP says: the honest learner starts from the base rate and then fits, it passes the leak test and
the masking test, and the two bots that leak on purpose are caught."""
import math
import pathlib
import sys

import numpy as np
import pandas as pd
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "evaluation" / "harness"))

import bot_benchmark as bb  # noqa: E402
import demo_setup as D  # noqa: E402

SMALL = {"n_tickers": 6, "n_days": 120, "every": 2, "n_ipos": 30}     # 360 stock events and 30 IPOs


@pytest.fixture(scope="module")
def demo():
    return D.build_demo(**SMALL)


@pytest.fixture(scope="module")
def learner(demo):
    """The honest learner after one walk-forward over the demo, and its predictions."""
    store, events = demo
    bot = D.LearningBot()
    return bot, bb.run_walk_forward(lambda s: bot, store, events)


@pytest.fixture(scope="module")
def candidate(learner):
    return learner[1]


def test_the_demo_world_is_well_formed_and_reproducible(demo):
    store, events = demo
    kinds = pd.Series([e.kind for e in events]).value_counts().to_dict()
    assert kinds == {"market": 6 * 60, "ipo": 30}
    assert len({e.event_id for e in events}) == len(events)
    assert {e.threshold for e in events if e.kind == "market"} == {0.0} and {e.threshold for e in events if e.kind == "ipo"} == {0.10}
    published = store.frame.query("field == 'outcome'").set_index("entity")["available_at"]
    assert published.index.is_unique and all(published[e.event_id] > e.as_of for e in events)   # no outcome is known early
    assert set(store.frame["field"]) == {"signal", "range_revision", "heat", "outcome"}
    again, _ = D.build_demo(**SMALL)
    pd.testing.assert_frame_equal(again.frame, store.frame)                                       # a seed, not luck
    assert not D.build_demo(seed=8, **SMALL)[0].frame.equals(store.frame)


def test_the_learner_starts_from_the_base_rate_then_fits_a_model(demo, candidate):
    store, events = demo
    assert len(candidate) == len(events) and candidate["prob_up"].between(0.01, 0.99).all()
    first = candidate[candidate["as_of"] == candidate["as_of"].min()]
    assert (first["prob_up"] == 0.5).all() and (first["expected_return"] == 0.0).all()        # nothing known yet
    # once 30 stock outcomes are in, each name's call follows its own signal instead of one shared base rate
    late = candidate[(candidate["as_of"] == candidate["as_of"].max()) & candidate["event_id"].str.startswith("TCK")]
    assert late["prob_up"].nunique() == len(late) == 6
    signal = store.view(late["as_of"].iloc[0]).latest_many("signal")
    order = late.assign(s=[signal[e.split("@")[0]] for e in late["event_id"]]).sort_values("s")
    assert order["expected_return"].is_monotonic_increasing                                       # a positive slope on the signal
    assert D._phi(0.0) == 0.5 and D._det_noise("x") == D._det_noise("x") != D._det_noise("y")


def test_the_rival_adds_noise_and_ignores_the_revision(demo, learner, candidate):
    store, events = demo
    rival = D.LearningBot(name="rival_bot", signal_noise=1.5, use_revision=False)
    run = bb.run_walk_forward(lambda s: rival, store, events)
    assert set(run["bot"]) == {"rival_bot"} and len(run) == len(events)
    assert all(x[1] == 0.0 for kind, x in rival._log.values() if kind == "ipo")                 # the revision is never read
    noisy = [x[1] for kind, x in rival._log.values() if kind == "market"]
    assert noisy != [x[1] for kind, x in learner[0]._log.values() if kind == "market"]
    scored = bb.attach_outcomes(pd.concat([candidate, run], ignore_index=True), store, events)
    mine, theirs = (scored[scored["bot"] == b] for b in ("candidate", "rival_bot"))
    assert bb.brier(mine["prob_up"], mine["y"]) < bb.brier(theirs["prob_up"], theirs["y"])   # the clean signal wins


def test_the_leak_test_passes_the_honest_bot_and_catches_both_planted_leaks(demo):
    store, events = demo
    cuts = bb.pick_cut_dates(events, 1)
    assert bb.future_invariance(lambda s: D.LearningBot(), store, events, cuts).empty
    for factory in (D.CheaterBot, D.LeakyScalerBot):
        flagged = bb.future_invariance(factory, store, events, cuts)
        assert len(flagged) and list(flagged.columns) == ["cut_date", "event_id", "prob_up", "prob_up_perturbed"]
        assert set(flagged["cut_date"]) == set(cuts)
    cheat = bb.run_walk_forward(D.CheaterBot, store, events)
    joined = bb.attach_outcomes(cheat, store, events)
    assert ((joined["prob_up"] > 0.5) == (joined["y"] == 1)).all()                               # it knows every answer


def test_scrambling_the_future_leaves_the_past_alone(demo):
    store, events = demo
    t = bb.pick_cut_dates(events, 1)[0]
    before, after = store.frame, store.perturb_after(t, seed=3).frame
    past = before["available_at"] <= t
    pd.testing.assert_frame_equal(before[past], after[past])
    assert not np.allclose(before.loc[~past, "value"], after.loc[~past, "value"])


def test_hiding_company_names_does_not_change_a_numbers_only_bot(demo, candidate):
    store, events = demo
    m_store, m_events, back = bb.mask_identities(store, events)
    assert all(e.entity.startswith(("ENT", "EVT")) for e in m_events) and not set(m_store.frame["entity"]) & {e.entity for e in events}
    assert sorted(back.values()) == sorted(e.event_id for e in events)
    masked = bb.run_walk_forward(lambda s: D.LearningBot(), m_store, m_events)
    masked["event_id"] = masked["event_id"].map(back)
    m = candidate.merge(masked, on="event_id", suffixes=("", "_masked"))
    assert len(m) == len(events) and np.allclose(m["prob_up"], m["prob_up_masked"], atol=1e-12)


def test_the_learner_ranks_stocks_and_its_report_names_every_bot(demo, candidate):
    store, events = demo
    base = bb.run_walk_forward(lambda s: bb.BaseRateBot(), store, events)
    joined = bb.attach_outcomes(pd.concat([candidate, base], ignore_index=True), store, events)
    market = joined[(joined["bot"] == "candidate") & (joined["kind"] == "market")]
    ic, t, n = bb.information_coefficient(market)
    assert n > 30 and ic > 0 and math.isfinite(t)
    text = bb.format_report(joined, "candidate", [base["bot"].iloc[0]])
    assert "candidate" in text and base["bot"].iloc[0] in text
