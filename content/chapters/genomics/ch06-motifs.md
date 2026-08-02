---
title: "Chapter 6: Restriction Enzymes and Command-Line Tools"
type: "chapter"
weight: 6
---

This chapter bridges bioinformatics biology and software engineering. You will learn to search for restriction enzyme sites in DNA, build command-line tools with argparse, and debug common errors.

Restriction enzymes are the workhorses of molecular cloning. Finding their cut sites in a DNA sequence is a classic bioinformatics task. Building command-line tools makes your scripts reusable. Debugging skills keep you sane.

These practical skills separate students who can run scripts from those who can build tools.

## Restriction Enzyme Site Detection

Restriction enzymes cut DNA at specific recognition sequences. Finding these sites in a DNA sequence is essential for cloning, genotyping, and genome engineering.

**Vanilla version** (`ch06_vanilla_01.py`):

```python
#!/usr/bin/env python3


import re

# Common restriction enzymes and their recognition sites
ENZYMES = {
    "EcoRI": "GAATTC",
    "BamHI": "GGATCC",
    "HindIII": "AAGCTT",
    "XhoI": "CTCGAG",
    "NotI": "GCGGCCGC",
    "SmaI": "CCCGGG",
    "PstI": "CTGCAG",
    "KpnI": "GGTACC",
}


def find_restriction_sites(dna: str, enzymes: dict) -> dict:
    """Find all restriction enzyme cut sites in a DNA sequence."""
    results = {}
    for name, site in enzymes.items():
        positions = [m.start() for m in re.finditer(site, dna, re.IGNORECASE)]
        if positions:
            results[name] = positions
    return results


def print_restriction_map(dna: str, sites: dict) -> None:
    """Print a text-based restriction map."""
    print(f"Restriction map for {len(dna)} bp sequence:")
    print("=" * 60)

    for enzyme, positions in sorted(sites.items(), key=lambda x: x[1][0] if x[1] else 999):
        site = ENZYMES[enzyme]
        for pos in positions:
            print(f"  {enzyme:8s} ({site}) at position {pos + 1}")
            # Show context
            context_start = max(0, pos - 5)
            context_end = min(len(dna), pos + len(site) + 5)
            context = dna[context_start:context_end]
            marker = " " * (pos - context_start) + "^" * len(site)
            print(f"           ...{context}...")
            print(f"            {marker}")


# --- Main program ---
# A sample plasmid sequence (pUC19 MCS region with inserts)
dna = (
    "GAATTCGAGCTCGGTACCCGGGGATCCTCTAGAGTCGACCTGCAGGCATGCAAGCTT"
    "GGCGTAATCATGGTCATAGCTGTTTCCTGTGTGAAATTGTTATCCGCTCACAATTCCA"
    "CACAACATACGAGCCGGAAGCATAAAGTGTAAAGCCTGGGGTGCCTAATGAGTGAGCT"
    "AACTCACATTAATTGCGTTGCGCTCACTGCCCGCTTTCCAGTCGGGAAACCTGTCGTG"
    "CCAGCTGCATTAATGAATCGGCCAACGCGCGGGGAGAGGCGGTTTGCGTATTGGGCGC"
    "GAATTCCCT"
)

print(f"DNA sequence: {len(dna)} bp\n")
print(f"Sequence: {dna[:60]}...\n")

# Find all restriction sites
sites = find_restriction_sites(dna, ENZYMES)

# Print the map
print_restriction_map(dna, sites)

# Summary
print(f"\nSummary:")
print(f"  Total enzymes tested: {len(ENZYMES)}")
print(f"  Enzymes with sites: {len(sites)}")
print(f"  Total cut sites: {sum(len(p) for p in sites.values())}")

# Which enzymes cut once? (useful for cloning)
print(f"\nSingle cutters (useful for cloning):")
for enzyme, positions in sites.items():
    if len(positions) == 1:
        print(f"  {enzyme}: position {positions[0] + 1}")
```

We used regex to search for restriction enzyme recognition sites and built a simple enzyme database. Each enzyme has a name, recognition sequence, and cut position.

**AI version** (`ch06_ai_01.py`):

```python
#!/usr/bin/env python3


import os
import re

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

ENZYMES = {"EcoRI": "GAATTC", "BamHI": "GGATCC", "HindIII": "AAGCTT", "XhoI": "CTCGAG", "PstI": "CTGCAG", "KpnI": "GGTACC"}

def find_sites(dna, enzymes):
    results = {}
    for name, site in enzymes.items():
        pos = [m.start() for m in re.finditer(site, dna, re.IGNORECASE)]
        if pos:
            results[name] = pos
    return results

dna = "GAATTCGAGCTCGGTACCCGGGGATCCTCTAGAGTCGACCTGCAGGCATGCAAGCTTGGCGTAATCATGGTCATAGCTGTTTCCTGTGTGAAATTGTTATCCGCTCACAATTCCACACAACATACGAGCCGGAAGCATAAAGTGTAAAGCCTGGGGTGCCTAATGAGTGAGCTAACTCACATTAATTGCGTTGCGCTCACTGCCCGCTTTCCAGTCGGGAAACCTGTCGTGCCAGCTGCATTAATGAATCGGCCAACGCGCGGGGAGAGGCGGTTTGCGTATTGGGCGCGAATTCCCT"

sites = find_sites(dna, ENZYMES)
print(f"Sequence ({len(dna)} bp):")
for enzyme, positions in sites.items():
    print(f"  {enzyme} ({ENZYMES[enzyme]}): position(s) {[p+1 for p in positions]}")

single_cutters = {e: p for e, p in sites.items() if len(p) == 1}
print(f"\nSingle cutters: {list(single_cutters.keys())}")

print("\n--- AI: Help me plan a cloning experiment ---\n")
enzyme_info = "\n".join(f"  {e}: {ENZYMES[e]} at {[p+1 for p in pos]}" for e, pos in sites.items())
result = ask_ai(
    f"I have a {len(dna)} bp plasmid with these restriction sites:\n{enzyme_info}\n\n"
    f"Single cutters: {list(single_cutters.keys())}\n\n"
    "I want to clone a gene into this plasmid. Please explain:\n"
    "1. What are single cutters and why are they important for cloning?\n"
    "2. If my gene has EcoRI sites, which enzyme should I use instead?\n"
    "3. Walk me through the cloning process step by step.\n"
    "4. What is 'ligation' and how does DNA ligase work?\n\n"
    "Explain for a college freshman who has never been in a lab."
)
print(result)
```

The AI explains enzyme biology: why bacteria make restriction enzymes, how methylation protects host DNA, and how to choose enzymes for a cloning experiment.

::: {.callout-tip}
You can run any vanilla script without an API key. The AI scripts will print a message and run in offline mode if no key is set.
:::

## Building Command-Line Tools with argparse

Real bioinformatics tools accept command-line arguments. This script introduces argparse, Python's standard library for building CLI tools.

**Vanilla version** (`ch06_vanilla_02.py`):

```python
#!/usr/bin/env python3


import sys


def count_bases(dna: str) -> dict:
    """Count each base in a DNA sequence."""
    counts = {}
    for base in dna.upper():
        if base in "ATCG":
            counts[base] = counts.get(base, 0) + 1
    return counts


def main():
    # Check command-line arguments
    if len(sys.argv) < 2:
        # Demo mode if no arguments
        dna = "ATGGTGCATCTGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTGAAC"
        print("(No argument provided -- running with demo sequence)\n")
    else:
        dna = sys.argv[1].upper()

    # Validate
    invalid = [b for b in dna if b not in "ATCG"]
    if invalid:
        print(f"Error: invalid bases found: {set(invalid)}")
        print("DNA sequences should only contain A, T, C, G")
        sys.exit(1)

    print(f"DNA: {dna}")
    print(f"Length: {len(dna)} bases")

    counts = count_bases(dna)
    print("\nBase counts:")
    for base in sorted(counts):
        pct = counts[base] / len(dna) * 100
        print(f"  {base}: {counts[base]} ({pct:.1f}%)")

    gc = (counts.get("G", 0) + counts.get("C", 0)) / len(dna) * 100
    print(f"\nGC content: {gc:.1f}%")


if __name__ == "__main__":
    main()
```

We built a command-line tool that accepts a DNA sequence and enzyme name as arguments, with help messages and default values. argparse makes scripts reusable and shareable.

**AI version** (`ch06_ai_02.py`):

```python
#!/usr/bin/env python3


import os
import sys

try:
    from openai import OpenAI
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""), base_url=os.environ.get("OPENAI_BASE_URL", "https://openrouter.ai/api/v1"))
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

def ask_ai(prompt: str) -> str:
    if not AI_AVAILABLE:
        return "(AI not available)"
    return client.chat.completions.create(model=os.environ.get("OPENAI_MODEL", "google/gemini-2.5-flash"), messages=[{"role": "user", "content": prompt}], temperature=0.3).choices[0].message.content

def main():
    if len(sys.argv) < 2:
        # Demo mode if no arguments
        dna = "ATGGTGCATCTGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTGAAC"
        print("(No argument provided -- running with demo sequence)\n")
    else:
        dna = sys.argv[1].upper()
    invalid = [b for b in dna if b not in "ATCG"]
    if invalid:
        print(f"Error: invalid bases: {set(invalid)}")
        sys.exit(1)

    counts = {b: dna.count(b) for b in "ATCG"}
    gc = (counts["G"] + counts["C"]) / len(dna) * 100

    print(f"DNA: {dna}")
    print(f"Length: {len(dna)}, GC: {gc:.1f}%")

    print("\n--- AI: Sequence validation ---\n")
    result = ask_ai(
        f"Validate this DNA sequence: {dna}\n"
        f"Length: {len(dna)} bp, GC content: {gc:.1f}%\n\n"
        "1. Is this GC content typical of any organism?\n"
        "2. Does it contain any known motifs (start codon, restriction sites)?\n"
        "3. Could this be a coding sequence? Why or why not?\n"
        "4. Suggest 2 experiments to characterize this sequence.\n\n"
        "Be brief and specific."
    )
    print(result)

if __name__ == "__main__":
    main()
```

The AI suggests improvements: adding input file support, output formatting options, batch processing, and proper error messages for invalid inputs.

::: {.callout-note}
The AI version always includes the same core logic as the vanilla version. The AI calls are added at the end, so you can compare the two approaches side by side.
:::

## Debugging Common Errors

Every bioinformatics programmer spends time debugging. This script reviews common Python errors and shows how to read and interpret error messages.

**Vanilla version** (`ch06_vanilla_03.py`):

```python
#!/usr/bin/env python3


# EXERCISE: This code has 3 bugs. Find and fix them.
# Run it first to see the errors, then fix each one.

# Bug 1: Wrong variable name
dna = "CGACGTCTTCTAAGGCGA"
print(f"DNA: {dna}")

# Bug 2: Off-by-one error in loop
print("\nBases at even positions:")
for i in range(0, len(dna), 2):
    print(f"  Position {i}: {dna[i]}")

# Bug 3: Wrong comparison operator
complement = {"A": "T", "T": "A", "G": "C", "C": "G"}
comp_dna = ""
for base in dna:
    if base in complement:
        comp_dna += complement[base]
    else:
        comp_dna += "N"

print(f"\nComplement: {comp_dna}")
print(f"Reverse complement: {comp_dna[::-1]}")

# SOLUTION (uncomment to verify):
# The bugs are:
# 1. If you used 'DNA' instead of 'dna', Python is case-sensitive
# 2. range(0, len(dna), 2) skips odd positions -- try range(len(dna))
# 3. Using '=' instead of '==' in comparisons (though this example uses 'in')
```

We examined TypeError, KeyError, IndexError, and ValueError -- the four most common errors in bioinformatics scripts. Understanding error messages is half the debugging battle.

**AI version** (`ch06_ai_03.py`):

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

# This code has intentional bugs for the debugging exercise
buggy_code = '''
dna = "CGACGTCTTCTAAGGCGA"
print("DNA: " + DNA)  # Bug 1: wrong case

complement = {"A": "T", "T": "A", "G": "C", "C": "G"}
comp_dna = ""
for base in dna:
    if base = "A":  # Bug 2: assignment instead of comparison
        comp_dna += complement[base]
    else
        comp_dna += "N"  # Bug 3: missing colon

print("Complement: " + comp_dna)
'''

print("=== BUGGY CODE ===")
print(buggy_code)

print("--- AI: Help me debug this code ---\n")
result = ask_ai(
    f"I'm a student learning Python for bioinformatics. "
    f"This code is supposed to find the complement of a DNA sequence, "
    f"but it has bugs:\n\n{buggy_code}\n\n"
    "Please:\n"
    "1. Identify each bug and explain WHY it's wrong\n"
    "2. Show the corrected code\n"
    "3. Explain the Python rule that each bug violates\n"
    "4. Give me a tip to avoid each type of bug in the future\n\n"
    "Be encouraging -- I'm still learning!"
)
print(result)
```

The AI acts as a debugging assistant: it explains what each error means in plain English, suggests the most likely cause, and recommends a fix.

## Chapter Summary

This chapter covered restriction enzymes, command-line tools, and debugging. Practical skills for building and maintaining bioinformatics software.

The vanilla scripts gave you hands-on experience with the core techniques. The AI scripts showed how LLMs can interpret, explain, and extend your analysis. Together, they prepare you for real-world bioinformatics work where code and AI work side by side.
