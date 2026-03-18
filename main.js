// Premium Zari Works — Main JavaScript
// JARVIS v2.0 — AI-Generated

document.addEventListener('DOMContentLoaded', function() {
    
    // Smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Navbar scroll effect
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(10, 10, 10, 0.98)';
            navbar.style.padding = '10px 0';
        } else {
            navbar.style.background = 'rgba(10, 10, 10, 0.95)';
            navbar.style.padding = '15px 0';
        }
    });
    
    // Form submission
    const leadForm = document.getElementById('leadForm');
    if (leadForm) {
        leadForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = {
                name: document.getElementById('name').value,
                phone: document.getElementById('phone').value,
                email: document.getElementById('email').value,
                service: document.getElementById('service').value,
                message: document.getElementById('message').value,
                timestamp: new Date().toISOString(),
                source: 'website'
            };
            
            // Validate phone
            const phoneRegex = /^[+]?[\d\s-]{10,}$/;
            if (!phoneRegex.test(formData.phone)) {
                alert('Please enter a valid phone number');
                return;
            }
            
            // Send to WhatsApp
            const whatsappMessage = `🌟 NEW LEAD — Premium Zari Works Website
            
📝 Name: ${formData.name}
📞 Phone: ${formData.phone}
📧 Email: ${formData.email}
🎯 Service: ${formData.service}
💬 Message: ${formData.message}`;
            
            const whatsappUrl = `https://wa.me/919876543210?text=${encodeURIComponent(whatsappMessage)}`;
            window.open(whatsappUrl, '_blank');
            
            // Show success message
            alert('✅ Thank you! Your message has been sent. We will contact you soon.');
            
            // Reset form
            leadForm.reset();
            
            // Store lead locally (for analytics)
            storeLead(formData);
        });
    }
    
    // Store lead in localStorage
    function storeLead(leadData) {
        let leads = JSON.parse(localStorage.getItem('zari_leads') || '[]');
        leads.push(leadData);
        localStorage.setItem('zari_leads', JSON.stringify(leads));
    }
    
    // Animation on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe service cards and portfolio items
    document.querySelectorAll('.service-card, .portfolio-item, .feature').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s, transform 0.6s';
        observer.observe(el);
    });
    
    // Mobile menu toggle
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    
    if (hamburger) {
        hamburger.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            this.classList.toggle('active');
        });
    }
    
    // Counter animation
    function animateCounter(element, target, duration = 2000) {
        let start = 0;
        const increment = target / (duration / 16);
        
        function updateCounter() {
            start += increment;
            if (start < target) {
                element.textContent = Math.floor(start) + '+';
                requestAnimationFrame(updateCounter);
            } else {
                element.textContent = target + '+';
            }
        }
        
        updateCounter();
    }
    
    // Animate stats on scroll
    const statsObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const statNumbers = entry.target.querySelectorAll('.stat-number');
                statNumbers.forEach(stat => {
                    const target = parseInt(stat.textContent);
                    animateCounter(stat, target);
                });
                statsObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    const heroStats = document.querySelector('.hero-stats');
    if (heroStats) {
        statsObserver.observe(heroStats);
    }
    
    console.log('🧵 Premium Zari Works — Website Loaded');
    console.log('🧠 Powered by JARVIS v2.0');
});
