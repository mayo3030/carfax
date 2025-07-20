/**
 * CARFAX VIN Checker - Main Application
 * Professional and Fast VIN Lookup Tool
 */

class CarfaxApp {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.setupValidation();
        this.initializeApp();
    }

    initializeElements() {
        // Form elements
        this.form = document.getElementById('vinForm');
        this.vinInput = document.getElementById('vinInput');
        this.submitBtn = document.getElementById('submitBtn');
        this.btnText = this.submitBtn.querySelector('.btn-text');
        this.btnLoading = this.submitBtn.querySelector('.btn-loading');

        // UI elements
        this.charCount = document.querySelector('.char-count');
        this.validationStatus = document.querySelector('.validation-status');
        this.resultCard = document.getElementById('resultCard');
        this.resultContent = document.getElementById('resultContent');
        this.closeResult = document.getElementById('closeResult');
        this.loadingOverlay = document.getElementById('loadingOverlay');
        this.toastContainer = document.getElementById('toastContainer');

        // Example buttons
        this.exampleBtns = document.querySelectorAll('.example-btn');
    }

    bindEvents() {
        // Form submission
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));

        // Input events
        this.vinInput.addEventListener('input', (e) => this.handleInput(e));
        this.vinInput.addEventListener('keydown', (e) => this.handleKeydown(e));
        this.vinInput.addEventListener('paste', (e) => this.handlePaste(e));

        // Example buttons
        this.exampleBtns.forEach(btn => {
            btn.addEventListener('click', (e) => this.handleExampleClick(e));
        });

        // Close result
        this.closeResult.addEventListener('click', () => this.hideResult());

        // About link
        document.getElementById('aboutLink').addEventListener('click', (e) => {
            e.preventDefault();
            this.showAbout();
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => this.handleGlobalKeydown(e));
    }

    setupValidation() {
        // VIN validation rules
        this.vinRules = {
            length: 17,
            invalidChars: ['I', 'O', 'Q'],
            pattern: /^[A-HJ-NPR-Z0-9]{17}$/
        };
    }

    initializeApp() {
        // Focus on input
        this.vinInput.focus();
        
        // Update character count
        this.updateCharCount();
        
        // Show welcome message
        this.showToast('Welcome to CARFAX VIN Checker!', 'success');
    }

    handleInput(e) {
        const value = e.target.value.toUpperCase();
        
        // Update input value
        e.target.value = value;
        
        // Update character count
        this.updateCharCount();
        
        // Validate VIN
        this.validateVIN(value);
        
        // Enable/disable submit button
        this.updateSubmitButton();
    }

    handleKeydown(e) {
        // Allow only valid VIN characters
        const validChars = /[A-HJ-NPR-Z0-9]/;
        const isSpecialKey = e.key === 'Backspace' || e.key === 'Delete' || e.key === 'Tab' || e.key === 'Enter';
        
        if (!isSpecialKey && !validChars.test(e.key)) {
            e.preventDefault();
        }
    }

    handlePaste(e) {
        e.preventDefault();
        
        const pastedText = (e.clipboardData || window.clipboardData).getData('text');
        const cleanText = pastedText.replace(/[^A-HJ-NPR-Z0-9]/gi, '').toUpperCase();
        
        // Set cursor position
        const cursorPos = e.target.selectionStart;
        const currentValue = e.target.value;
        const newValue = currentValue.slice(0, cursorPos) + cleanText + currentValue.slice(cursorPos);
        
        e.target.value = newValue.slice(0, 17);
        e.target.setSelectionRange(cursorPos + cleanText.length, cursorPos + cleanText.length);
        
        // Trigger input event
        e.target.dispatchEvent(new Event('input'));
    }

    handleGlobalKeydown(e) {
        // Ctrl+Enter to submit
        if (e.ctrlKey && e.key === 'Enter') {
            e.preventDefault();
            this.submitForm();
        }
        
        // Escape to clear
        if (e.key === 'Escape') {
            e.preventDefault();
            this.clearForm();
        }
    }

    handleExampleClick(e) {
        const vin = e.target.dataset.vin;
        this.vinInput.value = vin;
        this.vinInput.focus();
        this.vinInput.dispatchEvent(new Event('input'));
        this.showToast(`Example VIN loaded: ${vin}`, 'success');
    }

    updateCharCount() {
        const count = this.vinInput.value.length;
        this.charCount.textContent = `${count}/17`;
        
        // Update color based on count
        if (count === 17) {
            this.charCount.style.color = 'var(--success-color)';
        } else if (count > 17) {
            this.charCount.style.color = 'var(--error-color)';
        } else {
            this.charCount.style.color = 'var(--text-light)';
        }
    }

    validateVIN(vin) {
        let isValid = true;
        let errorMessage = '';

        // Check length
        if (vin.length !== this.vinRules.length) {
            isValid = false;
            errorMessage = `VIN must be exactly ${this.vinRules.length} characters`;
        }
        // Check invalid characters
        else {
            for (const char of this.vinRules.invalidChars) {
                if (vin.includes(char)) {
                    isValid = false;
                    errorMessage = `VIN cannot contain: ${char}`;
                    break;
                }
            }
        }

        // Update validation status
        this.validationStatus.textContent = errorMessage;
        this.validationStatus.className = 'validation-status ' + (isValid ? 'valid' : 'invalid');

        return isValid;
    }

    updateSubmitButton() {
        const vin = this.vinInput.value;
        const isValid = this.validateVIN(vin);
        
        this.submitBtn.disabled = !isValid || vin.length !== 17;
    }

    async handleSubmit(e) {
        e.preventDefault();
        
        const vin = this.vinInput.value.trim();
        
        if (!this.validateVIN(vin)) {
            this.showToast('Please enter a valid VIN', 'error');
            return;
        }

        await this.submitForm();
    }

    async submitForm() {
        const vin = this.vinInput.value.trim();
        
        // Show loading state
        this.setLoadingState(true);
        this.showLoadingOverlay();
        
        try {
            const response = await fetch('/api/vin', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ vin })
            });

            const data = await response.json();

            if (response.ok) {
                this.showSuccess(data);
            } else {
                this.showError(data.error || 'Failed to launch CARFAX');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showError('Network error. Please try again.');
        } finally {
            this.setLoadingState(false);
            this.hideLoadingOverlay();
        }
    }

    setLoadingState(loading) {
        this.submitBtn.disabled = loading;
        this.vinInput.disabled = loading;
        
        if (loading) {
            this.btnText.style.display = 'none';
            this.btnLoading.style.display = 'flex';
        } else {
            this.btnText.style.display = 'flex';
            this.btnLoading.style.display = 'none';
        }
    }

    showLoadingOverlay() {
        this.loadingOverlay.style.display = 'flex';
    }

    hideLoadingOverlay() {
        this.loadingOverlay.style.display = 'none';
    }

    showSuccess(data) {
        this.showResult({
            type: 'success',
            title: '✅ CARFAX Launched Successfully',
            message: data.message,
            vin: data.vin,
            timestamp: data.timestamp
        });
        
        this.showToast('CARFAX launched successfully!', 'success');
    }

    showError(message) {
        this.showResult({
            type: 'error',
            title: '❌ Error Launching CARFAX',
            message: message
        });
        
        this.showToast(message, 'error');
    }

    showResult(data) {
        const html = `
            <div class="result-item ${data.type}">
                <h4>${data.title}</h4>
                <p>${data.message}</p>
                ${data.vin ? `<p><strong>VIN:</strong> <code>${data.vin}</code></p>` : ''}
                ${data.timestamp ? `<p><strong>Time:</strong> ${new Date(data.timestamp).toLocaleString()}</p>` : ''}
            </div>
        `;
        
        this.resultContent.innerHTML = html;
        this.resultCard.style.display = 'block';
        
        // Scroll to result
        this.resultCard.scrollIntoView({ behavior: 'smooth' });
    }

    hideResult() {
        this.resultCard.style.display = 'none';
    }

    clearForm() {
        this.vinInput.value = '';
        this.vinInput.focus();
        this.vinInput.dispatchEvent(new Event('input'));
        this.hideResult();
        this.showToast('Form cleared', 'success');
    }

    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        
        this.toastContainer.appendChild(toast);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 5000);
        
        // Remove on click
        toast.addEventListener('click', () => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        });
    }

    showAbout() {
        const aboutContent = `
            <div class="about-content">
                <h3>About CARFAX VIN Checker</h3>
                <p>Professional vehicle history lookup tool that integrates with CARFAX to provide detailed vehicle information.</p>
                <ul>
                    <li>Fast and reliable VIN validation</li>
                    <li>Direct integration with CARFAX</li>
                    <li>Professional user interface</li>
                    <li>Real-time feedback</li>
                </ul>
                <p><strong>Version:</strong> 1.0.0</p>
            </div>
        `;
        
        this.showResult({
            type: 'info',
            title: 'ℹ️ About',
            message: aboutContent
        });
    }
}

// Performance optimizations
document.addEventListener('DOMContentLoaded', () => {
    // Initialize app with performance monitoring
    const startTime = performance.now();
    
    const app = new CarfaxApp();
    
    const loadTime = performance.now() - startTime;
    console.log(`App initialized in ${loadTime.toFixed(2)}ms`);
    
    // Service Worker registration for caching (if supported)
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('Service Worker registered');
            })
            .catch(error => {
                console.log('Service Worker registration failed:', error);
            });
    }
});

// Preload critical resources
const preloadResources = () => {
    const criticalResources = [
        '/static/css/style.css',
        '/static/js/app.js'
    ];
    
    criticalResources.forEach(resource => {
        const link = document.createElement('link');
        link.rel = 'preload';
        link.href = resource;
        link.as = resource.endsWith('.css') ? 'style' : 'script';
        document.head.appendChild(link);
    });
};

// Execute preloading
preloadResources(); 