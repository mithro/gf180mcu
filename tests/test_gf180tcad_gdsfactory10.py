# SPDX-License-Identifier: Apache-2.0
"""Regression tests of the mithro/gf180mcu fork for gf180-tcad (https://github.com/mithro/gf180-tcad).

The fork makes gf180mcu import under gdsfactory's development HEAD (10.0.0rc0), and must not change
the geometry of the transistors gf180-tcad uses. The fork's CI runs this module under gdsfactory
9.51.0 and under gdsfactory 10.0.0rc0 (.github/workflows/test.yml).

- ``test_import_*``: a fresh interpreter imports gf180mcu. Upstream main (96b7324) fails under
  gdsfactory 10.0.0rc0: with ``PDK=gf180mcu`` by a circular import ("partially initialized module
  'gf180mcu'"), without it with "No active PDK", because gf180mcu/tech.py built its cross-sections
  at import time and from gdsfactory 10 that layer lookup activates ``$PDK``.
- ``test_fet_gds_*``: ``nfet``/``pfet`` at ``volt="5.0V"`` against reference GDS files
  (tests/gf180tcad_ref/) written by upstream main 96b7324 under gdsfactory 9.51.0: the same bytes
  under gdsfactory 9.51.0, and an empty XOR on every layer under any gdsfactory.
"""

import os
import subprocess
import sys
from pathlib import Path

import gdsfactory as gf
import pytest

import gf180mcu
import klayout.db as kdb

ROOT = Path(__file__).resolve().parent.parent
REF = Path(__file__).resolve().parent / "gf180tcad_ref"
# The gdsfactory release under which the reference GDS files were written (by upstream 96b7324).
REF_GDSFACTORY = "9.51.0"

FETS = {
    "nfet_5v0": ("nfet", {"volt": "5.0V"}),
    "pfet_5v0": ("pfet", {"volt": "5.0V"}),
    "nfet_5v0_l0p6_w1_nf2": ("nfet", {"volt": "5.0V", "l_gate": 0.6, "w_gate": 1.0, "nf": 2}),
    "pfet_5v0_l0p6_w1_nf2": ("pfet", {"volt": "5.0V", "l_gate": 0.6, "w_gate": 1.0, "nf": 2}),
}


def _run_fresh(code: str, pdk: str | None) -> subprocess.CompletedProcess[str]:
    env = {k: v for k, v in os.environ.items() if k != "PDK"}
    if pdk is not None:
        env["PDK"] = pdk
    env["PYTHONPATH"] = os.pathsep.join(filter(None, [str(ROOT), env.get("PYTHONPATH")]))
    return subprocess.run(
        [sys.executable, "-c", code], env=env, cwd=ROOT, capture_output=True, text=True, check=False
    )


IMPORT_CODE = """
import gdsfactory as gf
import gf180mcu
assert gf180mcu.__file__.startswith(__import__("os").getcwd()), gf180mcu.__file__
print(gf.get_active_pdk().name)
print(gf.get_cross_section("metal1").width)
print(gf180mcu.cells.nfet(volt="5.0V").name)
"""


@pytest.mark.parametrize("pdk", ["gf180mcu", None], ids=["PDK=gf180mcu", "no-PDK"])
def test_import_fresh_interpreter(pdk: str | None) -> None:
    r = _run_fresh(IMPORT_CODE, pdk)
    assert r.returncode == 0, r.stderr
    lines = r.stdout.splitlines()
    assert lines[0] == "gf180mcu"
    assert float(lines[1]) == 0.2
    assert lines[2].startswith("nfet_LG0p28_WG0p22_")


@pytest.fixture(scope="module")
def written(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Path]:
    """Each cell, built and written once: a second write in one session differs in its metadata."""
    out = tmp_path_factory.mktemp("gf180tcad_fets")
    paths = {}
    for name, (cell, kwargs) in FETS.items():
        paths[name] = out / f"{name}.gds"
        getattr(gf180mcu.cells, cell)(**kwargs).write_gds(paths[name])
    return paths


def _regions(path: Path) -> dict[tuple[int, int], kdb.Region]:
    layout = kdb.Layout()
    layout.read(str(path))
    assert layout.dbu == 0.001
    top = layout.top_cell()
    out = {}
    for li in layout.layer_indices():
        info = layout.get_info(li)
        region = kdb.Region(top.begin_shapes_rec(li))
        region.merge()
        out[(info.layer, info.datatype)] = region
    return out


@pytest.mark.parametrize("name", sorted(FETS))
def test_fet_gds_xor_matches_upstream(name: str, written: dict[str, Path]) -> None:
    got = _regions(written[name])
    ref = _regions(REF / f"{name}.gds")
    assert sorted(got) == sorted(ref)
    for key in sorted(ref):
        assert (got[key] ^ ref[key]).is_empty(), f"{name}: XOR not empty on layer {key}"


@pytest.mark.skipif(
    gf.__version__ != REF_GDSFACTORY,
    reason=f"byte identity is defined under gdsfactory {REF_GDSFACTORY}, the reference's writer",
)
@pytest.mark.parametrize("name", sorted(FETS))
def test_fet_gds_bytes_match_upstream(name: str, written: dict[str, Path]) -> None:
    assert written[name].read_bytes() == (REF / f"{name}.gds").read_bytes()
