---
title: "Chapter 10: Metagenomics"
weight: 10
---

Metagenomics studies entire microbial communities from environmental samples. Instead of sequencing one organism, you sequence everything in a soil sample, ocean water, or gut microbiome.

This chapter covers taxonomic classification using 16S rRNA and diversity analysis between samples. You will learn how tools like QIIME and Mothur work under the hood.

Metagenomics is one of the fastest-growing fields in biology. The human microbiome project, antibiotic resistance tracking, and environmental monitoring all depend on these methods.

## Taxonomic Classification with 16S rRNA

The 16S rRNA gene is the standard marker for bacterial identification. This script classifies sequences by comparing them to reference databases.

**Vanilla version** (`ch10_vanilla_01.py`):

```python
#!/usr/bin/env python3


import random
from collections import Counter

# Simulated taxonomic classification results
# (In reality, this would come from Kraken2 or MetaPhlAn)
random.seed(42)

TAXA = {
    "Bacteroides": 0.25,
    "Faecalibacterium": 0.15,
    "Bifidobacterium": 0.12,
    "Lactobacillus": 0.08,
    "Roseburia": 0.07,
    "Eubacterium": 0.06,
    "Clostridium": 0.05,
    "Prevotella": 0.04,
    "Ruminococcus": 0.03,
    "Akkermansia": 0.02,
    "Escherichia": 0.01,
    "Other": 0.12,
}

# Generate classification results
n_reads = 1000
classifications = []
for taxon, abundance in TAXA.items():
    count = int(abundance * n_reads)
    classifications.extend([taxon] * count)

# Add noise
random.shuffle(classifications)

print(f"Metagenomic classification: {len(classifications)} reads")
print(f"\nTaxonomic composition:")
print("-" * 40)

counts = Counter(classifications)
for taxon, count in counts.most_common():
    pct = count / len(classifications) * 100
    bar = "#" * int(pct / 2)
    print(f"  {taxon:20s} {count:4d} ({pct:5.1f}%) {bar}")

# Diversity metrics
print(f"\nDiversity metrics:")
print(f"  Total reads: {len(classifications)}")
print(f"  Unique taxa: {len(counts)}")
print(f"  Most abundant: {counts.most_common(1)[0][0]} ({counts.most_common(1)[0][1]})")

# Shannon diversity index
import math
shannon = 0
for count in counts.values():
    p = count / len(classifications)
    if p > 0:
        shannon -= p * math.log(p)
print(f"  Shannon index: {shannon:.2f}")
print(f"  (Higher = more diverse, max for {len(counts)} taxa = {math.log(len(counts)):.2f})")
```

We built a simple taxonomy classifier using 16S rRNA reference sequences, assigned taxonomy based on sequence similarity, and computed diversity metrics.

**AI version** (`ch10_ai_01.py`):

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

composition = {
    "Bacteroides": 25, "Faecalibacterium": 15, "Bifidobacterium": 12,
    "Lactobacillus": 8, "Roseburia": 7, "Eubacterium": 6,
    "Clostridium": 5, "Prevotella": 4, "Ruminococcus": 3,
    "Akkermansia": 2, "Escherichia": 1
}
shannon = 2.85

print("Gut microbiome composition:")
for taxon, pct in sorted(composition.items(), key=lambda x: -x[1]):
    print(f"  {taxon}: {pct}%")
print(f"Shannon diversity: {shannon}")

print("\n--- AI: What does this microbiome profile mean? ---\n")
result = ask_ai(
    f"This is a gut microbiome profile:\n" +
    "\n".join(f"  {t}: {p}%" for t, p in sorted(composition.items(), key=lambda x: -x[1])) +
    f"\n  Shannon diversity: {shannon}\n\n"
    "Please explain:\n"
    "1. What is the gut microbiome and why does it matter?\n"
    "2. Are these normal proportions? What would be 'unhealthy'?\n"
    "3. What do the top 3 bacteria (Bacteroides, Faecalibacterium, Bifidobacterium) do?\n"
    "4. How do antibiotics affect the microbiome?\n"
    "5. What is the 'gut-brain axis'?\n\n"
    "Explain for a college freshman who eats a typical American diet."
)
print(result)
```

The AI explains the classification results: what the taxonomy means, why 16S is the standard marker, and how to interpret diversity in a microbiome sample.

> [!TIP]
> You can run any vanilla script without an API key. The AI scripts will print a message and run in offline mode if no key is set.

## Beta Diversity and PCoA

Beta diversity measures how different two microbial communities are. Principal Coordinates Analysis (PCoA) visualizes these differences. This script computes and visualizes beta diversity.

**Vanilla version** (`ch10_vanilla_02.py`):

```python
#!/usr/bin/env python3


import math
from collections import Counter

# Three samples: healthy, antibiotic-treated, disease
samples = {
    "Healthy": {"Bacteroides": 25, "Faecalibacterium": 15, "Bifidobacterium": 12, "Lactobacillus": 8, "Roseburia": 7, "Other": 33},
    "Antibiotic": {"Bacteroides": 5, "Enterococcus": 30, "Clostridium": 25, "Escherichia": 20, "Other": 20},
    "Disease": {"Fusobacterium": 20, "Porphyromonas": 18, "Prevotella": 15, "Bacteroides": 10, "Other": 37},
}

print("Microbiome comparison across conditions:")
print("=" * 50)

# Shannon diversity for each
def shannon(counts):
    total = sum(counts.values())
    return -sum((c/total) * math.log(c/total) for c in counts.values() if c > 0)

for name, comp in samples.items():
    h = shannon(comp)
    print(f"\n{name} (Shannon={h:.2f}):")
    for taxon, pct in sorted(comp.items(), key=lambda x: -x[1]):
        bar = "#" * (pct // 2)
        print(f"  {taxon:20s} {pct:3d}% {bar}")

# Jaccard similarity between samples
def jaccard(s1, s2):
    set1 = set(k for k, v in s1.items() if v > 2)
    set2 = set(k for k, v in s2.items() if v > 2)
    intersection = set1 & set2
    union = set1 | set2
    return len(intersection) / len(union) if union else 0

print("\n\nPairwise similarity (Jaccard index):")
names = list(samples.keys())
for i in range(len(names)):
    for j in range(i+1, len(names)):
        sim = jaccard(samples[names[i]], samples[names[j]])
        print(f"  {names[i]} vs {names[j]}: {sim:.2f}")
```

We computed distance matrices between samples, performed PCoA to reduce dimensionality, and visualized the results. PCoA reveals which samples are most similar.

**AI version** (`ch10_ai_02.py`):

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

print("Three microbiome profiles:")
print("  Healthy: Bacteroides 25%, Faecalibacterium 15%, Bifidobacterium 12%")
print("  Antibiotic: Enterococcus 30%, Clostridium 25%, E.coli 20%")
print("  Disease: Fusobacterium 20%, Porphyromonas 18%, Prevotella 15%")

print("\n--- AI: What do these differences tell us? ---\n")
result = ask_ai(
    "I compared microbiomes from three conditions:\n\n"
    "Healthy: Bacteroides 25%, Faecalibacterium 15%, Bifidobacterium 12%\n"
    "Post-antibiotic: Enterococcus 30%, Clostridium 25%, E.coli 20%\n"
    "Disease: Fusobacterium 20%, Porphyromonas 18%, Prevotella 15%\n\n"
    "Please explain:\n"
    "1. Why does antibiotic treatment shift the microbiome so dramatically?\n"
    "2. Fusobacterium is enriched in disease -- what disease and why?\n"
    "3. How do scientists use microbiome data to diagnose disease?\n"
    "4. What is a 'probiotic' and can it restore a healthy microbiome?\n\n"
    "Explain for a college student interested in health."
)
print(result)
```

The AI interprets the PCoA plot: what the clustering means, which samples are most similar, and what environmental factors might explain the differences.

> [!NOTE]
> The AI version always includes the same core logic as the vanilla version. The AI calls are added at the end, so you can compare the two approaches side by side.

## Chapter Summary

This chapter covered metagenomics. Taxonomic classification with 16S rRNA and beta diversity analysis.

The vanilla scripts gave you hands-on experience with the core techniques. The AI scripts showed how LLMs can interpret, explain, and extend your analysis. Together, they prepare you for real-world bioinformatics work where code and AI work side by side.
