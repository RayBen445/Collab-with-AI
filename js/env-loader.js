/**
 * Environment Configuration Loader
 * Loads environment variables for client-side use
 */

// Initialize environment variables
window.ENV = window.ENV || {};

// Firebase Configuration
// In production, these would be injected by the build system or loaded from a secure endpoint
window.ENV.FIREBASE_API_KEY = 'your-api-key-here';
window.ENV.FIREBASE_AUTH_DOMAIN = 'collab-with-ai.firebaseapp.com';
window.ENV.FIREBASE_PROJECT_ID = 'collab-with-ai';
window.ENV.FIREBASE_STORAGE_BUCKET = 'collab-with-ai.appspot.com';
window.ENV.FIREBASE_MESSAGING_SENDER_ID = '123456789';
window.ENV.FIREBASE_APP_ID = '1:123456789:web:abcdefghijklmnop';
window.ENV.FIREBASE_MEASUREMENT_ID = 'G-ABCDEFGHIJ';

// Admin Configuration
window.ENV.ADMIN_EMAIL = 'admin@collab-with-ai.com';

// Gemini API Configuration (handled by Cloud Functions in production)
window.ENV.GEMINI_API_AVAILABLE = true;

// Platform Configuration
window.ENV.PLATFORM_NAME = 'Collab-with-AI';
window.ENV.VERSION = '2.0.0';

console.log('Environment configuration loaded');