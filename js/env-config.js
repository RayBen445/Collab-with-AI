/**
 * Environment Configuration
 * This file provides a way to inject environment variables into client-side code
 * 
 * For Vercel deployment:
 * - Environment variables are injected at build time or runtime
 * - This provides a secure way to access configuration without exposing secrets
 */

// Create a global ENV object to store environment variables
window.ENV = window.ENV || {};

// This will be populated by the build process or runtime injection
// The actual values should be set through Vercel environment variables
if (typeof process !== 'undefined' && process.env) {
  // Node.js environment (for build-time injection)
  window.ENV = {
    FIREBASE_API_KEY: process.env.FIREBASE_API_KEY,
    FIREBASE_AUTH_DOMAIN: process.env.FIREBASE_AUTH_DOMAIN,
    FIREBASE_PROJECT_ID: process.env.FIREBASE_PROJECT_ID,
    FIREBASE_STORAGE_BUCKET: process.env.FIREBASE_STORAGE_BUCKET,
    FIREBASE_MESSAGING_SENDER_ID: process.env.FIREBASE_MESSAGING_SENDER_ID,
    FIREBASE_APP_ID: process.env.FIREBASE_APP_ID,
    FIREBASE_MEASUREMENT_ID: process.env.FIREBASE_MEASUREMENT_ID,
    ADMIN_EMAIL: process.env.ADMIN_EMAIL
  };
}

// Fallback for development - these should be overridden by actual environment variables
if (!window.ENV.FIREBASE_API_KEY) {
  console.warn('Environment variables not loaded. Using placeholder values for development.');
  console.warn('Set proper environment variables in Vercel for production deployment.');
}