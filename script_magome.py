import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_slides = '''
    <div class="kb-slide"><img src="new/yanagiya autumon.jpg" alt="Yanagiya in beautiful Autumn colors" loading="lazy" /></div>
    <div class="kb-slide"><img src="new/yanagiya in automn.jpg" alt="Yanagiya surrounded by fall foliage" loading="lazy" /></div>
    <div class="kb-slide"><img src="new/yanagiya summer.jpg" alt="Yanagiya during lush summer days" loading="lazy" /></div>
    <div class="kb-slide"><img src="new/yanagiya winter.jpg" alt="Yanagiya covered in winter snow" loading="lazy" /></div>
    <div class="kb-slide"><img src="new/yanagiya in clear day.jpg" alt="Yanagiya on a clear bright day" loading="lazy" /></div>
'''

# Find the end of kb-slider div or just insert before <div class="kb-slider-overlay">
content = content.replace('<div class="kb-slider-overlay"></div>', new_slides + '    <div class="kb-slider-overlay"></div>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
