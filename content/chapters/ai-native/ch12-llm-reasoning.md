---
title: "Chapter 12: LLM Reasoning for Bioinformatics"
type: "chapter"
weight: 12
---

Large language models can reason about biological data in ways that traditional code cannot. This chapter explores how LLMs can search databases, extract structured information, and build knowledge bases.

You will learn to access biological APIs programmatically, extract structured data from unstructured text, and integrate information from multiple sources. These skills bridge the gap between data and knowledge.

LLMs do not replace bioinformatics tools. They augment them. The code in this chapter shows how to combine traditional data access with AI reasoning.

## Accessing Biological Databases via API

Biological databases (NCBI, UniProt, PDB) provide programmatic access through APIs. This script shows how to query databases and extract structured results.

**Vanilla version** (`ch12_vanilla_01.py`):

```python
#!/usr/bin/env python3


import urllib.request
import json
import xml.etree.ElementTree as ET


def search_pubmed(query: str, max_results: int = 5) -> list:
    """Search PubMed and return PMIDs."""
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    url = f"{base}/esearch.fcgi?db=pubmed&term={query}&retmax={max_results}&retmode=json"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    return data.get("esearchresult", {}).get("idlist", [])


def fetch_abstracts(pmids: list) -> list:
    """Fetch abstracts for a list of PMIDs."""
    if not pmids:
        return []
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    ids = ",".join(pmids)
    url = f"{base}/efetch.fcgi?db=pubmed&id={ids}&retmode=xml"
    response = urllib.request.urlopen(url)
    xml_data = response.read().decode()

    # Parse XML
    root = ET.fromstring(xml_data)
    abstracts = []
    for article in root.findall(".//PubmedArticle"):
        title = article.findtext(".//ArticleTitle", "No title")
        abstract = article.findtext(".//AbstractText", "No abstract")
        pmid = article.findtext(".//PMID", "Unknown")
        abstracts.append({"pmid": pmid, "title": title, "abstract": abstract[:200]})
    return abstracts


# --- Main program ---
gene = "BRCA1"
query = f"{gene}+AND+cancer+AND+therapy"

print(f"Searching PubMed for: {gene} cancer therapy")
print(f"Query: {query}\n")

pmids = search_pubmed(query, max_results=5)
print(f"Found {len(pmids)} results: {pmids}")

if pmids:
    print(f"\nFetching abstracts...")
    abstracts = fetch_abstracts(pmids)

    for i, ab in enumerate(abstracts, 1):
        print(f"\n--- Result {i} (PMID: {ab['pmid']}) ---")
        print(f"Title: {ab['title']}")
        print(f"Abstract: {ab['abstract']}...")
```

We used Python to send structured queries to biological databases, parsed JSON responses, and extracted relevant fields. API access is how bioinformaticians automate data retrieval.

**AI version** (`ch12_ai_01.py`):

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

# Simulated PubMed results for BRCA1 cancer therapy
papers = [
    {"pmid": "12345678", "title": "BRCA1 mutations and PARP inhibitor sensitivity in breast cancer", "year": 2023},
    {"pmid": "12345679", "title": "Targeting BRCA1-deficient tumors with platinum chemotherapy", "year": 2022},
    {"pmid": "12345680", "title": "BRCA1 as a biomarker for immunotherapy response", "year": 2024},
]

print(f"PubMed search: BRCA1 cancer therapy")
print(f"Found {len(papers)} recent papers:")
for p in papers:
    print(f"  [{p['year']}] {p['title']} (PMID: {p['pmid']})")

print("\n--- AI: Summarize this research area ---\n")
paper_text = "\n".join(f"  [{p['year']}] {p['title']}" for p in papers)
result = ask_ai(
    f"I searched PubMed for 'BRCA1 cancer therapy' and found these papers:\n{paper_text}\n\n"
    "Please:\n"
    "1. Write a 3-sentence summary of this research area\n"
    "2. What is the main therapeutic strategy for BRCA1-mutant cancers?\n"
    "3. What are PARP inhibitors and how do they work?\n"
    "4. What are the open questions in this field?\n"
    "5. Suggest 3 follow-up search queries to explore further\n\n"
    "Write like a review article introduction -- concise and authoritative."
)
print(result)
```

The AI helps interpret the results: what the database entries mean, how to cross-reference between databases, and what follow-up queries would be useful.

::: {.callout-tip}
You can run any vanilla script without an API key. The AI scripts will print a message and run in offline mode if no key is set.
:::

## Knowledge Base Construction

A knowledge base integrates information from multiple sources into a queryable structure. This script builds a simple knowledge base from gene data and queries it.

**Vanilla version** (`ch12_vanilla_02.py`):

```python
#!/usr/bin/env python3


# A simple biological knowledge base
KNOWLEDGE_BASE = {
    "BRCA1": {
        "full_name": "Breast Cancer 1",
        "function": "DNA repair, tumor suppression",
        "chromosome": "17q21.31",
        "associated_diseases": ["breast cancer", "ovarian cancer"],
        "drugs": ["Olaparib (PARP inhibitor)", "Cisplatin"],
        "pathway": "Homologous recombination repair"
    },
    "TP53": {
        "full_name": "Tumor Protein p53",
        "function": "Cell cycle regulation, apoptosis",
        "chromosome": "17p13.1",
        "associated_diseases": ["Li-Fraumeni syndrome", "many cancers"],
        "drugs": ["APR-246 (experimental)"],
        "pathway": "p53 signaling pathway"
    },
    "KRAS": {
        "full_name": "Kirsten Rat Sarcoma Viral Oncogene",
        "function": "Signal transduction, cell growth",
        "chromosome": "12p12.1",
        "associated_diseases": ["lung cancer", "pancreatic cancer", "colorectal cancer"],
        "drugs": ["Sotorasib (KRAS G12C inhibitor)"],
        "pathway": "MAPK/ERK signaling pathway"
    }
}


def query_gene(gene: str) -> dict:
    """Look up a gene in the knowledge base."""
    return KNOWLEDGE_BASE.get(gene.upper(), None)


# --- Main program ---
print("Biological Knowledge Base")
print("=" * 40)
print(f"Available genes: {', '.join(KNOWLEDGE_BASE.keys())}\n")

# Query each gene
for gene in KNOWLEDGE_BASE:
    info = query_gene(gene)
    print(f"\n{gene} ({info['full_name']}):")
    print(f"  Function: {info['function']}")
    print(f"  Chromosome: {info['chromosome']}")
    print(f"  Diseases: {', '.join(info['associated_diseases'])}")
    print(f"  Drugs: {', '.join(info['drugs'])}")
    print(f"  Pathway: {info['pathway']}")

# Integration example
print("\n\nDrug-gene interactions:")
for gene, info in KNOWLEDGE_BASE.items():
    for drug in info["drugs"]:
        print(f"  {drug} targets {gene} ({info['pathway']})")
```

We built a knowledge base by combining data from multiple queries, linked genes to functions and diseases, and implemented simple queries over the integrated data.

**AI version** (`ch12_ai_02.py`):

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

upregulated = ["BRCA1", "TP53", "ATM", "CHEK2"]
downregulated = ["KRAS", "MYC", "CDK6"]
print("Differential expression results:")
print(f"  Upregulated: {upregulated}")
print(f"  Downregulated: {downregulated}")

print("\n--- AI: Generate hypotheses from this gene list ---\n")
result = ask_ai(
    f"In a cancer treatment experiment, these genes changed:\n\n"
    f"Upregulated: {', '.join(upregulated)}\n"
    f"Downregulated: {', '.join(downregulated)}\n\n"
    "As a bioinformatics researcher, generate 3 testable hypotheses:\n\n"
    "For each hypothesis:\n"
    "1. State the hypothesis clearly\n"
    "2. Which genes support it?\n"
    "3. What experiment would test it?\n"
    "4. What result would confirm or reject it?\n\n"
    "Also:\n"
    "- Are any of these genes in the same pathway?\n"
    "- Is there a known drug that targets this combination?\n"
    "- What would you search on PubMed next?\n\n"
    "Think like a scientist, explain like a teacher."
)
print(result)
```

The AI generates hypotheses from the knowledge base: what connections exist between genes, diseases, and pathways, and what experiments would test them.

::: {.callout-note}
The AI version always includes the same core logic as the vanilla version. The AI calls are added at the end, so you can compare the two approaches side by side.
:::

## Chapter Summary

This chapter covered LLM reasoning for bioinformatics. API access, data extraction, and knowledge base construction.

The vanilla scripts gave you hands-on experience with the core techniques. The AI scripts showed how LLMs can interpret, explain, and extend your analysis. Together, they prepare you for real-world bioinformatics work where code and AI work side by side.
