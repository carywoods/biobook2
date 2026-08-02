---
title: "Chapter 3: The Central Dogma"
weight: 3
---

The central dogma of molecular biology describes the flow of genetic information: DNA is transcribed to RNA, which is translated to protein. This chapter implements that process in code.

You will build a codon table, translate DNA to protein, explore all six reading frames, and parse FASTA files. These are the core operations of computational biology.

Each script adds one layer of complexity. By the end, you will have a working translation pipeline that reads a FASTA file and outputs protein sequences.

## Translating DNA to Protein

Translation converts DNA into protein using the genetic code. This script implements the standard codon table and translates DNA three bases at a time.

**Vanilla version** (`ch03_vanilla_01.py`):

```python
#!/usr/bin/env python3


# The standard genetic code -- each 3-letter DNA codon maps to one amino acid
# This is the dictionary that makes translation possible
CODON_TABLE = {
    "TTT": "F", "TTC": "F", "TTA": "L", "TTG": "L",
    "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
    "ATT": "I", "ATC": "I", "ATA": "I", "ATG": "M",
    "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
    "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S",
    "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "TAT": "Y", "TAC": "Y", "TAA": "*", "TAG": "*",
    "CAT": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
    "AAT": "N", "AAC": "N", "AAA": "K", "AAG": "K",
    "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E",
    "TGT": "C", "TGC": "C", "TGA": "*", "TGG": "W",
    "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    "AGT": "S", "AGC": "S", "AGA": "R", "AGG": "R",
    "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
}


def translate(dna: str) -> str:
    """Translate a DNA sequence into a protein sequence."""
    protein = ""
    # Walk through the DNA three bases at a time
    for i in range(0, len(dna) - 2, 3):
        codon = dna[i:i + 3]
        amino_acid = CODON_TABLE.get(codon, "?")  # ? for unknown codons
        protein += amino_acid
    return protein


# --- Main program ---
dna = "CGACGTCTTCGTACGGGACTAGCTCGTGTCGGTCGC"

print(f"DNA:     {dna}")
print(f"Length:  {len(dna)} bases")

protein = translate(dna)
print(f"Protein: {protein}")
print(f"Length:  {len(protein)} amino acids")

# Show each codon and its translation
print("\nCodon-by-codon translation:")
for i in range(0, len(dna) - 2, 3):
    codon = dna[i:i + 3]
    aa = CODON_TABLE.get(codon, "?")
    print(f"  {codon} -> {aa}")
```

The codon table is a Python dictionary: 64 key-value pairs mapping three-letter DNA codons to single-letter amino acid codes. The star (*) represents a stop codon.

**AI version** (`ch03_ai_01.py`):

```python
#!/usr/bin/env python3


import os

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


# Same genetic code and translation as vanilla
CODON_TABLE = {
    "TTT": "F", "TTC": "F", "TTA": "L", "TTG": "L",
    "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
    "ATT": "I", "ATC": "I", "ATA": "I", "ATG": "M",
    "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
    "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S",
    "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "TAT": "Y", "TAC": "Y", "TAA": "*", "TAG": "*",
    "CAT": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
    "AAT": "N", "AAC": "N", "AAA": "K", "AAG": "K",
    "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E",
    "TGT": "C", "TGC": "C", "TGA": "*", "TGG": "W",
    "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    "AGT": "S", "AGC": "S", "AGA": "R", "AGG": "R",
    "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
}


def translate(dna: str) -> str:
    protein = ""
    for i in range(0, len(dna) - 2, 3):
        codon = dna[i:i + 3]
        amino_acid = CODON_TABLE.get(codon, "?")
        protein += amino_acid
    return protein


# --- Main program ---
dna = "CGACGTCTTCGTACGGGACTAGCTCGTGTCGGTCGC"
protein = translate(dna)

print(f"DNA:     {dna}")
print(f"Protein: {protein}")
print(f"Length:  {len(protein)} amino acids")

# --- AI: Explain the protein ---
print("\n--- AI: What does this protein sequence mean? ---\n")

result = ask_ai(
    f"I translated a DNA sequence into a protein.\n\n"
    f"DNA: {dna}\n"
    f"Protein: {protein}\n\n"
    "Please explain:\n"
    "1. What do the one-letter amino acid codes mean? "
    "(List each unique amino acid in this protein with its full name)\n"
    "2. Is this protein likely to be functional? Why or why not?\n"
    "3. What kind of protein might contain this sequence?\n\n"
    "Explain for a college student with no biology background."
)
print(result)

# --- AI: Explain the stop codon ---
print("\n--- AI: Why does translation stop? ---\n")

if "*" in protein:
    stop_pos = protein.index("*")
    result = ask_ai(
        f"The protein sequence {protein} has a stop codon (*) at position {stop_pos + 1}.\n"
        f"The DNA codon at that position is {dna[stop_pos*3:stop_pos*3+3]}.\n\n"
        "Explain what a stop codon is and why it matters for protein synthesis. "
        "Use an analogy that a non-scientist would understand."
    )
    print(result)
else:
    print("No stop codon found -- this might be a partial sequence.")
```

The AI interprets the translated protein: what amino acids are present, whether the protein has a start and stop codon, and what the sequence might encode.

> [!TIP]
> You can run any vanilla script without an API key. The AI scripts will print a message and run in offline mode if no key is set.

## Six Reading Frame Translation

DNA can be read in six different ways: three reading frames on the forward strand and three on the reverse complement. This script translates all six and identifies open reading frames.

**Vanilla version** (`ch03_vanilla_02.py`):

```python
#!/usr/bin/env python3


CODON_TABLE = {
    "TTT": "F", "TTC": "F", "TTA": "L", "TTG": "L",
    "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
    "ATT": "I", "ATC": "I", "ATA": "I", "ATG": "M",
    "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
    "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S",
    "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "TAT": "Y", "TAC": "Y", "TAA": "*", "TAG": "*",
    "CAT": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
    "AAT": "N", "AAC": "N", "AAA": "K", "AAG": "K",
    "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E",
    "TGT": "C", "TGC": "C", "TGA": "*", "TGG": "W",
    "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    "AGT": "S", "AGC": "S", "AGA": "R", "AGG": "R",
    "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
}

COMPLEMENT = {"A": "T", "T": "A", "G": "C", "C": "G"}


def reverse_complement(dna: str) -> str:
    """Return the reverse complement of a DNA sequence."""
    return "".join(COMPLEMENT.get(base, "N") for base in reversed(dna))


def translate(dna: str) -> str:
    """Translate DNA to protein."""
    protein = ""
    for i in range(0, len(dna) - 2, 3):
        codon = dna[i:i + 3]
        protein += CODON_TABLE.get(codon, "?")
    return protein


def translate_frame(dna: str, frame: int) -> str:
    """Translate starting from a specific reading frame (0, 1, or 2)."""
    return translate(dna[frame:])


# --- Main program ---
dna = "CGACGTCTTCGTACGGGACTAGCTCGTGTCGGTCGC"

print(f"DNA sequence ({len(dna)} bases):")
print(f"  {dna}\n")

# The six reading frames:
# Frames +1, +2, +3: forward strand, starting at positions 0, 1, 2
# Frames -1, -2, -3: reverse complement, starting at positions 0, 1, 2
revcomp = reverse_complement(dna)

print(f"Reverse complement:")
print(f"  {revcomp}\n")

print("Six reading frame translations:")
print("-" * 50)

for frame in range(3):
    protein = translate_frame(dna, frame)
    print(f"  Frame +{frame + 1}: {protein}")

for frame in range(3):
    protein = translate_frame(revcomp, frame)
    print(f"  Frame -{frame + 1}: {protein}")

# Look for open reading frames (start at M, stop at *)
print("\nOpen reading frames (M...*):")
for frame in range(3):
    protein = translate_frame(dna, frame)
    # Find M...* patterns
    start = 0
    while start < len(protein):
        m_pos = protein.find("M", start)
        if m_pos == -1:
            break
        stop = protein.find("*", m_pos)
        if stop == -1:
            orf = protein[m_pos:]
            print(f"  Frame +{frame + 1}: M{orf} (no stop codon)")
            break
        else:
            orf = protein[m_pos:stop + 1]
            print(f"  Frame +{frame + 1}: {orf}")
            start = stop + 1
```

We implemented reverse_complement() and translate_frame(), then scanned for open reading frames (ORFs) -- stretches starting with M (methionine) and ending with * (stop).

**AI version** (`ch03_ai_02.py`):

```python
#!/usr/bin/env python3


import os

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


CODON_TABLE = {
    "TTT": "F", "TTC": "F", "TTA": "L", "TTG": "L",
    "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
    "ATT": "I", "ATC": "I", "ATA": "I", "ATG": "M",
    "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
    "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S",
    "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "TAT": "Y", "TAC": "Y", "TAA": "*", "TAG": "*",
    "CAT": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
    "AAT": "N", "AAC": "N", "AAA": "K", "AAG": "K",
    "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E",
    "TGT": "C", "TGC": "C", "TGA": "*", "TGG": "W",
    "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    "AGT": "S", "AGC": "S", "AGA": "R", "AGG": "R",
    "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
}

COMPLEMENT = {"A": "T", "T": "A", "G": "C", "C": "G"}


def reverse_complement(dna: str) -> str:
    return "".join(COMPLEMENT.get(base, "N") for base in reversed(dna))


def translate(dna: str) -> str:
    protein = ""
    for i in range(0, len(dna) - 2, 3):
        codon = dna[i:i + 3]
        protein += CODON_TABLE.get(codon, "?")
    return protein


def translate_frame(dna: str, frame: int) -> str:
    return translate(dna[frame:])


# --- Main program ---
dna = "CGACGTCTTCGTACGGGACTAGCTCGTGTCGGTCGC"
revcomp = reverse_complement(dna)

print(f"DNA: {dna}")
print(f"RevComp: {revcomp}\n")

# Collect all six frames
frames = {}
for frame in range(3):
    frames[f"+{frame + 1}"] = translate_frame(dna, frame)
for frame in range(3):
    frames[f"-{frame + 1}"] = translate_frame(revcomp, frame)

print("Six reading frame translations:")
for name, protein in frames.items():
    print(f"  Frame {name}: {protein}")

# --- AI: Which frame is most likely the real gene? ---
print("\n--- AI: Which reading frame is the real gene? ---\n")

frame_report = "\n".join(f"  Frame {name}: {protein}" for name, protein in frames.items())

result = ask_ai(
    f"I have a DNA sequence and its translations in six reading frames:\n\n"
    f"DNA: {dna}\n\n"
    f"{frame_report}\n\n"
    "Please analyze:\n"
    "1. Which frame is most likely to contain a real protein? Why?\n"
    "   (Look for: starts with M, reasonable length before a stop, "
    "no stop codons interrupting it)\n"
    "2. What is the longest open reading frame across all frames?\n"
    "3. For a non-scientist: why do biologists look at all six frames "
    "instead of just one?\n\n"
    "Be specific about which frame you recommend and why."
)
print(result)

# --- AI: Amino acid composition analysis ---
print("\n--- AI: Amino acid composition ---\n")

# Find the longest frame without stops
best_frame = max(frames.items(), key=lambda x: len(x[1].replace("*", "")))
result = ask_ai(
    f"The longest open reading frame is in frame {best_frame[0]}: {best_frame[1]}\n\n"
    "Analyze the amino acid composition:\n"
    "1. Which amino acids appear most frequently?\n"
    "2. Is this composition typical of any class of proteins?\n"
    "3. What can we infer about the chemical properties of this protein?\n\n"
    "Keep it brief and accessible."
)
print(result)
```

The AI helps interpret the six reading frames: which frame is most likely the real gene, why all six matter, and what open reading frames tell us about gene structure.

> [!NOTE]
> The AI version always includes the same core logic as the vanilla version. The AI calls are added at the end, so you can compare the two approaches side by side.

## Sequence Manipulation Functions

Bioinformatics scripts are built from reusable functions. This script defines functions for appending bases, substituting bases, and computing complements.

**Vanilla version** (`ch03_vanilla_03.py`):

```python
#!/usr/bin/env python3



def append_bases(dna: str, bases: str) -> str:
    """Append nucleotides to a DNA sequence."""
    return dna + bases


def substitute_base(dna: str, old: str, new: str) -> str:
    """Replace all occurrences of a base in DNA."""
    return dna.replace(old, new)


def complement(base: str) -> str:
    """Return the complement of a single base."""
    comp = {"A": "T", "T": "A", "G": "C", "C": "G"}
    return comp.get(base, "N")


# --- Main program ---
dna = "CGACGTCTTCTCAGGCGA"
print(f"Original DNA: {dna}")

# Append
longer = append_bases(dna, "ACGT")
print(f"After appending ACGT: {longer}")

# Substitute
changed = substitute_base(dna, "A", "T")
print(f"After replacing A with T: {changed}")

# Complement each base
comp = "".join(complement(b) for b in dna)
print(f"Complement: {comp}")

# Count specific bases
for base in "ACGT":
    count = dna.count(base)
    print(f"  {base} appears {count} times")
```

Functions use def, take parameters, and return values. We built append_bases(), substitute_base(), and complement(). Each mirrors a real molecular biology operation.

**AI version** (`ch03_ai_03.py`):

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

dna = "CGACGTCTTCTCAGGCGA"
print(f"Original: {dna}")

changed = dna.replace("A", "T")
print(f"A->T:     {changed}")

print("\n--- AI: What happens when we mutate DNA? ---\n")
result = ask_ai(
    f"I replaced every A with T in a DNA sequence:\n"
    f"Original: {dna}\n"
    f"Mutated:  {changed}\n\n"
    "Explain:\n"
    "1. This is a substitution mutation. What types of point mutations exist?\n"
    "2. If this sequence were part of a gene, what could happen to the protein?\n"
    "3. What is the difference between a synonymous and non-synonymous mutation?\n\n"
    "Use an analogy: think of DNA as a recipe book."
)
print(result)
```

The AI explains what each operation means biologically: appending bases extends a gene, substituting a base is a mutation, and computing the complement models strand pairing.

## FASTA Parsing and Translation Pipeline

FASTA is the universal file format for biological sequences. This script reads a FASTA file, parses it into a dictionary, and translates each sequence to protein.

**Vanilla version** (`ch03_vanilla_04.py`):

```python
#!/usr/bin/env python3


import os
import tempfile

CODON_TABLE = {
    "TTT": "F", "TTC": "F", "TTA": "L", "TTG": "L", "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
    "ATT": "I", "ATC": "I", "ATA": "I", "ATG": "M", "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
    "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S", "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T", "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "TAT": "Y", "TAC": "Y", "TAA": "*", "TAG": "*", "CAT": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
    "AAT": "N", "AAC": "N", "AAA": "K", "AAG": "K", "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E",
    "TGT": "C", "TGC": "C", "TGA": "*", "TGG": "W", "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    "AGT": "S", "AGC": "S", "AGA": "R", "AGG": "R", "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
}


def read_fasta(filename: str) -> dict:
    """Read a FASTA file and return {header: sequence}."""
    sequences = {}
    current_header = None
    current_seq = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if current_header:
                    sequences[current_header] = "".join(current_seq)
                current_header = line[1:]
                current_seq = []
            else:
                current_seq.append(line)
    if current_header:
        sequences[current_header] = "".join(current_seq)
    return sequences


def translate(dna: str) -> str:
    """Translate DNA to protein."""
    protein = ""
    for i in range(0, len(dna) - 2, 3):
        protein += CODON_TABLE.get(dna[i:i+3], "?")
    return protein


def print_sequence(seq: str, width: int = 60) -> None:
    """Print a sequence with line numbers."""
    for i in range(0, len(seq), width):
        chunk = seq[i:i+width]
        print(f"  {i+1:4d} {chunk}")


# --- Main program ---
# Create a sample FASTA file
sample = """>human_hemoglobin_beta partial mRNA
ATGGTGCATCTGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTGAAC
GTGGATGAAGTTGGTGGTGAGGCCCTGGGCAGGCTGCTGGTGGTCTACCCTTGGACCCAG
AGGTTCTTTGAGTCCTTTGGGGATCTGTCCACTCCTGATGCTGTTATGGGCAACCCTAAG
GTGAAGGCTCATGGCAAGAAAGTGCTCGGTGCCTTTAGTGATGGCCTGGCTCACCTGGAC
AACCTCAAGGGCACCTTTGCCACACTGAGTGAGCTGCACTGTGACAAGCTGCACGTGGAT
CCTGAGAACTTCAGG
>mouse_hemoglobin_beta partial mRNA
ATGGTGCACCTGACTGATGCTGAGAAGGCTGCCGTTACTGCCCTGTGGGGCAAGGTGAA
CGTGGATGAAGTTGGTGGTGAGGCCCTGGGCAGG
"""

sample_file = os.path.join(tempfile.gettempdir(), "sample.dna")
with open(sample_file, "w") as f:
    f.write(sample)

# Parse the FASTA file
sequences = read_fasta(sample_file)
os.remove(sample_file)

print(f"Read {len(sequences)} sequences from FASTA file:\n")

for header, dna in sequences.items():
    print(f">{header}")
    print(f"  Length: {len(dna)} bases")
    protein = translate(dna)
    print(f"  Protein ({len(protein)} aa):")
    print_sequence(protein)
    print()
```

We built read_fasta() to parse the standard format (header lines starting with >, followed by sequence lines), then translated each sequence.

**AI version** (`ch03_ai_04.py`):

```python
#!/usr/bin/env python3


import os
import tempfile

CODON_TABLE = {
    "TTT": "F", "TTC": "F", "TTA": "L", "TTG": "L", "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
    "ATT": "I", "ATC": "I", "ATA": "I", "ATG": "M", "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
    "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S", "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T", "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "TAT": "Y", "TAC": "Y", "TAA": "*", "TAG": "*", "CAT": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
    "AAT": "N", "AAC": "N", "AAA": "K", "AAG": "K", "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E",
    "TGT": "C", "TGC": "C", "TGA": "*", "TGG": "W", "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    "AGT": "S", "AGC": "S", "AGA": "R", "AGG": "R", "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
}

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

def read_fasta(filename: str) -> dict:
    sequences = {}
    current_header = None
    current_seq = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if current_header:
                    sequences[current_header] = "".join(current_seq)
                current_header = line[1:]
                current_seq = []
            else:
                current_seq.append(line)
    if current_header:
        sequences[current_header] = "".join(current_seq)
    return sequences

def translate(dna: str) -> str:
    protein = ""
    for i in range(0, len(dna) - 2, 3):
        protein += CODON_TABLE.get(dna[i:i+3], "?")
    return protein

# Create sample data
sample = """>human_hemoglobin_beta
ATGGTGCATCTGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTGAACGTGGATGAAGTTGGTGGTGAGGCCCTGGGCAGGCTGCTGGTGGTCTACCCTTGGACCCAGAGGTTCTTTGAGTCCTTTGGGGATCTGTCCACTCCTGATGCTGTTATGGGCAACCCTAAGGTGAAGGCTCATGGCAAGAAAGTGCTCGGTGCCTTTAGTGATGGCCTGGCTCACCTGGACAACCTCAAGGGCACCTTTGCCACACTGAGTGAGCTGCACTGTGACAAGCTGCACGTGGATCCTGAGAACTTCAGG
>mouse_hemoglobin_beta
ATGGTGCACCTGACTGATGCTGAGAAGGCTGCCGTTACTGCCCTGTGGGGCAAGGTGAACGTGGATGAAGTTGGTGGTGAGGCCCTGGGCAGG"""

sample_file = os.path.join(tempfile.gettempdir(), "sample.dna")
with open(sample_file, "w") as f:
    f.write(sample)

sequences = read_fasta(sample_file)
os.remove(sample_file)

print(f"Read {len(sequences)} sequences:\n")
proteins = {}
for header, dna in sequences.items():
    protein = translate(dna)
    proteins[header] = protein
    print(f">{header}")
    print(f"  DNA ({len(dna)} bp): {dna[:40]}...")
    print(f"  Protein ({len(protein)} aa): {protein[:40]}...")
    print()

# --- AI: Compare across species ---
print("--- AI: Comparing hemoglobin across species ---\n")
result = ask_ai(
    f"I have hemoglobin beta sequences from two species:\n\n"
    f"Human protein: {proteins.get('human_hemoglobin_beta', 'N/A')}\n"
    f"Mouse protein: {proteins.get('mouse_hemoglobin_beta', 'N/A')}\n\n"
    "Please:\n"
    "1. How similar are these two protein sequences? Count the identical positions.\n"
    "2. What does this similarity tell us about evolution?\n"
    "3. Why is hemoglobin one of the most-studied proteins in biology?\n\n"
    "Explain for a non-biology major."
)
print(result)
```

The AI analyzes the translated proteins: summarizing the output, identifying the longest protein, and suggesting what the sequences might represent biologically.

## Chapter Summary

This chapter covered the central dogma in code. You built a translation pipeline from scratch and learned to parse FASTA files.

The vanilla scripts gave you hands-on experience with the core techniques. The AI scripts showed how LLMs can interpret, explain, and extend your analysis. Together, they prepare you for real-world bioinformatics work where code and AI work side by side.
