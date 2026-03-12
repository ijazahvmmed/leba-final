import os
import re

LOCATIONS_HTML = """
<div class="foot-col">
<h5>Locations</h5>
<ul>
<li><a href="https://maps.app.goo.gl/dH8krCvaFFrTH3kt5?g_st=aw" target="_blank">Head Office (Ernakulam)</a></li>
<li><a href="https://maps.app.goo.gl/Mbe93N9HUfGVide56?g_st=aw" target="_blank">Branch (Thrissur)</a></li>
<li><a href="https://maps.google.com/?q=10.543257,76.186691" target="_blank">Speciality Unit</a></li>
</ul>
</div>
"""

def inject_footer_locations(directory):
    html_files = [f for f in os.listdir(directory) if f.endswith('.html')]
    success_count = 0
    
    for filename in html_files:
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # If it's already there, skip
        if '<h5>Locations</h5>' in content:
            continue

        # Regex to locate the end of foot-right
        pattern = re.compile(
            r'(<div class="foot-col">\s*<h5>Pages</h5>\s*<ul>.*?</ul>\s*</div>)(\s*</div>)', 
            re.DOTALL | re.IGNORECASE
        )
        
        match = pattern.search(content)
        if match:
            pages_col = match.group(1)
            end_div = match.group(2)
            
            # Form newly combined string
            new_block = pages_col + LOCATIONS_HTML + end_div
            
            new_content = content[:match.start()] + new_block + content[match.end():]
            
            with open(filepath, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(new_content)
            success_count += 1
            
    print(f"✅ Injected footer locations in {success_count} files.")

if __name__ == "__main__":
    inject_footer_locations(r"c:\Users\ijasa\OneDrive\Desktop\opleba")
