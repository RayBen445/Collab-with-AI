document.addEventListener('DOMContentLoaded', function() {
    // --- Time and Date ---
    const timeElement = document.getElementById('time');
    const dateElement = document.getElementById('date');

    function updateTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString('en-US');
        const dateString = now.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
        if (timeElement) timeElement.textContent = timeString;
        if (dateElement) dateElement.textContent = dateString;
    }

    setInterval(updateTime, 1000);
    updateTime();

    // --- Battery Status & Notification ---
    const batteryElement = document.getElementById('battery');
    const notificationElement = document.getElementById('low-battery-notification');
    const dismissButton = document.getElementById('dismiss-notification');

    function updateBatteryStatus(battery) {
        if (batteryElement) {
            const level = Math.floor(battery.level * 100);
            const charging = battery.charging ? ' (Charging)' : '';
            batteryElement.textContent = `Battery: ${level}%${charging}`;
        }
        // Check level for notification
        if (battery.level <= 0.20 && !battery.charging) {
            if (notificationElement) notificationElement.classList.remove('hidden');
        }
    }

    if (dismissButton) {
        dismissButton.addEventListener('click', function() {
            if (notificationElement) notificationElement.classList.add('hidden');
        });
    }

    if ('getBattery' in navigator) {
        navigator.getBattery().then(function(battery) {
            updateBatteryStatus(battery); // Initial call
            battery.addEventListener('levelchange', () => updateBatteryStatus(battery));
            battery.addEventListener('chargingchange', () => updateBatteryStatus(battery));
        });
    } else {
        if (batteryElement) batteryElement.textContent = 'Battery status not available';
    }
});
