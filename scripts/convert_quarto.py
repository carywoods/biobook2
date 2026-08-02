#!/usr/bin/env python3
"""Convert Quarto (.qmd) files to Hugo-compatible markdown (.md)."""

import os
import re
from pathlib import Path


def convert_qmd_to_md(qmd_path: str, md_path: str):
    """Convert a single QMD file to MD format for Hugo."""
    
    with open(qmd_path, 'r') as f:
        content = f.read()
    
    # Extract YAML front matter (between --- markers)
    yaml_match = re.search(r'^---\n(.*?)---\n', content, re.DOTALL)
    yaml_front_matter = {}
    if yaml_match:
        yaml_text = yaml_match.group(1)
        # Parse simple key-value pairs from YAML
        for line in yaml_text.split('\n'):
            if ':' in line and not line.strip().startswith('#'):
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip().strip('"')
                    yaml_front_matter[key] = value
        
        # Remove front matter from content
        content = content[yaml_match.end():]
    
    # Handle Quarto code blocks - convert attributes to comments or Hugo-friendly format
    def process_code_block(match):
        block_start = match.group(0)
        if '{#' in block_start:
            return '```' + block_start.split('```{')[1].split('\n', 1)[0] + '\n<!-- Non-executable example -->\n'
        return block_start
    
    content = re.sub(r'```{[^}]+}', process_code_block, content)
    
    # Convert Quarto-specific syntax
    content = content.replace('```{python}#', '```python\n<!-- Example code -->')
    content = re.sub(r'#\| eval: false', '', content)
    
    # Create Hugo-style front matter
    if yaml_front_matter.get('title'):
        title_val = yaml_front_matter['title']
        weight_search = re.search(r'\d+', yaml_front_matter.get('weight', '1'))
        weight_val = weight_search.group() if weight_search else '1'
        
        hugo_front = f"""---
title: "{title_val}"
weight: {weight_val}
---
"""
    else:
        hugo_front = "---\n---\n"
    
    # Write the converted file
    with open(md_path, 'w') as f:
        f.write(hugo_front + content.strip() + '\n')


def main():
    biobook_dir = Path('/home/cary/doffice/projects/bioinformatics-book')
    hugo_content_dir = Path('/home/cary/bio-hugo/content/chapters')
    
    # Create necessary directories
    hugo_content_dir.mkdir(parents=True, exist_ok=True)
    (hugo_content_dir / 'ch01-foundations').mkdir(exist_ok=True)
    (hugo_content_dir / 'ch02-analysis').mkdir(exist_ok=True)
    (hugo_content_dir / 'ch03-sequences').mkdir(exist_ok=True)
    (hugo_content_dir / 'ch04-genomics').mkdir(exist_ok=True)
    (hugo_content_dir / 'intro').mkdir(exist_ok=True)
    
    # Process each chapter file
    chapters_dir = biobook_dir / 'chapters'
    for qmd_file in sorted(chapters_dir.glob('ch*.qmd')):
        print(f"Converting {qmd_file.name}...")
        
        # Create appropriate subdirectory based on chapter numbers
        chapter_num_match = re.search(r'ch0*(\d+)', qmd_file.stem)
        if chapter_num_match:
            chap_num = int(chapter_num_match.group(1))
            if chap_num == 1:
                subdir = 'intro'
            elif 2 <= chap_num <= 4:
                subdir = 'ch01-foundations'
            elif 5 <= chap_num <= 8:
                subdir = 'ch02-analysis'  
            elif 9 <= chap_num <= 11:
                subdir = 'ch03-sequences'
            else:
                subdir = 'ch04-genomics'
        else:
            subdir = 'intro'
        
        os.makedirs(hugo_content_dir / subdir, exist_ok=True)
        md_path = hugo_content_dir / subdir / qmd_file.name.replace('.qmd', '.md')
        
        convert_qmd_to_md(str(qmd_file), str(md_path))
    
    print(f"\nConversion complete! Content available at {hugo_content_dir}")


if __name__ == '__main__':
    main()