# DDM Clustering Lab (WS 2026)

[![Install check (macOS, Windows, Linux)](https://github.com/timwirtz86/ddm-ws2026-clustering-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/timwirtz86/ddm-ws2026-clustering-lab/actions/workflows/ci.yml)

Hands-on material for *Data Driven Modelling*, Lecture 1: **standard clustering algorithms**
(TH Köln, winter term 2026).

In this lab we cluster a real dataset step by step and write the important parts ourselves:
preprocessing, distance measures (including the Gower distance for mixed attribute types),
agglomerative clustering and k-medoids. Then we evaluate the results and try DBSCAN. At the
start of the next lecture we explain the clusters with a small decision tree.

Everything that is *plumbing* (loading the data, saving intermediate results, plotting) is done
by the small helper library `ddm` in `src/ddm/`. Everything that is a *learning goal* is a TODO
in the notebooks.

---

## Installation (once, about 10 minutes)

We need two tools:

- **git** to download the lab and to get updates later (optional: a ZIP download also works),
- **[uv](https://docs.astral.sh/uv/)**, which installs the right Python version (3.12) and all
  packages into a folder `.venv/` inside the lab. Nothing is installed globally, and an existing
  Python installation on your computer is not touched.

Please do the installation **before the first lecture**: the first `uv sync` downloads Python
and all packages, and the lab needs about 500 MB of disk space. After that, everything works
offline.

### Step 1 · Open a terminal

| System | Terminal |
|--------|----------|
| macOS | *Terminal* (Spotlight: `Cmd` + `Space`, type "Terminal") |
| Windows | *PowerShell* (Start menu, type "PowerShell"; not the old "Command Prompt" if you can avoid it) |
| Linux | your usual terminal |

All commands below are typed into this terminal and confirmed with `Enter`.

### Step 2 · Install uv

**macOS and Linux**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

(If `curl` is missing on Linux: `wget -qO- https://astral.sh/uv/install.sh | sh`.
On macOS with Homebrew, `brew install uv` works as well.)

**Windows (PowerShell)**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

(Alternative: `winget install --id=astral-sh.uv -e`.)

Then **close the terminal and open a new one**, so that it finds the new command, and check:

```bash
uv --version
```

It should print a version number. If it says *command not found* / *not recognized*, see
[Troubleshooting](#troubleshooting).

### Step 3 · Get the lab

**Option A, with git (recommended, makes updates easy)**

Is git installed? `git --version` prints a version number. If not:

| System | Install git |
|--------|-------------|
| macOS | `xcode-select --install` (installs Apple's command line tools including git) or `brew install git` |
| Windows | `winget install --id Git.Git -e` or the installer from <https://git-scm.com/download/win>; then open a new terminal |
| Linux | `sudo apt install git` (Debian/Ubuntu) or `sudo dnf install git` (Fedora) |

Then go to the folder where you want the lab (e.g. your home folder) and download it:

```bash
git clone https://github.com/timwirtz86/ddm-ws2026-clustering-lab.git
cd ddm-ws2026-clustering-lab
```

**Option B, without git**

On the GitHub page click **Code → Download ZIP**, unpack the ZIP, and open a terminal in the
unpacked folder (`cd` into it). Updates then mean downloading the ZIP again.

> **Windows:** please do **not** put the lab into a OneDrive-synchronised folder (often
> `Documents` or `Desktop`). Syncing the `.venv/` folder makes the installation slow and can
> break it. A folder like `C:\Users\<your name>\ddm` is fine.

### Step 4 · Install Python and all packages

Inside the lab folder:

```bash
uv sync
```

uv downloads Python 3.12 and the exact package versions from `uv.lock`, so everybody gets the
same environment. This takes one to a few minutes the first time.

### Step 5 · Check the installation

```bash
uv run pytest
```

The last line should say something like `20 passed`. If yes, everything is ready.

### Step 6 · Start JupyterLab

```bash
uv run jupyter lab
```

JupyterLab opens in your browser. The notebooks are in the folder `notebooks/`; start with
`01_dataset.ipynb`. To stop JupyterLab, go back to the terminal and press `Ctrl` + `C` (twice).

**Every later session:** open a terminal, `cd` into the lab folder, `uv run jupyter lab`.

### Using VS Code instead of JupyterLab

Install the extensions *Python* and *Jupyter*, open the lab folder (*File → Open Folder*), open
a notebook and choose the kernel from `.venv` (*Select Kernel → Python Environments → .venv*).
Run `uv sync` once before, so that `.venv` exists.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `uv: command not found` (macOS/Linux) or `uv is not recognized` (Windows) | Open a **new** terminal after installing uv. Still missing? macOS/Linux: run `source $HOME/.local/bin/env`; Windows: log out and in again. |
| Windows: *running scripts is disabled on this system* | Use exactly the installer command from Step 2 (it contains `-ExecutionPolicy ByPass`), or use the `winget` alternative. |
| macOS: *xcrun: error: invalid active developer path* when using git | Run `xcode-select --install` and confirm the dialog. |
| `uv sync` is very slow or fails on Windows | Lab inside a OneDrive folder? Move it (see Step 3). Antivirus software can also slow down the first `uv sync`; just wait. |
| No internet / proxy in the lecture room | Run `uv sync` at home once; afterwards no internet is needed. The notebooks never download anything. |
| Wrong Python version | Not a problem: uv uses its own Python 3.12 for this lab, whatever else is installed. |
| `uv run pytest` shows `failed` | Run `uv sync` again, then `uv run pytest` again. If it still fails, bring the output to the lab session or open an issue in this repository. |
| JupyterLab does not open a browser window | Copy the link that starts with `http://localhost:8888/lab?token=...` from the terminal into your browser. |

---

## Getting updates

We may fix or add things during the semester. With git:

```bash
git pull
```

Our recommendation, so that `git pull` never conflicts with your own work: before you start
working on a notebook, make a copy of it (e.g. `02_distance_myname.ipynb`) and work in the copy.
If `git pull` complains about local changes anyway, `git stash`, then `git pull`, then
`git stash pop` brings your changes back.

---

## Notebooks

Run them in order. Each notebook saves its results to `data/processed/`; the next notebook
loads them. If a file is missing there (because a task is not solved yet), the next notebook
prints a `NOTICE` and continues with a simple baseline, so we never get stuck.

| Notebook | Block | Time | What we do |
|----------|-------|------|------------|
| `01_dataset.ipynb` | B1 | 10 min | choose a dataset, write our question, classify every attribute |
| `02_distance.ipynb` | B4 | 25 min | `preprocess`, Minkowski and cosine distance, **Gower distance** |
| `03_clustering.ipynb` | B6 | 25 min | **agglomerative clustering**, **k-medoids** (optional: k-means with our distance) |
| `04_beyond.ipynb` | B7–B8 | 20 min | silhouette, ARI, elbow; DBSCAN. Part 3 (cluster profiles and a surrogate tree) is for next week, start of Lecture 2 |
| `05_homework.ipynb` | B10 | homework | apply **DBSCAN** to our dataset and test it against the other methods, incl. "structure or artefact?" |

Every TODO function has a check cell below it that prints one line per test:
`PASS`, `FAIL` (with the reason), `TODO` (not implemented yet) or `ERROR` (with the traceback).
Hints are hidden in collapsed "click to open" boxes in the text cells.

## Choosing a dataset

Every group works on one dataset. Set it in the first code cell of every notebook:

```python
DATASET = "penguins"  # or "wholesale", "auto_mpg", "students"
```

| Name | Objects × attributes | Why it is interesting | Label candidates (known groups) |
|------|----------------------|-----------------------|-------------------------------|
| `penguins` | 344 × 8 | measurements on very different scales, missing values, few categories | species, sex |
| `wholesale` | 440 × 8 | spending is extremely skewed (log transform), integer codes that are nominal | channel, region |
| `auto_mpg` | 398 × 9 | raw text format, `?` for missing values, discrete and ordinal attributes | origin |
| `students` | 395 × 33 | every attribute type at once: binary, nominal, ordinal, numeric | school, G3 |

`ddm.list_datasets()` and `ddm.dataset_info(name)` show the details (question, pitfalls,
source, licence). `penguins` is the default and is used in all demos.

### Bringing our own dataset

Allowed, if it meets the same criteria as the course datasets:

1. **Size:** about 200–1000 objects (distance matrices grow with n², and our own algorithms
   are simple loops).
2. **Mixed attribute types:** at least two different types (e.g. numeric and nominal), so that
   preprocessing and the choice of distance actually matter.
3. **Transformation needed:** different scales, skewed values or missing values.
4. **Known groups:** at least one column with known group labels that we leave out of the
   clustering and only use afterwards to compare the clusters with.
5. **Open licence** that allows use in teaching (e.g. CC0, CC BY), and no personal data.

How: put the raw file into `data/raw/`, and add an entry to `DATASETS` plus a branch in
`load_dataset` in `src/ddm/datasets.py` (only parsing, no cleaning: the cleaning is part of
the lab). Ask us if unsure.

## Folder structure

```
ddm-ws2026-clustering-lab/
├── README.md           this file
├── LICENSE             MIT licence for the code and notebooks
├── pyproject.toml      dependencies (uv); uv.lock pins the exact versions
├── data/raw/           the four datasets as published (+ DATA_SOURCES.md)
├── data/processed/     intermediate results of the notebooks (created automatically, not in git)
├── src/ddm/            helper library: datasets, plots, checks, saving/loading (plumbing only)
├── notebooks/          01–05
├── figures/            for figures we want to keep
└── tests/              installation check: uv run pytest
```

## Licences

- **Code and notebooks:** [MIT licence](LICENSE).
- **Data:** the raw files in `data/raw/` keep their original licences and are redistributed
  unchanged, with attribution:

  | Dataset | Licence |
  |---------|---------|
  | Palmer penguins (Horst, Hill, Gorman 2020) | CC0 1.0 |
  | Wholesale customers (UCI 292) | CC BY 4.0 |
  | Auto MPG (UCI 9) | CC BY 4.0 |
  | Student performance (UCI 320) | CC BY 4.0 |

  Sources, citations and a description of each raw file are in
  [`data/DATA_SOURCES.md`](data/DATA_SOURCES.md). When you use the data in a report, cite it as
  given there.
- **Dependencies** (numpy, pandas, scipy, scikit-learn, matplotlib, JupyterLab, …) are not part
  of this repository; uv installs them from PyPI under their own (BSD/MIT-style) licences.
