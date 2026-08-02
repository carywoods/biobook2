---
title: "Downloads"
weight: 90
---

# Downloads

Every script from the book, ready to run. Choose `.zip` or `.tar.gz` — the
contents are identical.

## All scripts

Python and Perl together, with the setup README.

| Format | Size | Link |
|---|---|---|
| ZIP | 133 KB | [biobook-all-scripts.zip](../../downloads/biobook-all-scripts.zip) |
| TAR.GZ | 68 KB | [biobook-all-scripts.tar.gz](../../downloads/biobook-all-scripts.tar.gz) |

```bash
unzip biobook-all-scripts.zip
# or
tar -xzf biobook-all-scripts.tar.gz
```

## Python only

39 vanilla + 39 AI scripts (78 total).

| Format | Size | Link |
|---|---|---|
| ZIP | 93 KB | [biobook-python-scripts.zip](../../downloads/biobook-python-scripts.zip) |
| TAR.GZ | 47 KB | [biobook-python-scripts.tar.gz](../../downloads/biobook-python-scripts.tar.gz) |

## Perl only

49 companion scripts plus the `BeginPerlBioinfo.pm` module.

| Format | Size | Link |
|---|---|---|
| ZIP | 41 KB | [biobook-perl-scripts.zip](../../downloads/biobook-perl-scripts.zip) |
| TAR.GZ | 22 KB | [biobook-perl-scripts.tar.gz](../../downloads/biobook-perl-scripts.tar.gz) |

## How the scripts are paired

Every Python example exists in two versions:

- **`chNN_vanilla_NN.py`** — standard Python and BioPython only. Runs with no API
  key and no network access.
- **`chNN_ai_NN.py`** — the same task with an LLM added to interpret the results.

Reading them side by side is the point of the book.

> [!TIP]
> Start with the vanilla version of any script. Once you understand what it
> computes, open the AI version and look only at what was added.

## Setting up the AI scripts

Install the client library:

```bash
pip install openai
```

The scripts default to OpenRouter. Set your key:

```bash
export OPENAI_API_KEY="sk-..."
python3 ch01_ai_01.py
```

Three environment variables are honored:

| Variable | Default | Purpose |
|---|---|---|
| `OPENAI_API_KEY` | *(empty)* | your API key |
| `OPENAI_BASE_URL` | `https://openrouter.ai/api/v1` | API endpoint |
| `OPENAI_MODEL` | `google/gemini-2.5-flash` | model to call |

To run against a local model instead:

```bash
export OPENAI_BASE_URL="http://localhost:11434/v1"   # Ollama
export OPENAI_MODEL="llama3"
export OPENAI_API_KEY="ollama"
```

> [!NOTE]
> If the `openai` package is not installed, the AI scripts print a notice and
> still run their biological analysis — only the AI commentary is replaced with a
> placeholder. You can study every script without an API key. If the package is
> installed but the key is missing, the API call itself will error, so set a key
> before running the AI versions.

## Python dependencies

Most scripts need only the standard library. Some use:

```bash
pip install biopython pandas matplotlib numpy
```

## Running the Perl scripts

The Perl examples need the bundled module, so run them from inside `perl/`:

```bash
cd perl
perl example10-1.pl
```

From elsewhere, add the directory to the include path:

```bash
perl -I/path/to/perl example10-1.pl
```

## Script index

| 1 | The Language of Life | `ch01_vanilla_01-03.py` | `ch01_ai_01-03.py` | 6 |
| 2 | Python Basics | `ch02_vanilla_01-04.py` | `ch02_ai_01-04.py` | 8 |
| 3 | The Central Dogma | `ch03_vanilla_01-04.py` | `ch03_ai_01-04.py` | 8 |
| 4 | Biological Data | `ch04_vanilla_01-03.py` | `ch04_ai_01-03.py` | 6 |
| 5 | Sequence Alignment | `ch05_vanilla_01-04.py` | `ch05_ai_01-04.py` | 8 |
| 6 | Motifs & Restriction Enzymes | `ch06_vanilla_01-03.py` | `ch06_ai_01-03.py` | 6 |
| 7 | Gene Expression | `ch07_vanilla_01-03.py` | `ch07_ai_01-03.py` | 6 |
| 8 | Protein Structure | `ch08_vanilla_01-02.py` | `ch08_ai_01-02.py` | 4 |
| 9 | Genome Analysis | `ch09_vanilla_01-02.py` | `ch09_ai_01-02.py` | 4 |
| 10 | Metagenomics | `ch10_vanilla_01-02.py` | `ch10_ai_01-02.py` | 4 |
| 11 | Single-Cell Analysis | `ch11_vanilla_01-02.py` | `ch11_ai_01-02.py` | 4 |
| 12 | LLM Reasoning | `ch12_vanilla_01-02.py` | `ch12_ai_01-02.py` | 4 |
| 13 | Pipelines | `ch13_vanilla_01-03.py` | `ch13_ai_01-03.py` | 6 |
| 14 | Capstone Projects | `ch14_vanilla_01-02.py` | `ch14_ai_01-02.py` | 4 |

**Totals:** 39 vanilla + 39 AI = 78 Python scripts, plus 49 Perl scripts.

## Verification

These archives were checked at packaging time:

- all 78 Python scripts pass `python3 -m py_compile` — 0 syntax errors
- `pyflakes` reports 0 unused imports and 0 undefined names
- all 49 Perl scripts pass `perl -I. -c`
- verified again after extraction from each archive
