// Performance Optimizations for Phi-Chain Website

// Debounce function for scroll and resize events
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

// Throttle function for high-frequency events
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Smooth scrolling for navigation links with performance optimization
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
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

// Animate elements on scroll with Intersection Observer (more performant than scroll events)
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            // Unobserve after animation to free up resources
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe vision cards
document.querySelectorAll('.vision-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(card);
});

// Observe architecture cards
document.querySelectorAll('.arch-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(card);
});

// Observe resource cards
document.querySelectorAll('.resource-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(card);
});

// Observe wallet cards
document.querySelectorAll('.wallet-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(card);
});

// Observe feature cards
document.querySelectorAll('.feature-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(card);
});

// Observe use-case cards
document.querySelectorAll('.use-case-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(card);
});

// Performance: Use requestAnimationFrame for smooth animations
let ticking = false;

window.addEventListener('scroll', throttle(() => {
    if (!ticking) {
        requestAnimationFrame(() => {
            // Any scroll-based animations can go here
            ticking = false;
        });
        ticking = true;
    }
}, 100));

// Lazy load images with data-src attribute
function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.getAttribute('data-src');
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Preload critical resources
function preloadCriticalResources() {
    const criticalLinks = [
        'blockchain-simulator.html',
        'fibonacci-viz.html',
        'comparison.html'
    ];
    
    criticalLinks.forEach(link => {
        const preloadLink = document.createElement('link');
        preloadLink.rel = 'prefetch';
        preloadLink.href = link;
        document.head.appendChild(preloadLink);
    });
}

// Remove skeleton loading screen with smooth transition
function removeSkeleton() {
    const body = document.body;
    const skeleton = document.getElementById('skeleton-container');
    
    if (!skeleton) return;
    
    // Add fade-out class to skeleton
    skeleton.classList.add('skeleton-fade-out');
    
    // Wait for fade-out animation to complete, then remove elements and class
    setTimeout(() => {
        body.classList.remove('skeleton-loading');
        skeleton.remove();
    }, 500); // Matches the 0.5s duration in skeleton-loader.css
}

// Expose to global scope
window.removeSkeleton = removeSkeleton;
window.preloadCriticalResources = preloadCriticalResources;
window.lazyLoadImages = lazyLoadImages;

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Lazy load images
    lazyLoadImages();
    
    // Remove skeleton after a brief moment to ensure initial rendering
    setTimeout(removeSkeleton, 1500);
});

// Preload resources when page is fully loaded
window.addEventListener('load', function() {
    preloadCriticalResources();
});

// Performance: Reduce layout thrashing by batching DOM reads/writes
const domBatchQueue = [];
let batchScheduled = false;

function batchDOMOperation(operation) {
    domBatchQueue.push(operation);
    if (!batchScheduled) {
        batchScheduled = true;
        requestAnimationFrame(() => {
            domBatchQueue.forEach(op => op());
            domBatchQueue.length = 0;
            batchScheduled = false;
        });
    }
}

// Optimize CSS animations with will-change (use sparingly)
document.querySelectorAll('.vision-card, .arch-card, .resource-card, .wallet-card').forEach(card => {
    card.style.willChange = 'transform, opacity';
});

// Clean up will-change after animations
setTimeout(() => {
    document.querySelectorAll('.vision-card, .arch-card, .resource-card, .wallet-card').forEach(card => {
        card.style.willChange = 'auto';
    });
}, 2000);
