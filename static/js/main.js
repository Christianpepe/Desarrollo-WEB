// static/js/main.js

document.addEventListener('DOMContentLoaded', function() {
    
    // Inicializar animaciones
    initAnimations();
    
    // Mejorar formularios
    enhanceForms();
    
    // Mejorar alertas
    enhanceAlerts();
    
    // Mejorar navbar
    enhanceNavbar();
    
    // Inicializar tooltips de Bootstrap si existen
    initTooltips();
});

// Función para inicializar animaciones
function initAnimations() {
    // Agregar clase de animación a elementos visibles
    const elements = document.querySelectorAll('.auth-card, .hero-section');
    elements.forEach(el => {
        el.classList.add('fade-in-up');
    });
    
    // Animación de entrada para alertas
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach((alert, index) => {
        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-20px)';
        setTimeout(() => {
            alert.style.transition = 'all 0.3s ease';
            alert.style.opacity = '1';
            alert.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// Función para mejorar formularios
function enhanceForms() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        // Agregar loading state a botones de submit
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            form.addEventListener('submit', function() {
                submitBtn.disabled = true;
                const originalText = submitBtn.textContent;
                submitBtn.innerHTML = '<span class="loading-spinner"></span> Procesando...';
                
                // Restaurar botón después de 3 segundos si no hay redirección
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.textContent = originalText;
                }, 3000);
            });
        }
        
        // Mejorar campos de entrada
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            // Agregar efectos de focus
            input.addEventListener('focus', function() {
                this.parentElement.classList.add('focused');
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.classList.remove('focused');
                // Validación en tiempo real
                validateField(this);
            });
            
            // Quitar addFieldIcon(input); para no modificar la posición ni agregar iconos
            // Restaurar padding y posición por defecto
            input.style.paddingLeft = '';
            if (input.parentElement) input.parentElement.style.position = '';
        });
    });
}

// Función para validar campos individuales
function validateField(field) {
    const value = field.value.trim();
    const fieldType = field.type || field.tagName.toLowerCase();
    
    // Remover clases de validación previas
    field.classList.remove('is-valid', 'is-invalid');
    
    let isValid = true;
    let message = '';
    
    // Validaciones básicas
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        message = 'Este campo es obligatorio';
    } else if (fieldType === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            isValid = false;
            message = 'Ingresa un email válido';
        }
    } else if (field.name === 'telefono' && value) {
        const phoneRegex = /^[\d\s\-\+\(\)]+$/;
        if (!phoneRegex.test(value) || value.length < 10) {
            isValid = false;
            message = 'Ingresa un teléfono válido';
        }
    } else if (field.name === 'username' && value) {
        if (value.length < 3) {
            isValid = false;
            message = 'El nombre de usuario debe tener al menos 3 caracteres';
        }
    }
    
    // Aplicar estilos de validación
    field.classList.add(isValid ? 'is-valid' : 'is-invalid');
    
    // Mostrar mensaje de error personalizado
    showFieldMessage(field, message, isValid);
}

// Función para mostrar mensajes de campo
function showFieldMessage(field, message, isValid) {
    // Remover mensaje previo
    const existingMessage = field.parentElement.querySelector('.field-message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    if (!isValid && message) {
        const messageEl = document.createElement('div');
        messageEl.className = 'field-message text-danger mt-1';
        messageEl.style.fontSize = '0.875rem';
        messageEl.textContent = message;
        field.parentElement.appendChild(messageEl);
    }
}

// Función para mejorar alertas
function enhanceAlerts() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        // Auto-dismiss para alertas de éxito
        if (alert.classList.contains('alert-success')) {
            setTimeout(() => {
                dismissAlert(alert);
            }, 5000);
        }
        
        // Agregar botón de cerrar si no existe
        if (!alert.querySelector('.btn-close')) {
            const closeBtn = document.createElement('button');
            closeBtn.className = 'btn-close';
            closeBtn.setAttribute('aria-label', 'Cerrar');
            closeBtn.onclick = () => dismissAlert(alert);
            alert.appendChild(closeBtn);
        }
    });
}

// Función para descartar alertas
function dismissAlert(alert) {
    alert.style.transition = 'all 0.3s ease';
    alert.style.opacity = '0';
    alert.style.transform = 'translateY(-20px)';
    
    setTimeout(() => {
        alert.remove();
    }, 300);
}

// Función para mejorar navbar
function enhanceNavbar() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    
    // Efecto de scroll
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
    
    // Mejorar navegación móvil
    const navbarToggler = navbar.querySelector('.navbar-toggler');
    const navbarCollapse = navbar.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener('click', function() {
            // Agregar animación personalizada
            setTimeout(() => {
                if (navbarCollapse.classList.contains('show')) {
                    navbarCollapse.style.animation = 'fadeInDown 0.3s ease';
                }
            }, 10);
        });
    }
}

// Función para inicializar tooltips
function initTooltips() {
    // Solo si Bootstrap está cargado
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

// Función para mostrar notificaciones personalizadas
function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} notification-custom`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        box-shadow: var(--shadow-heavy);
        transform: translateX(400px);
        transition: transform 0.3s ease;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Mostrar notificación
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 10);
    
    // Ocultar después del tiempo especificado
    setTimeout(() => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, duration);
}

// Función para confirmar acciones
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Utilidades adicionales
const Utils = {
    // Formatear número de teléfono
    formatPhone: function(phone) {
        const cleaned = phone.replace(/\D/g, '');
        const match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/);
        if (match) {
            return '(' + match[1] + ') ' + match[2] + '-' + match[3];
        }
        return phone;
    },
    
    // Validar email
    isValidEmail: function(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },
    
    // Generar ID único
    generateId: function() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }
};

// Exportar utilidades globalmente
window.VueloReserva = {
    showNotification,
    confirmAction,
    Utils
};