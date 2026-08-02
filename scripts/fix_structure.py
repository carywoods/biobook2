import os
import re
from pathlib import Path

# Directories
hugo_dir = Path('/home/cary/bio-hugo/content')
biobook_src = Path('/home/cary/doffice/projects/bioinformatics-book/chapters')

def get_chapter_info(chap_num):
    """Get section and chapter directory name."""
    sections = {
        1: ('foundations', '01-language-of-life'),
        2: ('analysis', '02-python-basics'),
        3: ('foundations', '03-central-dogma'),
        4: ('genomics', '04-biological-data'),
        5: ('genomics', '05-alignment'),
        6: ('genomics', '06-motifs'),
        7: ('analysis', '07-expression-analysis'),
        8: ('genomics', '08-protein-structure'),
        9: ('ai-native', '09-genome-analysis'),
        10: ('ai-native', '10-metagenomics'),
        11: ('ai-native', '11-single-cell'),
        12: ('analysis', '12-llm-reasoning'),
        13: ('genomics', '13-pipelines'),
        14: ('ai-native', '14-capstone'),
    }
    return sections.get(chap_num, ('foundations', f'{chap_num:02d}-chapter'))

def create_section_index(section_dir):
    """Create index.md for a section."""
    section_name = section_dir.name.title()
    
    # Get chapters in this section
    chapters_dir = section_dir.parent / 'chapters' / section_dir.name
    chapter_files = sorted(chapters_dir.glob('*.md')) if chapters_dir.exists() else []
    
    content_lines = [
        '---',
        f'title: "{section_name}"',
        'type: "list"',
        'chapter: false',
        'weight: 1',
        'cascade:',
        '  type: "chapter"',
        '---',
        '',
        f'# {section_name}',
        '',
    ]
    
    # Add chapters as list items with proper weight ordering
    for chap_file in chapter_files:
        if chap_file.name == 'index.md':
            continue
        
        with open(chap_file) as f:
            content = f.read()
        
        # Extract title from front matter
        title_match = re.search(r'title:\s*["\']?(.+?)["\']?', content)
        if not title_match:
            title = chap_file.stem.replace('-', ' ').title()
        else:
            title = title_match.group(1).strip('"\'')
        
        # Extract chapter number for weight
        chap_num_match = re.search(r'ch0*(\d+)', chap_file.name)
        weight = int(chap_num_match.group(1)) if chap_num_match else 99
        
        # Get link from content
        link = f'/chapters/{section_dir.name}/{chap_file.stem}/'
        
        content_lines.append(f'- **[{title}]({{< relref "{link}" >}})**')
    
    content_lines.append('')
    
    section_index = section_dir / 'index.md'
    with open(section_index, 'w') as f:
        f.write('\n'.join(content_lines))

def create_chapter_content(chap_file):
    """Prepare a chapter file for Hugo pages."""
    chap_num_match = re.search(r'ch0*(\d+)', chap_file.name)
    if not chap_num_match:
        return None, None
    
    chap_num = int(chap_num_match.group(1))
    section_name, chap_dirname = get_chapter_info(chap_num)
    
    # Create proper Hugo page structure
    dest_dir = hugo_dir / 'chapters' / section_name / chap_dirname
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    # Read source file and update structure
    with open(chap_file) as f:
        content = f.read()
    
    # Update front matter for Hugo page
    yaml_match = re.search(r'^---\n.*?---', content, re.DOTALL)
    
    # Extract title
    title_match = re.search(r'title:\s*["\']?(.+?)["\']?', content)
    title = title_match.group(1).strip('"\'') if title_match else chap_file.stem.replace('-', ' ').title()
    
    # Get chapter number for weight
    weight = chap_num
    
    # Create new front matter for Hugo page structure
    new_front_matter = f'''---
title: "{title}"
type: "chapter"
weight: {weight}
chapter: true
---

'''
    
    # Get content after original front matter
    if yaml_match:
        body_content = content[yaml_match.end():].strip()
    else:
        body_content = content.strip()
    
    new_content = new_front_matter + body_content
    
    dest_file = dest_dir / 'index.md'
    with open(dest_file, 'w') as f:
        f.write(new_content)
    
    return section_name, dest_dirname

def main():
    # Process all chapters
    processed_sections = set()
    
    for chap_num in range(1, 15):
        src_file = biobook_src / f'ch{chap_num:02d}-*.qmd'
        matching = list(biobook_src.glob(f'ch{chap_num:02d}-*.qmd'))
        
        if not matching:
            continue
        
        src_file = matching[0]
        print(f"Processing chapter {chap_num}: {src_file.name}")
        
        section_name, chap_dirname = create_chapter_content(src_file)
        processed_sections.add(section_name)
        
        # Remove old file after conversion
        if src_file.exists():
            os.remove(src_file)
    
    # Create section index files
    print("\nCreating section indexes...")
    sections_dir = hugo_dir / 'chapters'
    for section in ['foundations', 'analysis', 'genomics', 'ai-native']:
        section_path = sections_dir / section
        if section_path.exists():
            create_section_index(section_path)
    
    print("\nDone restructuring chapters!")

if __name__ == '__main__':
    main()