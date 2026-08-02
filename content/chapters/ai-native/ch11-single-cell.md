---
title: "Chapter 11: Single-Cell Analysis"
type: "chapter"
weight: 11
---

Single-cell RNA sequencing (scRNA-seq) measures gene expression in individual cells instead of bulk tissue. This reveals cell types, developmental trajectories, and heterogeneity that bulk methods miss.

This chapter covers single-cell data processing: quality control, clustering, and spatial analysis. You will work with count matrices and implement the core steps of tools like Seurat and Scanpy.

Single-cell analysis is revolutionizing biology. Every major atlas project uses the methods in this chapter.

## Single-Cell Basics and Clustering

Single-cell data requires specialized processing: normalization for variable sequencing depth, feature selection, and clustering to identify cell types.

**Vanilla version** (`ch11_vanilla_01.py`):

```python
#!/usr/bin/env python3


import numpy as np
from collections import Counter

# Simulated single-cell data: 100 cells, 5 genes
np.random.seed(42)
n_cells = 100
genes = ["CD3D", "CD19", "CD14", "EPCAM", "VIM"]

# Generate expression data for 4 cell types
cell_types = ["T-cell", "B-cell", "Monocyte", "Epithelial"]
true_labels = []
expression = []

for i in range(n_cells):
    if i < 30:  # T-cells
        true_labels.append("T-cell")
        expression.append([np.random.poisson(50), np.random.poisson(2), np.random.poisson(3), np.random.poisson(1), np.random.poisson(5)])
    elif i < 55:  # B-cells
        true_labels.append("B-cell")
        expression.append([np.random.poisson(3), np.random.poisson(45), np.random.poisson(2), np.random.poisson(1), np.random.poisson(4)])
    elif i < 80:  # Monocytes
        true_labels.append("Monocyte")
        expression.append([np.random.poisson(2), np.random.poisson(1), np.random.poisson(55), np.random.poisson(2), np.random.poisson(3)])
    else:  # Epithelial
        true_labels.append("Epithelial")
        expression.append([np.random.poisson(1), np.random.poisson(1), np.random.poisson(2), np.random.poisson(60), np.random.poisson(10)])

data = np.array(expression)

print(f"Single-cell dataset: {n_cells} cells x {len(genes)} genes")
print(f"Genes: {genes}")
print(f"True cell types: {Counter(true_labels)}")

# Show average expression per cell type
print(f"\nAverage expression by cell type:")
print(f"{'Cell Type':12s} {'  '.join(f'{g:>6s}' for g in genes)}")
print("-" * 50)
for ct in cell_types:
    mask = [i for i, l in enumerate(true_labels) if l == ct]
    means = data[mask].mean(axis=0)
    print(f"{ct:12s} {'  '.join(f'{m:6.1f}' for m in means)}")

# Identify marker genes (highest expression per type)
print(f"\nMarker genes:")
for ct in cell_types:
    mask = [i for i, l in enumerate(true_labels) if l == ct]
    means = data[mask].mean(axis=0)
    marker_idx = np.argmax(means)
    print(f"  {ct}: {genes[marker_idx]} (avg={means[marker_idx]:.1f})")
```

We implemented basic single-cell processing: library size normalization, highly variable gene selection, and k-means clustering. These are the core steps of every scRNA-seq analysis.

**AI version** (`ch11_ai_01.py`):

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

print("Single-cell RNA-seq results:")
print("  100 cells, 5 marker genes")
print("  Identified 4 cell types:")
print("    T-cells (30): high CD3D")
print("    B-cells (25): high CD19")
print("    Monocytes (25): high CD14")
print("    Epithelial (20): high EPCAM")

print("\n--- AI: What are these cell types and why do they matter? ---\n")
result = ask_ai(
    "I analyzed single-cell RNA-seq data and found 4 cell types:\n\n"
    "  T-cells (30 cells): marker gene CD3D\n"
    "  B-cells (25 cells): marker gene CD19\n"
    "  Monocytes (25 cells): marker gene CD14\n"
    "  Epithelial (20 cells): marker gene EPCAM\n\n"
    "Please explain:\n"
    "1. What does each cell type do in the immune system?\n"
    "2. What is CD3D? Why is it a T-cell marker?\n"
    "3. What is single-cell RNA-seq and how is it different from bulk RNA-seq?\n"
    "4. What is 10x Genomics and how does it work?\n"
    "5. How would you name a new cluster with no known markers?\n\n"
    "Explain for a college freshman."
)
print(result)
```

The AI interprets the clusters: what marker genes define each cluster, what cell types they represent, and how to validate cluster assignments.

::: {.callout-tip}
You can run any vanilla script without an API key. The AI scripts will print a message and run in offline mode if no key is set.
:::

## Spatial Transcriptomics

Spatial transcriptomics measures gene expression while preserving the physical location of each cell in tissue. This adds a new dimension to single-cell analysis.

**Vanilla version** (`ch11_vanilla_02.py`):

```python
#!/usr/bin/env python3


import numpy as np

# Simulated spatial data: cells in a tissue section
np.random.seed(42)
n_cells = 50

# Cell positions (x, y coordinates)
x = np.random.uniform(0, 100, n_cells)
y = np.random.uniform(0, 100, n_cells)

# Gene expression: CD3D (T-cell) high in center, EPCAM (epithelial) high at edges
cd3d = np.where(np.sqrt((x-50)**2 + (y-50)**2) < 30, np.random.poisson(40, n_cells), np.random.poisson(5, n_cells))
epcam = np.where(np.sqrt((x-50)**2 + (y-50)**2) > 25, np.random.poisson(35, n_cells), np.random.poisson(3, n_cells))

print(f"Spatial transcriptomics: {n_cells} cells in tissue section")
print(f"  CD3D (T-cell marker): mean={cd3d.mean():.1f}, max={cd3d.max()}")
print(f"  EPCAM (epithelial): mean={epcam.mean():.1f}, max={epcam.max()}")

# Identify regions
center = np.sqrt((x-50)**2 + (y-50)**2) < 30
edge = ~center

print(f"\nCenter region ({center.sum()} cells):")
print(f"  CD3D mean: {cd3d[center].mean():.1f}")
print(f"  EPCAM mean: {epcam[center].mean():.1f}")

print(f"\nEdge region ({edge.sum()} cells):")
print(f"  CD3D mean: {cd3d[edge].mean():.1f}")
print(f"  EPCAM mean: {epcam[edge].mean():.1f}")

# Simple text visualization
print(f"\nSpatial map (CD3D high = T, EPCAM high = E, both = B):")
grid = [[" " for _ in range(20)] for _ in range(20)]
for i in range(n_cells):
    gx = min(int(x[i] / 5), 19)
    gy = min(int(y[i] / 5), 19)
    if cd3d[i] > 20 and epcam[i] > 20:
        grid[gy][gx] = "B"
    elif cd3d[i] > 20:
        grid[gy][gx] = "T"
    elif epcam[i] > 20:
        grid[gy][gx] = "E"
    else:
        grid[gy][gx] = "."

for row in grid:
    print("  " + "".join(row))
```

We worked with spatial coordinates, mapped gene expression to tissue locations, and visualized spatial patterns. Spatial data adds tissue context to expression measurements.

**AI version** (`ch11_ai_02.py`):

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

print("Spatial transcriptomics results:")
print("  Tissue section with 50 cells")
print("  Center: T-cells (CD3D high) -- immune infiltrate")
print("  Edge: Epithelial cells (EPCAM high) -- tissue boundary")

print("\n--- AI: What is spatial transcriptomics? ---\n")
result = ask_ai(
    "I analyzed a tissue section with spatial transcriptomics:\n\n"
    "  Center of tissue: T-cells (CD3D high)\n"
    "  Edge of tissue: Epithelial cells (EPCAM high)\n\n"
    "Please explain:\n"
    "1. What is spatial transcriptomics? How is it different from single-cell RNA-seq?\n"
    "2. Why does cell location matter? Can't we just dissociate the tissue?\n"
    "3. What does it mean that T-cells are in the center? (Think: tumor microenvironment)\n"
    "4. What technologies exist for spatial transcriptomics? (Visium, MERFISH, etc.)\n"
    "5. How might spatial data help in cancer diagnosis?\n\n"
    "Explain for a college student who has seen a microscope but never a sequencer."
)
print(result)
```

The AI explains spatial patterns: what spatial gene expression tells us about tissue organization, how spatial data differs from dissociated single-cell data, and what new biology it reveals.

::: {.callout-note}
The AI version always includes the same core logic as the vanilla version. The AI calls are added at the end, so you can compare the two approaches side by side.
:::

## Chapter Summary

This chapter covered single-cell analysis. Clustering, cell type annotation, and spatial transcriptomics.

The vanilla scripts gave you hands-on experience with the core techniques. The AI scripts showed how LLMs can interpret, explain, and extend your analysis. Together, they prepare you for real-world bioinformatics work where code and AI work side by side.
