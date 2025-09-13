/**
 * Secure API endpoint for Gemini API key management
 * This file should be deployed as a serverless function on Vercel
 * Path: /api/get-gemini-key.js
 */

// This is a Vercel serverless function
export default async function handler(req, res) {
    // Only allow POST requests
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    try {
        // Verify user authentication
        const authHeader = req.headers.authorization;
        if (!authHeader || !authHeader.startsWith('Bearer ')) {
            return res.status(401).json({ error: 'Unauthorized: Missing or invalid token' });
        }

        const userToken = authHeader.substring(7); // Remove 'Bearer ' prefix
        
        // Validate user token (implement your authentication logic here)
        const isValidUser = await validateUserToken(userToken);
        if (!isValidUser) {
            return res.status(401).json({ error: 'Unauthorized: Invalid token' });
        }

        // Get the Gemini API key from environment variables
        const geminiApiKey = process.env.GEMINI_API_KEY;
        
        if (!geminiApiKey) {
            return res.status(500).json({ error: 'API key not configured' });
        }

        // Return the API key securely
        res.status(200).json({
            apiKey: geminiApiKey,
            timestamp: new Date().toISOString()
        });

    } catch (error) {
        console.error('Error in get-gemini-key API:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
}

/**
 * Validate user authentication token
 * Implement your authentication logic here
 */
async function validateUserToken(token) {
    try {
        // This is a placeholder implementation
        // In a real application, you would:
        // 1. Verify JWT token signature
        // 2. Check token expiration
        // 3. Validate user session in database
        // 4. Check user permissions
        
        if (!token || token.length < 10) {
            return false;
        }

        // In production, implement proper JWT verification
        // Check against environment-based admin token only
        const adminToken = process.env.ADMIN_TOKEN;
        
        if (!adminToken) {
            console.warn('ADMIN_TOKEN environment variable not set');
            return false;
        }

        return token === adminToken;

    } catch (error) {
        console.error('Token validation error:', error);
        return false;
    }
}

/**
 * Alternative function for rate limiting (optional)
 */
function checkRateLimit(req) {
    // Implement rate limiting logic here
    // Return true if request is within limits, false otherwise
    return true;
}

/**
 * Log API usage for monitoring (optional)
 */
function logApiUsage(userToken, success) {
    // Implement usage logging here
    console.log(`API Key Request - Token: ${userToken.substring(0, 10)}... - Success: ${success} - Time: ${new Date().toISOString()}`);
}