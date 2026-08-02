import re
from pathlib import Path

hugo_dir = Path('/home/cary/bio-hugo/content')

# Find all markdown files
md_files = list(hugo_dir.rglob('*.md'))
print("Found {} markdown files".format(len(md_files)))

fixed_count = 0

# Quarto uses ```{python} / ```{r} / ```{bash} style fenced code blocks.
# Hugo Goldmark interprets {..} after a fence opener as an attribute list,
# which fails to parse. Convert to plain (or quoted) language specifiers.
brace_pattern = re.compile(r'^(\s*)```\{([a-zA-Z0-9_]+)\}\s*$', re.MULTILINE)

for md_file in md_files:
    with open(md_file) as f:
        content = f.read()

    original = content

    # 1) Convert ```{lang}  ->  ```lang  (Quarto brace form)
    content = brace_pattern.sub(lambda m: m.group(1) + '```' + m.group(2), content)

    # 1b) Normalize leftover ```"lang" (quoted) back to plain ```lang
    content = re.sub(
        r'^(\s*)```"([a-zA-Z][a-zA-Z0-9_]*)"\s*$',
        lambda m: m.group(1) + '```' + m.group(2),
        content,
        flags=re.MULTILINE,
    )

    # 2) Also normalize any remaining plain ```lang that might carry trailing attrs
    content = re.sub(
        r'^(\s*)```([a-zA-Z][a-zA-Z0-9_]*)[ \t]+.*$',
        lambda m: m.group(1) + '```' + m.group(2),
        content,
        flags=re.MULTILINE,
    )

    if content != original:
        with open(md_file, 'w') as f:
            f.write(content)
        print("Fixed: {}".format(md_file.relative_to(hugo_dir)))
        fixed_count += 1

print("\nFixed {} files".format(fixed_count))
