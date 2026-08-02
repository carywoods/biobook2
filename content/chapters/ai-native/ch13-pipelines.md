---
title: "Chapter 13: Building Bioinformatics Pipelines"
type: "chapter"
weight: 13
---

Real bioinformatics work chains multiple steps into pipelines: read data, process it, analyze it, and output results. This chapter teaches you to build robust, reusable pipelines in Python.

You will parse BLAST output, handle errors gracefully, and design multi-step workflows with logging and error recovery. These are the engineering skills that separate scripts from software.

A pipeline that crashes on bad input is useless in production. This chapter teaches you to build pipelines that handle the messy reality of biological data.

## Parsing BLAST Output

BLAST is the most widely used bioinformatics tool. This script parses BLAST tabular output and extracts hits, scores, and statistics for downstream analysis.

**Vanilla version** (`ch13_vanilla_01.py`):

```python
#!/usr/bin/env python3


# Simulated BLAST output (tabular format)
BLAST_OUTPUT = """\
# BLASTN 2.12.0+
# Query: query_sequence
# Database: nr
# Fields: query_id, subject_id, %identity, alignment_length, mismatches, gap_opens, q_start, q_end, s_start, s_end, evalue, bit_score
query_seq  NM_007294.4  99.85  675  1  0  1  675  1  675  0.0  1241
query_seq  NM_007294.3  99.70  675  2  0  1  675  1  675  0.0  1237
query_seq  XM_006710328.4  98.22  675  12  0  1  675  1  675  0.0  1204
query_seq  NM_001354609.2  97.48  675  17  0  1  675  1  675  0.0  1189
query_seq  XM_017003169.3  95.56  675  30  0  1  675  1  675  0.0  1144
"""


def parse_blast_tabular(output: str) -> list:
    """Parse BLAST tabular output."""
    results = []
    for line in output.strip().split("\n"):
        if line.startswith("#"):
            continue
        fields = line.split()
        if len(fields) >= 12:
            results.append({
                "query": fields[0].strip(),
                "subject": fields[1].strip(),
                "identity": float(fields[2]),
                "alignment_length": int(fields[3]),
                "mismatches": int(fields[4]),
                "evalue": float(fields[10]),
                "bit_score": float(fields[11]),
            })
    return results


# --- Main program ---
results = parse_blast_tabular(BLAST_OUTPUT)

print(f"BLAST results: {len(results)} hits\n")
print(f"{'Subject':25s} {'%ID':>6s} {'Length':>6s} {'Mis':>4s} {'E-value':>10s} {'Score':>7s}")
print("-" * 65)

for r in results:
    print(f"{r['subject']:25s} {r['identity']:6.1f} {r['alignment_length']:6d} "
          f"{r['mismatches']:4d} {r['evalue']:10.1e} {r['bit_score']:7.0f}")

# Analysis
print(f"\nSummary:")
print(f"  Best hit: {results[0]['subject']} ({results[0]['identity']}% identity)")
print(f"  All hits have E-value = 0.0 (extremely significant)")
print(f"  Identity range: {min(r['identity'] for r in results):.1f}% - {max(r['identity'] for r in results):.1f}%")
```

We parsed BLAST tabular format (12 columns), stored results in dictionaries, and computed summary statistics. Parsing structured output is a core bioinformatics skill.

**AI version** (`ch13_ai_01.py`):

```python
#!/usr/bin/env python3


import os

try:
    from openai import OpenAI
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""), base_url=os.environ.get("OPENAI_BASE_URL", "https://openrouter.ai/api/v1"))
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("Note: Install openai package for AI features\n")

def ask_ai(prompt: str) -> str:
    if not AI_AVAILABLE:
        return "(AI not available)"
    return client.chat.completions.create(model=os.environ.get("OPENAI_MODEL", "google/gemini-2.5-flash"), messages=[{"role": "user", "content": prompt}], temperature=0.3).choices[0].message.content

hits = [
    {"subject": "NM_007294.4 (BRCA1)", "identity": 99.85, "evalue": 0.0, "score": 1241},
    {"subject": "NM_007294.3 (BRCA1)", "identity": 99.70, "evalue": 0.0, "score": 1237},
    {"subject": "XM_006710328.4 (BRCA1)", "identity": 98.22, "evalue": 0.0, "score": 1204},
]

print("BLAST results (top 3 hits):")
for h in hits:
    print(f"  {h['subject']}: {h['identity']}% identity, E={h['evalue']}, score={h['score']}")

print("\n--- AI: What do these BLAST results mean? ---\n")
result = ask_ai(
    "I BLASTed a DNA sequence and got these top hits:\n\n"
    "  NM_007294.4 (BRCA1): 99.85% identity, E-value=0.0\n"
    "  NM_007294.3 (BRCA1): 99.70% identity, E-value=0.0\n"
    "  XM_006710328.4 (BRCA1): 98.22% identity, E-value=0.0\n\n"
    "Please explain:\n"
    "1. What is BLAST and how does it work? (Explain the algorithm simply)\n"
    "2. What does E-value = 0.0 mean? Is it really zero?\n"
    "3. Why are there multiple BRCA1 entries? What's the difference between NM_ and XM_?\n"
    "4. 99.85% identity over 675 bases -- how many bases differ?\n"
    "5. How would you cite this result in a paper?\n\n"
    "Explain for a student running BLAST for the first time."
)
print(result)
```

The AI explains the BLAST results: what E-values mean, why there are multiple entries for the same gene, and how to cite BLAST results in a paper.

::: {.callout-tip}
You can run any vanilla script without an API key. The AI scripts will print a message and run in offline mode if no key is set.
:::

## Error Handling and Defensive Programming

Bioinformatics scripts fail often: missing files, corrupt data, permission errors. This script demonstrates robust error handling with try/except blocks.

**Vanilla version** (`ch13_vanilla_02.py`):

```python
#!/usr/bin/env python3


import os
import sys


def read_sequence_file(filename: str) -> str:
    """Read a sequence file with proper error handling."""
    # Check if file exists
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")

    # Check if it's actually a file
    if not os.path.isfile(filename):
        raise IsADirectoryError(f"Not a file: {filename}")

    # Check if readable
    if not os.access(filename, os.R_OK):
        raise PermissionError(f"Cannot read: {filename}")

    # Check file size
    size = os.path.getsize(filename)
    if size == 0:
        raise ValueError(f"File is empty: {filename}")
    if size > 1_000_000:  # 1MB
        print(f"Warning: large file ({size:,} bytes)")

    # Read the file
    with open(filename) as f:
        content = f.read().strip()

    return content


def validate_dna(sequence: str) -> tuple:
    """Validate a DNA sequence. Returns (is_valid, errors)."""
    errors = []
    valid_bases = set("ATCGatcg")

    invalid = set(sequence) - valid_bases
    if invalid:
        errors.append(f"Invalid characters: {invalid}")

    if len(sequence) < 10:
        errors.append(f"Sequence too short ({len(sequence)} bases)")

    return (len(errors) == 0, errors)


# --- Main program ---
test_files = ["test.dna", "/tmp/sample.dna", "/etc/passwd"]

for filename in test_files:
    print(f"\nTrying to read: {filename}")
    try:
        content = read_sequence_file(filename)
        print(f"  Read {len(content)} characters")

        is_valid, errors = validate_dna(content)
        if is_valid:
            print(f"  Valid DNA sequence")
        else:
            print(f"  Validation errors: {errors}")

    except FileNotFoundError as e:
        print(f"  Error: {e}")
    except PermissionError as e:
        print(f"  Error: {e}")
    except ValueError as e:
        print(f"  Error: {e}")
    except Exception as e:
        print(f"  Unexpected error: {type(e).__name__}: {e}")
```

We checked file existence, validated permissions, handled empty files, and tested for invalid characters in sequences. Defensive programming prevents silent failures.

**AI version** (`ch13_ai_02.py`):

```python
#!/usr/bin/env python3


import os

try:
    from openai import OpenAI
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""), base_url=os.environ.get("OPENAI_BASE_URL", "https://openrouter.ai/api/v1"))
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("Note: Install openai package for AI features\n")

def ask_ai(prompt: str) -> str:
    if not AI_AVAILABLE:
        return "(AI not available)"
    return client.chat.completions.create(model=os.environ.get("OPENAI_MODEL", "google/gemini-2.5-flash"), messages=[{"role": "user", "content": prompt}], temperature=0.3).choices[0].message.content

# Simulate common bioinformatics errors
errors = [
    {"file": "sample.fasta", "error": "FileNotFoundError", "detail": "No such file or directory"},
    {"file": "data.vcf", "error": "ValueError", "detail": "could not convert string to float: '.'"},
    {"file": "sequences.fq", "error": "UnicodeDecodeError", "detail": "'utf-8' codec can't decode byte 0x89"},
    {"file": "genome.bam", "error": "PermissionError", "detail": "Permission denied"},
]

print("Common bioinformatics file errors:")
for e in errors:
    print(f"  {e['file']}: {e['error']} -- {e['detail']}")

print("\n--- AI: Help me handle these errors ---\n")
error_text = "\n".join(f"  {e['file']}: {e['error']} ({e['detail']})" for e in errors)
result = ask_ai(
    f"I'm building a bioinformatics pipeline and keep hitting these errors:\n\n{error_text}\n\n"
    "For each error:\n"
    "1. What causes it?\n"
    "2. How should I handle it in Python? (try/except pattern)\n"
    "3. Should I skip the file, retry, or abort?\n"
    "4. What's the best practice for logging errors in pipelines?\n\n"
    "Also explain:\n"
    "- Why might a FASTQ file fail to decode as UTF-8?\n"
    "- What does a '.' mean in a VCF file and why does it break parsing?\n"
    "- How do production pipelines handle thousands of files with occasional errors?\n\n"
    "Give me Python code for a robust file processor."
)
print(result)
```

The AI helps debug common errors: why FASTQ files fail to decode, what a dot in a VCF file means, and how production pipelines handle occasional errors.

::: {.callout-note}
The AI version always includes the same core logic as the vanilla version. The AI calls are added at the end, so you can compare the two approaches side by side.
:::

## Multi-Step Pipeline Design

A real pipeline chains multiple steps: read, filter, analyze, output. This script builds a complete pipeline with logging and error recovery.

**Vanilla version** (`ch13_vanilla_03.py`):

```python
#!/usr/bin/env python3


import os
import subprocess
import tempfile


def run_step(name: str, func, *args, **kwargs):
    """Run a pipeline step with logging."""
    print(f"  [{name}] Starting...")
    try:
        result = func(*args, **kwargs)
        print(f"  [{name}] Complete")
        return result
    except Exception as e:
        print(f"  [{name}] FAILED: {e}")
        return None


def step1_read_sequences(input_file: str) -> list:
    """Read sequences from FASTA file."""
    sequences = {}
    current = None
    with open(input_file) as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                current = line[1:]
                sequences[current] = ""
            elif current:
                sequences[current] += line
    return sequences


def step2_filter_sequences(sequences: dict, min_length: int = 50) -> dict:
    """Filter sequences by minimum length."""
    return {k: v for k, v in sequences.items() if len(v) >= min_length}


def step3_compute_stats(sequences: dict) -> dict:
    """Compute basic statistics."""
    lengths = [len(v) for v in sequences.values()]
    gc_counts = [v.count("G") + v.count("C") for v in sequences.values()]
    return {
        "count": len(sequences),
        "total_bases": sum(lengths),
        "mean_length": sum(lengths) / len(lengths) if lengths else 0,
        "gc_content": sum(gc_counts) / sum(lengths) * 100 if lengths else 0,
    }


def step4_write_output(sequences: dict, output_file: str) -> int:
    """Write filtered sequences to output file."""
    with open(output_file, "w") as f:
        for header, seq in sequences.items():
            f.write(f">{header}\n")
            for i in range(0, len(seq), 60):
                f.write(seq[i:i+60] + "\n")
    return len(sequences)


# --- Main program ---
# Create sample input
sample = ">seq1\nATGGTGCATCTGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTGAAC\n>short\nATCG\n>seq2\nGTGGATGAAGTTGGTGGTGAGGCCCTGGGCAGGCTGCTGGTGGTCTACCCTTGGACCCAG\n"

input_file = os.path.join(tempfile.gettempdir(), "pipeline_input.fasta")
output_file = os.path.join(tempfile.gettempdir(), "pipeline_output.fasta")

with open(input_file, "w") as f:
    f.write(sample)

print("Bioinformatics Pipeline")
print("=" * 40)
print(f"Input: {input_file}\n")

# Run pipeline
sequences = run_step("Read", step1_read_sequences, input_file)
if sequences:
    filtered = run_step("Filter", step2_filter_sequences, sequences, min_length=50)
    if filtered:
        stats = run_step("Stats", step3_compute_stats, filtered)
        count = run_step("Write", step4_write_output, filtered, output_file)

        print(f"\nPipeline Results:")
        print(f"  Input sequences: {len(sequences)}")
        print(f"  After filtering: {stats['count']}")
        print(f"  Total bases: {stats['total_bases']}")
        print(f"  Mean length: {stats['mean_length']:.0f}")
        print(f"  GC content: {stats['gc_content']:.1f}%")
        print(f"  Output: {output_file}")

# Cleanup
os.remove(input_file)
if os.path.exists(output_file):
    os.remove(output_file)
```

We built a four-step pipeline (read, filter, stats, output) with a run_step() wrapper that logs each step and handles failures gracefully.

**AI version** (`ch13_ai_03.py`):

```python
#!/usr/bin/env python3


import os

try:
    from openai import OpenAI
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""), base_url=os.environ.get("OPENAI_BASE_URL", "https://openrouter.ai/api/v1"))
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("Note: Install openai package for AI features\n")

def ask_ai(prompt: str) -> str:
    if not AI_AVAILABLE:
        return "(AI not available)"
    return client.chat.completions.create(model=os.environ.get("OPENAI_MODEL", "google/gemini-2.5-flash"), messages=[{"role": "user", "content": prompt}], temperature=0.3).choices[0].message.content

# Pipeline design
pipeline_steps = [
    {"step": 1, "name": "Quality Control", "tool": "FastQC", "input": "raw FASTQ", "output": "QC report"},
    {"step": 2, "name": "Trimming", "tool": "Trimmomatic", "input": "raw FASTQ", "output": "trimmed FASTQ"},
    {"step": 3, "name": "Alignment", "tool": "BWA/BOWTIE2", "input": "trimmed FASTQ", "output": "BAM file"},
    {"step": 4, "name": "Quantification", "tool": "featureCounts", "input": "BAM file", "output": "count matrix"},
    {"step": 5, "name": "Differential Expression", "tool": "DESeq2", "input": "count matrix", "output": "gene list"},
]

print("RNA-seq Pipeline Design:")
for s in pipeline_steps:
    print(f"  Step {s['step']}: {s['name']}")
    print(f"    Tool: {s['tool']}")
    print(f"    {s['input']} -> {s['output']}")

print("\n--- AI: Help me build this pipeline ---\n")
result = ask_ai(
    "I'm designing an RNA-seq pipeline for a college bioinformatics course:\n\n"
    "Step 1: FastQC (quality control)\n"
    "Step 2: Trimmomatic (adapter trimming)\n"
    "Step 3: BWA (alignment to reference genome)\n"
    "Step 4: featureCounts (gene quantification)\n"
    "Step 5: DESeq2 (differential expression)\n\n"
    "Please:\n"
    "1. Explain each step in one sentence for a freshman\n"
    "2. What are the key parameters for each tool?\n"
    "3. How do I check if each step succeeded?\n"
    "4. What are common failure modes and how do I debug them?\n"
    "5. How would I run this on 100 samples? (parallelization)\n"
    "6. How could I use an LLM to automate the QC interpretation?\n\n"
    "Give me a Snakemake skeleton for this pipeline."
)
print(result)
```

The AI helps design the pipeline: explains each step, suggests key parameters, identifies failure modes, and provides a Snakemake skeleton for scaling to hundreds of samples.

## Chapter Summary

This chapter covered pipeline engineering. BLAST parsing, error handling, and multi-step workflow design.

The vanilla scripts gave you hands-on experience with the core techniques. The AI scripts showed how LLMs can interpret, explain, and extend your analysis. Together, they prepare you for real-world bioinformatics work where code and AI work side by side.
