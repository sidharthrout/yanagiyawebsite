import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the insta-grid div with an embed placeholder
insta_placeholder = '''
  <div class="insta-feed-container reveal" style="max-width: 1200px; margin: 2.5rem auto; min-height: 300px; display: flex; align-items: center; justify-content: center; background: #f9f9f9; border: 1px dashed #ccc; border-radius: 8px;">
     <!-- INSTAGRAM WIDGET EMBED CODE GOES HERE -->
     <!-- Example: <script src="https://apps.elfsight.com/p/platform.js" defer></script><div class="elfsight-app-YOUR-ID-HERE"></div> -->
     <p style="color: var(--muted); font-size: 0.9rem; text-align: center; padding: 2rem;">
        <em>Your live Instagram feed will appear here.<br>Paste your embed code (e.g., from Elfsight, Curator.io, or SnapWidget) into this container in index.html.</em>
     </p>
  </div>
'''

content = re.sub(r'<div class="insta-grid reveal">.*?</div>', insta_placeholder, content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
