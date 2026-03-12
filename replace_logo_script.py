import os
import re

LOGO_HTML = """<img src="images/logo.png" alt="Leba Papers" class="site-logo" style="height: 40px; width: auto; object-fit: contain;">"""

def replace_logo(directory):
    html_files = [f for f in os.listdir(directory) if f.endswith('.html')]
    success_count = 0
    
    for filename in html_files:
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        original_content = content

        # In header and mobile header:
        content = re.sub(
            r'<a class="logo" href="index\.html">\s*©Leba Papers\s*</a>',
            f'<a class="logo" href="index.html">\n                {LOGO_HTML}\n            </a>',
            content
        )
        
        # In footer:
        content = re.sub(
            r'<div class="foot-logo">\s*©Leba Papers\s*</div>',
            f'<div class="foot-logo">\n                {LOGO_HTML}\n            </div>',
            content
        )

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(content)
            success_count += 1
            
    print(f"✅ Replaced logo in {success_count} files.")

if __name__ == "__main__":
    replace_logo(r"c:\Users\ijasa\OneDrive\Desktop\opleba")
