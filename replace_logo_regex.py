import os
import re

LOGO_HTML = """
                <img src="images/logo.png" alt="Leba Papers" class="site-logo" style="height: 40px; width: auto; object-fit: contain;">
"""

def replace_logo_relaxed(directory):
    html_files = [f for f in os.listdir(directory) if f.endswith('.html')]
    success_count = 0
    
    for filename in html_files:
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        original_content = content

        # Replace 1: Header logo and mobile logo
        # Need to match <a ...> ...Leba Papers... </a> but be careful not to match `<a class="logo" href="index.html"> <img...> </a>`
        # Because we've already done index.html and contact.html possibly
        
        # Look for the exact tag structure and ensure it DOES NOT currently contain <img
        content = re.sub(
            r'<a class="logo" href="index\.html">\s*[^<]*?Leba Papers[^<]*?\s*</a>',
            f'<a class="logo" href="index.html">{LOGO_HTML}            </a>',
            content
        )
        
        # Replace 2: Footer logo
        content = re.sub(
            r'<div class="foot-logo">\s*[^<]*?Leba Papers[^<]*?\s*</div>',
            f'<div class="foot-logo">{LOGO_HTML}            </div>',
            content
        )

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(content)
            success_count += 1
            
    print(f"✅ Relaxed Regex Replaced logo in {success_count} files.")

if __name__ == "__main__":
    replace_logo_relaxed(r"c:\Users\ijasa\OneDrive\Desktop\opleba")
