"""scripts/js_coverage.py on a tiny synthetic V8 coverage file: no Node needed.

The source is CRLF and has astral characters (two UTF-16 units each) before the code that matters, because V8 reports
offsets in UTF-16 units of the file as it read it: a mapping that counted code points, or dropped the CRs, would put
the missed branch and the uncalled function on the wrong line.
"""
import importlib.util
import json
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("js_coverage", ROOT / "scripts" / "js_coverage.py")
jc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(jc)

LINES = [
    "function f(x) {",                                    # 1
    '  const s = "' + "\U0001F600" * 30 + '";',          # 2: 30 astral characters, 60 UTF-16 units
    "  if (x) { return 1; }",                             # 3
    "  else { return 2; }",                               # 4: the branch the first process never takes
    "}",                                                  # 5
    "function g() { return 3; }",                         # 6: called by no process but the second
    "// only a comment",                                  # 7
    "",                                                   # 8
]
SOURCE = "\r\n".join(LINES)


def units(text):
    return len(text.encode("utf-16-le")) // 2


def start_of(line, col=0):
    """The UTF-16 offset of column col (in characters) of a 1-based line."""
    before = "\r\n".join(LINES[:line - 1]) + ("\r\n" if line > 1 else "")
    return units(before + LINES[line - 1][:col])


F = (start_of(1), start_of(5, 1))
G = (start_of(6), start_of(6, len(LINES[5])))
ELSE = (start_of(4, 2), start_of(4, len(LINES[3])))
END = units(SOURCE)


def rng(span, count):
    return {"startOffset": span[0], "endOffset": span[1], "count": count}


def process(url, f_count=1, else_count=0, g_count=0, wrapper_end=END):
    """One process's report: the wrapper around the module, then f (with its else block) and g."""
    return {"result": [
        {"scriptId": "1", "url": "node:internal/x", "functions": [{"functionName": "", "isBlockCoverage": True, "ranges": [rng((0, 5), 1)]}]},
        {"scriptId": "2", "url": url, "functions": [
            {"functionName": "", "isBlockCoverage": True, "ranges": [rng((0, wrapper_end), 1)]},
            {"functionName": "f", "isBlockCoverage": True, "ranges": [rng(F, f_count), rng(ELSE, else_count)]},
            {"functionName": "g", "isBlockCoverage": False, "ranges": [rng(G, g_count)]},
        ]}]}


@pytest.fixture
def app(tmp_path, monkeypatch):
    folder = tmp_path / "docs" / "app"
    folder.mkdir(parents=True)
    path = folder / "core.js"
    path.write_bytes(SOURCE.encode("utf-8"))                 # the CRs stay
    monkeypatch.setattr(jc, "APP", folder)
    return path


def write(tmp_path, name, data, bom=False):
    d = tmp_path / "cov"
    d.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data) if not isinstance(data, str) else data
    (d / name).write_bytes((b"\xef\xbb\xbf" if bom else b"") + text.encode("utf-8"))
    return d


def figures(app, cov_dir):
    files = jc.collect(str(cov_dir))
    return jc.report(app.resolve(), *files[app.resolve()])


def test_offsets_become_lines_with_crlf_and_astral_characters(app, tmp_path):
    r = figures(app, write(tmp_path, "a.json", process(str(app.resolve()))))
    assert r["lines"] == (4, 6)                               # lines 1-3 and 5 ran; 4 and 6 did not; the comment and blank do not count
    assert r["missed_lines"] == [4, 6]
    assert r["functions"] == (1, 2) and r["missed_functions"] == ["g (line 6)"]   # the wrapper around the module is not a function
    assert r["branches"] == (0, 1) and r["missed_branch_lines"] == [4]
    assert jc.utf16_text(app)[0] == SOURCE and len(jc.utf16_text(app)[1]) == END


def test_processes_add_up_and_a_file_url_is_the_same_file(app, tmp_path):
    d = write(tmp_path, "a.json", process(str(app.resolve())))
    write(tmp_path, "b.json", process(app.resolve().as_uri(), f_count=1, else_count=3, g_count=2))
    r = figures(app, d)
    assert r["lines"] == (6, 6) and r["functions"] == (2, 2) and r["branches"] == (1, 1)     # a branch is covered if any process took it
    assert r["missed_lines"] == r["missed_functions"] == r["missed_branch_lines"] == []


def test_a_file_no_process_loaded_is_all_missed(app, tmp_path):
    d = write(tmp_path, "a.json", {"result": [{"scriptId": "1", "url": "node:internal/x", "functions": []}]})
    files = jc.collect(str(d))
    assert files[app.resolve()][0] is None
    r = jc.report(app.resolve(), *files[app.resolve()])
    assert r["lines"] == (0, 6) and r["functions"] == (0, 0) and r["branches"] == (0, 0)


def test_fail_under_compares_lines_functions_and_branches(app, tmp_path, capsys):
    one = write(tmp_path, "a.json", process(str(app.resolve())))           # lines 4/6 = 66.7%, functions 1/2 = 50%, branches 0/1 = 0%
    jc.main([str(one)])
    out = capsys.readouterr().out
    assert "core.js" in out and "66.7%" in out and "50.0%" in out and "missed lines: 4, 6" in out
    assert "missed branches on lines: 4" in out and "missed functions: g (line 6)" in out
    jc.main([str(one), "--fail-under", "0"])
    for floor in ("1", "50", "100"):                              # branches are at 0%, so any floor above 0 fails
        with pytest.raises(SystemExit) as e:
            jc.main([str(one), "--fail-under", floor])
        assert f"under {float(floor)}%" in str(e.value)
    full = write(tmp_path / "full", "a.json", process(str(app.resolve()), else_count=1, g_count=1))
    jc.main([str(full), "--fail-under", "100"])                  # everything ran: 100% passes a 100% floor
    assert "100.0%   6/6" in capsys.readouterr().out


def test_a_floor_applies_to_each_measure_on_its_own(app, tmp_path):
    lines_only = write(tmp_path, "a.json", process(str(app.resolve()), else_count=1, g_count=1))
    jc.main([str(lines_only), "--fail-under", "100"])
    functions_low = write(tmp_path / "f", "a.json", process(str(app.resolve()), else_count=1, g_count=0))
    with pytest.raises(SystemExit):                              # g never ran: lines and functions are under 100
        jc.main([str(functions_low), "--fail-under", "100"])


def test_no_coverage_for_the_app_is_an_error_not_a_pass(app, tmp_path):
    d = write(tmp_path, "a.json", {"result": [{"scriptId": "1", "url": "node:internal/x", "functions": []}]})
    with pytest.raises(SystemExit) as e:
        jc.main([str(d), "--fail-under", "100"])
    assert "no coverage for docs/app/*.js" in str(e.value)


def test_a_utf8_bom_on_the_coverage_file_is_read(app, tmp_path):
    r = figures(app, write(tmp_path, "a.json", process(str(app.resolve())), bom=True))     # what a Windows shell's redirect writes
    assert r["lines"] == (4, 6)


def test_a_half_written_coverage_file_is_a_clear_error(app, tmp_path):
    d = write(tmp_path, "a.json", '{"result": [{"scriptId": "1", "ur')
    with pytest.raises(SystemExit) as e:
        jc.collect(str(d))
    assert "cannot read the V8 coverage file" in str(e.value) and "a.json" in str(e.value)
    d = write(tmp_path / "k", "a.json", {"no": "result"})
    with pytest.raises(SystemExit):
        jc.collect(str(d))


def test_a_range_that_starts_at_the_end_of_the_file_does_not_crash(app, tmp_path):
    data = process(str(app.resolve()))
    eof = rng((END, END + 1), 0)                                 # V8 can end a block at the final newline or beyond it
    data["result"][1]["functions"][1]["ranges"].append(eof)
    data["result"][1]["functions"].append({"functionName": "tail", "isBlockCoverage": True, "ranges": [rng((END, END), 0), rng((END, END), 0)]})
    r = figures(app, write(tmp_path, "a.json", data))
    assert r["lines"] == (4, 6)
    assert "tail (line 7)" in r["missed_functions"]              # the last character's line, not an IndexError
    assert r["missed_branch_lines"] == [4, 7]


def test_an_empty_file_has_nothing_to_cover(tmp_path, monkeypatch):
    folder = tmp_path / "docs" / "app"
    folder.mkdir(parents=True)
    (folder / "empty.js").write_bytes(b"")
    monkeypatch.setattr(jc, "APP", folder)
    r = jc.report((folder / "empty.js").resolve(), None, {(0, 0): "x"}, {(0, 0)})
    assert r["lines"] == (0, 0) and r["missed_functions"] == ["x (line 1)"] and r["missed_branch_lines"] == [1]


def test_ranges_text_joins_runs():
    assert jc.ranges_text([3, 4, 5, 9, 11, 12]) == "3-5, 9, 11-12" and jc.ranges_text([]) == ""
    assert jc.pct((0, 0)) == 100.0 and jc.script_path("node:internal/x") is None and jc.script_path("") is None


def test_run_tests_runs_the_node_tests_with_coverage_switched_on(monkeypatch, tmp_path):
    seen = []

    def run(cmd, cwd, env):
        seen.append((cmd, cwd, env))
        return type("Done", (), {"returncode": seen_code[0]})()
    seen_code = [0]
    monkeypatch.setattr(jc.subprocess, "run", run)                # no Node, no second pytest
    jc.run_tests(str(tmp_path))
    cmd, cwd, env = seen[0]
    assert cmd[:6] == [sys.executable, "-B", "-m", "pytest", "-q", "-p"] and cwd == jc.ROOT
    assert env["NODE_V8_COVERAGE"] == str(tmp_path)               # what every Node process the tests start inherits
    assert any(c.endswith("test_js_coverage.py") for c in cmd) and all("test_js_" in c for c in cmd[7:])
    seen_code[0] = 3
    with pytest.raises(SystemExit) as e:                          # a failing Node test fails the report, with its code
        jc.run_tests(str(tmp_path))
    assert e.value.code == 3


def test_with_no_directory_the_tests_run_into_a_temporary_one(app, monkeypatch, capsys):
    dirs = []

    def run_tests(cov_dir):                                       # stands in for Node writing its raw coverage
        dirs.append(cov_dir)
        (pathlib.Path(cov_dir) / "a.json").write_text(json.dumps(process(str(app.resolve()), else_count=1, g_count=1)))
    monkeypatch.setattr(jc, "run_tests", run_tests)
    jc.main(["--fail-under", "100"])
    assert "100.0%   6/6" in capsys.readouterr().out
    assert len(dirs) == 1 and not pathlib.Path(dirs[0]).exists()  # the temporary directory is cleaned up
