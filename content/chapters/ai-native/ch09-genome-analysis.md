---
title: "Chapter 9: Genome Analysis"
type: "chapter"
weight: 9
---

Genome analysis scales everything you have learned to billions of bases. This chapter covers variant calling, mutation classification, and the computational challenges of working with whole genomes.

You will parse VCF files (the standard variant format), classify mutations by their effect on protein coding, and understand the workflow from raw sequencing reads to variant calls.

Genome analysis is where bioinformatics meets public health. Every genetic test, every ancestry report, and every pharmacogenomics decision starts with variant analysis.

## VCF Parsing and Variant Annotation

VCF (Variant Call Format) is the standard format for genetic variants. This script parses VCF files and extracts variant information for downstream analysis.

**Vanilla version** (`ch09_vanilla_01.py`):

```python
#!/usr/bin/env python3


# Sample VCF data (simplified)
vcf_data = """\
##fileformat=VCFv4.2
##source=sample
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
chr1	11856378	rs123456	G	A	99	PASS	DP=50;AF=0.45
chr1	11856424	rs789012	T	C	85	PASS	DP=42;AF=0.38
chr7	55191822	rs1212127	T	G	95	PASS	DP=67;AF=0.52
chr17	41245466	rs80357906	A	G	99	PASS	DP=55;AF=0.01
chr12	25398284	rs121913529	C	T	99	PASS	DP=48;AF=0.02
"""

# Parse VCF
print("Parsing VCF file:\n")
print(f"{'CHROM':8s} {'POS':>10s} {'ID':>12s} {'REF':>4s} {'ALT':>4s} {'QUAL':>5s} {'AF':>6s}")
print("-" * 55)

variants = []
for line in vcf_data.strip().split("\n"):
    if line.startswith("#"):
        continue
    fields = line.split("\t")
    chrom, pos, vid, ref, alt, qual, filt, info = fields
    # Extract allele frequency
    af = 0.0
    for item in info.split(";"):
        if item.startswith("AF="):
            af = float(item.split("=")[1])
    variants.append({"chrom": chrom, "pos": int(pos), "id": vid, "ref": ref, "alt": alt, "qual": int(qual), "af": af})
    print(f"{chrom:8s} {pos:>10s} {vid:>12s} {ref:>4s} {alt:>4s} {qual:>5s} {af:>6.2f}")

# Classify variants
print(f"\nTotal variants: {len(variants)}")

snps = [v for v in variants if len(v["ref"]) == 1 and len(v["alt"]) == 1]
indels = [v for v in variants if len(v["ref"]) != len(v["alt"])]
print(f"SNPs: {len(snps)}")
print(f"Indels: {len(indels)}")

# Common vs rare
common = [v for v in variants if v["af"] > 0.05]
rare = [v for v in variants if v["af"] <= 0.05]
print(f"\nCommon (AF > 5%): {len(common)}")
for v in common:
    print(f"  {v['id']}: {v['ref']}>{v['alt']} AF={v['af']:.2f}")
print(f"Rare (AF <= 5%): {len(rare)}")
for v in rare:
    print(f"  {v['id']}: {v['ref']}>{v['alt']} AF={v['af']:.2f}")
```

We parsed VCF columns (chromosome, position, reference allele, alternate allele, quality), computed simple statistics, and classified variants by type (SNP, indel).

**AI version** (`ch09_ai_01.py`):

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

variants = [
    {"chrom": "chr7", "pos": 55191822, "id": "rs1212127", "ref": "T", "alt": "G", "af": 0.52, "gene": "BRAF"},
    {"chrom": "chr17", "pos": 41245466, "id": "rs80357906", "ref": "A", "alt": "G", "af": 0.01, "gene": "BRCA1"},
    {"chrom": "chr12", "pos": 25398284, "id": "rs121913529", "ref": "C", "alt": "T", "af": 0.02, "gene": "KRAS"},
]

print("Notable variants found:")
for v in variants:
    print(f"  {v['id']}: {v['ref']}>{v['alt']} in {v['gene']} (AF={v['af']:.2f})")

print("\n--- AI: What do these variants mean for health? ---\n")
var_text = "\n".join(f"  {v['id']}: {v['ref']}>{v['alt']} in {v['gene']}, allele frequency={v['af']}" for v in variants)
result = ask_ai(
    f"I found these genetic variants in a patient's genome:\n{var_text}\n\n"
    "Please explain:\n"
    "1. What does each variant do? Are they pathogenic or benign?\n"
    "2. What is the clinical significance of BRCA1 variants?\n"
    "3. What is pharmacogenomics? Could these variants affect drug response?\n"
    "4. How do genetic counselors use this information?\n\n"
    "Be sensitive -- this could be someone's real genetic data."
)
print(result)
```

The AI interprets variants: which ones are likely pathogenic, what the quality scores mean, and how to prioritize variants for clinical follow-up.

::: {.callout-tip}
You can run any vanilla script without an API key. The AI scripts will print a message and run in offline mode if no key is set.
:::

## Mutation Classification

Mutations affect proteins in different ways: missense mutations change one amino acid, nonsense mutations create premature stops, and synonymous mutations do not change the protein at all.

**Vanilla version** (`ch09_vanilla_02.py`):

```python
#!/usr/bin/env python3


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


def annotate_variant(codon: str, position: int, new_base: str) -> str:
    """Predict the effect of a single-base change in a codon."""
    ref_aa = CODON_TABLE.get(codon, "?")
    mutated_codon = codon[:position] + new_base + codon[position + 1:]
    alt_aa = CODON_TABLE.get(mutated_codon, "?")

    if ref_aa == alt_aa:
        return "synonymous"
    elif alt_aa == "*":
        return "nonsense (stop gain)"
    elif ref_aa == "*":
        return "stop loss"
    else:
        return "missense"


# Known pathogenic variants
variants = [
    {"gene": "BRAF", "codon": "GTG", "pos": 0, "alt": "T", "note": "V600E -- most common BRAF mutation in cancer"},
    {"gene": "KRAS", "codon": "GGT", "pos": 1, "alt": "A", "note": "G12D -- common in pancreatic cancer"},
    {"gene": "HBB", "codon": "GAG", "pos": 1, "alt": "T", "note": "E6V -- causes sickle cell disease"},
]

print("Variant annotation:")
print("=" * 60)
for v in variants:
    ref_aa = CODON_TABLE.get(v["codon"], "?")
    effect = annotate_variant(v["codon"], v["pos"], v["alt"])
    mut_codon = v["codon"][:v["pos"]] + v["alt"] + v["codon"][v["pos"] + 1:]
    alt_aa = CODON_TABLE.get(mut_codon, "?")
    print(f"\n  {v['gene']}: {v['codon']}({ref_aa}) -> {mut_codon}({alt_aa})")
    print(f"  Effect: {effect}")
    print(f"  Note: {v['note']}")
```

We built a codon table and classified mutations as missense, nonsense, or synonymous based on how they change the protein sequence.

**AI version** (`ch09_ai_02.py`):

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

variants = [
    {"gene": "BRAF", "change": "V600E", "effect": "missense", "disease": "melanoma"},
    {"gene": "KRAS", "change": "G12D", "effect": "missense", "disease": "pancreatic cancer"},
    {"gene": "HBB", "change": "E6V", "effect": "missense", "disease": "sickle cell disease"},
]

print("Pathogenic variants:")
for v in variants:
    print(f"  {v['gene']} {v['change']}: {v['effect']} -- {v['disease']}")

print("\n--- AI: From mutation to disease mechanism ---\n")
result = ask_ai(
    f"These three mutations all change one amino acid:\n"
    f"  BRAF V600E: valine -> glutamic acid at position 600\n"
    f"  KRAS G12D: glycine -> aspartic acid at position 12\n"
    f"  HBB E6V: glutamic acid -> valine at position 6\n\n"
    "For each mutation:\n"
    "1. How does ONE amino acid change cause disease?\n"
    "2. What is the molecular mechanism?\n"
    "3. Is there a drug that targets this specific mutation?\n"
    "4. How common is this mutation in the population?\n\n"
    "Then explain: why are some single-letter changes devastating "
    "while others have no effect? Use an analogy."
)
print(result)
```

The AI explains the clinical significance of each mutation type: why nonsense mutations are usually more harmful, why some missense mutations are benign, and how to use mutation classification in genetic counseling.

::: {.callout-note}
The AI version always includes the same core logic as the vanilla version. The AI calls are added at the end, so you can compare the two approaches side by side.
:::

## Chapter Summary

This chapter covered genome-scale variant analysis. VCF parsing and mutation classification.

The vanilla scripts gave you hands-on experience with the core techniques. The AI scripts showed how LLMs can interpret, explain, and extend your analysis. Together, they prepare you for real-world bioinformatics work where code and AI work side by side.
