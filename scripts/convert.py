import os
import re
from pathlib import Path

# Directories
biobook = Path('/home/cary/doffice/projects/bioinformatics-book')
hugo_dir = Path('/home/cary/bio-hugo/content')

def get_chapter_section(chap_num):
    """Map chapter number to section name."""
    if chap_num == 1:
        return 'foundations'
    elif 2 <= chap_num <= 4:  
        return 'analysis'
    elif 5 <= chap_num <= 8:
        return 'genomics'
    else:
        return 'ai-native'

def convert_qmd_to_hugo(src, dst):
    """Convert .qmd to Hugo-markdown."""
    src_path = Path(src) if isinstance(src, str) else src
    dst_path = Path(dst) if isinstance(dst, str) else dst
    
    with open(src_path) as f:
        content = f.read()
    
    # Check for YAML front matter
    yaml_match = re.search(r'^---\n(.*?)---\n', content, re.DOTALL)
    title = "Untitled"
    
    if yaml_match:
        yaml_text = yaml_match.group(1)
        # Extract title
        for line in yaml_text.split('\n'):
            if 'title:' in line:
                title = line.split(':', 1)[1].strip().strip('"')
                break
        content = content[yaml_match.end():]
    else:
        # First heading is the title - extract chapter number from filename
        chap_num_match = re.search(r'ch0*(\d+)', src_path.stem)
        chap_num = int(chap_num_match.group(1)) if chap_num_match else 1
        
        h1_match = re.search(r'^# (.+)', content, re.MULTILINE)
        if h1_match:
            title = h1_match.group(1).replace('#', '').strip()
    
    # Clean up any Quarto-specific syntax (#| eval: false)
    content = re.sub(r'#\| eval: false', '', content)
    
    # Get chapter number for weight
    chap_num_match = re.search(r'ch0*(\d+)', src_path.stem)
    chap_num = int(chap_num_match.group(1)) if chap_num_match else 1
    
    # Create proper Hugo front matter (avoiding f-strings with backslashes)
    front_matter = '---\n' + \
                   'title: "' + title + '"\n' + \
                   'type: "chapter"\n' + \
                   'weight: ' + str(chap_num) + '\n' + \
                   '---\n\n'
    
    # Ensure destination directory exists
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(dst_path, 'w') as f:
        f.write(front_matter + content.strip() + '\n')

# Main conversion loop for chapters only (filter for chXX- pattern files)
chapters_dir = biobook / 'chapters'
for qmd_file in sorted(chapters_dir.glob('*.qmd')):
    # Only process files that match the chapter numbering pattern
    chap_num_match = re.search(r'^ch0*(\d+)-', qmd_file.name)
    if not chap_num_match:
        print("Skipping (not a chapter file): {}".format(qmd_file.name))
        continue
    
    chap_num = int(chap_num_match.group(1))
    section = get_chapter_section(chap_num)
    dest_dir = hugo_dir / 'chapters' / section
    dest_file = dest_dir / (qmd_file.stem + '.md')
    
    print("Converting: {} -> {}".format(qmd_file.name, dest_file))
    convert_qmd_to_hugo(str(qmd_file), str(dest_file))

print("\nDone converting chapters!")