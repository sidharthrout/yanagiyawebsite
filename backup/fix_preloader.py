import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix inline script
content = re.sub(
    r"<script>\s*if \(sessionStorage\.getItem\('preloaderShown'\) === 'true'\) \{\s*document\.getElementById\('zen-preloader'\)\.style\.display = 'none';\s*\}\s*</script>",
    "",
    content,
    flags=re.DOTALL
)

# Fix the main JS block
pattern = r"document\.addEventListener\('DOMContentLoaded', \(\) => \{\s*const zp = document\.getElementById\('zen-preloader'\);\s*const isShown = sessionStorage\.getItem\('preloaderShown'\) === 'true';\s*if \(!isShown && zp\) \{\s*setTimeout\(\(\) => \{\s*zp\.classList\.add\('slide-up'\);\s*setTimeout\(\(\) => zp\.remove\(\), 1500\); // Remove from DOM after slide\s*sessionStorage\.setItem\('preloaderShown', 'true'\);\s*\}, 2500\); // Slide up after 2\.5s\s*\} else if \(zp\) \{\s*zp\.style\.display = 'none';\s*\}\s*\}\);"

new_code = '''document.addEventListener('DOMContentLoaded', () => {
    const zp = document.getElementById('zen-preloader');
    if (zp) {
      window.scrollTo(0, 0);
      document.body.style.overflow = 'hidden';
      setTimeout(() => {
        zp.classList.add('slide-up');
        document.body.style.overflow = '';
        setTimeout(() => zp.remove(), 1500);
      }, 2000);
    }
  });'''

content = re.sub(pattern, new_code, content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
