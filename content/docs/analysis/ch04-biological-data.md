---
title: "Chapter 4: Biological Data"
weight: 4
---

Bioinformatics runs on structured data. Gene annotations, variant calls, protein databases, and sequence alignments all follow specific formats. This chapter teaches you to parse and work with biological data formats.

You will learn to handle GenBank and FASTA formats using BioPython, extract features from sequence records, and write sequences to files. These skills are the bridge between raw data and biological insight.

Every tool in bioinformatics depends on parsing structured data correctly. This chapter gives you that foundation.

## Reading Biological File Formats

BioPython's SeqIO module handles multiple file formats: FASTA, GenBank, and more. This script reads sequences from different formats and extracts key information.

**Vanilla version** (`ch04_vanilla_01.py`):

```python
#!/usr/bin/env python3


from Bio import SeqIO


def parse_genbank(filename: str) -> None:
    """Parse a GenBank file and display its contents."""
    record = SeqIO.read(filename, "genbank")

    # Basic information
    print(f"ID:          {record.id}")
    print(f"Name:        {record.name}")
    print(f"Description: {record.description}")
    print(f"Length:       {len(record.seq)} bases")
    print(f"Molecule:     {record.annotations.get('molecule_type', 'unknown')}")
    print(f"Organism:     {record.annotations.get('organism', 'unknown')}")

    # Sequence
    print(f"\nSequence (first 60 bases):")
    seq_str = str(record.seq)
    for i in range(0, min(60, len(seq_str)), 60):
        print(f"  {seq_str[i:i+60]}")

    # Features
    print(f"\nFeatures ({len(record.features)} total):")
    for feature in record.features[:10]:  # Show first 10
        print(f"  {feature.type}: {feature.location}")
        if "gene" in feature.qualifiers:
            print(f"    Gene: {feature.qualifiers['gene']}")
        if "product" in feature.qualifiers:
            print(f"    Product: {feature.qualifiers['product']}")

    if len(record.features) > 10:
        print(f"  ... and {len(record.features) - 10} more features")

    # References
    print(f"\nReferences ({len(record.annotations.get('references', []))}):")
    for ref in record.annotations.get("references", []):
        print(f"  {ref.title[:80]}..." if ref.title and len(ref.title) > 80 else f"  {ref.title}")


# --- Main program ---
# Use a sample GenBank file if available, otherwise create one
import os
import tempfile

SAMPLE_GENBANK = """\
LOCUS       SAMPLE_SEQ              576 bp    DNA     linear   PRI 01-JAN-2026
DEFINITION  Homo sapiens hemoglobin subunit beta (HBB) partial sequence.
ACCESSION   SAMPLE001
VERSION     SAMPLE001.1
KEYWORDS    .
SOURCE      Homo sapiens
  ORGANISM  Homo sapiens
            Eukaryota; Metazoa; Chordata; Craniata; Vertebrata; Euteleostomi;
            Mammalia; Eutheria; Euarchontoglires; Primates; Haplorrhini;
            Catarrhini; Hominidae; Homo.
FEATURES             Location/Qualifiers
     source          1..576
                     /organism="Homo sapiens"
                     /mol_type="genomic DNA"
     gene            1..576
                     /gene="HBB"
     CDS             1..576
                     /gene="HBB"
                     /product="hemoglobin subunit beta"
                     /translation="MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFES
                     FGDLSTPDAVMGNPKVKAHGKKVLGAFSDGLAHLDNLKGTFATLSELHCDKLHVDPE
                     NFRLLGNVLVCVLAHHFGKEFTPPVQAAYQKVVAGVANALAHKYH"
ORIGIN
        1 atggtgcatc tgactcctga ggagaagtct gccgttactg ccctgtgggg caaggtgaac
       61 gtggatgaag ttggtggtga ggccctgggc aggctgctgg tggtctaccc ttggacccag
      121 aggttctttg agtcctttgg ggatctgtcc actcctgatg ctgttatggg caaccctaag
      181 gtgaaggctc atggcaagaa agtgctcggt gcctttagtg atggcctggc tcacctggac
      241 aacctcaagg gcacctttgc cacactgagt gagctgcact gtgacaagct gcacgtggat
      301 cctgagaact tcagggagcc tctgccatgc tggatacatt catcacccag aatccaggac
      361 tccagccttc tgggcatcat tctgaccctc agctgcctcc aggtcctctg cttgagcttc
      421 cctttctgtt tcctgtccaa tctgctccca cccatggcta ttgagacact cttgttccct
      481 cctctgctga tgtggaagct gaaggtgctg gacttcatca cctttgccaa cctgctgggt
      541 gccctgtgga tgaactatgg caagaacttc atgacc
//
"""

# Write sample file
sample_file = os.path.join(tempfile.gettempdir(), "sample.gb")
with open(sample_file, "w") as f:
    f.write(SAMPLE_GENBANK)

print(f"Parsing sample GenBank file: {sample_file}\n")
parse_genbank(sample_file)

# Clean up
os.remove(sample_file)
```

We used Bio.SeqIO to parse sequences, access record attributes (id, description, seq), and handle different file formats with the same API.

**AI version** (`ch04_ai_01.py`):

```python
#!/usr/bin/env python3


import os
import tempfile
from Bio import SeqIO

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


SAMPLE_GENBANK = """\
LOCUS       SAMPLE_SEQ              576 bp    DNA     linear   PRI 01-JAN-2026
DEFINITION  Homo sapiens hemoglobin subunit beta (HBB) partial sequence.
ACCESSION   SAMPLE001
VERSION     SAMPLE001.1
KEYWORDS    .
SOURCE      Homo sapiens
  ORGANISM  Homo sapiens
            Eukaryota; Metazoa; Chordata; Craniata; Vertebrata; Euteleostomi;
            Mammalia; Eutheria; Euarchontoglires; Primates; Haplorrhini;
            Catarrhini; Hominidae; Homo.
FEATURES             Location/Qualifiers
     source          1..576
                     /organism="Homo sapiens"
                     /mol_type="genomic DNA"
     gene            1..576
                     /gene="HBB"
     CDS             1..576
                     /gene="HBB"
                     /product="hemoglobin subunit beta"
                     /translation="MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFES
                     FGDLSTPDAVMGNPKVKAHGKKVLGAFSDGLAHLDNLKGTFATLSELHCDKLHVDPE
                     NFRLLGNVLVCVLAHHFGKEFTPPVQAAYQKVVAGVANALAHKYH"
ORIGIN
        1 atggtgcatc tgactcctga ggagaagtct gccgttactg ccctgtgggg caaggtgaac
       61 gtggatgaag ttggtggtga ggccctgggc aggctgctgg tggtctaccc ttggacccag
      121 aggttctttg agtcctttgg ggatctgtcc actcctgatg ctgttatggg caaccctaag
      181 gtgaaggctc atggcaagaa agtgctcggt gcctttagtg atggcctggc tcacctggac
      241 aacctcaagg gcacctttgc cacactgagt gagctgcact gtgacaagct gcacgtggat
      301 cctgagaact tcagggagcc tctgccatgc tggatacatt catcacccag aatccaggac
      361 tccagccttc tgggcatcat tctgaccctc agctgcctcc aggtcctctg cttgagcttc
      421 cctttctgtt tcctgtccaa tctgctccca cccatggcta ttgagacact cttgttccct
      481 cctctgctga tgtggaagct gaaggtgctg gacttcatca cctttgccaa cctgctgggt
      541 gccctgtgga tgaactatgg caagaacttc atgacc
//
"""

# Write sample file
sample_file = os.path.join(tempfile.gettempdir(), "sample.gb")
with open(sample_file, "w") as f:
    f.write(SAMPLE_GENBANK)

# Parse with BioPython
record = SeqIO.read(sample_file, "genbank")
os.remove(sample_file)

# Display basics (same as vanilla)
print(f"ID:          {record.id}")
print(f"Description: {record.description}")
print(f"Length:       {len(record.seq)} bases")
print(f"Organism:     {record.annotations.get('organism', 'unknown')}")
print(f"Features:     {len(record.features)}")

# Collect feature summary for AI
feature_summary = []
for f in record.features:
    info = f"  {f.type}: {f.location}"
    if "gene" in f.qualifiers:
        info += f" (gene={f.qualifiers['gene'][0]})"
    if "product" in f.qualifiers:
        info += f" (product={f.qualifiers['product'][0]})"
    feature_summary.append(info)

features_text = "\n".join(feature_summary)

# --- AI: Explain the GenBank record ---
print("\n--- AI: What does this GenBank record tell us? ---\n")

result = ask_ai(
    f"I parsed a GenBank record for a DNA sequence. Here's the summary:\n\n"
    f"ID: {record.id}\n"
    f"Description: {record.description}\n"
    f"Organism: {record.annotations.get('organism', 'unknown')}\n"
    f"Length: {len(record.seq)} bases\n\n"
    f"Features:\n{features_text}\n\n"
    "Please explain for a college student:\n"
    "1. What is a GenBank record? Why do scientists submit sequences to it?\n"
    "2. What does each feature type mean (source, gene, CDS)?\n"
    "3. What is hemoglobin subunit beta, and why is it important?\n"
    "4. The CDS has a /translation qualifier. Why is that useful?\n\n"
    "Keep it brief and use analogies where possible."
)
print(result)

# --- AI: Downstream analysis suggestions ---
print("\n--- AI: What should we do next with this sequence? ---\n")

result = ask_ai(
    f"I have a GenBank record for human hemoglobin beta ({len(record.seq)} bases).\n"
    f"The protein sequence is:\n{record.features[-1].qualifiers.get('translation', [''])[0]}\n\n"
    "As a bioinformatics instructor, suggest 3 analyses a student could do next:\n"
    "1. A simple analysis they could do in 5 minutes\n"
    "2. A medium-difficulty analysis for a homework assignment\n"
    "3. A challenging analysis for a class project\n\n"
    "For each, name the tool or database they would use."
)
print(result)
```

The AI interprets the parsed records: what the accession numbers mean, what organisms the sequences come from, and how to navigate between formats.

> [!TIP]
> You can run any vanilla script without an API key. The AI scripts will print a message and run in offline mode if no key is set.

## GenBank Records and Feature Extraction

GenBank records contain rich annotation: gene names, features, qualifiers, and references. This script parses GenBank records and extracts biological features.

**Vanilla version** (`ch04_vanilla_02.py`):

```python
#!/usr/bin/env python3


import os
import tempfile
from Bio import SeqIO

SAMPLE_GENBANK = """\
LOCUS       HBB_GENE                576 bp    DNA     linear   PRI 01-JAN-2026
DEFINITION  Homo sapiens hemoglobin subunit beta (HBB) partial sequence.
ACCESSION   SAMPLE001
SOURCE      Homo sapiens
  ORGANISM  Homo sapiens
            Eukaryota; Metazoa; Chordata; Craniata; Vertebrata; Euteleostomi;
            Mammalia; Eutheria; Primates; Haplorrhini; Hominidae; Homo.
FEATURES             Location/Qualifiers
     source          1..576
                     /organism="Homo sapiens"
                     /mol_type="genomic DNA"
     gene            1..576
                     /gene="HBB"
     CDS             1..576
                     /gene="HBB"
                     /product="hemoglobin subunit beta"
ORIGIN
        1 atggtgcatc tgactcctga ggagaagtct gccgttactg ccctgtgggg caaggtgaac
       61 gtggatgaag ttggtggtga ggccctgggc aggctgctgg tggtctaccc ttggacccag
      121 aggttctttg agtcctttgg ggatctgtcc actcctgatg ctgttatggg caaccctaag
      181 gtgaaggctc atggcaagaa agtgctcggt gcctttagtg atggcctggc tcacctggac
      241 aacctcaagg gcacctttgc cacactgagt gagctgcact gtgacaagct gcacgtggat
      301 cctgagaact tcagggagcc tctgccatgc tggatacatt catcacccag aatccaggac
      361 tccagccttc tgggcatcat tctgaccctc agctgcctcc aggtcctctg cttgagcttc
      421 cctttctgtt tcctgtccaa tctgctccca cccatggcta ttgagacact cttgttccct
      481 cctctgctga tgtggaagct gaaggtgctg gacttcatca cctttgccaa cctgctgggt
      541 gccctgtgga tgaactatgg caagaacttc atgacc
//
"""

sample_file = os.path.join(tempfile.gettempdir(), "hbb.gb")
with open(sample_file, "w") as f:
    f.write(SAMPLE_GENBANK)

record = SeqIO.read(sample_file, "genbank")
os.remove(sample_file)

# Show the full annotation
print("=== ANNOTATION ===")
print(f"ID: {record.id}")
print(f"Description: {record.description}")
print(f"Organism: {record.annotations.get('organism', 'unknown')}")
print(f"Topology: {record.annotations.get('topology', 'unknown')}")

# Show each feature with its qualifiers
print("\n=== FEATURES ===")
for feature in record.features:
    print(f"\n  Type: {feature.type}")
    print(f"  Location: {feature.location}")
    for key, values in feature.qualifiers.items():
        for val in values:
            print(f"    {key}: {val}")

# Show the raw sequence
print(f"\n=== SEQUENCE ({len(record.seq)} bp) ===")
seq = str(record.seq)
for i in range(0, len(seq), 60):
    print(f"  {i+1:4d} {seq[i:i+60]}")
```

We accessed SeqRecord features, extracted CDS and gene annotations, and used qualifier dictionaries to get gene names and protein products.

**AI version** (`ch04_ai_02.py`):

```python
#!/usr/bin/env python3


import os
import tempfile
from Bio import SeqIO

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

SAMPLE_GENBANK = """\
LOCUS       HBB_GENE                576 bp    DNA     linear   PRI 01-JAN-2026
DEFINITION  Homo sapiens hemoglobin subunit beta (HBB) partial sequence.
ACCESSION   SAMPLE001
SOURCE      Homo sapiens
  ORGANISM  Homo sapiens
            Eukaryota; Metazoa; Chordata; Craniata; Vertebrata; Euteleostomi;
            Mammalia; Eutheria; Primates; Haplorrhini; Hominidae; Homo.
FEATURES             Location/Qualifiers
     source          1..576
                     /organism="Homo sapiens"
     gene            1..576
                     /gene="HBB"
     CDS             1..576
                     /gene="HBB"
                     /product="hemoglobin subunit beta"
ORIGIN
        1 atggtgcatc tgactcctga ggagaagtct gccgttactg ccctgtgggg caaggtgaac
       61 gtggatgaag ttggtggtga ggccctgggc aggctgctgg tggtctaccc ttggacccag
      121 aggttctttg agtcctttgg ggatctgtcc actcctgatg ctgttatggg caaccctaag
      181 gtgaaggctc atggcaagaa agtgctcggt gcctttagtg atggcctggc tcacctggac
      241 aacctcaagg gcacctttgc cacactgagt gagctgcact gtgacaagct gcacgtggat
      301 cctgagaact tcagggagcc tctgccatgc tggatacatt catcacccag aatccaggac
      361 tccagccttc tgggcatcat tctgaccctc agctgcctcc aggtcctctg cttgagcttc
      421 cctttctgtt tcctgtccaa tctgctccca cccatggcta ttgagacact cttgttccct
      481 cctctgctga tgtggaagct gaaggtgctg gacttcatca cctttgccaa cctgctgggt
      541 gccctgtgga tgaactatgg caagaacttc atgacc
//
"""

sample_file = os.path.join(tempfile.gettempdir(), "hbb.gb")
with open(sample_file, "w") as f:
    f.write(SAMPLE_GENBANK)
record = SeqIO.read(sample_file, "genbank")
os.remove(sample_file)

print(f"Parsed: {record.id} -- {record.description}")
print(f"Features: {len(record.features)}")

# Build feature summary
feature_text = ""
for f in record.features:
    feature_text += f"  {f.type}: {f.location}\n"
    for k, v in f.qualifiers.items():
        feature_text += f"    {k}: {v[0]}\n"

print("\n--- AI: What do these GenBank features mean? ---\n")
result = ask_ai(
    f"A GenBank record for {record.id} has these features:\n\n{feature_text}\n"
    "Explain for a college student:\n"
    "1. What is the difference between 'source', 'gene', and 'CDS' features?\n"
    "2. What does /mol_type='genomic DNA' tell us?\n"
    "3. Why is the CDS feature important? What would happen if it were wrong?\n"
    "4. How do scientists verify that a GenBank annotation is correct?\n\n"
    "Use the analogy of a library catalog entry."
)
print(result)
```

The AI explains the biological significance of GenBank features: what CDS regions mean, how gene annotations work, and what the qualifiers tell us about function.

> [!NOTE]
> The AI version always includes the same core logic as the vanilla version. The AI calls are added at the end, so you can compare the two approaches side by side.

## Writing Sequences and Format Conversion

Converting between formats and writing output files is a core bioinformatics task. This script writes sequences to FASTA and performs format conversion.

**Vanilla version** (`ch04_vanilla_03.py`):

```python
#!/usr/bin/env python3


from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq

# Create sequence records
sequences = [
    SeqRecord(Seq("ATGGTGCATCTGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTGAAC"),
              id="seq001", description="hemoglobin beta fragment 1"),
    SeqRecord(Seq("GTGGATGAAGTTGGTGGTGAGGCCCTGGGCAGGCTGCTGGTGGTCTACCCTTGGACCCAG"),
              id="seq002", description="hemoglobin beta fragment 2"),
    SeqRecord(Seq("AGGTTCTTTGAGTCCTTTGGGGATCTGTCCACTCCTGATGCTGTTATGGGCAACCCTAAG"),
              id="seq003", description="hemoglobin beta fragment 3"),
]

# Write to stdout in FASTA format
from Bio import SeqIO
import sys

print("=== FASTA output ===")
SeqIO.write(sequences, sys.stdout, "fasta")

# Write to file
output_file = "/tmp/output.fasta"
count = SeqIO.write(sequences, output_file, "fasta")
print(f"\nWrote {count} sequences to {output_file}")

# Read it back to verify
print("\n=== Read back ===")
for record in SeqIO.parse(output_file, "fasta"):
    print(f"{record.id}: {record.seq[:30]}... ({len(record.seq)} bp)")

import os
os.remove(output_file)
```

We used Bio.SeqIO.write() to output sequences and built a simple format converter. Writing clean output files is as important as reading input.

**AI version** (`ch04_ai_03.py`):

```python
#!/usr/bin/env python3


import os
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from Bio import SeqIO

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

sequences = [
    SeqRecord(Seq("ATGGTGCATCTGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTGAAC"), id="seq001", description="hemoglobin beta fragment 1"),
    SeqRecord(Seq("GTGGATGAAGTTGGTGGTGAGGCCCTGGGCAGGCTGCTGGTGGTCTACCCTTGGACCCAG"), id="seq002", description="hemoglobin beta fragment 2"),
    SeqRecord(Seq("AGGTTCTTTGAGTCCTTTGGGGATCTGTCCACTCCTGATGCTGTTATGGGCAACCCTAAG"), id="seq003", description="hemoglobin beta fragment 3"),
]

output_file = "/tmp/output.fasta"
SeqIO.write(sequences, output_file, "fasta")
print(f"Wrote {len(sequences)} sequences to {output_file}")

seq_text = "\n".join(f"  {r.id}: {r.seq}" for r in sequences)

print("\n--- AI: What can we do with these sequences? ---\n")
result = ask_ai(
    f"I wrote {len(sequences)} DNA sequences to a FASTA file:\n{seq_text}\n\n"
    "As a bioinformatics instructor, suggest:\n"
    "1. What experiments could a student design with these sequences?\n"
    "2. What databases should they search? (BLAST, Ensembl, etc.)\n"
    "3. If these are fragments of the same gene, what's the next step to assemble them?\n\n"
    "Give 3 concrete next steps a freshman could follow."
)
print(result)
os.remove(output_file)
```

The AI discusses format choices: when to use FASTA vs. GenBank, what information is lost in conversion, and best practices for data management.

## Chapter Summary

This chapter covered biological data formats and BioPython. Parsing GenBank, extracting features, and writing sequences to files.

The vanilla scripts gave you hands-on experience with the core techniques. The AI scripts showed how LLMs can interpret, explain, and extend your analysis. Together, they prepare you for real-world bioinformatics work where code and AI work side by side.
