/**
 * Eco-Friendly Marketplace - Main JavaScript File
 * Global functions and interactions
 */

// Document Ready Function
document.addEventListener('DOMContentLoaded', function() {
    console.log('🌱 Eco-Friendly Marketplace Loaded');

    // Initialize all components
    initializeTooltips();
    initializeScrollAnimations();
    initializeCategoryCards();
    initializeSearchFeatures();
    initializeFormEnhancements();
    initializeNavigationEffects();
    initializeEcoCounters();

    // Show welcome message
    showWelcomeMessage();
});

/**
 * Initialize Bootstrap Tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Scroll Animations
 */
function initializeScrollAnimations() {
    const animateElements = document.querySelectorAll('.scroll-animate');

    if (animateElements.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate');
                    entry.target.style.animationDelay = Math.random() * 0.5 + 's';
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        animateElements.forEach(el => observer.observe(el));
    }
}

/**
 * Category Cards Interactive Effects
 */
function initializeCategoryCards() {
    const categoryCards = document.querySelectorAll('.category-card');

    categoryCards.forEach(card => {
        // Hover effects
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
            this.style.transition = 'all 0.3s ease';

            // Add ripple effect
            createRippleEffect(this, event);
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });

        // Click analytics (for future implementation)
        card.addEventListener('click', function() {
            const categoryName = this.querySelector('h6').textContent;
            trackCategoryClick(categoryName);
        });
    });
}

/**
 * Create Ripple Effect
 */
function createRippleEffect(element, event) {
    const ripple = document.createElement('span');
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;

    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';
    ripple.classList.add('ripple');

    element.appendChild(ripple);

    setTimeout(() => {
        ripple.remove();
    }, 600);
}

/**
 * Search Features Enhancement
 */
function initializeSearchFeatures() {
    const searchInputs = document.querySelectorAll('input[type="search"]');

    searchInputs.forEach(input => {
        // Auto-suggest functionality (placeholder for future)
        input.addEventListener('input', function() {
            const query = this.value.trim();
            if (query.length >= 2) {
                // Future: Implement auto-suggest
                showSearchSuggestions(query);
            } else {
                hideSearchSuggestions();
            }
        });

        // Search analytics
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                trackSearch(this.value);
            }
        });
    });
}

/**
 * Form Enhancements
 */
function initializeFormEnhancements() {
    // Add floating labels effect
    const formInputs = document.querySelectorAll('.form-control');

    formInputs.forEach(input => {
        // Focus effects
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });

        input.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('focused');
            }
        });

        // Validation feedback
        input.addEventListener('input', function() {
            validateField(this);
        });
    });

    // Newsletter signup
    const newsletterForm = document.querySelector('footer form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', handleNewsletterSignup);
    }
}

/**
 * Navigation Effects
 */
function initializeNavigationEffects() {
    const navbar = document.querySelector('.navbar');

    // Scroll effect
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }
    });

    // Mobile menu enhancements
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');

    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener('click', function() {
            this.classList.toggle('active');
        });
    }
}

/**
 * Eco-friendly Counters Animation
 */
function initializeEcoCounters() {
    const counters = document.querySelectorAll('[data-count]');

    const animateCounters = () => {
        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-count'));
            const current = parseInt(counter.textContent.replace(/[^\d]/g, ''));
            const increment = target / 100;

            if (current < target) {
                counter.textContent = Math.ceil(current + increment).toLocaleString();
                setTimeout(animateCounters, 20);
            } else {
                counter.textContent = target.toLocaleString();
            }
        });
    };

    // Start animation when counters are visible
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounters();
                observer.unobserve(entry.target);
            }
        });
    });

    counters.forEach(counter => observer.observe(counter));
}

/**
 * Show Welcome Message
 */
function showWelcomeMessage() {
    // Check if user is new (using localStorage)
    const isNewUser = !localStorage.getItem('visited');

    if (isNewUser) {
        setTimeout(() => {
            showNotification('🌱 Welcome to our Eco-Friendly Marketplace!', 'success');
            localStorage.setItem('visited', 'true');
        }, 1000);
    }
}

/**
 * Show Search Suggestions (placeholder for future implementation)
 */
function showSearchSuggestions(query) {
    // Future: Implement AJAX search suggestions
    console.log('Search suggestion for:', query);
}

/**
 * Hide Search Suggestions
 */
function hideSearchSuggestions() {
    const suggestions = document.querySelector('.search-suggestions');
    if (suggestions) {
        suggestions.style.display = 'none';
    }
}

/**
 * Track Category Click (Analytics placeholder)
 */
function trackCategoryClick(categoryName) {
    console.log('Category clicked:', categoryName);
    // Future: Send to analytics service
}

/**
 * Track Search (Analytics placeholder)
 */
function trackSearch(query) {
    console.log('Search performed:', query);
    // Future: Send to analytics service
}

/**
 * Validate Form Field
 */
function validateField(field) {
    const value = field.value.trim();
    const fieldType = field.type;
    let isValid = true;
    let message = '';

    // Remove existing validation classes
    field.classList.remove('is-valid', 'is-invalid');

    // Basic validation rules
    switch (fieldType) {
        case 'email':
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            isValid = emailRegex.test(value);
            message = isValid ? '' : 'Please enter a valid email address';
            break;

        case 'password':
            isValid = value.length >= 6;
            message = isValid ? '' : 'Password must be at least 6 characters';
            break;

        case 'text':
            isValid = value.length >= 2;
            message = isValid ? '' : 'This field requires at least 2 characters';
            break;
    }

    // Required field check
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        message = 'This field is required';
    }

    // Apply validation styling
    if (value) {
        field.classList.add(isValid ? 'is-valid' : 'is-invalid');

        // Show/hide feedback message
        let feedback = field.nextElementSibling;
        if (feedback && feedback.classList.contains('invalid-feedback')) {
            feedback.textContent = message;
        } else if (!isValid) {
            feedback = document.createElement('div');
            feedback.className = 'invalid-feedback';
            feedback.textContent = message;
            field.parentNode.insertBefore(feedback, field.nextSibling);
        }
    }

    return isValid;
}

/**
 * Handle Newsletter Signup
 */
function handleNewsletterSignup(event) {
    event.preventDefault();

    const emailInput = event.target.querySelector('input[type="email"]');
    const email = emailInput.value.trim();

    if (validateField(emailInput)) {
        // Show loading state
        const submitBtn = event.target.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        submitBtn.disabled = true;

        // Simulate API call
        setTimeout(() => {
            showNotification('🌱 Thank you for subscribing to our eco-newsletter!', 'success');
            emailInput.value = '';
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }, 1500);
    }
}

/**
 * Show Notification
 */
function showNotification(message, type = 'info', duration = 4000) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    `;

    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    // Add to page
    document.body.appendChild(notification);

    // Auto-remove after duration
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, duration);
}

/**
 * Utility Functions
 */

// Smooth scroll to element
function scrollToElement(elementId, offset = 0) {
    const element = document.getElementById(elementId);
    if (element) {
        const elementPosition = element.offsetTop - offset;
        window.scrollTo({
            top: elementPosition,
            behavior: 'smooth'
        });
    }
}

// Format currency
function formatCurrency(amount, currency = 'USD') {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency
    }).format(amount);
}

// Debounce function for search
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            timeout = null;
            if (!immediate) func(...args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func(...args);
    };
}

// Check if element is in viewport
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

// Local Storage helpers
const storage = {
    set: (key, value) => {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (e) {
            console.warn('LocalStorage not available:', e);
        }
    },

    get: (key, defaultValue = null) => {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (e) {
            console.warn('LocalStorage not available:', e);
            return defaultValue;
        }
    },

    remove: (key) => {
        try {
            localStorage.removeItem(key);
        } catch (e) {
            console.warn('LocalStorage not available:', e);
        }
    }
};

/**
 * Performance Monitoring
 */
function initializePerformanceMonitoring() {
    // Monitor page load time
    window.addEventListener('load', () => {
        const loadTime = performance.now();
        console.log(`🚀 Page loaded in ${Math.round(loadTime)}ms`);

        // Track slow loading
        if (loadTime > 3000) {
            console.warn('⚠️ Slow page load detected');
        }
    });
}

/**
 * Error Handling
 */
window.addEventListener('error', function(event) {
    console.error('🚨 JavaScript Error:', event.error);

    // Show user-friendly error message for critical errors
    if (event.error.name === 'TypeError' || event.error.name === 'ReferenceError') {
        showNotification('⚠️ Something went wrong. Please refresh the page.', 'warning');
    }
});

/**
 * Accessibility Enhancements
 */
function initializeAccessibility() {
    // Keyboard navigation for cards
    const cards = document.querySelectorAll('.card, .category-card');

    cards.forEach(card => {
        card.setAttribute('tabindex', '0');

        card.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    });

    // Skip to main content link
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.textContent = 'Skip to main content';
    skipLink.className = 'sr-only sr-only-focusable btn btn-primary';
    skipLink.style.cssText = `
        position: absolute;
        top: -40px;
        left: 6px;
        z-index: 10000;
        padding: 8px 16px;
    `;

    skipLink.addEventListener('focus', function() {
        this.style.top = '6px';
    });

    skipLink.addEventListener('blur', function() {
        this.style.top = '-40px';
    });

    document.body.insertBefore(skipLink, document.body.firstChild);
}

/**
 * Initialize everything when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function() {
    initializePerformanceMonitoring();
    initializeAccessibility();
});

/**
 * Export functions for use in other scripts
 */
window.EcoMarketplace = {
    showNotification,
    scrollToElement,
    formatCurrency,
    storage,
    validateField,
    debounce,
    isInViewport
};