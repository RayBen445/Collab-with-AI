// Real-Time Status Bar Component
class StatusBar {
    constructor() {
        this.battery = null;
        this.batteryWarningShown = false;
        this.currentUser = null;
        this.locationCache = null;
        this.locationUpdateTime = null;
        this.connection = null;
        this.deviceMotionActive = false;
        this.showExtendedStatus = false;
        this.init();
    }

    async init() {
        this.createStatusBar();
        this.startTimeUpdates();
        await this.initBatteryAPI();
        this.loadUserInfo();
        this.initLocationServices();
        this.initNetworkMonitoring();
        this.initMemoryMonitoring();
        this.initOrientationMonitoring();
        this.initMotionDetection();
        this.initThemeDetection();
        this.initPermissionsStatus();
        this.attachToAllPages();
    }

    createStatusBar() {
        // Create status bar HTML
        const statusBarHTML = `
            <div id="realtime-status-bar" class="status-bar">
                <div class="status-left">
                    <div class="user-info">
                        <img id="status-user-avatar" src="https://via.placeholder.com/32x32/667eea/white?text=?" alt="User" class="user-avatar">
                        <span id="status-username">Guest User</span>
                    </div>
                </div>
                <div class="status-center">
                    <div class="time-display">
                        <span id="status-time">--:--:--</span>
                        <span id="status-date">-- -- ----</span>
                        <span id="status-location">📍 Getting location...</span>
                    </div>
                </div>
                <div class="status-right">
                    <div class="system-info">
                        <div class="battery-info">
                            <span id="battery-icon">🔋</span>
                            <span id="battery-percentage">--</span>
                        </div>
                        <button id="toggle-extended" class="toggle-btn" onclick="statusBarInstance.toggleExtended()" title="Show more device info">📊</button>
                        <button id="profile-btn" class="profile-btn" onclick="openProfile()">Profile</button>
                    </div>
                </div>
            </div>
            <div id="extended-status-bar" class="extended-status hidden">
                <div class="status-row">
                    <div class="status-item" title="Network Connection">
                        <span id="network-icon">📶</span>
                        <span id="network-info">--</span>
                    </div>
                    <div class="status-item" title="Memory Usage">
                        <span id="memory-icon">🧠</span>
                        <span id="memory-info">--</span>
                    </div>
                    <div class="status-item" title="Screen Orientation">
                        <span id="orientation-icon">📱</span>
                        <span id="orientation-info">--</span>
                    </div>
                    <div class="status-item" title="Device Motion">
                        <span id="motion-icon">🎯</span>
                        <span id="motion-info">--</span>
                    </div>
                    <div class="status-item" title="Theme Mode">
                        <span id="theme-icon">🌙</span>
                        <span id="theme-info">--</span>
                    </div>
                    <div class="status-item" title="Permissions Status">
                        <span id="permissions-icon">🔒</span>
                        <span id="permissions-info">--</span>
                    </div>
                </div>
            </div>
        `;

        // Add CSS styles
        const statusBarCSS = `
            <style>
                .status-bar {
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    height: 50px;
                    background: rgba(255, 255, 255, 0.95);
                    backdrop-filter: blur(10px);
                    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    padding: 0 20px;
                    z-index: 1000;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    font-size: 14px;
                    color: #333;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                    transition: all 0.3s ease;
                }

                .extended-status {
                    position: fixed;
                    top: 50px;
                    left: 0;
                    right: 0;
                    background: rgba(255, 255, 255, 0.9);
                    backdrop-filter: blur(10px);
                    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
                    padding: 8px 20px;
                    z-index: 999;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    font-size: 12px;
                    color: #666;
                    transition: all 0.3s ease;
                    transform: translateY(-100%);
                    opacity: 0;
                }

                .extended-status.show {
                    transform: translateY(0);
                    opacity: 1;
                }

                .extended-status.hidden {
                    display: none;
                }

                .status-row {
                    display: flex;
                    justify-content: space-around;
                    align-items: center;
                    flex-wrap: wrap;
                    gap: 15px;
                }

                .status-item {
                    display: flex;
                    align-items: center;
                    gap: 4px;
                    padding: 4px 8px;
                    background: rgba(102, 126, 234, 0.1);
                    border-radius: 8px;
                    cursor: pointer;
                    transition: background 0.2s ease;
                    min-width: 60px;
                    justify-content: center;
                }

                .status-item:hover {
                    background: rgba(102, 126, 234, 0.2);
                }

                .status-left, .status-center, .status-right {
                    display: flex;
                    align-items: center;
                    gap: 15px;
                }

                .system-info {
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }

                .user-info {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                }

                .user-avatar {
                    width: 32px;
                    height: 32px;
                    border-radius: 50%;
                    border: 2px solid #667eea;
                    object-fit: cover;
                }

                .time-display {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    text-align: center;
                }

                #status-time {
                    font-weight: bold;
                    font-size: 16px;
                    color: #667eea;
                }

                #status-date {
                    font-size: 12px;
                    color: #666;
                }

                #status-location {
                    font-size: 11px;
                    color: #888;
                    margin-top: 2px;
                    max-width: 200px;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    white-space: nowrap;
                }

                .battery-info {
                    display: flex;
                    align-items: center;
                    gap: 5px;
                    padding: 4px 8px;
                    background: rgba(102, 126, 234, 0.1);
                    border-radius: 12px;
                }

                .battery-low {
                    background: rgba(255, 59, 48, 0.1) !important;
                    color: #ff3b30;
                }

                .battery-charging {
                    background: rgba(52, 199, 89, 0.1) !important;
                }

                .toggle-btn {
                    background: rgba(102, 126, 234, 0.1);
                    color: #667eea;
                    border: none;
                    padding: 6px 8px;
                    border-radius: 12px;
                    cursor: pointer;
                    font-size: 14px;
                    transition: all 0.3s ease;
                }

                .toggle-btn:hover {
                    background: rgba(102, 126, 234, 0.2);
                    transform: translateY(-1px);
                }

                .toggle-btn.active {
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    color: white;
                }

                .profile-btn {
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    border-radius: 15px;
                    cursor: pointer;
                    font-size: 12px;
                    font-weight: 500;
                    transition: all 0.3s ease;
                }

                .profile-btn:hover {
                    transform: translateY(-1px);
                    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
                }

                /* Status indicators */
                .network-excellent { color: #34c759; }
                .network-good { color: #ff9500; }
                .network-poor { color: #ff3b30; }
                .memory-ok { color: #34c759; }
                .memory-warning { color: #ff9500; }
                .memory-critical { color: #ff3b30; }
                .motion-active { color: #34c759; animation: pulse 2s infinite; }
                .motion-idle { color: #999; }

                @keyframes pulse {
                    0%, 100% { opacity: 1; }
                    50% { opacity: 0.5; }
                }

                /* Notification Toast */
                .battery-notification {
                    position: fixed;
                    top: 60px;
                    right: 20px;
                    background: #ff3b30;
                    color: white;
                    padding: 12px 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 12px rgba(255, 59, 48, 0.3);
                    z-index: 1001;
                    animation: slideIn 0.3s ease;
                    font-size: 14px;
                    max-width: 300px;
                }

                .battery-notification .close-btn {
                    background: none;
                    border: none;
                    color: white;
                    font-size: 16px;
                    cursor: pointer;
                    float: right;
                    margin-left: 10px;
                }

                @keyframes slideIn {
                    from {
                        transform: translateX(100%);
                        opacity: 0;
                    }
                    to {
                        transform: translateX(0);
                        opacity: 1;
                    }
                }

                /* Adjust body padding to account for status bar */
                body {
                    padding-top: 50px !important;
                }

                body.extended-status-visible {
                    padding-top: 85px !important;
                }

                /* Mobile responsive */
                @media (max-width: 768px) {
                    .status-bar {
                        padding: 0 10px;
                        font-size: 12px;
                    }
                    
                    .status-center {
                        display: none;
                    }
                    
                    .user-avatar {
                        width: 24px;
                        height: 24px;
                    }
                    
                    #status-location {
                        max-width: 150px;
                    }

                    .status-row {
                        gap: 8px;
                    }

                    .status-item {
                        min-width: 45px;
                        padding: 2px 6px;
                        font-size: 10px;
                    }

                    .extended-status {
                        padding: 5px 10px;
                    }
                }
            </style>
        `;

        // Insert CSS and HTML into document
        document.head.insertAdjacentHTML('beforeend', statusBarCSS);
        document.body.insertAdjacentHTML('afterbegin', statusBarHTML);
    }

    startTimeUpdates() {
        const updateTime = () => {
            const now = new Date();
            const timeString = now.toLocaleTimeString();
            const dateString = now.toLocaleDateString('en-US', { 
                weekday: 'short', 
                month: 'short', 
                day: 'numeric',
                year: 'numeric'
            });

            const timeElement = document.getElementById('status-time');
            const dateElement = document.getElementById('status-date');
            
            if (timeElement) timeElement.textContent = timeString;
            if (dateElement) dateElement.textContent = dateString;
        };

        // Update immediately and then every second
        updateTime();
        setInterval(updateTime, 1000);
    }

    async initBatteryAPI() {
        try {
            if ('getBattery' in navigator) {
                this.battery = await navigator.getBattery();
                this.updateBatteryInfo();
                
                // Listen for battery events
                this.battery.addEventListener('levelchange', () => this.updateBatteryInfo());
                this.battery.addEventListener('chargingchange', () => this.updateBatteryInfo());
            } else {
                // Fallback for browsers that don't support Battery API
                this.updateBatteryInfo(null);
            }
        } catch (error) {
            console.log('Battery API not supported');
            this.updateBatteryInfo(null);
        }
    }

    updateBatteryInfo(batteryLevel = null) {
        const batteryIcon = document.getElementById('battery-icon');
        const batteryPercentage = document.getElementById('battery-percentage');
        const batteryInfo = document.querySelector('.battery-info');

        if (!batteryIcon || !batteryPercentage || !batteryInfo) return;

        if (this.battery) {
            const level = Math.round(this.battery.level * 100);
            const isCharging = this.battery.charging;

            batteryPercentage.textContent = `${level}%`;
            
            // Update battery icon and styling
            if (isCharging) {
                batteryIcon.textContent = '⚡';
                batteryInfo.classList.add('battery-charging');
                batteryInfo.classList.remove('battery-low');
            } else if (level <= 20) {
                batteryIcon.textContent = '🪫';
                batteryInfo.classList.add('battery-low');
                batteryInfo.classList.remove('battery-charging');
                
                // Show low battery notification
                if (level <= 20 && !this.batteryWarningShown) {
                    this.showBatteryWarning();
                    this.batteryWarningShown = true;
                }
            } else {
                batteryIcon.textContent = '🔋';
                batteryInfo.classList.remove('battery-low', 'battery-charging');
                this.batteryWarningShown = false;
            }
        } else {
            // Fallback when Battery API is not available
            batteryIcon.textContent = '🔋';
            batteryPercentage.textContent = 'N/A';
        }
    }

    initLocationServices() {
        // Check if geolocation is supported
        if ('geolocation' in navigator) {
            this.getCurrentLocation();
        } else {
            this.updateLocationDisplay('📍 Location unavailable');
        }
    }

    getCurrentLocation() {
        const locationElement = document.getElementById('status-location');
        
        // Check if we have cached location (less than 10 minutes old)
        if (this.locationCache && this.locationUpdateTime) {
            const now = new Date().getTime();
            const cacheAge = now - this.locationUpdateTime;
            if (cacheAge < 10 * 60 * 1000) { // 10 minutes
                this.updateLocationDisplay(this.locationCache);
                return;
            }
        }

        const options = {
            enableHighAccuracy: false,
            timeout: 10000,
            maximumAge: 600000 // 10 minutes
        };

        navigator.geolocation.getCurrentPosition(
            (position) => {
                this.getLocationName(position.coords.latitude, position.coords.longitude);
            },
            (error) => {
                this.handleLocationError(error);
            },
            options
        );
    }

    async getLocationName(latitude, longitude) {
        try {
            // Use OpenStreetMap Nominatim API for reverse geocoding (free, no API key required)
            const response = await fetch(
                `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}&zoom=10&addressdetails=1`,
                {
                    headers: {
                        'User-Agent': 'Collab-with-AI-StatusBar/1.0'
                    }
                }
            );
            
            if (response.ok) {
                const data = await response.json();
                const address = data.address;
                
                // Format location string with city and country/state
                let locationStr = '';
                if (address.city || address.town || address.village) {
                    locationStr += address.city || address.town || address.village;
                }
                if (address.state || address.country) {
                    if (locationStr) locationStr += ', ';
                    locationStr += address.state || address.country;
                }
                
                if (!locationStr) {
                    locationStr = data.display_name?.split(',').slice(0, 2).join(', ') || 'Unknown location';
                }

                const formattedLocation = `📍 ${locationStr}`;
                this.locationCache = formattedLocation;
                this.locationUpdateTime = new Date().getTime();
                this.updateLocationDisplay(formattedLocation);
            } else {
                throw new Error('Geocoding failed');
            }
        } catch (error) {
            console.log('Error getting location name:', error);
            this.updateLocationDisplay('📍 Location found');
        }
    }

    handleLocationError(error) {
        let errorMessage = '📍 Location unavailable';
        
        switch (error.code) {
            case error.PERMISSION_DENIED:
                errorMessage = '📍 Location access denied';
                break;
            case error.POSITION_UNAVAILABLE:
                errorMessage = '📍 Location unavailable';
                break;
            case error.TIMEOUT:
                errorMessage = '📍 Location timeout';
                break;
        }
        
        this.updateLocationDisplay(errorMessage);
    }

    updateLocationDisplay(locationText) {
        const locationElement = document.getElementById('status-location');
        if (locationElement) {
            locationElement.textContent = locationText;
        }
    }

    showBatteryWarning() {
        const notification = document.createElement('div');
        notification.className = 'battery-notification';
        notification.innerHTML = `
            ⚠️ Your battery is running low. Please connect your device to a power source.
            <button class="close-btn" onclick="this.parentElement.remove()">&times;</button>
        `;

        document.body.appendChild(notification);

        // Auto-remove after 10 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 10000);
    }

    async loadUserInfo() {
        // Check if Firebase Auth is available
        if (typeof auth !== 'undefined' && auth.currentUser) {
            this.currentUser = auth.currentUser;
            this.updateUserDisplay();
        } else {
            // Check for stored user info
            const userInfo = localStorage.getItem('userInfo');
            if (userInfo) {
                try {
                    const user = JSON.parse(userInfo);
                    this.updateUserDisplay(user);
                } catch (e) {
                    console.log('Error parsing user info');
                }
            }
        }
    }

    updateUserDisplay(user = null) {
        const avatarElement = document.getElementById('status-user-avatar');
        const usernameElement = document.getElementById('status-username');

        if (user || this.currentUser) {
            const userData = user || this.currentUser;
            const displayName = userData.displayName || userData.username || userData.email?.split('@')[0] || 'User';
            const photoURL = userData.photoURL || userData.avatar || `https://ui-avatars.com/api/?name=${encodeURIComponent(displayName)}&background=667eea&color=fff`;

            if (usernameElement) usernameElement.textContent = displayName;
            if (avatarElement) {
                avatarElement.src = photoURL;
                avatarElement.alt = displayName;
            }
        }
    }

    attachToAllPages() {
        // This method can be extended to ensure the status bar appears on all pages
        // For now, it's automatically attached when this script is loaded
    }

    toggleExtended() {
        const extendedBar = document.getElementById('extended-status-bar');
        const toggleBtn = document.getElementById('toggle-extended');
        
        if (this.showExtendedStatus) {
            extendedBar.classList.remove('show');
            extendedBar.classList.add('hidden');
            toggleBtn.classList.remove('active');
            document.body.classList.remove('extended-status-visible');
            this.showExtendedStatus = false;
        } else {
            extendedBar.classList.remove('hidden');
            extendedBar.classList.add('show');
            toggleBtn.classList.add('active');
            document.body.classList.add('extended-status-visible');
            this.showExtendedStatus = true;
        }
    }

    initNetworkMonitoring() {
        try {
            // Check for Network Information API
            if ('connection' in navigator || 'mozConnection' in navigator || 'webkitConnection' in navigator) {
                this.connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
                this.updateNetworkInfo();
                
                // Listen for connection changes
                this.connection.addEventListener('change', () => this.updateNetworkInfo());
            } else {
                // Fallback: monitor online/offline status
                this.updateNetworkInfo();
                window.addEventListener('online', () => this.updateNetworkInfo());
                window.addEventListener('offline', () => this.updateNetworkInfo());
            }
        } catch (error) {
            console.log('Network monitoring not supported');
            this.updateNetworkInfo(null);
        }
    }

    updateNetworkInfo() {
        const networkIcon = document.getElementById('network-icon');
        const networkInfo = document.getElementById('network-info');
        
        if (!networkIcon || !networkInfo) return;

        if (!navigator.onLine) {
            networkIcon.textContent = '📶';
            networkInfo.textContent = 'Offline';
            networkInfo.className = 'network-poor';
            return;
        }

        if (this.connection) {
            const type = this.connection.effectiveType || this.connection.type || 'unknown';
            const downlink = this.connection.downlink;
            
            let icon = '📶';
            let className = 'network-good';
            
            if (type === '4g' || downlink > 10) {
                icon = '📶';
                className = 'network-excellent';
            } else if (type === '3g' || downlink > 1) {
                icon = '📶';
                className = 'network-good';
            } else {
                icon = '📶';
                className = 'network-poor';
            }
            
            networkIcon.textContent = icon;
            networkInfo.textContent = type.toUpperCase() || 'Online';
            networkInfo.className = className;
        } else {
            networkIcon.textContent = '📶';
            networkInfo.textContent = 'Online';
            networkInfo.className = 'network-good';
        }
    }

    initMemoryMonitoring() {
        try {
            // Update memory info periodically
            this.updateMemoryInfo();
            setInterval(() => this.updateMemoryInfo(), 30000); // Update every 30 seconds
        } catch (error) {
            console.log('Memory monitoring not supported');
            this.updateMemoryInfo(null);
        }
    }

    updateMemoryInfo() {
        const memoryIcon = document.getElementById('memory-icon');
        const memoryInfo = document.getElementById('memory-info');
        
        if (!memoryIcon || !memoryInfo) return;

        try {
            // Check for Performance Memory API
            if (performance.memory) {
                const used = Math.round(performance.memory.usedJSHeapSize / 1024 / 1024);
                const total = Math.round(performance.memory.totalJSHeapSize / 1024 / 1024);
                const limit = Math.round(performance.memory.jsHeapSizeLimit / 1024 / 1024);
                
                const percentage = (used / total) * 100;
                
                let className = 'memory-ok';
                if (percentage > 80) {
                    className = 'memory-critical';
                } else if (percentage > 60) {
                    className = 'memory-warning';
                }
                
                memoryIcon.textContent = '🧠';
                memoryInfo.textContent = `${used}MB`;
                memoryInfo.className = className;
            } else {
                memoryIcon.textContent = '🧠';
                memoryInfo.textContent = 'N/A';
                memoryInfo.className = '';
            }
        } catch (error) {
            memoryIcon.textContent = '🧠';
            memoryInfo.textContent = 'N/A';
            memoryInfo.className = '';
        }
    }

    initOrientationMonitoring() {
        try {
            this.updateOrientationInfo();
            
            // Listen for orientation changes
            if (screen.orientation) {
                screen.orientation.addEventListener('change', () => this.updateOrientationInfo());
            } else {
                // Fallback for older browsers
                window.addEventListener('orientationchange', () => {
                    setTimeout(() => this.updateOrientationInfo(), 100);
                });
            }
        } catch (error) {
            console.log('Orientation monitoring not supported');
            this.updateOrientationInfo(null);
        }
    }

    updateOrientationInfo() {
        const orientationIcon = document.getElementById('orientation-icon');
        const orientationInfo = document.getElementById('orientation-info');
        
        if (!orientationIcon || !orientationInfo) return;

        try {
            let orientation = 'Unknown';
            let icon = '📱';
            
            if (screen.orientation) {
                orientation = screen.orientation.type.split('-')[0];
            } else {
                // Fallback detection
                const angle = window.orientation;
                if (angle === 0 || angle === 180) {
                    orientation = 'portrait';
                } else if (angle === 90 || angle === -90) {
                    orientation = 'landscape';
                }
            }
            
            if (orientation === 'landscape') {
                icon = '📱';
                orientationInfo.textContent = 'Landscape';
            } else {
                icon = '📱';
                orientationInfo.textContent = 'Portrait';
            }
            
            orientationIcon.textContent = icon;
        } catch (error) {
            orientationIcon.textContent = '📱';
            orientationInfo.textContent = 'Unknown';
        }
    }

    initMotionDetection() {
        try {
            if (typeof DeviceMotionEvent !== 'undefined') {
                let lastUpdate = Date.now();
                let motionThreshold = 0.5;
                
                window.addEventListener('devicemotion', (event) => {
                    const now = Date.now();
                    if (now - lastUpdate < 100) return; // Throttle updates
                    
                    const acceleration = event.accelerationIncludingGravity;
                    if (acceleration) {
                        const totalAcceleration = Math.abs(acceleration.x) + Math.abs(acceleration.y) + Math.abs(acceleration.z);
                        
                        if (totalAcceleration > motionThreshold) {
                            this.deviceMotionActive = true;
                        } else {
                            this.deviceMotionActive = false;
                        }
                        
                        this.updateMotionInfo();
                        lastUpdate = now;
                    }
                });
                
                // Reset motion state after inactivity
                setInterval(() => {
                    this.deviceMotionActive = false;
                    this.updateMotionInfo();
                }, 2000);
            } else {
                this.updateMotionInfo(null);
            }
        } catch (error) {
            console.log('Motion detection not supported');
            this.updateMotionInfo(null);
        }
    }

    updateMotionInfo() {
        const motionIcon = document.getElementById('motion-icon');
        const motionInfo = document.getElementById('motion-info');
        
        if (!motionIcon || !motionInfo) return;

        if (this.deviceMotionActive) {
            motionIcon.textContent = '🎯';
            motionInfo.textContent = 'Active';
            motionInfo.className = 'motion-active';
        } else {
            motionIcon.textContent = '🎯';
            motionInfo.textContent = 'Idle';
            motionInfo.className = 'motion-idle';
        }
    }

    initThemeDetection() {
        try {
            this.updateThemeInfo();
            
            // Listen for theme changes
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            mediaQuery.addEventListener('change', () => this.updateThemeInfo());
        } catch (error) {
            console.log('Theme detection not supported');
            this.updateThemeInfo(null);
        }
    }

    updateThemeInfo() {
        const themeIcon = document.getElementById('theme-icon');
        const themeInfo = document.getElementById('theme-info');
        
        if (!themeIcon || !themeInfo) return;

        try {
            const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            
            if (isDark) {
                themeIcon.textContent = '🌙';
                themeInfo.textContent = 'Dark';
            } else {
                themeIcon.textContent = '☀️';
                themeInfo.textContent = 'Light';
            }
        } catch (error) {
            themeIcon.textContent = '🌙';
            themeInfo.textContent = 'Auto';
        }
    }

    async initPermissionsStatus() {
        try {
            await this.updatePermissionsStatus();
        } catch (error) {
            console.log('Permissions API not supported');
            this.updatePermissionsStatus(null);
        }
    }

    async updatePermissionsStatus() {
        const permissionsIcon = document.getElementById('permissions-icon');
        const permissionsInfo = document.getElementById('permissions-info');
        
        if (!permissionsIcon || !permissionsInfo) return;

        try {
            if ('permissions' in navigator) {
                const permissions = ['camera', 'microphone', 'geolocation', 'notifications'];
                let grantedCount = 0;
                
                for (const permission of permissions) {
                    try {
                        const result = await navigator.permissions.query({ name: permission });
                        if (result.state === 'granted') {
                            grantedCount++;
                        }
                    } catch (e) {
                        // Permission not supported
                    }
                }
                
                permissionsIcon.textContent = '🔒';
                if (grantedCount === 0) {
                    permissionsInfo.textContent = 'None';
                } else if (grantedCount < permissions.length) {
                    permissionsInfo.textContent = 'Some';
                } else {
                    permissionsInfo.textContent = 'All';
                }
            } else {
                permissionsIcon.textContent = '🔒';
                permissionsInfo.textContent = 'N/A';
            }
        } catch (error) {
            permissionsIcon.textContent = '🔒';
            permissionsInfo.textContent = 'N/A';
        }
    }
}

// Global status bar instance
let statusBarInstance = null;

// Global function to open profile page
function openProfile() {
    window.location.href = 'user-profile.html';
}

// Initialize status bar when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        statusBarInstance = new StatusBar();
    });
} else {
    statusBarInstance = new StatusBar();
}

// Export for potential module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = StatusBar;
}