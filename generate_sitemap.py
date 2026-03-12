import os
from datetime import datetime

def generate_sitemap(directory, base_url):
    html_files = []
    # Only map the root directory files as per current structure
    for filename in os.listdir(directory):
        if filename.endswith('.html') and filename != 'index_backup.html' and filename != 'divider.html':
            html_files.append(filename)

    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    today = datetime.now().strftime('%Y-%m-%d')
    for file in html_files:
        priority = "1.0" if file == "index.html" else "0.8"
        sitemap_content += f'  <url>\n'
        sitemap_content += f'    <loc>{base_url}{file}</loc>\n'
        sitemap_content += f'    <lastmod>{today}</lastmod>\n'
        sitemap_content += f'    <priority>{priority}</priority>\n'
        sitemap_content += f'  </url>\n'

    sitemap_content += '</urlset>'

    with open(os.path.join(directory, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    
    print(f"✅ sitemap.xml generated with {len(html_files)} URLs.")

if __name__ == "__main__":
    generate_sitemap(r"c:\Users\ijasa\OneDrive\Desktop\opleba", "https://lebapapers.com/")
