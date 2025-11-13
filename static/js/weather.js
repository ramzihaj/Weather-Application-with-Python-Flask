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

// GPS Location functionality
function getLocationWeather() {
    if (navigator.geolocation) {
        const button = document.querySelector('.gps-btn');
        const originalText = button.textContent;
        button.textContent = '📍 Getting location...';
        button.disabled = true;
        
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                const units = document.getElementById('units')?.value || 'metric';
                
                window.location.href = `/weather?lat=${lat}&lon=${lon}&units=${units}`;
            },
            function(error) {
                alert('Unable to get your location. Please enter a city name manually.');
                button.textContent = originalText;
                button.disabled = false;
            },
            {
                timeout: 10000,
                enableHighAccuracy: true
            }
        );
    } else {
        alert('Geolocation is not supported by this browser.');
    }
}

// City search autocomplete
let searchTimeout;
function setupCityAutocomplete() {
    const cityInput = document.getElementById('city');
    const datalist = document.getElementById('city-suggestions');
    
    if (!cityInput || !datalist) return;
    
    cityInput.addEventListener('input', function() {
        const query = this.value.trim();
        
        clearTimeout(searchTimeout);
        
        if (query.length < 2) {
            datalist.innerHTML = '';
            return;
        }
        
        searchTimeout = setTimeout(() => {
            fetch(`/api/search_cities?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(cities => {
                    datalist.innerHTML = '';
                    cities.forEach(city => {
                        const option = document.createElement('option');
                        option.value = city.name;
                        option.textContent = city.display_name;
                        datalist.appendChild(option);
                    });
                })
                .catch(error => {
                    console.error('Error fetching cities:', error);
                });
        }, 300);
    });
}

// Temperature unit conversion
function setupUnitConversion() {
    const unitsSelect = document.getElementById('units');
    if (!unitsSelect) return;
    
    unitsSelect.addEventListener('change', function() {
        const currentUrl = new URL(window.location.href);
        currentUrl.searchParams.set('units', this.value);
        
        // If we have city or coordinates, reload with new units
        if (currentUrl.searchParams.get('city') || 
            (currentUrl.searchParams.get('lat') && currentUrl.searchParams.get('lon'))) {
            window.location.href = currentUrl.toString();
        }
    });
}

// Enhanced form validation
function setupFormValidation() {
    const form = document.getElementById('weatherForm');
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        const cityInput = document.getElementById('city');
        const city = cityInput.value.trim();
        
        if (!city) {
            e.preventDefault();
            cityInput.focus();
            cityInput.style.borderColor = 'rgba(255, 87, 108, 0.5)';
            
            setTimeout(() => {
                cityInput.style.borderColor = '';
            }, 2000);
            
            return false;
        }
        
        addLoadingAnimation();
    });
}

// Keyboard shortcuts
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K to focus search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const cityInput = document.getElementById('city');
            if (cityInput) {
                cityInput.focus();
                cityInput.select();
            }
        }
        
        // Escape to clear search
        if (e.key === 'Escape') {
            const cityInput = document.getElementById('city');
            if (cityInput && document.activeElement === cityInput) {
                cityInput.value = '';
                cityInput.blur();
            }
        }
    });
}

// Weather data refresh
function setupAutoRefresh() {
    // Auto-refresh weather data every 10 minutes if on weather page
    if (window.location.pathname === '/weather') {
        setInterval(() => {
            const currentUrl = new URL(window.location.href);
            if (currentUrl.searchParams.get('city') || 
                (currentUrl.searchParams.get('lat') && currentUrl.searchParams.get('lon'))) {
                
                // Add a subtle indicator that data is refreshing
                const container = document.querySelector('.weather-container');
                if (container) {
                    container.style.opacity = '0.8';
                    
                    fetch(window.location.href)
                        .then(response => response.text())
                        .then(html => {
                            // Parse the new HTML and update weather data
                            const parser = new DOMParser();
                            const doc = parser.parseFromString(html, 'text/html');
                            
                            // Update temperature and other dynamic content
                            const newTemp = doc.querySelector('.temperature');
                            const currentTemp = document.querySelector('.temperature');
                            if (newTemp && currentTemp) {
                                currentTemp.innerHTML = newTemp.innerHTML;
                            }
                            
                            container.style.opacity = '1';
                        })
                        .catch(error => {
                            console.error('Auto-refresh failed:', error);
                            container.style.opacity = '1';
                        });
                }
            }
        }, 600000); // 10 minutes
    }
}

// Enhanced initialization
document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('city');
    const form = document.querySelector('.search-form');
    
    // Auto-focus on input
    if (input) {
        input.focus();
    }
    
    // Update weather icon based on current status
    updateWeatherIcon();
    
    // Setup all new features
    setupCityAutocomplete();
    setupUnitConversion();
    setupFormValidation();
    setupKeyboardShortcuts();
    setupAutoRefresh();
    
    // Add input animation on focus
    if (input) {
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
        });
    }
    
    // Add tooltips for action buttons
    const actionButtons = document.querySelectorAll('.action-btn');
    actionButtons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px) scale(1.05)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
});

// Call visual effects after a short delay
setTimeout(addVisualEffects, 500);

// Service Worker for offline functionality (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/static/js/sw.js')
            .then(function(registration) {
                console.log('ServiceWorker registration successful');
            })
            .catch(function(err) {
                console.log('ServiceWorker registration failed');
            });
    });
}
