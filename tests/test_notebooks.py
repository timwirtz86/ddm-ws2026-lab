"""Execute the student notebooks top to bottom (installation check on every OS).

The unsolved TODO functions raise ``NotImplementedError``; that is expected.
Any other error (import error, missing file, broken path) fails the test.

Slow (about a minute), so it only runs when the environment variable
``DDM_RUN_NOTEBOOK_TESTS=1`` is set (the GitHub workflow sets it):

    DDM_RUN_NOTEBOOK_TESTS=1 uv run pytest tests/test_notebooks.py
"""

from __future__ import annotations

import os
from pathlib import Path

import nbformat
import pytest
from nbconvert.preprocessors import ExecutePreprocessor

NOTEBOOK_DIR = Path(__file__).resolve().parents[1] / "notebooks"
# one folder per lecture (lecture01/, lecture02/, ...); solutions/ subfolders are not matched
NOTEBOOKS = sorted(NOTEBOOK_DIR.glob("lecture*/0*.ipynb"))
EXPECTED_ERRORS = {"NotImplementedError"}

pytestmark = pytest.mark.skipif(
    os.environ.get("DDM_RUN_NOTEBOOK_TESTS") != "1",
    reason="set DDM_RUN_NOTEBOOK_TESTS=1 to execute the notebooks",
)


@pytest.fixture(scope="module")
def processed_dir(tmp_path_factory) -> Path:
    """One shared, empty processed/ folder: the notebooks run in order like in class."""
    return tmp_path_factory.mktemp("processed")


@pytest.mark.parametrize("path", NOTEBOOKS, ids=[f"{p.parent.name}/{p.name}" for p in NOTEBOOKS])
def test_notebook_runs(path: Path, processed_dir: Path, monkeypatch) -> None:
    monkeypatch.setenv("DDM_PROCESSED_DIR", str(processed_dir))
    monkeypatch.setenv("MPLBACKEND", "Agg")
    nb = nbformat.read(path, as_version=4)
    ExecutePreprocessor(timeout=600, allow_errors=True).preprocess(
        nb, {"metadata": {"path": str(path.parent)}}
    )
    errors = [
        out.get("ename")
        for cell in nb.cells
        for out in cell.get("outputs", [])
        if out.get("output_type") == "error"
    ]
    unexpected = [e for e in errors if e not in EXPECTED_ERRORS]
    assert not unexpected, f"{path.name}: unexpected errors {unexpected}"
