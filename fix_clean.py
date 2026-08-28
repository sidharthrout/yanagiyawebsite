import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# The JS block that was injected
js_block = r'\n  /\* DYNAMIC SPLIT SLIDER \*/.*?  \)\(\);\n'

# Replace all occurrences of it followed by </script> with just </script>
content = re.sub(js_block + r'</script>', '</script>', content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
