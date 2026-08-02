---
title: "Chapter 2: Python Basics"
type: "chapter"
weight: 2
---

This chapter introduces Python through the lens of molecular biology. Every concept you learn here -- variables, strings, conditionals, and lists -- maps directly to something you will do with DNA sequences.

We start by storing a DNA sequence in a variable. From there, we learn to concatenate fragments, classify codons, and iterate over collections of sequences. Each vanilla script builds one concept; each AI script shows how an LLM can interpret the biological meaning behind your code.

By the end of this chapter, you will be comfortable manipulating strings in Python and will have asked an AI to analyze your first DNA sequences.

## Storing and Printing DNA Sequences

Every bioinformatics program starts by putting a DNA sequence into a variable. This script stores a sequence and shows how Python strings work with biological data.

**Vanilla version** (`ch02_vanilla_01.py`):

```python
#!/usr/bin/env python3


# Store a DNA sequence in a variable
dna = "ACGGGAGGACGGGAAAATTACTACGGCATTAGC"

# Print it
print(dna)

# A few things you can do with a string
print(f"Length: {len(dna)}")
print(f"First base: {dna[0]}")
print(f"Last base: {dna[-1]}")
print(f"First 10 bases: {dna[:10]}")
```

We used basic string operations: indexing (getting a single base), slicing (getting a range of bases), and len() (counting bases). These are the building blocks for everything that follows.

**AI version** (`ch02_ai_01.py`):

```python
#!/usr/bin/env python3


import os

# Try to import the AI client -- works with OpenAI-compatible APIs
try:
    from openai import OpenAI
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY", ""),
        base_url=os.environ.get("OPENAI_BASE_URL", "https://openrouter.ai/api/v1"),
    )
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("Note: Install openai package for AI features (pip install openai)")
    print("Running in offline mode.\n")


def ask_ai(prompt: str) -> str:
    """Send a prompt to the LLM and return the response."""
    if not AI_AVAILABLE:
        return "(AI not available -- set OPENAI_API_KEY environment variable)"
    response = client.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL", "google/gemini-2.5-flash"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content


# --- Same code as the vanilla version ---
dna = "ACGGGAGGACGGGAAAATTACTACGGCATTAGC"
print(dna)
print(f"Length: {len(dna)}")
print(f"First base: {dna[0]}")
print(f"Last base: {dna[-1]}")
print(f"First 10 bases: {dna[:10]}")

# --- Now add AI analysis ---
print("\n--- AI Analysis ---\n")

# Ask the LLM to analyze the sequence
result = ask_ai(
    f"I have a DNA sequence: {dna}\n\n"
    "Please tell me:\n"
    "1. What is the GC content (percentage of G and C bases)?\n"
    "2. Is this likely a coding sequence or random DNA? Why?\n"
    "3. What organism might this come from?\n\n"
    "Keep your answer brief and suitable for a college freshman."
)
print(result)

# Ask for a biological interpretation
print("\n--- Biological Context ---\n")
result = ask_ai(
    f"Given this DNA sequence: {dna}\n\n"
    "If this were part of a gene, what kinds of proteins might it help encode? "
    "Explain in one paragraph, using language a non-biology major would understand."
)
print(result)
```

The AI version asks an LLM to interpret the sequence: its GC content, whether it looks like a coding sequence, and what organism it might come from. The AI adds biological context that raw code cannot provide.

::: {.callout-tip}
You can run any vanilla script without an API key. The AI scripts will print a message and run in offline mode if no key is set.
:::

## Concatenating DNA Fragments

In the lab, scientists join DNA fragments using restriction enzymes and ligase. In Python, we use the + operator. This script concatenates two fragments and examines the result.

**Vanilla version** (`ch02_vanilla_02.py`):

```python
#!/usr/bin/env python3


# Two DNA fragments
dna1 = "ACGGGAGGACGGGAAAATTACTACGGCATTAGC"
dna2 = "ATAGTGCCGTGAGAGTGATGTAGTA"

print("Here are the original two DNA fragments:\n")
print(dna1)
print(dna2)

# Concatenate them
combined = dna1 + dna2
print(f"\nConcatenated DNA ({len(combined)} bases):")
print(combined)

# You can also use f-strings
print(f"\nFragment 1 is {len(dna1)} bases, fragment 2 is {len(dna2)} bases")
print(f"Combined length: {len(dna1) + len(dna2)} bases")

# Insert a spacer
spacer = "NNNNN"
with_spacer = dna1 + spacer + dna2
print(f"\nWith spacer '{spacer}':")
print(with_spacer)
```

String concatenation with +, f-strings for formatted output, and inserting spacer sequences. These operations mirror what happens in molecular cloning.

**AI version** (`ch02_ai_02.py`):

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


dna1 = "ACGGGAGGACGGGAAAATTACTACGGCATTAGC"
dna2 = "ATAGTGCCGTGAGAGTGATGTAGTA"

print("Fragment 1:", dna1)
print("Fragment 2:", dna2)

combined = dna1 + dna2
print(f"\nConcatenated ({len(combined)} bases): {combined}")

# --- AI: Analyze the junction ---
print("\n--- AI: What happens at the junction? ---\n")

result = ask_ai(
    f"I concatenated two DNA fragments:\n"
    f"Fragment 1 (ends with): ...{dna1[-10:]}\n"
    f"Fragment 2 (starts with): {dna2[:10]}...\n"
    f"Combined: {combined}\n\n"
    "In molecular biology, when scientists join two DNA fragments:\n"
    "1. What is this process called? (Hint: think restriction enzymes and ligase)\n"
    "2. The junction between the two fragments -- does it create a new sequence "
    "that wasn't in either original fragment?\n"
    "3. Could this new junction accidentally create a start codon (ATG) "
    "or stop codon (TAA, TAG, TGA)?\n\n"
    "Explain for a college freshman."
)
print(result)

# --- AI: GC content comparison ---
print("\n--- AI: Comparing the fragments ---\n")

gc1 = (dna1.count("G") + dna1.count("C")) / len(dna1) * 100
gc2 = (dna2.count("G") + dna2.count("C")) / len(dna2) * 100

result = ask_ai(
    f"Two DNA fragments were concatenated:\n"
    f"Fragment 1 ({len(dna1)} bases, GC={gc1:.1f}%): {dna1}\n"
    f"Fragment 2 ({len(dna2)} bases, GC={gc2:.1f}%): {dna2}\n\n"
    "The GC content differs between the fragments. What does this tell us?\n"
    "1. Could these fragments come from different organisms?\n"
    "2. What is 'GC content' and why do scientists care about it?\n"
    "3. How might different GC content affect DNA stability?\n\n"
    "Keep it brief."
)
print(result)
```

The AI examines the junction between fragments and answers questions about molecular biology: what happens at the join point, whether new codons are accidentally created, and what GC content differences mean.

::: {.callout-note}
The AI version always includes the same core logic as the vanilla version. The AI calls are added at the end, so you can compare the two approaches side by side.
:::

## Conditionals: Classifying Codons

The genetic code uses 64 codons to encode 20 amino acids, a start signal, and three stop signals. This script uses if/elif/else to classify codons.

**Vanilla version** (`ch02_vanilla_03.py`):

```python
#!/usr/bin/env python3


codon = "ATG"

# Check if this is a start codon
if codon == "ATG":
    print(f"{codon} is the universal start codon (codes for Methionine)")
elif codon in ("TAA", "TAG", "TGA"):
    print(f"{codon} is a stop codon (translation ends here)")
else:
    print(f"{codon} is a regular codon")

# Check a sequence for start and stop codons
dna = "ATGGCCTGAACCGATCGATCG"
print(f"\nAnalyzing: {dna}")
print(f"First 3 bases: {dna[:3]}")
print(f"Last 3 bases:  {dna[-3:]}")

if dna[:3] == "ATG":
    print("  -> Starts with ATG (start codon)")
else:
    print(f"  -> Starts with {dna[:3]} (not a start codon)")

if dna[-3:] in ("TAA", "TAG", "TGA"):
    print(f"  -> Ends with {dna[-3:]} (stop codon)")
else:
    print(f"  -> Ends with {dna[-3:]} (not a stop codon)")

# Categorize multiple codons
print("\nCodon classification:")
codons = ["ATG", "TAA", "GCT", "TGA", "TAG", "ATC", "TTT"]
for c in codons:
    if c == "ATG":
        category = "START"
    elif c in ("TAA", "TAG", "TGA"):
        category = "STOP"
    else:
        category = "coding"
    print(f"  {c}: {category}")
```

Conditionals let your program make decisions. We classified codons as START (ATG), STOP (TAA, TAG, TGA), or coding. This is the simplest form of biological sequence analysis.

**AI version** (`ch02_ai_03.py`):

```python
#!/usr/bin/env python3


import os

try:
    from openai import OpenAI
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""), base_url=os.environ.get("OPENAI_BASE_URL", "https://openrouter.ai/api/v1"))
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("Note: Install openai package for AI features (pip install openai)\n")

def ask_ai(prompt: str) -> str:
    if not AI_AVAILABLE:
        return "(AI not available)"
    response = client.chat.completions.create(model=os.environ.get("OPENAI_MODEL", "google/gemini-2.5-flash"), messages=[{"role": "user", "content": prompt}], temperature=0.3)
    return response.choices[0].message.content

codons = ["ATG", "TAA", "GCT", "TGA", "TAG", "ATC", "TTT"]
print("Codon classification:")
for c in codons:
    if c == "ATG":
        category = "START"
    elif c in ("TAA", "TAG", "TGA"):
        category = "STOP"
    else:
        category = "coding"
    print(f"  {c}: {category}")

print("\n--- AI: Why does the genetic code work this way? ---\n")
result = ask_ai(
    "I classified DNA codons into START (ATG), STOP (TAA, TAG, TGA), and coding.\n\n"
    "Please explain:\n"
    "1. Why is ATG the universal start codon? Is it always the first codon?\n"
    "2. Why are there exactly three stop codons and not one?\n"
    "3. There are 64 possible codons (4^3) but only 20 amino acids. "
    "What does this 'redundancy' mean? Is it a bug or a feature?\n\n"
    "Use analogies a non-scientist would understand."
)
print(result)
```

The AI explains the deeper biology: why ATG is the universal start codon, why there are three stop codons instead of one, and what codon redundancy means for evolution.

## Lists and Iteration

Real bioinformatics work involves collections of sequences, not just one. This script introduces Python lists and shows how to iterate over, filter, and summarize collections.

**Vanilla version** (`ch02_vanilla_04.py`):

```python
#!/usr/bin/env python3


# A collection of short DNA sequences
sequences = [
    "ATGGCC",
    "GCTAGT",
    "TTACGA",
    "CCGATG",
    "AATTCC",
]

# Basic iteration
print("All sequences:")
for seq in sequences:
    print(f"  {seq}")

# With enumerate (numbered)
print("\nNumbered sequences:")
for i, seq in enumerate(sequences, start=1):
    print(f"  {i}. {seq} ({len(seq)} bases)")

# Lengths as a list
lengths = [len(s) for s in sequences]
print(f"\nLengths: {lengths}")
print(f"Total bases: {sum(lengths)}")
print(f"Average length: {sum(lengths) / len(lengths):.1f}")

# Filter: which sequences start with ATG?
print("\nSequences starting with ATG (potential start codons):")
starts_with_atg = [s for s in sequences if s.startswith("ATG")]
for seq in starts_with_atg:
    print(f"  {seq}")

# Parallel iteration with zip
labels = ["hemoglobin", "insulin", "p53", "BRCA1", "GAPDH"]
print("\nGene names and sequences:")
for label, seq in zip(labels, sequences):
    print(f"  {label}: {seq}")
```

We covered enumerate() for numbered iteration, list comprehensions for filtering, zip() for parallel iteration, and built-in functions like sum() and len() for summarizing data.

**AI version** (`ch02_ai_04.py`):

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

sequences = ["ATGGCC", "GCTAGT", "TTACGA", "CCGATG", "AATTCC"]

print("Our sequences:")
for i, seq in enumerate(sequences, 1):
    print(f"  {i}. {seq}")

print("\n--- AI: What are these sequences? ---\n")
result = ask_ai(
    f"I have {len(sequences)} short DNA sequences:\n" +
    "\n".join(f"  {i+1}. {s}" for i, s in enumerate(sequences)) +
    "\n\nFor each sequence:\n"
    "1. Translate it to protein (use the standard genetic code)\n"
    "2. Classify it: does it start with ATG? Does it contain a stop codon?\n"
    "3. If this were part of a real gene, what might it encode?\n\n"
    "Present as a table. Be brief."
)
print(result)
```

The AI takes the same list of sequences and translates each one to protein, classifies them by codon content, and predicts what genes they might come from.

## Chapter Summary

This chapter covered Python fundamentals through biological examples. Variables, strings, conditionals, and lists are the building blocks of every bioinformatics program.

The vanilla scripts gave you hands-on experience with the core techniques. The AI scripts showed how LLMs can interpret, explain, and extend your analysis. Together, they prepare you for real-world bioinformatics work where code and AI work side by side.
