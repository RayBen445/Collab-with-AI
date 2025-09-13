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
        const response = await fetch('/api/get-env-config');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success && data.config) {
            // Load configuration from server
            window.ENV = {
                ...window.ENV,
                ...data.config
            };
            
            console.log('Environment configuration loaded successfully from Vercel');
            console.log('Admin email configured:', window.ENV.ADMIN_EMAIL);
            
            if (!data.hasFirebaseConfig) {
                console.warn('Firebase configuration incomplete. Please set all Firebase environment variables in Vercel.');
            }
        } else {
            throw new Error('Failed to load configuration from server');
        }
        
    } catch (error) {
        console.error('Error loading environment config:', error);
        
        // Fallback configuration with correct admin email
        window.ENV = {
            ...window.ENV,
            ADMIN_EMAIL: 'oladoyeheritage445@gmail.com',
            PLATFORM_NAME: 'Collab-with-AI',
            VERSION: '2.0.0'
        };
        
        console.warn('Using fallback configuration. Please ensure environment variables are set in Vercel.');
        console.log('Fallback admin email set to:', window.ENV.ADMIN_EMAIL);
    }
}

// Load configuration immediately
loadEnvironmentConfig();