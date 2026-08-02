---
title: "Chapter 8: Protein Structure"
type: "chapter"
weight: 8
---

Protein structure determines function. A protein's three-dimensional shape dictates what it binds, what reactions it catalyzes, and how drugs can target it. This chapter bridges sequence and structure.

You will learn to parse PDB files and use AlphaFold predictions. These skills connect sequence analysis to the physical world of drug design and molecular biology.

Protein structure is where bioinformatics meets biophysics. The code in this chapter is the same logic used by structural biologists at the bench.

## Parsing PDB Files

The Protein Data Bank (PDB) stores 3D structures of proteins. PDB files contain atomic coordinates, and parsing them lets you extract structural information.

**Vanilla version** (`ch08_vanilla_01.py`):

```python
#!/usr/bin/env python3


import os
import urllib.request


def fetch_pdb(pdb_id: str, output_dir: str = "/tmp/pdb") -> str:
    """Download a PDB file from RCSB."""
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"{pdb_id}.pdb")
    if os.path.exists(filename):
        return filename
    url = f"https://files.rcsb.org/download/{pdb_id.upper()}.pdb"
    print(f"Downloading {pdb_id} from RCSB...")
    urllib.request.urlretrieve(url, filename)
    return filename


def parse_pdb_atoms(filename: str) -> list:
    """Extract ATOM records from a PDB file."""
    atoms = []
    with open(filename) as f:
        for line in f:
            if line.startswith("ATOM"):
                atom = {
                    "serial": int(line[6:11]),
                    "name": line[12:16].strip(),
                    "resname": line[17:20].strip(),
                    "chain": line[21],
                    "resseq": int(line[22:26]),
                    "x": float(line[30:38]),
                    "y": float(line[38:46]),
                    "z": float(line[46:54]),
                }
                atoms.append(atom)
    return atoms


def get_chains(atoms: list) -> dict:
    """Group atoms by chain."""
    chains = {}
    for atom in atoms:
        chain = atom["chain"]
        if chain not in chains:
            chains[chain] = []
        chains[chain].append(atom)
    return chains


# --- Main program ---
pdb_id = "1HHO"  # Human oxy-hemoglobin
filename = fetch_pdb(pdb_id)

print(f"PDB file: {filename}")

atoms = parse_pdb_atoms(filename)
print(f"Total atoms: {len(atoms)}")

chains = get_chains(atoms)
print(f"\nChains: {len(chains)}")
for chain_id, chain_atoms in chains.items():
    residues = set(a["resseq"] for a in chain_atoms)
    print(f"  Chain {chain_id}: {len(chain_atoms)} atoms, {len(residues)} residues")

# Show first few atoms
print(f"\nFirst 5 atoms:")
for atom in atoms[:5]:
    print(f"  {atom['serial']:4d} {atom['name']:4s} {atom['resname']:3s} "
          f"{atom['chain']}{atom['resseq']:4d} "
          f"({atom['x']:.1f}, {atom['y']:.1f}, {atom['z']:.1f})")
```

We parsed ATOM records from PDB format, extracted coordinates, and explored the structure of real proteins. The PDB format is fixed-width, so each column has a specific meaning.

**AI version** (`ch08_ai_01.py`):

```python
#!/usr/bin/env python3


import os
import urllib.request

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

def fetch_pdb(pdb_id, out="/tmp/pdb"):
    os.makedirs(out, exist_ok=True)
    fn = os.path.join(out, f"{pdb_id}.pdb")
    if not os.path.exists(fn):
        urllib.request.urlretrieve(f"https://files.rcsb.org/download/{pdb_id.upper()}.pdb", fn)
    return fn

def parse_chains(filename):
    chains = {}
    with open(filename) as f:
        for line in f:
            if line.startswith("ATOM"):
                chain = line[21]
                resname = line[17:20].strip()
                if chain not in chains:
                    chains[chain] = set()
                chains[chain].add(resname)
    return chains

pdb_id = "1HHO"
filename = fetch_pdb(pdb_id)
chains = parse_chains(filename)

print(f"PDB: {pdb_id} (Human oxy-hemoglobin)")
for chain_id, residues in chains.items():
    print(f"  Chain {chain_id}: {len(residues)} unique residues")

print("\n--- AI: What is this protein? ---\n")
result = ask_ai(
    f"I downloaded PDB structure {pdb_id} from RCSB.\n"
    f"It has {len(chains)} chains: {list(chains.keys())}\n\n"
    "Please explain:\n"
    "1. What is hemoglobin? What does it do in the body?\n"
    "2. Why does hemoglobin have multiple chains (subunits)?\n"
    "3. What is the difference between oxy- and deoxy-hemoglobin?\n"
    "4. How does the 3D structure relate to its function?\n"
    "5. What disease is caused by a single amino acid change in hemoglobin?\n\n"
    "Explain for a college freshman."
)
print(result)
```

The AI interprets the structure: what the protein looks like, what its active site contains, and how mutations might affect the 3D shape.

::: {.callout-tip}
You can run any vanilla script without an API key. The AI scripts will print a message and run in offline mode if no key is set.
:::

## AlphaFold and Structure Prediction

AlphaFold predicts 3D structure from amino acid sequence. This script discusses AlphaFold predictions, confidence scores, and how predicted structures are used in research.

**Vanilla version** (`ch08_vanilla_02.py`):

```python
#!/usr/bin/env python3


import os
import urllib.request
import json


def fetch_alphafold(uniprot_id: str, out_dir: str = "/tmp/alphafold") -> dict:
    """Fetch AlphaFold prediction metadata for a protein."""
    os.makedirs(out_dir, exist_ok=True)
    url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"
    try:
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        return data[0] if data else {}
    except Exception as e:
        print(f"Error fetching {uniprot_id}: {e}")
        return {}


def download_pdb(url: str, filename: str) -> str:
    """Download a PDB file."""
    if not os.path.exists(filename):
        urllib.request.urlretrieve(url, filename)
    return filename


# --- Main program ---
# Human hemoglobin beta subunit
uniprot_id = "P68871"

print(f"Fetching AlphaFold prediction for {uniprot_id}...")
info = fetch_alphafold(uniprot_id)

if info:
    print(f"\nProtein: {info.get('uniprotId', 'unknown')}")
    print(f"Gene: {info.get('gene', 'unknown')}")
    print(f"Organism: {info.get('organismScientificName', 'unknown')}")
    print(f"Model confidence URL: {info.get('paeImageUrl', 'N/A')}")

    # Download the predicted structure
    pdb_url = info.get("pdbUrl")
    if pdb_url:
        pdb_file = download_pdb(pdb_url, f"/tmp/alphafold/{uniprot_id}.pdb")
        print(f"\nPredicted structure saved to: {pdb_file}")

        # Parse confidence scores from B-factor column
        confidences = []
        with open(pdb_file) as f:
            for line in f:
                if line.startswith("ATOM") and line[12:16].strip() == "CA":
                    bfactor = float(line[60:66])
                    confidences.append(bfactor)

        if confidences:
            avg_conf = sum(confidences) / len(confidences)
            print(f"\nConfidence scores (pLDDT):")
            print(f"  Average: {avg_conf:.1f}")
            print(f"  Min: {min(confidences):.1f}")
            print(f"  Max: {max(confidences):.1f}")

            # Interpret confidence
            high = sum(1 for c in confidences if c > 90)
            good = sum(1 for c in confidences if 70 < c <= 90)
            low = sum(1 for c in confidences if c <= 70)
            print(f"\n  Very high confidence (>90): {high} residues")
            print(f"  High confidence (70-90): {good} residues")
            print(f"  Low confidence (<=70): {low} residues")
else:
    print("Could not fetch AlphaFold data. Check the UniProt ID.")
```

We explored AlphaFold database entries, examined confidence scores (pLDDT), and compared predicted structures to experimental ones.

**AI version** (`ch08_ai_02.py`):

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

# Simulated AlphaFold results for hemoglobin beta
print("AlphaFold prediction: Human Hemoglobin Beta (P68871)")
print(f"  Length: 147 amino acids")
print(f"  Average pLDDT: 92.4 (very high confidence)")
print(f"  High confidence residues: 130/147 (88%)")
print(f"  Low confidence residues: 5/147 (3%)")

print("\n--- AI: How does AlphaFold work? ---\n")
result = ask_ai(
    "AlphaFold predicted the structure of hemoglobin beta with 92.4 average pLDDT.\n\n"
    "Please explain:\n"
    "1. What is AlphaFold and why was it a breakthrough?\n"
    "2. What does pLDDT mean? How should I interpret scores of 90+, 70-90, and <70?\n"
    "3. How is AlphaFold different from X-ray crystallography and cryo-EM?\n"
    "4. What are AlphaFold's limitations? When might it be wrong?\n"
    "5. How has AlphaFold changed drug discovery?\n\n"
    "Explain for a college student who has never heard of protein folding."
)
print(result)
```

The AI explains how AlphaFold works, what confidence scores mean, and how predicted structures are used in drug discovery. It also discusses the limitations of computational prediction.

::: {.callout-note}
The AI version always includes the same core logic as the vanilla version. The AI calls are added at the end, so you can compare the two approaches side by side.
:::

## Chapter Summary

This chapter covered protein structure analysis. Parsing PDB files and understanding AlphaFold predictions.

The vanilla scripts gave you hands-on experience with the core techniques. The AI scripts showed how LLMs can interpret, explain, and extend your analysis. Together, they prepare you for real-world bioinformatics work where code and AI work side by side.
