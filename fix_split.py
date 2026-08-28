import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add CSS
ds_css = '''
    /* DYNAMIC SPLIT SECTION */
    #dynamic-split { display: flex; flex-wrap: wrap; background: var(--paper); overflow: hidden; border-top: 1px solid rgba(0,0,0,0.05); }
    .ds-left { flex: 1; min-width: 300px; padding: 8rem 8%; display: flex; align-items: center; justify-content: center; position: relative; }
    .ds-text-content { position: absolute; opacity: 0; transform: translateY(20px); transition: all 1s ease; pointer-events: none; width: 80%; }
    .ds-text-content.active { opacity: 1; transform: translateY(0); pointer-events: auto; position: relative; }
    
    .ds-right { flex: 1; min-width: 300px; position: relative; min-height: 600px; background: var(--card); overflow: hidden; }
    .ds-collage { position: absolute; inset: 0; opacity: 0; transition: opacity 1.2s ease; pointer-events: none; }
    .ds-collage.active { opacity: 1; pointer-events: auto; }
    
    .ds-col-item { position: absolute; border-radius: 8px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.15); transition: opacity 0.8s ease, transform 0.8s ease; }
    .ds-col-item img { width: 100%; height: 100%; object-fit: cover; }
    
    .ds-col-item.pos-1 { top: 10%; left: 10%; width: 45%; height: 50%; z-index: 3; }
    .ds-col-item.pos-2 { top: 30%; right: 10%; width: 40%; height: 45%; z-index: 2; }
    .ds-col-item.pos-3 { bottom: 10%; left: 20%; width: 50%; height: 40%; z-index: 4; }
    
    @media (max-width: 850px) {
      .ds-left { padding: 4rem 6%; }
      .ds-right { min-height: 400px; }
      .ds-col-item.pos-1 { top: 5%; left: 5%; width: 50%; height: 45%; }
      .ds-col-item.pos-2 { top: 25%; right: 5%; width: 45%; height: 45%; }
      .ds-col-item.pos-3 { bottom: 5%; left: 15%; width: 60%; height: 40%; }
    }
'''
if 'DYNAMIC SPLIT SECTION' not in content:
    content = content.replace('</style>', ds_css + '\n</style>')

# 2. Add JS
ds_js = '''
  /* DYNAMIC SPLIT SLIDER */
  (function() {
    const foodImages = [
      "new/food for customer.jpg", "new/food for custoemr 2434.jpg", "new/food for customer 53.jpg", 
      "new/food for customer353.jpg", "new/food for custommerrr.jpg", "new/food fotr customer.jpg",
      "new/food for cusotmer31232.jpg", "new/food for custoemrrr.jpg", "new/food for custome 33.jpg",
      "new/food for customer443.jpg", "new/food for customer444.jpg", "new/food for customerrr.jpg"
    ];
    const custImages = [
      "new/with customer 4.jpg", "new/with customer 55.jpg", "new/with customer.jpg", 
      "new/witcusotmer.jpg", "new/with customer (2).jpg"
    ];
    
    let isFood = true;
    let foodIdx = 3, custIdx = 3;
    
    function randomImg(arr, currentIdx) {
      const img = arr[currentIdx % arr.length];
      return img;
    }
    
    // Switch main tabs (Food <-> Customer)
    setInterval(() => {
      isFood = !isFood;
      const tf = document.getElementById('ds-text-food');
      const tc = document.getElementById('ds-text-customer');
      const cf = document.getElementById('ds-collage-food');
      const cc = document.getElementById('ds-collage-customer');
      if(tf) tf.classList.toggle('active', isFood);
      if(tc) tc.classList.toggle('active', !isFood);
      if(cf) cf.classList.toggle('active', isFood);
      if(cc) cc.classList.toggle('active', !isFood);
    }, 7000);
    
    // Rotate images inside collages
    setInterval(() => {
       if (isFood) {
          const randId = Math.floor(Math.random()*3)+1;
          const imgEl = document.getElementById('food-img-' + randId);
          if(imgEl && imgEl.parentElement) {
              imgEl.parentElement.style.opacity = 0;
              setTimeout(() => {
                 imgEl.src = randomImg(foodImages, foodIdx++);
                 imgEl.parentElement.style.opacity = 1;
              }, 800);
          }
       } else {
          const randId = Math.floor(Math.random()*3)+1;
          const imgEl = document.getElementById('cust-img-' + randId);
          if(imgEl && imgEl.parentElement) {
              imgEl.parentElement.style.opacity = 0;
              setTimeout(() => {
                 imgEl.src = randomImg(custImages, custIdx++);
                 imgEl.parentElement.style.opacity = 1;
              }, 800);
          }
       }
    }, 3500);
  })();
'''
if 'DYNAMIC SPLIT SLIDER' not in content:
    # insert before the last </script> tag
    content = content.replace('</script>', ds_js + '\n</script>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
