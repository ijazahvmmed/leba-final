import os
import re

MENU_HTML = r"""
<!-- Mobile Menu Overlay -->
<div class="mobile-menu-overlay" id="mobileMenuGlobal">
    <div class="mobile-menu-header">
        <a class="logo" href="index.html">©Leba Papers</a>
        <button class="mobile-menu-close" id="mobileMenuCloseGlobal" aria-label="Close menu">
            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
        </button>
    </div>
    <div class="mobile-menu-links">
        <a href="about.html" class="mobile-top-link">COMPANY</a>
        
        <div class="mobile-accordion">
            <button class="mobile-accordion-btn">GRAPHIC SPECIALITY <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="chevron"><path d="m6 9 6 6 6-6"/></svg></button>
            <div class="mobile-accordion-content">
                <div class="mobile-sub-group">
                    <h4>Covering</h4>
                    <a href="covering-buckram.html">Buckram</a>
                    <a href="covering-classy-covers.html">Classy Covers</a>
                </div>
                <div class="mobile-sub-group">
                    <h4>White &amp; Cream</h4>
                    <a href="whitecream-eco-cream.html">Eco Cream</a>
                    <a href="whitecream-ecowhite.html">Eco White</a>
                </div>
                <div class="mobile-sub-group">
                    <h4>Kraft &amp; Recycled</h4>
                    <a href="kraft-papers-boards.html">Kraft Papers</a>
                    <a href="blackpaperboard-brilliantblack.html">Brilliant Black</a>
                </div>
                <div class="mobile-sub-group">
                    <h4>Textures &amp; Art</h4>
                    <a href="textures.html">Textured Boards</a>
                    <a href="textures-perfumed-paper-board.html">Perfumed Paper Board</a>
                </div>
            </div>
        </div>

        <div class="mobile-accordion">
            <button class="mobile-accordion-btn">LABELS <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="chevron"><path d="m6 9 6 6 6-6"/></svg></button>
            <div class="mobile-accordion-content">
                <div class="mobile-sub-group">
                    <h4>Paper Labels</h4>
                    <a href="maplitho-paper-labels.html">Maplitho</a>
                    <a href="chromo-paper-labels.html">Chromo</a>
                    <a href="highgloss-paper-labels.html">High Gloss</a>
                </div>
                <div class="mobile-sub-group">
                    <h4>Film Labels</h4>
                    <a href="pvcclear-film-labels.html">PVC Clear</a>
                    <a href="synthetic-film-labels.html">Synthetic</a>
                </div>
                <div class="mobile-sub-group">
                    <h4>Special Labels</h4>
                    <a href="removable-special-labels.html">Removable</a>
                    <a href="kraftpaper-special-labels.html">Kraft Paper</a>
                </div>
            </div>
        </div>

        <div class="mobile-accordion">
            <button class="mobile-accordion-btn">DIGITAL PRINT <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="chevron"><path d="m6 9 6 6 6-6"/></svg></button>
            <div class="mobile-accordion-content">
                <div class="mobile-sub-group" style="margin-top:0;">
                    <a href="digital-laser-printer-film.html">Laser Printer Film</a>
                    <a href="digital-hp-indigo-sheet.html">HP Indigo</a>
                    <a href="digital-dry-toner.html">Dry Toner</a>
                </div>
            </div>
        </div>

        <a href="contact.html" class="mobile-top-link">CONTACT</a>
    </div>
    <div class="mobile-menu-footer">
        <div class="footer-block">
            <strong>Sales issues</strong>
            <a href="tel:+919388555999">+91 93 88 555 999</a>
            <a href="mailto:lebapapers@gmail.com">lebapapers@gmail.com</a>
        </div>
        <div class="footer-block">
            <strong>Office</strong>
            <p>31/741A, Vyttila Junction<br>Ernakulam – 19<br>Kerala, India</p>
        </div>
    </div>
</div>

<script>
    document.addEventListener('DOMContentLoaded', function() {
        const menuBtn = document.querySelector('.mobile-menu-btn');
        const closeBtn = document.getElementById('mobileMenuCloseGlobal');
        const overlay = document.getElementById('mobileMenuGlobal');
        
        if(menuBtn && closeBtn && overlay) {
            menuBtn.addEventListener('click', function(e) {
                e.preventDefault();
                overlay.classList.add('active');
                document.body.style.overflow = 'hidden';
            });
            
            closeBtn.addEventListener('click', function() {
                overlay.classList.remove('active');
                document.body.style.overflow = '';
            });
        }

        const accordions = document.querySelectorAll('.mobile-accordion-btn');
        accordions.forEach(acc => {
            acc.addEventListener('click', function() {
                this.classList.toggle('active');
                const content = this.nextElementSibling;
                if (content.style.maxHeight) {
                    content.style.maxHeight = null;
                } else {
                    content.style.maxHeight = content.scrollHeight + "px";
                }
            });
        });
    });
</script>
"""

HAMBURGER_HTML = r"""<button class="mobile-menu-btn" aria-label="Toggle menu"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-menu"><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/></svg></button>"""

def inject_mobile_menu(directory):
    html_files = [f for f in os.listdir(directory) if f.endswith('.html')]
    success_count = 0
    
    for filename in html_files:
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        original_content = content
            
        # 1. Inject the hamburger button into .nav-pill right before </nav>
        if 'class="mobile-menu-btn"' not in content:
            nav_end = re.search(r'</nav>', content)
            if nav_end:
                content = content[:nav_end.start()] + '\n            ' + HAMBURGER_HTML + '\n        ' + content[nav_end.start():]
                
        # 2. Inject the mobile menu overlay and script right before </body>
        # First remove old block if it exists
        old_block_pattern = re.compile(r'<!-- Mobile Menu Overlay -->.*?<div class="mobile-menu-overlay" id="mobileMenuGlobal">.*?</script>', re.DOTALL)
        content = old_block_pattern.sub('', content)
        
        body_end = re.search(r'</body>', content)
        if body_end:
            content = content[:body_end.start()] + MENU_HTML + '\n' + content[body_end.start():]
                
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(content)
            success_count += 1
            
    print(f"✅ Injected mobile menu into {success_count} files out of {len(html_files)}")

if __name__ == "__main__":
    inject_mobile_menu(r"c:\Users\ijasa\OneDrive\Desktop\opleba")
