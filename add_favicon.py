import os
import re
import urllib.parse

def add_favicon(directory):
    html_files = [f for f in os.listdir(directory) if f.endswith('.html')]
    success_count = 0
    img_path = 'images/logohanbee -asd Copy.png'
    encoded_path = urllib.parse.quote(img_path)
    favicon_tag = f'\n    <link rel="icon" type="image/png" href="{img_path}" />\n'
    
    for filename in html_files:
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        if '<link rel="icon"' not in content:
            new_content = content.replace('</head>', f'{favicon_tag}</head>')
            with open(filepath, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(new_content)
            success_count += 1
            
    print(f"✅ Added favicon to {success_count} files.")

if __name__ == "__main__":
    add_favicon(r"c:\Users\ijasa\OneDrive\Desktop\opleba")
