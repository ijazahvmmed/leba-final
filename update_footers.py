import os
import re

def clean_footers(directory):
    html_files = [f for f in os.listdir(directory) if f.endswith('.html')]
    success_count = 0
    
    for filename in html_files:
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Regex to locate the Pages <ul> block in the footer
        # We look for <div class="foot-col"> <h5>Pages</h5> <ul> ... </ul>
        pattern = re.compile(
            r'(<div class="foot-col">\s*<h5>Pages</h5>\s*<ul>)(.*?)(</ul>\s*</div>)', 
            re.DOTALL | re.IGNORECASE
        )
        
        match = pattern.search(content)
        if match:
            start_tag, ul_content, end_tag = match.groups()
            
            # Remove specific <li> lines
            # Projects, Solutions, Careers
            ul_content = re.sub(r'<li>\s*<a href="#">Projects</a>\s*</li>', '', ul_content, flags=re.IGNORECASE)
            ul_content = re.sub(r'<li>\s*<a href="#">Solutions</a>\s*</li>', '', ul_content, flags=re.IGNORECASE)
            ul_content = re.sub(r'<li>\s*<a href="#">Careers</a>\s*</li>', '', ul_content, flags=re.IGNORECASE)
            
            # Clean up empty lines created
            ul_content = re.sub(r'\n\s*\n', '\n', ul_content)
            
            new_block = start_tag + ul_content + end_tag
            
            new_content = content[:match.start()] + new_block + content[match.end():]
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8', errors='ignore') as f:
                    f.write(new_content)
                success_count += 1
            
    print(f"✅ Cleaned footers in {success_count} files out of {len(html_files)}")

if __name__ == "__main__":
    clean_footers(r"c:\Users\ijasa\OneDrive\Desktop\opleba")
