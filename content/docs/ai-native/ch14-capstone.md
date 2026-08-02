---
title: "Chapter 14: Capstone Projects"
weight: 14
---

This chapter brings everything together. Each capstone project integrates skills from multiple chapters into a complete bioinformatics analysis.

The first capstone traces a disease variant from DNA to drug target. The second builds a gene expression analysis for cancer. Both demonstrate the full power of the toolkit you have built.

These projects are not exercises. They are real analyses. The variant analysis mirrors what clinical geneticists do every day. The expression dashboard mirrors what cancer researchers use to guide treatment.

## Capstone 1: From Variant to Drug Target

This project traces the BRAF V600E mutation from DNA change to protein effect to clinical treatment. It integrates variant annotation, codon tables, protein structure, and drug databases.

**Vanilla version** (`ch14_vanilla_01.py`):

```python
#!/usr/bin/env python3


# This capstone ties together skills from Chapters 3-9
# Task: Given a disease variant, trace its path from DNA to protein to structure

# Step 1: The variant
print("=" * 60)
print("CAPSTONE: From Variant to Drug Target")
print("=" * 60)

print("\nStep 1: The Variant")
print("-" * 40)
gene = "BRAF"
variant = "V600E"
print(f"  Gene: {gene}")
print(f"  Variant: {variant}")
print(f"  Clinical significance: Oncogenic (causes cancer)")

# Step 2: DNA-level analysis
print("\nStep 2: DNA-Level Analysis")
print("-" * 40)
codon_wild = "GTG"
codon_mutant = "GAG"
print(f"  Wild-type codon: {codon_wild} (Valine)")
print(f"  Mutant codon: {codon_mutant} (Glutamic acid)")
print(f"  Change: Single nucleotide (T -> A at position 1)")

# Step 3: Protein-level analysis
print("\nStep 3: Protein-Level Analysis")
print("-" * 40)
print(f"  Wild-type amino acid: Valine (V) -- hydrophobic, nonpolar")
print(f"  Mutant amino acid: Glutamic acid (E) -- acidic, charged")
print(f"  Impact: Introduces a negative charge into the hydrophobic pocket")

# Step 4: Structural analysis
print("\nStep 4: Structural Analysis")
print("-" * 40)
print(f"  PDB structure: 4MNE (BRAF V600E bound to vemurafenib)")
print(f"  AlphaFold prediction: P15056")
print(f"  Location: Activation segment of kinase domain")
print(f"  Effect: Constitutive activation of kinase activity")

# Step 5: Clinical relevance
print("\nStep 5: Clinical Relevance")
print("-" * 40)
print(f"  Disease: Melanoma (skin cancer)")
print(f"  Frequency: ~50% of melanomas harbor BRAF V600E")
print(f"  Approved drugs:")
print(f"    - Vemurafenib (Zelboraf)")
print(f"    - Dabrafenib (Tafinlar)")
print(f"    - Encorafenib (Braftovi)")

print("\n" + "=" * 60)
print("This analysis integrated: variant annotation, codon tables,")
print("amino acid properties, protein structure, drug databases,")
print("and clinical genetics -- all from skills in this textbook.")
```

We walked through the analysis step by step: identifying the variant, translating to protein, analyzing the amino acid change, locating it in the structure, and listing approved drugs.

**AI version** (`ch14_ai_01.py`):

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

print("=" * 60)
print("CAPSTONE: AI-Assisted Variant-to-Drug Analysis")
print("=" * 60)

gene = "BRAF"
variant = "V600E"
print(f"\nGene: {gene}, Variant: {variant}")
print(f"Wild-type: GTG (Valine) -> Mutant: GAG (Glutamic acid)")

print("\n--- AI: Full clinical interpretation ---\n")
result = ask_ai(
    f"I'm analyzing the {gene} {variant} variant for a capstone project.\n\n"
    f"Variant: c.1799T>A (GTG->GAG, Valine->Glutamic acid)\n"
    f"Gene: BRAF (serine/threonine-protein kinase B-Raf)\n"
    f"Chromosome: 7q34\n\n"
    "Please provide a comprehensive analysis:\n\n"
    "1. MOLECULAR MECHANISM:\n"
    "   - How does V600E change the protein's structure?\n"
    "   - Why does this make the kinase constitutively active?\n\n"
    "2. CLINICAL SIGNIFICANCE:\n"
    "   - What cancers carry this mutation?\n"
    "   - What is the prognosis difference with vs without this mutation?\n\n"
    "3. THERAPEUTIC TARGETING:\n"
    "   - What drugs target BRAF V600E?\n"
    "   - How do they work (mechanism of action)?\n"
    "   - What is resistance and why does it develop?\n\n"
    "4. BIOINFORMATICS WORKFLOW:\n"
    "   - If I wanted to find this variant in patient sequencing data,\n"
    "     what tools would I use? (aligner, caller, annotator)\n\n"
    "Write like a clinical genetics review article."
)
print(result)

print("\n--- AI: What would you research next? ---\n")
result = ask_ai(
    "Given the BRAF V600E analysis above:\n"
    "1. What are the top 3 open research questions about this variant?\n"
    "2. If you had a patient's whole genome sequence, what else would you look for?\n"
    "3. How is AI changing cancer genomics today?\n\n"
    "Be specific and cite real approaches."
)
print(result)
```

The AI provides a clinical genetics perspective: the molecular mechanism, how it causes cancer, what drugs target it, why resistance develops, and what a bioinformatics workflow looks like.

> [!TIP]
> You can run any vanilla script without an API key. The AI scripts will print a message and run in offline mode if no key is set.

## Capstone 2: Gene Expression Cancer Analysis

This project simulates a gene expression experiment comparing cancer to normal tissue. It generates expression data, computes fold changes, and interprets the biological significance.

**Vanilla version** (`ch14_vanilla_02.py`):

```python
#!/usr/bin/env python3


import numpy as np

# Simulated gene expression experiment
# Comparing cancer tissue vs normal tissue
np.random.seed(42)

# Gene names and their expected behavior
genes_info = {
    "TP53": {"normal": 100, "cancer": 30, "role": "tumor suppressor"},
    "MYC": {"normal": 50, "cancer": 200, "role": "oncogene"},
    "BRCA1": {"normal": 80, "cancer": 20, "role": "DNA repair"},
    "VEGFA": {"normal": 30, "cancer": 150, "role": "angiogenesis"},
    "CDH1": {"normal": 120, "cancer": 40, "role": "cell adhesion"},
    "KRAS": {"normal": 60, "cancer": 180, "role": "signal transduction"},
    "PTEN": {"normal": 90, "cancer": 25, "role": "tumor suppressor"},
    "EGFR": {"normal": 40, "cancer": 160, "role": "growth factor receptor"},
}

# Generate expression data with noise
n_replicates = 3
print("Gene Expression Analysis: Cancer vs Normal Tissue")
print("=" * 60)
print(f"\n{'Gene':8s} {'Role':20s} {'Normal':>10s} {'Cancer':>10s} {'log2FC':>8s} {'Status':>10s}")
print("-" * 70)

results = []
for gene, info in genes_info.items():
    normal_expr = np.random.poisson(info["normal"], n_replicates)
    cancer_expr = np.random.poisson(info["cancer"], n_replicates)

    normal_mean = normal_expr.mean()
    cancer_mean = cancer_expr.mean()
    log2fc = np.log2(cancer_mean / normal_mean) if normal_mean > 0 else 0

    status = "UP" if log2fc > 1 else ("DOWN" if log2fc < -1 else "NS")
    results.append((gene, info["role"], normal_mean, cancer_mean, log2fc, status))
    print(f"{gene:8s} {info['role']:20s} {normal_mean:10.1f} {cancer_mean:10.1f} {log2fc:+8.2f} {status:>10s}")

# Summary
upregulated = [r for r in results if r[5] == "UP"]
downregulated = [r for r in results if r[5] == "DOWN"]

print(f"\nSummary:")
print(f"  Total genes: {len(results)}")
print(f"  Upregulated in cancer: {len(upregulated)} -- {', '.join(r[0] for r in upregulated)}")
print(f"  Downregulated in cancer: {len(downregulated)} -- {', '.join(r[0] for r in downregulated)}")

print(f"\nBiological interpretation:")
print(f"  Oncogenes activated: {', '.join(r[0] for r in upregulated if 'oncogene' in r[1] or 'growth' in r[1] or 'angiogenesis' in r[1] or 'signal' in r[1])}")
print(f"  Tumor suppressors lost: {', '.join(r[0] for r in downregulated if 'tumor' in r[1] or 'repair' in r[1] or 'adhesion' in r[1])}")
```

We simulated replicates with noise, computed log2 fold changes, classified genes as up- or down-regulated, and interpreted the results in terms of oncogenes and tumor suppressors.

**AI version** (`ch14_ai_02.py`):

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

upregulated = [("MYC", "oncogene", 4.0), ("VEGFA", "angiogenesis", 2.3), ("KRAS", "signal transduction", 1.6), ("EGFR", "growth factor receptor", 2.0)]
downregulated = [("TP53", "tumor suppressor", -1.7), ("BRCA1", "DNA repair", -2.0), ("CDH1", "cell adhesion", -1.6), ("PTEN", "tumor suppressor", -1.8)]

print("Cancer vs Normal: Expression Dashboard")
print(f"\nUpregulated: {', '.join(f'{g}({fc:+.1f})' for g, _, fc in upregulated)}")
print(f"Downregulated: {', '.join(f'{g}({fc:+.1f})' for g, _, fc in downregulated)}")

print("\n--- AI: Clinical interpretation and treatment recommendations ---\n")
result = ask_ai(
    "I analyzed gene expression in a cancer tumor vs normal tissue:\n\n"
    "Upregulated (overactive):\n" +
    "\n".join(f"  - {g} (log2FC={fc:+.1f}): {r}" for g, r, fc in upregulated) +
    "\n\nDownregulated (lost/silenced):\n" +
    "\n".join(f"  - {g} (log2FC={fc:+.1f}): {r}" for g, r, fc in downregulated) +
    "\n\nPlease provide:\n"
    "1. What type of cancer might this be? (based on the pattern)\n"
    "2. What pathways are dysregulated?\n"
    "3. Which upregulated genes are druggable? Name specific drugs.\n"
    "4. Could BRCA1 loss make this tumor sensitive to PARP inhibitors?\n"
    "5. What clinical trial would you recommend for this patient?\n\n"
    "Write as if you're a tumor board consultant presenting to oncologists."
)
print(result)

print("\n--- AI: Student reflection questions ---\n")
result = ask_ai(
    "For a bioinformatics student who just completed this capstone:\n"
    "1. What was the most important bioinformatics skill used in this analysis?\n"
    "2. If you could only use ONE tool for cancer genomics, what would it be?\n"
    "3. How will AI change cancer diagnosis in the next 10 years?\n"
    "4. What ethical considerations arise from genomic testing?\n\n"
    "Write as discussion questions for a class seminar."
)
print(result)
```

The AI acts as a tumor board consultant: it identifies the likely cancer type, names druggable targets, recommends drugs and clinical trials, and poses discussion questions.

> [!NOTE]
> The AI version always includes the same core logic as the vanilla version. The AI calls are added at the end, so you can compare the two approaches side by side.

## Chapter Summary

This chapter covered capstone projects that integrate skills from every chapter into complete bioinformatics analyses.

The vanilla scripts gave you hands-on experience with the core techniques. The AI scripts showed how LLMs can interpret, explain, and extend your analysis. Together, they prepare you for real-world bioinformatics work where code and AI work side by side.
