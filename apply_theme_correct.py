import os
import re

dir_path = r"c:\Users\ijasa\OneDrive\Desktop\opleba"
index_path = os.path.join(dir_path, "index.html")

with open(index_path, "r", encoding="utf-8") as f:
    index_content = f.read()

# Extract NEW HEADER
h_start = index_content.find('<!-- Header Island -->')
if h_start == -1: h_start = index_content.find('<div class="header-wrap">')
h_end = index_content.find('<!-- Hero Full -->')
if h_end == -1: h_end = index_content.find('<!-- Intro -->')

new_header = index_content[h_start:h_end].strip() if h_start != -1 and h_end != -1 else ""

# Extract NEW FOOTER
f_start = index_content.find('<!-- Footer -->')
if f_start == -1: f_start = index_content.find('<footer class="footer">')
f_end = index_content.find('</footer>')

new_footer = index_content[f_start:f_end+9].strip() if f_start != -1 and f_end != -1 else ""

# Extract NEW SCRIPT (lucide and scroll sticky)
s_start = index_content.rfind('<script>')
s_end = index_content.rfind('</script>')
new_script = index_content[s_start:s_end+9].strip() if s_start != -1 and s_end != -1 else ""

for filename in os.listdir(dir_path):
    if not filename.endswith('.html') or filename in ['index.html', 'index_backup.html']:
        continue
    
    filepath = os.path.join(dir_path, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    original = content
    
    # --- 1. REPLACE HEADER ---
    head_start = content.find('<!-- Site Header -->')
    if head_start == -1:
        head_start = content.find('<header class="site-header">')
        
    active_script_end = -1
    if head_start != -1:
        # Find Active Link script block
        active_str = '<!-- Active Link Script -->'
        act_idx = content.find(active_str)
        if act_idx != -1:
             scr_end = content.find('</script>', act_idx)
             if scr_end != -1:
                 active_script_end = scr_end + 9
                 
    if head_start != -1 and active_script_end != -1:
        content = content[:head_start] + new_header + "\n" + content[active_script_end:]
    else:
        # Fallback Replacement using regex if pristine structure isn't exactly matched
        content = re.sub(r'(?s)<!-- Site Header -->.*?<!-- Active Link Script -->.*?</script>', new_header, content)

    # Clean up empty divs right before Blur wrapper if they exist
    content = content.replace('</div>\n    \n    <!-- Blur Wrapper Start', '<!-- Blur Wrapper Start')

    # --- 2. REPLACE FOOTER ---
    foot_start = content.find('<!-- Footer -->')
    if foot_start == -1:
        foot_start = content.find('<footer')
    
    if foot_start != -1:
        foot_end = content.find('</footer>', foot_start)
        if foot_end != -1:
            content = content[:foot_start] + new_footer + "\n" + content[foot_end+9:]

    # --- 3. INJECT STYLES AND FONTS ---
    if 'css/new-theme.css' not in content:
        content = content.replace('</head>', '    <link href="css/new-theme.css" rel="stylesheet" />\n</head>')
    if 'Inter+Tight' not in content:
        content = content.replace('</head>', '    <link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@700&display=swap" rel="stylesheet">\n</head>')

    # --- 4. REPLACE LUCIDE/STICKY SCRIPT ---
    # Find the old <script>lucideIcons();</script> or <script>lucide.createIcons();</script>
    # and replace with our new script logic
    script_pattern = re.compile(r'<script>\s*lucide(?:\.create)?Icons\(\);?\s*</script>', re.DOTALL)
    if script_pattern.search(content):
        content = script_pattern.sub(new_script, content)
    else:
        # Check if the new script is already there
        if 'window.addEventListener(\'scroll\'' not in content:
            content = content.replace('</body>', new_script + '\n</body>')

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print("Safely string-replaced:", filename)

print("Done.")
