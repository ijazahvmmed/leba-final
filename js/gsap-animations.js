document.addEventListener("DOMContentLoaded", () => {
    // Wait for GSAP and tools to load
    if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined' || typeof Lenis === 'undefined' || typeof SplitType === 'undefined') {
        console.warn('GSAP, ScrollTrigger, Lenis, or SplitType missing!');
        return;
    }

    // 1. Lenis Smooth Scroll Setup
    const lenis = new Lenis({
        duration: 1.2,
        easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)), 
        direction: 'vertical',
        gestureDirection: 'vertical',
        smooth: true,
        smoothTouch: false,
    });

    function raf(time) {
        lenis.raf(time);
        requestAnimationFrame(raf);
    }
    requestAnimationFrame(raf);

    // Sync Lenis with ScrollTrigger
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add((time) => {
      lenis.raf(time * 1000);
    });
    gsap.ticker.lagSmoothing(0, 0);

    gsap.registerPlugin(ScrollTrigger);

    // 2. Disable old CSS data-motion styles (GSAP handles it now)
    const style = document.createElement('style');
    style.innerHTML = `
        [data-motion] { transition: none !important; opacity: 1; transform: none; }
        .nav-dropdown { transition: none !important; opacity: 1; visibility: visible; }
    `;
    document.head.appendChild(style);

    // 3. Drawer & Mega Menu Hover Animation
    const navItems = document.querySelectorAll('.nav-item-group');
    
    // Set initial state for mega menus (hidden)
    const megaMenus = document.querySelectorAll('.nav-dropdown');
    gsap.set(megaMenus, { 
        autoAlpha: 0, 
        y: 15,
        scale: 0.98,
        transformOrigin: "top center",
        display: "none"
    });

    navItems.forEach(item => {
        const dropdown = item.querySelector('.nav-dropdown');
        if(!dropdown) return;
        
        let hoverTl = gsap.timeline({ paused: true });
        hoverTl.to(dropdown, {
            autoAlpha: 1,
            display: "grid", // or block, but mega-menu uses grid
            y: 10,
            scale: 1,
            duration: 0.4,
            ease: 'power3.out'
        });
        
        let isHovered = false;
        
        item.addEventListener('mouseenter', () => {
            isHovered = true;
            gsap.killTweensOf(dropdown);
            if (dropdown.classList.contains('mini-menu')) {
                 gsap.set(dropdown, {display: 'block'});
            } else {
                 gsap.set(dropdown, {display: 'grid'});
            }
            gsap.to(dropdown, { autoAlpha: 1, y: 10, scale: 1, duration: 0.4, ease: 'power3.out' });
        });
        
        item.addEventListener('mouseleave', () => {
            isHovered = false;
            gsap.to(dropdown, { 
                autoAlpha: 0, y: 15, scale: 0.98, duration: 0.3, ease: 'power2.in',
                onComplete: () => {
                    if (!isHovered) gsap.set(dropdown, {display: 'none'});
                }
            });
        });
    });

    // 4. Text Strip Animations with SplitType
    // Select headers (excluding button texts or nested un-splittables)
    const textElements = document.querySelectorAll('h1, h2:not(.wwd-title), .intro-text h2, .reveal-text');
    textElements.forEach(el => {
        // Prepare SplitType
        const split = new SplitType(el, { types: 'lines, words, chars' });
        
        // Wrap chars for overflow hidden effect
        split.chars.forEach(char => {
            const wrapper = document.createElement('span');
            wrapper.style.overflow = 'hidden';
            wrapper.style.display = 'inline-block';
            wrapper.style.verticalAlign = 'bottom';
            char.parentNode.insertBefore(wrapper, char);
            wrapper.appendChild(char);
        });

        gsap.from(split.chars, {
            scrollTrigger: {
                trigger: el,
                start: 'top 85%',
                once: true
            },
            yPercent: 120,
            rotationZ: 5,
            opacity: 0,
            duration: 0.8,
            stagger: 0.015,
            ease: 'power4.out'
        });
    });

    // 5. Normal text paragraphs
    const paragraphs = document.querySelectorAll('p:not(.label-text)');
    paragraphs.forEach(p => {
        gsap.from(p, {
            scrollTrigger: {
                trigger: p,
                start: 'top 90%',
                once: true
            },
            y: 30,
            opacity: 0,
            duration: 0.8,
            ease: 'power3.out'
        });
    });

    // 6. Labels/Tags
    const labels = document.querySelectorAll('.label, .label-text');
    labels.forEach(lbl => {
        gsap.from(lbl, {
            scrollTrigger: {
                trigger: lbl,
                start: 'top 90%',
                once: true
            },
            x: -20,
            opacity: 0,
            duration: 0.6,
            ease: 'power2.out'
        });
    });

    // 7. Button Reveal & Interactions
    const buttons = document.querySelectorAll('.btn, .btn-glass, .btn-primary, .btn-header');
    buttons.forEach(btn => {
        gsap.from(btn, {
            scrollTrigger: {
                trigger: btn,
                start: 'top 95%',
                once: true
            },
            y: 30,
            scale: 0.9,
            opacity: 0,
            duration: 0.8,
            ease: 'back.out(1.5)'
        });
        
        // Liquid/Smooth Hover Effect
        btn.addEventListener('mouseenter', () => {
            gsap.to(btn, { scale: 1.05, duration: 0.4, ease: 'expo.out' });
        });
        btn.addEventListener('mouseleave', () => {
            gsap.to(btn, { scale: 1, duration: 0.6, ease: 'elastic.out(1, 0.4)' });
        });
    });

    // 8. Card Grid / Image Staggered Reveals
    const grids = document.querySelectorAll('.cards, .proj-grid, .grid-3, .product-grid');
    grids.forEach(grid => {
        const items = grid.querySelectorAll('.card, .proj-item, .stat, > div');
        if (items.length > 0) {
            gsap.from(items, {
                scrollTrigger: {
                    trigger: grid,
                    start: 'top 85%',
                    once: true
                },
                y: 60,
                opacity: 0,
                scale: 0.95,
                duration: 1,
                stagger: 0.1,
                ease: 'power3.out'
            });
        }
    });

    // 9. Full Width Images (Hero/Banner)
    const banners = document.querySelectorAll('.hero, .banner-sec, .panel-hero-modern');
    banners.forEach(banner => {
        gsap.fromTo(banner, 
            { backgroundPosition: '50% 100%' },
            {
                backgroundPosition: '50% 0%',
                ease: 'none',
                scrollTrigger: {
                    trigger: banner,
                    start: 'top bottom',
                    end: 'bottom top',
                    scrub: true
                }
            }
        );
    });

});
