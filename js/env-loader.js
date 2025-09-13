/**
 * Environment Configuration Loader
 * Loads environment variables for client-side use from Vercel environment variables
 * This file ensures proper configuration is available before Firebase initialization
 */

// Initialize environment variables
window.ENV = window.ENV || {};

// Set the correct admin email as specified by the user
window.ENV.ADMIN_EMAIL = 'oladoyeheritage445@gmail.com';

// Platform Configuration
window.ENV.PLATFORM_NAME = 'Collab-with-AI';
window.ENV.VERSION = '2.0.0';

// Firebase Configuration will be loaded from Vercel environment variables
// These values should be set in Vercel dashboard as regular environment variables (not secret references)
// The actual Firebase configuration will be loaded by env-config.js from the server API

console.log('Environment configuration initialized');
console.log('Admin email set to:', window.ENV.ADMIN_EMAIL);
console.log('Note: Firebase configuration will be loaded from Vercel environment variables via server API');