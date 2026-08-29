import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

infinity_css = '''
    /* INFINITY SCROLL MARQUEE */
    @keyframes scrollInfinity { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }
    @keyframes scrollInfinityReverse { 0% { transform: translateX(-50%); } 100% { transform: translateX(0); } }
    .infinity-track:hover { animation-play-state: paused !important; }
    .food-img-box {
      flex-shrink: 0; width: 280px; height: 280px; border-radius: 12px;
      overflow: visible; position: relative; z-index: 1;
      transition: transform 0.4s cubic-bezier(0.25, 1, 0.5, 1), z-index 0s;
    }
    .food-img-box img { width: 100%; height: 100%; object-fit: cover; border-radius: 12px; transition: transform 0.4s cubic-bezier(0.25, 1, 0.5, 1), box-shadow 0.4s; }
    .food-img-box:hover { z-index: 20; transform: scale(1.2) translateY(-10px); }
    .food-img-box:hover img { box-shadow: 0 25px 60px rgba(0,0,0,0.5); }
    
    /* Smooth transitions for Magome and Stars sections */
    #magome, #stars {
      opacity: 0;
      transform: translateY(50px);
      transition: opacity 1.5s cubic-bezier(0.25, 1, 0.5, 1), transform 1.5s cubic-bezier(0.25, 1, 0.5, 1);
    }
    #magome.in-view, #stars.in-view {
      opacity: 1;
      transform: translateY(0);
    }
'''

# Insert CSS before </head>
content = re.sub(r'</style>\s*</head>', infinity_css + '\n</style>\n</head>', content)

# Add IntersectionObserver for #magome and #stars in JS
fade_in_js = '''
  // FADE IN MAGOME AND STARS
  const fadeObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if(entry.isIntersecting) {
        entry.target.classList.add('in-view');
      }
    });
  }, { threshold: 0.15 });
  
  const magomeSec = document.getElementById('magome');
  const starsSec = document.getElementById('stars');
  if(magomeSec) fadeObserver.observe(magomeSec);
  if(starsSec) fadeObserver.observe(starsSec);
'''

# Insert JS before </script></body>
last_script = content.rfind('</script>')
content = content[:last_script] + fade_in_js + content[last_script:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
