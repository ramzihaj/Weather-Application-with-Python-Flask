// Weather icons mapping
const weatherIcons = {
    'clear sky': '☀️',
    'few clouds': '🌤️',
    'scattered clouds': '⛅',
    'broken clouds': '☁️',
    'shower rain': '🌦️',
    'rain': '🌧️',
    'thunderstorm': '⛈️',
    'snow': '❄️',
    'mist': '🌫️',
    'fog': '🌫️',
    'haze': '🌫️',
    'dust': '🌪️',
    'sand': '🌪️',
    'ash': '🌋',
    'squall': '💨',
    'tornado': '🌪️',
    'default': '🌤️'
};

// Get weather icon based on status
function getWeatherIcon(status) {
    const lowerStatus = status.toLowerCase();
    
    // Check for exact matches first
    if (weatherIcons[lowerStatus]) {
        return weatherIcons[lowerStatus];
    }
    
    // Check for partial matches
    for (const [key, icon] of Object.entries(weatherIcons)) {
        if (lowerStatus.includes(key) || key.includes(lowerStatus)) {
            return icon;
        }
    }
    
    return weatherIcons.default;
}

// Update weather icon dynamically
function updateWeatherIcon() {
    const statusElement = document.querySelector('.weather-status');
    const iconElement = document.querySelector('.weather-icon');
    
    if (statusElement && iconElement) {
        const status = statusElement.textContent.trim();
        const icon = getWeatherIcon(status);
        iconElement.textContent = icon;
    }
}

// Add loading animation
function addLoadingAnimation() {
    const button = document.querySelector('.search-button');
    if (button) {
        button.innerHTML = `
            <span style="display: inline-flex; align-items: center; gap: 0.5rem;">
                <span class="loading-spinner"></span>
                Loading...
            </span>
        `;
    }
}

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('city');
    const form = document.querySelector('.search-form');
    
    // Auto-focus on input
    if (input) {
        input.focus();
    }
    
    // Update weather icon based on current status
    updateWeatherIcon();
    
    // Add form submission handler
    if (form) {
        form.addEventListener('submit', function(e) {
            addLoadingAnimation();
        });
    }
    
    // Add enter key support
    if (input) {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                form.submit();
            }
        });
    }
    
    // Add input animation on focus
    if (input) {
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
        });
    }
});

// Add some visual effects
function addVisualEffects() {
    // Add floating particles effect
    const container = document.querySelector('.weather-container');
    if (container) {
        for (let i = 0; i < 5; i++) {
            const particle = document.createElement('div');
            particle.className = 'floating-particle';
            particle.style.cssText = `
                position: absolute;
                width: 4px;
                height: 4px;
                background: rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                animation: float ${3 + Math.random() * 2}s ease-in-out infinite;
                animation-delay: ${Math.random() * 2}s;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
            `;
            container.appendChild(particle);
        }
    }
}

// Call visual effects after a short delay
setTimeout(addVisualEffects, 500);
