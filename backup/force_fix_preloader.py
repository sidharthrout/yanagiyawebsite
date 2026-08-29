import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# First remove the inline script block up top that hides it early
content = re.sub(
    r"<script>\s*if \(sessionStorage\.getItem\('preloaderShown'\).*?</script>",
    "",
    content,
    flags=re.DOTALL
)

# Next replace the main preloader logic
preloader_pattern = r"\/\* .*? PRELOADER \(Zen Reveal\) .*?\*\/.*?\}\);"
new_preloader = '''/*  PRELOADER (Zen Reveal)  */
  document.addEventListener('DOMContentLoaded', () => {
    const zp = document.getElementById('zen-preloader');
    if (zp) {
      window.scrollTo(0,0);
      document.body.style.overflow = 'hidden';
      setTimeout(() => {
        zp.classList.add('slide-up');
        document.body.style.overflow = '';
        setTimeout(() => zp.remove(), 1500);
      }, 2000);
    }
  });'''

content = re.sub(preloader_pattern, new_preloader, content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
