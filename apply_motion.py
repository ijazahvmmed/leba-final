import os
from bs4 import BeautifulSoup
import re

dir_path = r"c:\Users\ijasa\OneDrive\Desktop\opleba"

def add_motion(soup):
    added_count = 0
    # Find all main sections where elements should animate
    sections = soup.find_all(['section', 'div'], class_=re.compile(r'panel|sec|main-wrapper|content-blur-wrapper|related-products-section'))
    if not sections:
        sections = [soup.find('body')] # fallback to body
        
    for section in sections:
        # Don't animate header/footer/modals
        if section.name in ['header', 'footer'] or section.get('class') and any(c in ['header-wrap', 'site-header', 'footer', 'mobile-nav-overlay'] for c in section.get('class')):
            continue
        if section.find_parent(class_=re.compile(r'header-wrap|site-header|footer|mobile-nav-overlay')):
            continue
            
        elements = section.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'a', 'img', 'div'], recursive=True)
        # Filter to things that look like distinct components
        animatable = []
        for el in elements:
            # Skip if already has motion
            if el.has_attr('data-motion'):
                continue
            # Skip if it's inside something that's already getting animated as a block
            parent_in_list = False
            for p in el.find_parents():
                if p in animatable:
                    parent_in_list = True
                    break
            if parent_in_list:
                continue

            # Check if it should be animated based on tag/class
            tag = el.name
            classes = el.get('class', [])
            is_card = bool(classes and any(c in ['card', 'card-modern', 'proj-item', 'stat', 'label-text'] for c in classes))
            is_btn = bool(classes and 'btn' in classes)
            is_image = tag == 'img'
            is_heading = tag in ['h1', 'h2', 'h3', 'h4']
            is_para = tag == 'p'
            
            if is_card or is_btn or is_image or is_heading or is_para:
                animatable.append(el)
        
        # Apply stagger to the animatable elements found in this section
        delay = 1
        for el in animatable:
            tag = el.name
            classes = el.get('class', [])
            
            # Determine motion type based on skill guide
            m_type = "fade-up" # default
            if tag == 'img' or (classes and 'proj-item' in classes):
                m_type = "fade-scale"
            elif classes and 'label-text' in classes:
                m_type = "fade-up"
                
            el['data-motion'] = m_type
            el['data-motion-delay'] = str(min(delay, 10))
            delay += 1
            added_count += 1
            
    return added_count

def inject_observer(soup):
    # Check if script exists
    scripts = soup.find_all('script')
    for s in scripts:
        if s.string and 'IntersectionObserver' in s.string and 'data-motion' in s.string:
            return False # Already exists
            
    # Create the observer script
    script_str = """
(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var root = document.querySelector('.main-wrapper') || document.body;
  if (!root) return;
  var elements = root.querySelectorAll('[data-motion]');
  if (!elements.length) return;

  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15, rootMargin: '0px 0px -40px 0px' }
  );
  document.querySelectorAll('[data-motion]').forEach(function (el) { observer.observe(el); });
})();
"""
    new_script = soup.new_tag('script')
    new_script.string = script_str
    
    body = soup.find('body')
    if body:
        body.append(new_script)
        return True
    return False

# --- 1. Modify CSS ---
css_path = os.path.join(dir_path, 'css', 'new-theme.css')
with open(css_path, 'r', encoding='utf-8') as f:
    css_content = f.read()

motion_css = '''
/* --- Motion: Base --- */
[data-motion] {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1), transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
  will-change: opacity, transform;
}
[data-motion].is-visible {
  opacity: 1;
  transform: translateY(0) translateX(0) scale(1) !important;
}
[data-motion-delay="1"]  { transition-delay: 0.08s; }
[data-motion-delay="2"]  { transition-delay: 0.16s; }
[data-motion-delay="3"]  { transition-delay: 0.24s; }
[data-motion-delay="4"]  { transition-delay: 0.32s; }
[data-motion-delay="5"]  { transition-delay: 0.40s; }
[data-motion-delay="6"]  { transition-delay: 0.48s; }
[data-motion-delay="7"]  { transition-delay: 0.56s; }
[data-motion-delay="8"]  { transition-delay: 0.64s; }
[data-motion-delay="9"]  { transition-delay: 0.72s; }
[data-motion-delay="10"] { transition-delay: 0.80s; }

[data-motion="fade-up"] { transform: translateY(24px); }
[data-motion="fade-down"] { transform: translateY(-24px); }
[data-motion="fade-left"] { transform: translateX(24px); }
[data-motion="fade-right"] { transform: translateX(-24px); }
[data-motion="fade-in"] { transform: none; }
[data-motion="fade-scale"] { transform: scale(0.95); }
[data-motion="fade-scale-up"] { transform: translateY(24px) scale(0.97); }

@media (prefers-reduced-motion: reduce) {
  [data-motion] {
    opacity: 1 !important;
    transform: none !important;
    transition: none !important;
    will-change: auto;
  }
}
'''
if '/* --- Motion: Base --- */' not in css_content:
    with open(css_path, 'a', encoding='utf-8') as f:
        f.write('\\n' + motion_css)
    print("Added motion CSS to new-theme.css")
else:
    print("Motion CSS already exists")

# --- 2. Process HTML files ---
for filename in os.listdir(dir_path):
    if not filename.endswith('.html') or filename == 'index_backup.html':
        continue
        
    filepath = os.path.join(dir_path, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        html_content = f.read()
        
    # We apply beautifulsoup only to add exactly what's needed.
    soup = BeautifulSoup(html_content, 'html.parser')
    
    modified_motion = add_motion(soup)
    modified_js = inject_observer(soup)
    
    if modified_motion > 0 or modified_js:
        # Save back parsing output
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"Updated {filename}: Added {modified_motion} motion attributes, JS Observer: {modified_js}")
    
print("All pages fully animated!")
