// Real-Time Status Bar Component
class StatusBar {
    constructor() {
        this.battery = null;
        this.batteryWarningShown = false;
        this.currentUser = null;
        this.init();
    }

    async init() {
        this.createStatusBar();
        this.startTimeUpdates();
        await this.initBatteryAPI();
        this.loadUserInfo();
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
                    </div>
                </div>
                <div class="status-right">
                    <div class="battery-info">
                        <span id="battery-icon">🔋</span>
                        <span id="battery-percentage">--</span>
                    </div>
                    <button id="profile-btn" class="profile-btn" onclick="openProfile()">Profile</button>
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
                }

                .status-left, .status-center, .status-right {
                    display: flex;
                    align-items: center;
                    gap: 15px;
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
}

// Global function to open profile page
function openProfile() {
    window.location.href = 'user-profile.html';
}

// Initialize status bar when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => new StatusBar());
} else {
    new StatusBar();
}

// Export for potential module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = StatusBar;
}