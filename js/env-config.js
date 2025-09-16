/**
 * Environment Configuration
 * This file loads environment variables from Vercel through a secure API endpoint
 * 
 * For Vercel deployment:
 * - Environment variables are loaded from /api/get-env-config endpoint
 * - This provides a secure way to access configuration from server-side environment variables
 */

// Create a global ENV object to store environment variables
window.ENV = window.ENV || {};

/**
 * Load environment configuration from server
 */
async function loadEnvironmentConfig() {
    try {
        // Add timeout to prevent hanging
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout
        
        const response = await fetch('/api/get-env-config', {
            signal: controller.signal,
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success && data.config) {
            // Validate required configuration
            const requiredFields = ['ADMIN_EMAIL', 'PLATFORM_NAME'];
            const missingFields = requiredFields.filter(field => !data.config[field]);
            
            if (missingFields.length > 0) {
                console.warn('Missing required configuration fields:', missingFields);
            }
            
            // Load configuration from server
            window.ENV = {
                ...window.ENV,
                ...data.config
            };
            
            console.log('Environment configuration loaded successfully');
            
            if (!data.hasFirebaseConfig) {
                console.warn('Firebase configuration incomplete. Some features may not work properly.');
                // Dispatch event to notify other components
                window.dispatchEvent(new CustomEvent('envConfigError', { 
                    detail: { type: 'firebase_config_incomplete' }
                }));
            }
            
            // Dispatch successful config load event
            window.dispatchEvent(new CustomEvent('envConfigLoaded', { 
                detail: { config: window.ENV }
            }));
            
        } else {
            throw new Error('Invalid response format from configuration endpoint');
        }
        
    } catch (error) {
        console.error('Error loading environment config:', error);
        
        // Set fallback configuration
        window.ENV = {
            ...window.ENV,
            ADMIN_EMAIL: 'oladoyeheritage445@gmail.com',
            PLATFORM_NAME: 'Collab-with-AI',
            VERSION: '2.0.0'
        };
        
        // Dispatch error event
        window.dispatchEvent(new CustomEvent('envConfigError', { 
            detail: { 
                type: 'load_failed', 
                error: error.message,
                usingFallback: true 
            }
        }));
        
        console.warn('Using fallback configuration due to error:', error.message);
    }
}

// Load configuration immediately
loadEnvironmentConfig();