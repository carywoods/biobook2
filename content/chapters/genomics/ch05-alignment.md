---
title: "Chapter 5: Sequence Analysis"
type: "chapter"
weight: 5
---

This chapter covers the fundamental operations of sequence analysis: counting nucleotides, simulating mutations, comparing sequences, and finding patterns. These are the building blocks for more advanced bioinformatics.

You will learn to compute GC content, simulate evolution through random mutations, measure sequence similarity with percent identity, and search for motifs using regular expressions.

Every analysis in bioinformatics starts with these basic operations. Master them here, and the rest of the textbook will make sense.

## Nucleotide Composition and GC Content

The first thing you do with any DNA sequence is count the bases. GC content -- the percentage of G and C bases -- is a key property that affects DNA stability and gene expression.

**Vanilla version** (`ch05_vanilla_01.py`):

```python
#!/usr/bin/env python3


from collections import Counter


def count_nucleotides(dna: str) -> dict:
    """Count each nucleotide in a DNA sequence."""
    counts = Counter(dna.upper())
    return dict(counts)


def nucleotide_percentages(dna: str) -> dict:
    """Calculate the percentage of each nucleotide."""
    counts = count_nucleotides(dna)
    total = len(dna)
    return {base: count / total * 100 for base, count in counts.items()}


def gc_content(dna: str) -> float:
    """Calculate GC content as a percentage."""
    dna = dna.upper()
    gc = dna.count("G") + dna.count("C")
    return gc / len(dna) * 100


# --- Main program ---
# A real human hemoglobin subunit beta mRNA fragment
dna = (
    "ATGGTGCATCTGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTG"
    "AACGTGGATGAAGTTGGTGGTGAGGCCCTGGGCAGGCTGCTGGTGGTCTACCCTTGG"
    "ACCCAGAGGTTCTTTGAGTCCTTTGGGGATCTGTCCACTCCTGATGCTGTTATGGGCA"
    "ACCCTAAGGTGAAGGCTCATGGCAAGAAAGTGCTCGGTGCCTTTAGTGATGGCCTGG"
    "CTCACCTGGACAACCTCAAGGGCACCTTTGCCACACTGAGTGAGCTGCACTGTGACAA"
    "GCTGCACGTGGATCCTGAGAACTTCAGG"
)

print(f"DNA sequence ({len(dna)} bases):")
print(f"  {dna[:60]}...\n")

# Count nucleotides
counts = count_nucleotides(dna)
print("Nucleotide counts:")
for base in sorted(counts):
    print(f"  {base}: {counts[base]}")

# Percentages
print("\nNucleotide percentages:")
pcts = nucleotide_percentages(dna)
for base in sorted(pcts):
    print(f"  {base}: {pcts[base]:.1f}%")

# GC content
gc = gc_content(dna)
print(f"\nGC content: {gc:.1f}%")
print(f"AT content: {100 - gc:.1f}%")

# Biological interpretation
print("\nInterpretation:")
if gc > 60:
    print("  High GC content -- typical of bacteria and some plant genes")
elif gc > 45:
    print("  Moderate GC content -- typical of many vertebrate genes")
else:
    print("  Low GC content -- may indicate AT-rich region or viral origin")
```

We used Counter from collections to count nucleotides, computed percentages, and calculated GC content. These statistics are the starting point for any sequence analysis.

**AI version** (`ch05_ai_01.py`):

```python
#!/usr/bin/env python3


import os
from collections import Counter

try:
    from openai import OpenAI
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY", ""),
        base_url=os.environ.get("OPENAI_BASE_URL", "https://openrouter.ai/api/v1"),
    )
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("Note: Install openai package for AI features (pip install openai)\n")


def ask_ai(prompt: str) -> str:
    if not AI_AVAILABLE:
        return "(AI not available -- set OPENAI_API_KEY environment variable)"
    response = client.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL", "google/gemini-2.5-flash"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content


def count_nucleotides(dna: str) -> dict:
    return dict(Counter(dna.upper()))


def nucleotide_percentages(dna: str) -> dict:
    counts = count_nucleotides(dna)
    total = len(dna)
    return {base: count / total * 100 for base, count in counts.items()}


def gc_content(dna: str) -> float:
    dna = dna.upper()
    gc = dna.count("G") + dna.count("C")
    return gc / len(dna) * 100


# --- Main program ---
dna = (
    "ATGGTGCATCTGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTG"
    "AACGTGGATGAAGTTGGTGGTGAGGCCCTGGGCAGGCTGCTGGTGGTCTACCCTTGG"
    "ACCCAGAGGTTCTTTGAGTCCTTTGGGGATCTGTCCACTCCTGATGCTGTTATGGGCA"
    "ACCCTAAGGTGAAGGCTCATGGCAAGAAAGTGCTCGGTGCCTTTAGTGATGGCCTGG"
    "CTCACCTGGACAACCTCAAGGGCACCTTTGCCACACTGAGTGAGCTGCACTGTGACAA"
    "GCTGCACGTGGATCCTGAGAACTTCAGG"
)

print(f"DNA sequence ({len(dna)} bases):")
print(f"  {dna[:60]}...\n")

counts = count_nucleotides(dna)
pcts = nucleotide_percentages(dna)
gc = gc_content(dna)

print("Nucleotide counts and percentages:")
for base in sorted(counts):
    print(f"  {base}: {counts[base]} ({pcts[base]:.1f}%)")

print(f"\nGC content: {gc:.1f}%")
print(f"AT content: {100 - gc:.1f}%")

# --- AI: What does this sequence composition tell us? ---
print("\n--- AI: Sequence composition analysis ---\n")

result = ask_ai(
    f"I analyzed a DNA sequence and found these nucleotide frequencies:\n\n"
    f"A: {pcts.get('A', 0):.1f}%\n"
    f"T: {pcts.get('T', 0):.1f}%\n"
    f"G: {pcts.get('G', 0):.1f}%\n"
    f"C: {pcts.get('C', 0):.1f}%\n"
    f"GC content: {gc:.1f}%\n"
    f"Sequence length: {len(dna)} bases\n\n"
    "Please tell me:\n"
    "1. Is this GC content typical of any particular organism or gene type?\n"
    "2. The A and T percentages -- are they expected to be roughly equal? "
    "Why or why not? (Think about base pairing)\n"
    "3. What does GC content tell us about the stability of the DNA double helix?\n\n"
    "Explain for a college student with no biology background."
)
print(result)

# --- AI: Compare to known genes ---
print("\n--- AI: Is this a known gene? ---\n")

result = ask_ai(
    f"Here is a DNA sequence of {len(dna)} bases:\n{dna}\n\n"
    "Based on the sequence alone:\n"
    "1. Does this look like it could be from a human gene? Why?\n"
    "2. The sequence starts with ATG (start codon). What does that suggest?\n"
    "3. Can you identify what gene this might be from? "
    "(It's from a very well-known human gene family.)\n\n"
    "Be specific but accessible."
)
print(result)
```

The AI interprets the composition: what GC content tells us about the organism, how it affects DNA melting temperature, and why GC-rich regions are harder to sequence.

::: {.callout-tip}
You can run any vanilla script without an API key. The AI scripts will print a message and run in offline mode if no key is set.
:::

## Mutation Simulation

Evolution works through mutation. This script simulates random mutations in a DNA sequence and measures the effect. Simulating mutations helps us understand how sequences change over time.

**Vanilla version** (`ch05_vanilla_02.py`):

```python
#!/usr/bin/env python3


import random

def mutate_dna(dna: str, mutation_rate: float = 0.1) -> str:
    """Randomly mutate bases in a DNA sequence."""
    bases = ["A", "T", "G", "C"]
    mutated = []
    for base in dna:
        if random.random() < mutation_rate:
            # Pick a different base
            choices = [b for b in bases if b != base]
            new_base = random.choice(choices)
            mutated.append(new_base)
        else:
            mutated.append(base)
    return "".join(mutated)


def count_mutations(original: str, mutated: str) -> int:
    """Count the number of positions that differ."""
    return sum(1 for a, b in zip(original, mutated) if a != b)


# --- Main program ---
random.seed(42)  # For reproducibility

dna = "A" * 30  # Easy to see mutations
print(f"Original: {dna}")

# Mutate at different rates
for rate in [0.05, 0.1, 0.2, 0.5]:
    mutated = mutate_dna(dna, rate)
    changes = count_mutations(dna, mutated)
    print(f"  Rate {rate:.0%}: {mutated} ({changes} mutations)")

# Real-world example
print("\nReal sequence:")
original = "ATGGTGCATCTGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTGAAC"
mutated = mutate_dna(original, 0.05)
changes = count_mutations(original, mutated)
print(f"  Original: {original}")
print(f"  Mutated:  {mutated}")
print(f"  Changes:  {changes}/{len(original)} positions ({changes/len(original):.1%})")

# Show which positions changed
print("\n  Position-by-position:")
for i, (a, b) in enumerate(zip(original, mutated)):
    if a != b:
        print(f"    Position {i+1}: {a} -> {b}")
```

We used Python's random module to introduce point mutations at a given rate, then compared the original and mutated sequences to count changes.

**AI version** (`ch05_ai_02.py`):

```python
#!/usr/bin/env python3


import os
import random

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

def mutate_dna(dna, rate=0.1):
    bases = ["A", "T", "G", "C"]
    return "".join(random.choice([b for b in bases if b != c]) if random.random() < rate else c for c in dna)

random.seed(42)
original = "ATGGTGCATCTGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTGAAC"
mutated = mutate_dna(original, 0.05)
changes = sum(1 for a, b in zip(original, mutated) if a != b)

print(f"Original: {original}")
print(f"Mutated:  {mutated}")
print(f"Changes:  {changes}/{len(original)} positions")

print("\n--- AI: What do these mutations mean? ---\n")
mutations = [(i+1, original[i], mutated[i]) for i in range(len(original)) if original[i] != mutated[i]]
mut_text = ", ".join(f"pos {p}: {a}->{b}" for p, a, b in mutations)

result = ask_ai(
    f"A DNA sequence was mutated at {changes} positions:\n{mut_text}\n\n"
    f"Original: {original}\nMutated:  {mutated}\n\n"
    "Please explain:\n"
    "1. Classify each mutation: transition (purine->purine or pyrimidine->pyrimidine) "
    "vs transversion (purine->pyrimidine or vice versa)\n"
    "2. At a 5% mutation rate, is this typical of real evolution?\n"
    "3. How do scientists use mutation rates to estimate evolutionary time?\n\n"
    "Keep it accessible for a college freshman."
)
print(result)
```

The AI explains mutation rates: what a 10% mutation rate means biologically, how real mutation rates compare, and what types of mutations are most common in nature.

::: {.callout-note}
The AI version always includes the same core logic as the vanilla version. The AI calls are added at the end, so you can compare the two approaches side by side.
:::

## Sequence Comparison and Percent Identity

Comparing two sequences tells you how similar they are. Percent identity -- the fraction of matching positions -- is the simplest measure of sequence similarity.

**Vanilla version** (`ch05_vanilla_03.py`):

```python
#!/usr/bin/env python3


import random

def random_dna(length: int) -> str:
    """Generate a random DNA sequence."""
    return "".join(random.choice("ATCG") for _ in range(length))


def percent_identity(seq1: str, seq2: str) -> float:
    """Calculate the percentage of identical positions."""
    matches = sum(1 for a, b in zip(seq1, seq2) if a == b)
    return matches / min(len(seq1), len(seq2)) * 100


# --- Main program ---
random.seed(42)

# Generate random sequences
print("Generating 6 random DNA sequences (20-30 bases each):\n")
sequences = []
for i in range(6):
    length = random.randint(20, 30)
    seq = random_dna(length)
    sequences.append(seq)
    print(f"  Seq {i+1} ({length} bp): {seq}")

# Compare all pairs
print("\nPairwise percent identity:")
print("-" * 40)
for i in range(len(sequences)):
    for j in range(i + 1, len(sequences)):
        pid = percent_identity(sequences[i], sequences[j])
        print(f"  Seq {i+1} vs Seq {j+1}: {pid:.1f}%")

# Average identity
identities = []
for i in range(len(sequences)):
    for j in range(i + 1, len(sequences)):
        identities.append(percent_identity(sequences[i], sequences[j]))

print(f"\nAverage pairwise identity: {sum(identities)/len(identities):.1f}%")
print(f"Expected for random DNA: ~25% (1/4 bases match by chance)")
```

We generated random DNA sequences, compared them position by position, and computed percent identity. Even random sequences share about 25% identity by chance.

**AI version** (`ch05_ai_03.py`):

```python
#!/usr/bin/env python3


import os
import random

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

def random_dna(length):
    return "".join(random.choice("ATCG") for _ in range(length))

def percent_identity(s1, s2):
    return sum(1 for a, b in zip(s1, s2) if a == b) / min(len(s1), len(s2)) * 100

random.seed(42)
seqs = [random_dna(random.randint(20, 30)) for _ in range(6)]

print("Random sequences:")
for i, s in enumerate(seqs, 1):
    print(f"  {i}: {s}")

identities = []
for i in range(len(seqs)):
    for j in range(i+1, len(seqs)):
        identities.append(percent_identity(seqs[i], seqs[j]))

avg = sum(identities)/len(identities)
print(f"\nAverage pairwise identity: {avg:.1f}%")
print(f"Expected for random DNA: ~25%")

print("\n--- AI: When does sequence similarity matter? ---\n")
result = ask_ai(
    f"I compared {len(seqs)} random DNA sequences and found {avg:.1f}% average identity.\n"
    "For random sequences, we expect ~25%.\n\n"
    "Explain:\n"
    "1. If two REAL gene sequences are 90% identical, what does that mean?\n"
    "2. What's the difference between 'homology' and 'similarity'?\n"
    "3. How do scientists decide if two sequences are 'significantly similar'?\n"
    "4. What is an E-value in BLAST, and why does it matter?\n\n"
    "Use an analogy: comparing DNA is like comparing two editions of a book."
)
print(result)
```

The AI explains what percent identity means: how to interpret 25% vs. 90% identity, what thresholds indicate homology, and how this relates to evolutionary distance.

## Pattern Matching and Motif Discovery

Finding specific patterns in DNA -- restriction sites, promoter elements, coding regions -- requires pattern matching. This script uses regular expressions to search for biological motifs.

**Vanilla version** (`ch05_vanilla_04.py`):

```python
#!/usr/bin/env python3


import re

def find_motifs(sequence: str, pattern: str) -> list:
    """Find all occurrences of a motif pattern in a sequence."""
    return [(m.start(), m.group()) for m in re.finditer(pattern, sequence, re.IGNORECASE)]


# --- Main program ---
# A partial human insulin protein sequence
protein = "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT"

print(f"Protein sequence ({len(protein)} aa):")
print(f"  {protein}\n")

# Search for common motifs
motifs = {
    "N-glycosylation": r"N[^P][ST][^P]",  # Asn-X-Ser/Thr (X != Pro)
    "Phosphorylation (Ser)": r"[ST]..[DE]",  # Ser/Thr followed by acidic residues
    "Zinc finger (C2H2)": r"C.{2,4}C.{12}H.{3,5}H",
    "Leucine zipper": r"L.{6}L.{6}L.{6}L",
    "KR cleavage site": r"KR|RR",  # dibasic cleavage
}

print("Motif search results:")
print("-" * 50)
for name, pattern in motifs.items():
    matches = find_motifs(protein, pattern)
    if matches:
        print(f"  {name}:")
        for pos, match in matches:
            print(f"    Position {pos}: {match}")
    else:
        print(f"  {name}: not found")

# Custom pattern search
print("\nCustom pattern search:")
# Find all occurrences of a specific amino acid pattern
pattern = "LL"
matches = find_motifs(protein, pattern)
print(f"  Pattern '{pattern}' found {len(matches)} times:")
for pos, match in matches:
    print(f"    Position {pos}: ...{protein[max(0,pos-3):pos+len(match)+3]}...")
```

We used Python's re module to find patterns in DNA sequences, including restriction enzyme sites and degenerate motifs using regex syntax.

**AI version** (`ch05_ai_04.py`):

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

def find_motifs(seq, pattern):
    return [(m.start(), m.group()) for m in re.finditer(pattern, seq, re.IGNORECASE)]

protein = "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT"
motifs = {"N-glycosylation": r"N[^P][ST][^P]", "Phosphorylation": r"[ST]..[DE]", "Dibasic cleavage": r"KR|RR"}

print(f"Protein: {protein}\n")
found = {}
for name, pattern in motifs.items():
    matches = find_motifs(protein, pattern)
    found[name] = matches
    if matches:
        print(f"{name}: {len(matches)} match(es)")
        for pos, m in matches:
            print(f"  Position {pos}: {m}")

print("\n--- AI: What do these protein motifs tell us? ---\n")
motif_summary = "\n".join(f"  {n}: {len(m)} matches" for n, m in found.items())
result = ask_ai(
    f"I found these motifs in a protein sequence:\n{motif_summary}\n\n"
    f"Protein: {protein}\n\n"
    "Please explain:\n"
    "1. What does N-glycosylation mean? Why does the cell add sugar to proteins?\n"
    "2. What is a dibasic cleavage site? What happens there?\n"
    "3. Based on these motifs, what kind of protein might this be?\n"
    "4. How do scientists use motif databases like PROSITE or Pfam?\n\n"
    "This protein is actually proinsulin. Can you explain its processing?"
)
print(result)
```

The AI explains the biological significance of each pattern: why restriction sites matter for cloning, what degenerate motifs tell us about protein binding flexibility.

## Chapter Summary

This chapter covered sequence analysis fundamentals. Nucleotide composition, mutation simulation, sequence comparison, and pattern matching.

The vanilla scripts gave you hands-on experience with the core techniques. The AI scripts showed how LLMs can interpret, explain, and extend your analysis. Together, they prepare you for real-world bioinformatics work where code and AI work side by side.
