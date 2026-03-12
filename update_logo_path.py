import os

def replace_logo_filename(directory):
    html_files = [f for f in os.listdir(directory) if f.endswith('.html')]
    success_count = 0
    
    old_path = 'images/logo.png'
    new_path = 'images/logohanbee.png'
    
    for filename in html_files:
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        if old_path in content:
            new_content = content.replace(old_path, new_path)
            with open(filepath, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(new_content)
            success_count += 1
            
    print(f"✅ Replaced logo filename in {success_count} files.")

if __name__ == "__main__":
    replace_logo_filename(r"c:\Users\ijasa\OneDrive\Desktop\opleba")
