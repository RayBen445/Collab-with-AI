/**
 * Secure API endpoint for environment configuration
 * This file provides safe environment variables to the client side
 * Path: /api/get-env-config.js
 */

// This is a Vercel serverless function
export default async function handler(req, res) {
    // Only allow GET requests
    if (req.method !== 'GET') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    try {
        // Get environment variables from Vercel
        const config = {
            // Firebase Configuration - safe to expose client-side
            FIREBASE_API_KEY: process.env.FIREBASE_API_KEY || null,
            FIREBASE_AUTH_DOMAIN: process.env.FIREBASE_AUTH_DOMAIN || null,
            FIREBASE_PROJECT_ID: process.env.FIREBASE_PROJECT_ID || null,
            FIREBASE_STORAGE_BUCKET: process.env.FIREBASE_STORAGE_BUCKET || null,
            FIREBASE_MESSAGING_SENDER_ID: process.env.FIREBASE_MESSAGING_SENDER_ID || null,
            FIREBASE_APP_ID: process.env.FIREBASE_APP_ID || null,
            FIREBASE_MEASUREMENT_ID: process.env.FIREBASE_MEASUREMENT_ID || null,
            
            // Admin email - safe to expose for client-side admin detection
            ADMIN_EMAIL: process.env.ADMIN_EMAIL || 'oladoyeheritage445@gmail.com',
            
            // Platform information
            PLATFORM_NAME: 'Collab-with-AI',
            VERSION: '2.0.0'
        };

        // Check if essential Firebase config is available
        const hasFirebaseConfig = config.FIREBASE_API_KEY && 
                                config.FIREBASE_AUTH_DOMAIN && 
                                config.FIREBASE_PROJECT_ID;

        // Return configuration with status
        res.status(200).json({
            success: true,
            config: config,
            hasFirebaseConfig: hasFirebaseConfig,
            timestamp: new Date().toISOString()
        });

    } catch (error) {
        console.error('Error in get-env-config API:', error);
        res.status(500).json({ 
            success: false,
            error: 'Internal server error',
            config: {
                // Fallback admin email
                ADMIN_EMAIL: 'oladoyeheritage445@gmail.com',
                PLATFORM_NAME: 'Collab-with-AI',
                VERSION: '2.0.0'
            }
        });
    }
}