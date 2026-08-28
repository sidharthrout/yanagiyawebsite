with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Splitting by the comment marker of JS block
parts = content.split('/* DYNAMIC SPLIT SLIDER */')
# part[0] is everything before first block
# part[1] is the first block
# part[2] is the second block (if exists)

if len(parts) > 1:
    # Just take the original script from git
    pass
