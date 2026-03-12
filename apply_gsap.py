import os
from bs4 import BeautifulSoup
import re

dir_path = r"c:\Users\ijasa\OneDrive\Desktop\opleba"

# 1. Patch CSS to disable CSS hover for GSAP drawer
css_path = os.path.join(dir_path, 'css', 'new-theme.css')
with open(css_path, 'r', encoding='utf-8') as f:
    css_content = f.read()

# Disable pure CSS mega-menu hover so GSAP can handle it smoothly
css_content = css_content.replace(
    '.nav-item-group:hover .nav-dropdown {',
    '/*.nav-item-group:hover .nav-dropdown {*/\n.nav-item-group-css-disabled-hover {'
)

# Also disable CSS transition on dropdowns if exists to prevent fighting
css_content = css_content.replace(
    'transition: all 0.3s;',
    '/*transition: all 0.3s;*/'
)
css_content = css_content.replace(
    'transition: all 0.3s ease;',
    '/*transition: all 0.3s ease;*/'
)

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css_content)

print("Patched css/new-theme.css for GSAP")

# 2. Inject Scripts into all HTML files
for filename in os.listdir(dir_path):
    if not filename.endswith('.html') or filename == 'index_backup.html':
        continue
    filepath = os.path.join(dir_path, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    changed = False

    # Remove inline intersection observer logic for [data-motion]
    for script in soup.find_all('script'):
        if script.string and 'IntersectionObserver' in script.string and ('data-motion' in script.string or 'is-visible' in script.string):
            script.decompose()
            changed = True
            
        if script.string and 'document.querySelectorAll' in script.string and 'data-motion' in script.string:
            script.decompose()
            changed = True

    # Add dependencies to <head>
    head = soup.find('head')
    if head:
        # Check if already added
        if not head.find('script', src=lambda s: s and 'lenis' in s):
            new_script = soup.new_tag('script', src="https://unpkg.com/@studio-freight/lenis@1.0.35/dist/lenis.min.js")
            head.append(new_script)
            changed = True
            
        if not head.find('script', src=lambda s: s and 'split-type' in s):
            new_script = soup.new_tag('script', src="https://unpkg.com/split-type")
            head.append(new_script)
            changed = True

    # Add custom GSAP file to <body>
    body = soup.find('body')
    if body:
        if not body.find('script', src="js/gsap-animations.js"):
            new_script = soup.new_tag('script', src="js/gsap-animations.js")
            body.append(new_script)
            changed = True

    # Save
    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Updated scripts in {filename}")

print("GSAP initialization complete.")
