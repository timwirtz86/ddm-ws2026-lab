"""Smoke tests: the data loads and the helper library works (no notebook needed).

Run with:  uv run pytest
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")  # headless: no window needed

import matplotlib.pyplot as plt  # noqa: E402
import nbformat  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import pytest  # noqa: E402
from scipy.cluster.hierarchy import linkage  # noqa: E402
from scipy.spatial.distance import pdist, squareform  # noqa: E402

import ddm  # noqa: E402
from ddm.processed import processed_dir  # noqa: E402

EXPECTED_ROWS = {"penguins": 344, "wholesale": 440, "auto_mpg": 398, "students": 395}
NOTEBOOK_DIR = ddm.datasets.RAW_DIR.parents[1] / "notebooks"


@pytest.fixture(autouse=True)
def _close_figures():
    yield
    plt.close("all")


@pytest.mark.parametrize("name", list(EXPECTED_ROWS))
def test_dataset_loads_with_expected_rows(name):
    df = ddm.load_dataset(name)
    assert len(df) == EXPECTED_ROWS[name]
    info = ddm.dataset_info(name)
    for label in info.label_candidates:
        assert label in df.columns


def test_registry_and_overview():
    assert set(ddm.DATASETS) == set(EXPECTED_ROWS)
    overview = ddm.list_datasets()
    assert list(overview.index) == list(EXPECTED_ROWS)
    with pytest.raises(KeyError):
        ddm.dataset_info("no-such-dataset")


def test_missing_values_are_parsed_as_nan():
    assert ddm.load_dataset("auto_mpg")["horsepower"].isna().sum() == 6
    assert ddm.load_dataset("penguins")["sex"].isna().sum() == 11


def test_numeric_summary():
    summary = ddm.numeric_summary(ddm.load_dataset("penguins"))
    assert {"dtype", "missing", "distinct", "example"} <= set(summary.columns)


def test_toy_village():
    village = ddm.load_toy_village()
    assert len(village) == 24
    assert {"x", "y", "type", "size", "occupied", "bank"} <= set(village.columns)
    assert set(village["bank"]) == {"west", "east"}


def _toy_data():
    rng = np.random.default_rng(0)
    X = np.vstack([rng.normal(0, 1, (20, 3)), rng.normal(5, 1, (20, 3))])
    labels = np.repeat([0, 1], 20)
    return X, labels


def test_plot_clusters_pca_and_mds():
    X, labels = _toy_data()
    noisy = labels.copy()
    noisy[:3] = -1  # DBSCAN noise convention
    fig = ddm.plot_clusters_pca(X, {"truth": labels, "with noise": noisy}, title="pca")
    assert len([ax for ax in fig.axes if ax.get_visible()]) == 2
    fig = ddm.plot_clusters_mds(squareform(pdist(X)), labels)
    assert fig.axes


def test_plot_clusters_pca_rejects_nan():
    X, labels = _toy_data()
    X[0, 0] = np.nan
    with pytest.raises(ValueError):
        ddm.plot_clusters_pca(X, labels)


def test_plot_dendrogram():
    X, _ = _toy_data()
    fig = ddm.plot_dendrogram(linkage(X, "average"), cut_height=3.0, title="t", truncate_mode="lastp", p=10)
    assert fig.axes


def test_plot_clusters_2d_and_village():
    X, labels = _toy_data()
    assert ddm.plot_clusters_2d(X[:, :2], {"a": labels, "b": labels[::-1]}, equal_aspect=True).axes
    village = ddm.load_toy_village()
    fig = ddm.plot_toy_village({"bank": village["bank"].to_numpy(), "all": np.zeros(24, dtype=int)})
    assert fig.axes


def test_processed_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setenv("DDM_PROCESSED_DIR", str(tmp_path))
    assert processed_dir() == tmp_path
    assert ddm.load_array("toy", "X") is None
    assert ddm.load_json("toy", "meta") is None
    ddm.save_array("toy", "X", np.eye(3))
    ddm.save_json("toy", "meta", {"rows": np.arange(3), "n": np.int64(3), "types": {"a": "numeric"}})
    assert np.array_equal(ddm.load_array("toy", "X"), np.eye(3))
    assert ddm.load_json("toy", "meta") == {"rows": [0, 1, 2], "n": 3, "types": {"a": "numeric"}}
    assert (tmp_path / "toy_X.npy").exists()


def test_check_helper(capsys):
    def passing():
        assert True

    def failing():
        assert 1 == 2, "one is not two"

    def todo():
        raise NotImplementedError("later")

    def crashing():
        raise IndexError("boom")

    for test in (passing, failing, todo, crashing):
        ddm.check(test.__name__, test)
    out = capsys.readouterr()
    assert "PASS   passing" in out.out
    assert "FAIL   failing: one is not two" in out.out
    assert "TODO   todo" in out.out
    assert "ERROR  crashing" in out.out
    assert "IndexError" in out.err


@pytest.mark.parametrize("name", ["lecture01/01_dataset", "lecture01/02_distance",
                                  "lecture02/03_clustering", "lecture02/04_beyond", "lecture02/05_homework"])
def test_notebooks_are_valid_and_clean(name):
    nb = nbformat.read(NOTEBOOK_DIR / f"{name}.ipynb", as_version=4)
    nbformat.validate(nb)
    code = [c for c in nb.cells if c.cell_type == "code"]
    assert code[0].source.startswith('DATASET = "penguins"')
    assert "INSTRUCTOR" not in "".join(c.source for c in nb.cells)


def test_pandas_strings_are_supported():
    """pandas 3 stores text as the 'str' dtype; the loaders must keep working with it."""
    df = ddm.load_dataset("students")
    assert pd.api.types.is_string_dtype(df["school"])
