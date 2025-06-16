// static/js/inicio.js - JavaScript mejorado para VueloReserva

document.addEventListener('DOMContentLoaded', function() {
    
    // ========== INICIALIZACIÓN DEL CARRUSEL ==========
    initializeCarousel();
    
    // ========== SCROLL SUAVE ==========
    initializeSmoothScroll();
    
    // ========== ANIMACIONES AL HACER SCROLL ==========
    initializeScrollAnimations();
    
    // ========== FORMULARIO DE BÚSQUEDA ==========
    initializeSearchForm();
    
    // ========== EFECTOS VISUALES ADICIONALES ==========
    initializeVisualEffects();
    
    // ========== NAVEGACIÓN INTELIGENTE ==========
    initializeSmartNavigation();
});

// ========== FUNCIONES PRINCIPALES ==========

function initializeCarousel() {
    const carouselElement = document.querySelector('#heroCarousel');
    if (!carouselElement) {
        console.warn('⚠️ Elemento carrusel no encontrado');
        return;
    }
    
    // Verificar si Bootstrap está disponible
    if (!window.bootstrap) {
        console.warn('⚠️ Bootstrap no está disponible');
        return;
    }
    
    try {
        // Configuración del carrusel
        const carousel = new bootstrap.Carousel(carouselElement, {
            interval: 6000,
            ride: 'carousel',
            pause: 'hover',
            wrap: true,
            touch: true
        });
        
        // Añadir efectos de transición personalizados
        carouselElement.addEventListener('slide.bs.carousel', function(event) {
            const activeSlide = event.relatedTarget;
            
            // Animar contenido del slide entrante
            if (activeSlide) {
                const content = activeSlide.querySelectorAll('.fade-in-up');
                content.forEach((element, index) => {
                    element.style.opacity = '0';
                    element.style.transform = 'translateY(30px)';
                    
                    setTimeout(() => {
                        element.style.transition = 'all 0.8s ease';
                        element.style.opacity = '1';
                        element.style.transform = 'translateY(0)';
                    }, index * 200 + 300);
                });
            }
        });
        
        // ===== CONTROLES DE TECLADO MEJORADOS =====
        let carouselFocused = false;
        
        // Detectar si el carrusel está en viewport
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                carouselFocused = entry.isIntersecting;
            });
        }, { threshold: 0.3 });
        
        observer.observe(carouselElement);
        
        // Control con teclado - solo cuando el carrusel está visible
        document.addEventListener('keydown', function(e) {
            // Solo funcionar si el carrusel está visible y no hay input activo
            if (!carouselFocused || document.activeElement.tagName === 'INPUT') return;
            
            switch(e.key) {
                case 'ArrowLeft':
                    e.preventDefault();
                    carousel.prev();
                    console.log('⬅️ Carrusel: anterior');
                    break;
                case 'ArrowRight':
                    e.preventDefault();
                    carousel.next();
                    console.log('➡️ Carrusel: siguiente');
                    break;
                case ' ': // Espacio para pausar/reanudar
                    e.preventDefault();
                    if (carouselElement.classList.contains('paused')) {
                        carousel.cycle();
                        carouselElement.classList.remove('paused');
                    } else {
                        carousel.pause();
                        carouselElement.classList.add('paused');
                    }
                    break;
            }
        });
        
        // ===== CONTROLES MANUALES =====
        // Asegurar que los botones prev/next funcionen
        const prevBtn = carouselElement.querySelector('.carousel-control-prev');
        const nextBtn = carouselElement.querySelector('.carousel-control-next');
        
        if (prevBtn) {
            prevBtn.addEventListener('click', function(e) {
                // e.preventDefault(); // Eliminado para compatibilidad Bootstrap
                carousel.prev();
                console.log('🔄 Botón anterior clickeado');
            });
        }
        
        if (nextBtn) {
            nextBtn.addEventListener('click', function(e) {
                // e.preventDefault(); // Eliminado para compatibilidad Bootstrap
                carousel.next();
                console.log('🔄 Botón siguiente clickeado');
            });
        }
        
        // Controles de indicadores
        const indicators = carouselElement.querySelectorAll('[data-bs-slide-to]');
        indicators.forEach((indicator, index) => {
            indicator.addEventListener('click', function(e) {
                e.preventDefault();
                carousel.to(index);
                console.log(` Ir al slide ${index}`);
            });
        });
        
        // ===== CONTROLES TÁCTILES MEJORADOS (para móviles) =====
        let startX = 0;
        let endX = 0;
        
        carouselElement.addEventListener('touchstart', function(e) {
            startX = e.touches[0].clientX;
        }, { passive: true });
        
        carouselElement.addEventListener('touchend', function(e) {
            endX = e.changedTouches[0].clientX;
            handleSwipe();
        }, { passive: true });
        
        function handleSwipe() {
            const threshold = 50; // mínima distancia para considerar swipe
            const diff = startX - endX;
            
            if (Math.abs(diff) > threshold) {
                if (diff > 0) {
                    // Swipe izquierda (siguiente)
                    carousel.next();
                } else {
                    // Swipe derecha (anterior)
                    carousel.prev();
                }
            }
        }
        
        console.log('✅ Carrusel inicializado correctamente con todos los controles');
        
        // Debugging: Mostrar qué controles están disponibles
        console.log('🎮 Controles disponibles:');
        console.log('- Flechas ← → (cuando carrusel visible)');
        console.log('- Espacio (pausar/reanudar)');
        console.log('- Botones prev/next');
        console.log('- Indicadores');
        console.log('- Swipe en móviles');
        
    } catch (error) {
        console.error('❌ Error al inicializar carrusel:', error);
    }
}

function initializeSmoothScroll() {
    // Scroll suave mejorado con offset para navbar fijo
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Validar que el href no esté vacío y el elemento exista
            if (href.length <= 1) return;
            
            const targetElement = document.querySelector(href);
            if (!targetElement) return;
            
            e.preventDefault();
            
            // Calcular offset para navbar fijo (si existe)
            const navbar = document.querySelector('.navbar');
            const offset = navbar ? navbar.offsetHeight + 20 : 20;
            
            // Scroll suave con offset
            const targetPosition = targetElement.offsetTop - offset;
            
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
            
            // Añadir efecto de highlight temporal
            targetElement.style.transition = 'all 0.3s ease';
            targetElement.style.transform = 'scale(1.02)';
            
            setTimeout(() => {
                targetElement.style.transform = 'scale(1)';
            }, 300);
        });
    });
}

function initializeScrollAnimations() {
    // Crear observer para animaciones al hacer scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                
                // Animar elementos hijos con delay
                const children = entry.target.querySelectorAll('.animate-child');
                children.forEach((child, index) => {
                    setTimeout(() => {
                        child.classList.add('animate-in');
                    }, index * 100);
                });
            }
        });
    }, observerOptions);
    
    // Observar elementos que necesiten animación
    const animateElements = document.querySelectorAll(
        '.feature-card, .search-card, .cta-card, .section-title, .section-subtitle'
    );
    
    animateElements.forEach(el => {
        el.classList.add('animate-element');
        observer.observe(el);
    });
}

function initializeSearchForm() {
    const searchForm = document.querySelector('#searchForm');
    if (!searchForm) return;
    
    // Validación y efectos del formulario
    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const origen = this.querySelector('input[placeholder*="origen"]').value;
        const destino = this.querySelector('input[placeholder*="destino"]').value;
        const fechaSalida = this.querySelector('input[type="date"]').value;
        
        // Validación básica
        if (!origen || !destino || !fechaSalida) {
            showNotification('Por favor, completa todos los campos obligatorios', 'warning');
            return;
        }
        
        // Validar que la fecha no sea en el pasado
        const today = new Date().toISOString().split('T')[0];
        if (fechaSalida < today) {
            showNotification('La fecha de salida no puede ser en el pasado', 'error');
            return;
        }
        
        // Simular búsqueda con loading
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Buscando...';
        submitBtn.disabled = true;
        
        // Simular delay de búsqueda
        setTimeout(() => {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
            showNotification(`Búsqueda realizada: ${origen} → ${destino}`, 'success');
        }, 2000);
    });
    
    // Auto-completado básico para ciudades (ejemplo)
    const ciudades = [
        'Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Bilbao',
        'Ciudad de México', 'Guadalajara', 'Monterrey', 'Tijuana',
        'New York', 'Los Angeles', 'Miami', 'Chicago', 'Las Vegas'
    ];
    
    const origenInput = searchForm.querySelector('input[placeholder*="origen"]');
    const destinoInput = searchForm.querySelector('input[placeholder*="destino"]');
    
    [origenInput, destinoInput].forEach(input => {
        if (input) {
            input.addEventListener('input', function() {
                // Aquí podrías implementar un sistema de autocompletado más sofisticado
                this.style.borderColor = this.value.length > 2 ? '#059669' : '#e2e8f0';
            });
        }
    });
}

function initializeVisualEffects() {
    // Efecto parallax suave en el hero
    const heroElements = document.querySelectorAll('.hero-content');
    
    window.addEventListener('scroll', throttle(() => {
        const scrolled = window.pageYOffset;
        const rate = scrolled * -0.5;
        
        heroElements.forEach(hero => {
            if (hero.offsetTop < scrolled + window.innerHeight) {
                hero.style.transform = `translateY(${rate}px)`;
            }
        });
    }, 16));
    
    // Efecto hover mejorado en cards
    document.querySelectorAll('.feature-card, .search-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Efecto de typing en títulos (opcional)
    const heroTitles = document.querySelectorAll('.hero-title');
    heroTitles.forEach((title, index) => {
        setTimeout(() => {
            animateTyping(title);
        }, index * 1000);
    });
    
    // Contador animado en estadísticas
    animateCounters();
}

function initializeSmartNavigation() {
    // Detectar dirección del scroll para efectos
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', throttle(() => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const isScrollingDown = scrollTop > lastScrollTop;
        
        // Cambiar opacidad del hero basado en scroll
        const hero = document.querySelector('.hero-carousel');
        if (hero) {
            const opacity = Math.max(0, 1 - (scrollTop / hero.offsetHeight));
            hero.style.opacity = opacity;
        }
        
        lastScrollTop = scrollTop;
    }, 16));
    
    // Navegación con teclado mejorada
    document.addEventListener('keydown', function(e) {
        // Scroll suave con teclas
        if (e.key === 'Home') {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
        if (e.key === 'End') {
            e.preventDefault();
            window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
        }
    });
}

// ========== FUNCIONES AUXILIARES ==========

function showNotification(message, type = 'info') {
    // Crear notification toast
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${getIconForType(type)} me-2"></i>
            <span>${message}</span>
            <button class="notification-close">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    // Estilos inline para la notificación
    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        zIndex: '9999',
        padding: '1rem 1.5rem',
        borderRadius: '10px',
        color: 'white',
        fontSize: '0.9rem',
        fontWeight: '500',
        boxShadow: '0 10px 30px rgba(0,0,0,0.2)',
        transform: 'translateX(400px)',
        transition: 'all 0.3s ease',
        maxWidth: '400px',
        backgroundColor: getColorForType(type)
    });
    
    document.body.appendChild(notification);
    
    // Animar entrada
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Auto-remove después de 5 segundos
    const autoRemove = setTimeout(() => {
        removeNotification(notification);
    }, 5000);
    
    // Botón de cerrar
    notification.querySelector('.notification-close').addEventListener('click', () => {
        clearTimeout(autoRemove);
        removeNotification(notification);
    });
}

function removeNotification(notification) {
    notification.style.transform = 'translateX(400px)';
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 300);
}

function getIconForType(type) {
    const icons = {
        success: 'check-circle',
        error: 'exclamation-circle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };
    return icons[type] || icons.info;
}

function getColorForType(type) {
    const colors = {
        success: '#059669',
        error: '#dc2626',
        warning: '#d97706',
        info: '#2563eb'
    };
    return colors[type] || colors.info;
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

function animateTyping(element) {
    if (!element) return;
    
    const text = element.textContent;
    element.textContent = '';
    element.style.borderRight = '2px solid white';
    
    let i = 0;
    const typeInterval = setInterval(() => {
        element.textContent += text.charAt(i);
        i++;
        
        if (i >= text.length) {
            clearInterval(typeInterval);
            setTimeout(() => {
                element.style.borderRight = 'none';
            }, 1000);
        }
    }, 100);
}

function animateCounters() {
    const counters = document.querySelectorAll('.stat-number');
    
    counters.forEach(counter => {
        const target = counter.textContent;
        const numericValue = parseInt(target.replace(/\D/g, ''));
        
        if (isNaN(numericValue)) return;
        
        let current = 0;
        const increment = numericValue / 50;
        const suffix = target.replace(/[\d,]/g, '');
        
        const updateCounter = () => {
            current += increment;
            if (current < numericValue) {
                counter.textContent = Math.floor(current) + suffix;
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target;
            }
        };
        
        // Iniciar animación cuando el elemento sea visible
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    updateCounter();
                    observer.unobserve(counter);
                }
            });
        });
        
        observer.observe(counter);
    });
}

// ========== CSS DINÁMICO PARA ANIMACIONES ==========
const style = document.createElement('style');
style.textContent = `
    .animate-element {
        opacity: 0;
        transform: translateY(30px);
        transition: all 0.8s ease;
    }
    
    .animate-element.animate-in {
        opacity: 1;
        transform: translateY(0);
    }
    
    .animate-child {
        opacity: 0;
        transform: translateX(-20px);
        transition: all 0.6s ease;
    }
    
    .animate-child.animate-in {
        opacity: 1;
        transform: translateX(0);
    }
    
    .notification-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .notification-close {
        background: none;
        border: none;
        color: inherit;
        cursor: pointer;
        padding: 0;
        margin-left: 1rem;
        opacity: 0.8;
        transition: opacity 0.2s ease;
    }
    
    .notification-close:hover {
        opacity: 1;
    }
    
    @media (max-width: 768px) {
        .notification {
            left: 20px;
            right: 20px;
            transform: translateY(-100px) !important;
        }
        
        .notification.show {
            transform: translateY(0) !important;
        }
    }
`;

document.head.appendChild(style);

console.log('🚀 VueloReserva JavaScript cargado correctamente');