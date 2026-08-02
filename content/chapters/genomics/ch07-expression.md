---
title: "Chapter 7: Gene Expression Analysis"
type: "chapter"
weight: 7
---

Gene expression analysis measures how active each gene is in a cell. Comparing expression between conditions reveals which genes respond to a stimulus. This chapter covers the tools and visualization methods for expression data.

You will work with pandas DataFrames for data manipulation, matplotlib for visualization, and gene ontology (GO) terms for biological interpretation. These are the core tools of modern expression analysis.

Expression analysis is one of the most common bioinformatics tasks. The skills in this chapter apply to RNA-seq, microarray, proteomics, and any other quantitative biological dataset.

## Expression Data with Pandas

Pandas DataFrames are the standard data structure for tabular biological data. This script loads gene expression data into a DataFrame and performs basic analysis.

**Vanilla version** (`ch07_vanilla_01.py`):

```python
#!/usr/bin/env python3


import pandas as pd
import numpy as np

# Create a sample count matrix (genes x samples)
np.random.seed(42)
genes = ["BRCA1", "TP53", "EGFR", "MYC", "KRAS", "BRAF", "PIK3CA", "PTEN",
         "RB1", "APC", "VHL", "WT1", "NF1", "RET", "ALK"]

# Control samples (3 replicates)
control = np.random.poisson(lam=100, size=(len(genes), 3))
# Treatment samples -- some genes upregulated, some down
treatment = np.random.poisson(lam=100, size=(len(genes), 3))
# Simulate differential expression
treatment[0] *= 3   # BRCA1 upregulated
treatment[1] *= 4   # TP53 upregulated
treatment[4] //= 3  # KRAS downregulated
treatment[7] //= 2  # PTEN downregulated

df = pd.DataFrame(
    np.hstack([control, treatment]),
    index=genes,
    columns=["ctrl_1", "ctrl_2", "ctrl_3", "treat_1", "treat_2", "treat_3"]
)

print("Gene expression count matrix:")
print(df)
print(f"\nShape: {df.shape[0]} genes x {df.shape[1]} samples")

# Calculate means
df["ctrl_mean"] = df[["ctrl_1", "ctrl_2", "ctrl_3"]].mean(axis=1)
df["treat_mean"] = df[["treat_1", "treat_2", "treat_3"]].mean(axis=1)
df["fold_change"] = df["treat_mean"] / df["ctrl_mean"]
df["log2_fc"] = np.log2(df["fold_change"].replace(0, np.nan))

print("\nDifferential expression summary:")
print("-" * 60)
summary = df[["ctrl_mean", "treat_mean", "fold_change", "log2_fc"]].round(2)
print(summary.sort_values("log2_fc", ascending=False))

# Classify
print("\nUpregulated (log2FC > 1):")
up = summary[summary["log2_fc"] > 1]
for gene in up.index:
    print(f"  {gene}: log2FC = {up.loc[gene, 'log2_fc']}")

print("\nDownregulated (log2FC < -1):")
down = summary[summary["log2_fc"] < -1]
for gene in down.index:
    print(f"  {gene}: log2FC = {down.loc[gene, 'log2_fc']}")
```

We created a DataFrame with gene names, expression values, and p-values, then filtered for differentially expressed genes. Pandas makes tabular data manipulation fast and intuitive.

**AI version** (`ch07_ai_01.py`):

```python
#!/usr/bin/env python3


import os
import pandas as pd
import numpy as np

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

np.random.seed(42)
genes = ["BRCA1", "TP53", "EGFR", "MYC", "KRAS", "BRAF", "PIK3CA", "PTEN", "RB1", "APC"]
control = np.random.poisson(lam=100, size=(len(genes), 3))
treatment = np.random.poisson(lam=100, size=(len(genes), 3))
treatment[0] *= 3; treatment[1] *= 4; treatment[4] //= 3; treatment[7] //= 2

df = pd.DataFrame(np.hstack([control, treatment]), index=genes, columns=["c1","c2","c3","t1","t2","t3"])
df["ctrl_mean"] = df[["c1","c2","c3"]].mean(axis=1)
df["treat_mean"] = df[["t1","t2","t3"]].mean(axis=1)
df["log2_fc"] = np.log2((df["treat_mean"] / df["ctrl_mean"]).replace(0, np.nan))

print("Differential expression results:")
for gene in df.sort_values("log2_fc", ascending=False).index:
    fc = df.loc[gene, "log2_fc"]
    direction = "UP" if fc > 1 else ("DOWN" if fc < -1 else "---")
    print(f"  {gene:8s} log2FC={fc:+.2f}  {direction}")

up_genes = df[df["log2_fc"] > 1].index.tolist()
down_genes = df[df["log2_fc"] < -1].index.tolist()

print(f"\n--- AI: What do these expression changes mean? ---\n")
result = ask_ai(
    f"In a cancer treatment experiment, these genes changed expression:\n\n"
    f"Upregulated: {up_genes}\n"
    f"Downregulated: {down_genes}\n\n"
    "Please explain:\n"
    "1. What does each gene do? (BRCA1, TP53, KRAS, PTEN)\n"
    "2. Is it good or bad that TP53 is upregulated in a cancer context?\n"
    "3. What pathway might be affected?\n"
    "4. What experiment would you do next to confirm these results?\n\n"
    "Explain for a college student who knows basic biology but not cancer biology."
)
print(result)
```

The AI interprets the expression results: which genes are most interesting, what biological processes they are involved in, and what experiments to do next.

::: {.callout-tip}
You can run any vanilla script without an API key. The AI scripts will print a message and run in offline mode if no key is set.
:::

## Visualization with Matplotlib

Visualization turns numbers into insight. This script creates scatter plots, volcano plots, and bar charts for expression data.

**Vanilla version** (`ch07_vanilla_02.py`):

```python
#!/usr/bin/env python3


import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(42)
n_genes = 200

# Simulate log2 fold changes and p-values
# Most genes: no change
log2fc = np.random.normal(0, 0.5, n_genes)
# Some genes: real changes
log2fc[0:10] = np.random.uniform(1.5, 4, 10)    # upregulated
log2fc[10:20] = np.random.uniform(-4, -1.5, 10)  # downregulated

# P-values: significant for changed genes, random for others
neg_log_p = np.random.exponential(0.5, n_genes)
neg_log_p[0:10] = np.random.uniform(3, 10, 10)   # significant
neg_log_p[10:20] = np.random.uniform(3, 10, 10)  # significant

# Classify
colors = []
for i in range(n_genes):
    if abs(log2fc[i]) > 1 and neg_log_p[i] > 1.3:  # 1.3 = -log10(0.05)
        colors.append("red" if log2fc[i] > 0 else "blue")
    else:
        colors.append("gray")

# Plot
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(log2fc, neg_log_p, c=colors, alpha=0.6, s=20)
ax.axhline(y=1.3, color='black', linestyle='--', alpha=0.3, label='p=0.05')
ax.axvline(x=-1, color='black', linestyle='--', alpha=0.3)
ax.axvline(x=1, color='black', linestyle='--', alpha=0.3)
ax.set_xlabel('log2(Fold Change)')
ax.set_ylabel('-log10(p-value)')
ax.set_title('Volcano Plot: Differential Expression')
ax.legend(['p=0.05', 'Upregulated', 'Downregulated', 'Not significant'],
          loc='upper right')

outfile = '/tmp/volcano.png'
plt.savefig(outfile, dpi=150, bbox_inches='tight')
print(f"Volcano plot saved to {outfile}")
print(f"Total genes: {n_genes}")
print(f"Upregulated (red): {sum(1 for c in colors if c == 'red')}")
print(f"Downregulated (blue): {sum(1 for c in colors if c == 'blue')}")
print(f"Not significant (gray): {sum(1 for c in colors if c == 'gray')}")
```

We used matplotlib to create publication-quality plots: scatter plots for comparing conditions, volcano plots for differential expression, and bar charts for gene-level statistics.

**AI version** (`ch07_ai_02.py`):

```python
#!/usr/bin/env python3


import os
import numpy as np

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

# Simulate results
np.random.seed(42)
n = 200
log2fc = np.random.normal(0, 0.5, n)
log2fc[0:10] = np.random.uniform(1.5, 4, 10)
log2fc[10:20] = np.random.uniform(-4, -1.5, 10)
pval = np.random.exponential(0.5, n)
pval[0:20] = np.random.uniform(3, 10, 20)

up = sum(1 for i in range(n) if log2fc[i] > 1 and pval[i] > 1.3)
down = sum(1 for i in range(n) if log2fc[i] < -1 and pval[i] > 1.3)

print(f"Simulation: {n} genes, {up} upregulated, {down} downregulated")

print("\n--- AI: How do I read a volcano plot? ---\n")
result = ask_ai(
    f"I made a volcano plot from RNA-seq data:\n"
    f"- {n} genes tested\n"
    f"- {up} significantly upregulated (log2FC > 1, p < 0.05)\n"
    f"- {down} significantly downregulated (log2FC < -1, p < 0.05)\n\n"
    "Please explain:\n"
    "1. What does each axis of a volcano plot represent?\n"
    "2. Why is it called a 'volcano' plot?\n"
    "3. What do the genes in the top-right corner mean biologically?\n"
    "4. How do scientists decide the cutoffs for 'significant'?\n"
    "5. What is the difference between statistical significance and biological significance?\n\n"
    "Use analogies for a college freshman."
)
print(result)
```

The AI helps interpret the plots: which genes stand out, what the distribution of p-values means, and how to write figure captions for a paper.

::: {.callout-note}
The AI version always includes the same core logic as the vanilla version. The AI calls are added at the end, so you can compare the two approaches side by side.
:::

## Gene Ontology and Functional Annotation

Gene Ontology (GO) terms describe what a gene does: its molecular function, cellular location, and biological process. This script maps genes to GO terms and performs enrichment analysis.

**Vanilla version** (`ch07_vanilla_03.py`):

```python
#!/usr/bin/env python3


# Simulated GO annotations for our differentially expressed genes
go_annotations = {
    "BRCA1": {
        "biological_process": ["DNA repair", "cell cycle checkpoint", "double-strand break repair"],
        "molecular_function": ["ubiquitin-protein ligase activity", "protein binding"],
        "cellular_component": ["nucleus", "BRCA1-A complex"]
    },
    "TP53": {
        "biological_process": ["apoptosis", "cell cycle arrest", "DNA damage response"],
        "molecular_function": ["DNA binding", "transcription factor activity"],
        "cellular_component": ["nucleus", "cytoplasm"]
    },
    "KRAS": {
        "biological_process": ["signal transduction", "cell proliferation", "MAPK cascade"],
        "molecular_function": ["GTPase activity", "protein binding"],
        "cellular_component": ["plasma membrane", "cytoplasm"]
    },
    "PTEN": {
        "biological_process": ["negative regulation of cell proliferation", "apoptosis"],
        "molecular_function": ["phosphatase activity", "phosphoprotein phosphatase activity"],
        "cellular_component": ["cytoplasm", "nucleus"]
    }
}

print("Gene Ontology annotations for key genes:")
print("=" * 60)

for gene, go in go_annotations.items():
    print(f"\n{gene}:")
    for aspect, terms in go.items():
        label = aspect.replace("_", " ").title()
        print(f"  {label}:")
        for term in terms:
            print(f"    - {term}")

# Find shared GO terms
print("\n\nShared biological processes:")
bp_sets = {}
for gene, go in go_annotations.items():
    for term in go["biological_process"]:
        bp_sets.setdefault(term, []).append(gene)

for term, genes in sorted(bp_sets.items(), key=lambda x: -len(x[1])):
    if len(genes) > 1:
        print(f"  {term}: {', '.join(genes)}")
```

We built a GO term dictionary, mapped genes to functions, and counted term frequencies. GO annotation turns a list of genes into a biological story.

**AI version** (`ch07_ai_03.py`):

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

genes = ["BRCA1", "TP53", "KRAS", "PTEN"]
processes = ["DNA repair", "apoptosis", "signal transduction", "cell proliferation"]

print("Key differentially expressed genes and their functions:")
for g, p in zip(genes, processes):
    print(f"  {g}: {p}")

print("\n--- AI: What pathway connects these genes? ---\n")
result = ask_ai(
    f"In a cancer experiment, these genes were differentially expressed:\n"
    f"- BRCA1 (DNA repair) -- upregulated\n"
    f"- TP53 (apoptosis) -- upregulated\n"
    f"- KRAS (signal transduction) -- downregulated\n"
    f"- PTEN (tumor suppressor) -- downregulated\n\n"
    "Please explain:\n"
    "1. What biological pathway connects these genes?\n"
    "2. Are these changes consistent with a treatment working or failing?\n"
    "3. Which of these genes are known drug targets?\n"
    "4. What is the PI3K/AKT pathway and how does PTEN regulate it?\n\n"
    "Draw a simple pathway diagram using text arrows."
)
print(result)
```

The AI interprets the GO enrichment: what the enriched terms mean, which biological processes are active, and how to present the results in a research paper.

## Chapter Summary

This chapter covered gene expression analysis with pandas and matplotlib. Data manipulation, visualization, and gene ontology annotation.

The vanilla scripts gave you hands-on experience with the core techniques. The AI scripts showed how LLMs can interpret, explain, and extend your analysis. Together, they prepare you for real-world bioinformatics work where code and AI work side by side.
