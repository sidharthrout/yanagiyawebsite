import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Enlarge infinity marquee images and increase distance
content = content.replace('width: 280px; height: 280px;', 'width: 350px; height: 350px;')
content = content.replace('gap:1.5rem;', 'gap:3rem;')

# 2. Fix the black right edge issue (Windows scrollbar gap)
content = content.replace('max-width: 100vw;', 'width: 100%;')

# 3. Fix Preloader inline script (remove it)
content = re.sub(
    r"<script>\s*if \(sessionStorage\.getItem\('preloaderShown'\) === 'true'\) \{\s*document\.getElementById\('zen-preloader'\)\.style\.display = 'none';\s*\}\s*</script>",
    "",
    content
)

# 4. Fix Preloader logic at the bottom
old_preloader_logic = '''  /* ?? PRELOADER (Zen Reveal) ?? */
  document.addEventListener('DOMContentLoaded', () => {
    const zp = document.getElementById('zen-preloader');
    const isShown = sessionStorage.getItem('preloaderShown') === 'true';

    if (!isShown && zp) {
      setTimeout(() => {
        zp.classList.add('slide-up');
        setTimeout(() => zp.remove(), 1500); // Remove from DOM after slide
        sessionStorage.setItem('preloaderShown', 'true');
      }, 2500); // Slide up after 2.5s
    } else if (zp) {
      zp.style.display = 'none';
    }
  });'''

new_preloader_logic = '''  /* ?? PRELOADER (Zen Reveal) ?? */
  document.addEventListener('DOMContentLoaded', () => {
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

# Let's use regex in case of slight whitespace differences, but specifically target the JS section
content = re.sub(
    r"\/\* ?? PRELOADER \(Zen Reveal\) ?? \*\/[\s\S]*?\}\);",
    new_preloader_logic,
    content,
    count=1
)

# 5. GSAP Logic Update
gsap_logic_old = '''  // MAGOME PINNED SCROLL
  const magomePanels = document.querySelectorAll('.magome-panel');
  if (magomePanels.length > 0) {
    const tl1 = gsap.timeline({ scrollTrigger: { trigger: '#magome', pin: true, scrub: 1, start: 'center center', end: '+=150%' } });
    tl1.to(magomePanels[0], { opacity: 0, duration: 1 }).to(magomePanels[1], { opacity: 1, duration: 1 }, "<")
       .to(magomePanels[1], { opacity: 0, duration: 1 }).to(magomePanels[2], { opacity: 1, duration: 1 }, "<")
       .to(magomePanels[2], { opacity: 0, duration: 1 }).to(magomePanels[3], { opacity: 1, duration: 1 }, "<");
  }
  // STARS PINNED SCROLL
  const starPanels = document.querySelectorAll('.star-panel');
  if (starPanels.length > 0) {
    const tl2 = gsap.timeline({ scrollTrigger: { trigger: '#stars', pin: true, scrub: 1, start: 'center center', end: '+=150%' } });
    tl2.to(starPanels[0], { opacity: 0, duration: 1 }).to(starPanels[1], { opacity: 1, duration: 1 }, "<")
       .to(starPanels[1], { opacity: 0, duration: 1 }).to(starPanels[2], { opacity: 1, duration: 1 }, "<");
  }'''

gsap_logic_new = '''  // TRAIL ZOOM-SCROLL EFFECT
  const trailCard = document.querySelector('.trail-feature-card');
  if (trailCard) {
    gsap.fromTo(trailCard,
      { filter: 'blur(1.5rem)', scale: 0.85, opacity: 0 },
      { 
        filter: 'blur(0rem)', scale: 1, opacity: 1, 
        scrollTrigger: {
          trigger: trailCard,
          start: 'top bottom',
          end: 'center center',
          scrub: 1
        }
      }
    );
  }

  // MAGOME PINNED SCROLL
  const magomePanels = document.querySelectorAll('.magome-panel');
  if (magomePanels.length > 0) {
    const tl1 = gsap.timeline({ scrollTrigger: { trigger: '#magome', pin: true, scrub: 1, start: 'center center', end: '+=180%' } });
    tl1.to(magomePanels[0], { opacity: 0, duration: 1 }).to(magomePanels[1], { opacity: 1, duration: 1 }, "<")
       .to(magomePanels[1], { opacity: 0, duration: 1 }).to(magomePanels[2], { opacity: 1, duration: 1 }, "<")
       .to(magomePanels[2], { opacity: 0, duration: 1 }).to(magomePanels[3], { opacity: 1, duration: 1 }, "<")
       .to('.magome-right', { opacity: 0, y: -50, duration: 1, delay: 0.5 }); // Smooth exit fade out
  }
  
  // STARS PINNED SCROLL
  const starPanels = document.querySelectorAll('.star-panel');
  if (starPanels.length > 0) {
    const tl2 = gsap.timeline({ scrollTrigger: { trigger: '#stars', pin: true, scrub: 1, start: 'center center', end: '+=150%' } });
    tl2.to(starPanels[0], { opacity: 0, duration: 1 }).to(starPanels[1], { opacity: 1, duration: 1 }, "<")
       .to(starPanels[1], { opacity: 0, duration: 1 }).to(starPanels[2], { opacity: 1, duration: 1 }, "<")
       .to('.stars-right', { opacity: 0, y: -50, duration: 1, delay: 0.5 }); // Smooth exit fade out
  }'''

content = content.replace(gsap_logic_old, gsap_logic_new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
