import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove old customer-time section
content = re.sub(r'<!-- TIME WITH CUSTOMER -->.*?</section>\s*', '', content, flags=re.DOTALL)

# 2. Add the new 50/50 dynamic split section
ds_html = '''
<!-- DYNAMIC 50/50 SECTION: FOOD & CUSTOMERS -->
<section id="dynamic-split">
  <div class="ds-left">
     <div class="ds-text-content active" id="ds-text-food">
        <span class="section-label">Farm to Table</span>
        <h2 class="section-title">Nourishing Local Foods</h2>
        <div class="divider"></div>
        <p class="section-sub">We serve wholesome, locally-sourced meals prepared with care, showcasing the seasonal flavors of the Kiso Valley.</p>
     </div>
     <div class="ds-text-content" id="ds-text-customer">
        <span class="section-label">Moments We Cherish</span>
        <h2 class="section-title">Time with Our Customers</h2>
        <div class="divider"></div>
        <p class="section-sub">Capturing the smiles, stories, and shared memories with guests from around the world.</p>
     </div>
  </div>
  <div class="ds-right">
     <div class="ds-collage active" id="ds-collage-food">
        <div class="ds-col-item pos-1"><img id="food-img-1" src="new/food for customer.jpg" alt="Food" loading="lazy"></div>
        <div class="ds-col-item pos-2"><img id="food-img-2" src="new/food for custoemr 2434.jpg" alt="Food" loading="lazy"></div>
        <div class="ds-col-item pos-3"><img id="food-img-3" src="new/food for customer 53.jpg" alt="Food" loading="lazy"></div>
     </div>
     <div class="ds-collage" id="ds-collage-customer">
        <div class="ds-col-item pos-1"><img id="cust-img-1" src="new/with customer 4.jpg" alt="Customer" loading="lazy"></div>
        <div class="ds-col-item pos-2"><img id="cust-img-2" src="new/with customer 55.jpg" alt="Customer" loading="lazy"></div>
        <div class="ds-col-item pos-3"><img id="cust-img-3" src="new/with customer.jpg" alt="Customer" loading="lazy"></div>
     </div>
  </div>
</section>
'''
content = content.replace('<!-- INSTAGRAM STRIP -->', ds_html + '\n<!-- INSTAGRAM STRIP -->')

# 3. Add CSS
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
content = content.replace('/*  INSTAGRAM STRIP  */', ds_css + '\n    /*  INSTAGRAM STRIP  */')

# 4. Add JS logic to rotate text and images
ds_js = '''
  /* DYNAMIC SPLIT SLIDER */
  (function() {
    const foodImages = [
      "new/food for customer.jpg", "new/food for custoemr 2434.jpg", "new/food for customer 53.jpg", 
      "new/food for customer353.jpg", "new/food for custommerrr.jpg", "new/food fotr customer.jpg"
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
      document.getElementById('ds-text-food').classList.toggle('active', isFood);
      document.getElementById('ds-text-customer').classList.toggle('active', !isFood);
      document.getElementById('ds-collage-food').classList.toggle('active', isFood);
      document.getElementById('ds-collage-customer').classList.toggle('active', !isFood);
    }, 7000);
    
    // Rotate images inside collages
    setInterval(() => {
       if (isFood) {
          // fade out, change src, fade in
          const imgEl = document.getElementById('food-img-' + (Math.floor(Math.random()*3)+1));
          imgEl.parentElement.style.opacity = 0;
          setTimeout(() => {
             imgEl.src = randomImg(foodImages, foodIdx++);
             imgEl.parentElement.style.opacity = 1;
          }, 800);
       } else {
          const imgEl = document.getElementById('cust-img-' + (Math.floor(Math.random()*3)+1));
          imgEl.parentElement.style.opacity = 0;
          setTimeout(() => {
             imgEl.src = randomImg(custImages, custIdx++);
             imgEl.parentElement.style.opacity = 1;
          }, 800);
       }
    }, 3500);
  })();
'''
content = content.replace('/* "?"? SCROLL REVEAL "?"? */', ds_js + '\n  /* "?"? SCROLL REVEAL "?"? */')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
