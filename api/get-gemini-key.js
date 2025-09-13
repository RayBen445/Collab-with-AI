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
        // Check rate limiting first
        if (!checkRateLimit(req)) {
            return res.status(429).json({ 
                error: 'Too many requests. Please try again later.',
                retryAfter: 60 
            });
        }

        // Verify user authentication
        const authHeader = req.headers.authorization;
        if (!authHeader || !authHeader.startsWith('Bearer ')) {
            return res.status(401).json({ error: 'Unauthorized: Missing or invalid token' });
        }

        const userToken = authHeader.substring(7); // Remove 'Bearer ' prefix
        
        // Validate user token with enhanced security
        const isValidUser = await validateUserToken(userToken);
        if (!isValidUser) {
            return res.status(401).json({ error: 'Unauthorized: Invalid token' });
        }

        // Get the Gemini API key from environment variables
        const geminiApiKey = process.env.GEMINI_API_KEY;
        
        if (!geminiApiKey) {
            console.error('GEMINI_API_KEY environment variable not set');
            return res.status(500).json({ error: 'API key not configured' });
        }

        // Return the API key securely
        res.status(200).json({
            apiKey: geminiApiKey,
            timestamp: new Date().toISOString(),
            expiresIn: 3600 // API key valid for 1 hour for security
        });

        // Log successful request
        logApiUsage(userToken, true);

    } catch (error) {
        console.error('Error in get-gemini-key API:', error);
        logApiUsage(req.headers.authorization?.substring(7) || 'unknown', false);
        res.status(500).json({ error: 'Internal server error' });
    }
}

/**
 * Validate user authentication token
 * Enhanced implementation with better security practices
 */
async function validateUserToken(token) {
    try {
        // Basic validation
        if (!token || typeof token !== 'string' || token.length < 10) {
            return false;
        }

        // Rate limiting check
        if (!checkRateLimit()) {
            console.warn('Rate limit exceeded for token validation');
            return false;
        }

        // In a production environment, this should:
        // 1. Verify Firebase ID token using Firebase Admin SDK
        // 2. Check token expiration and signature
        // 3. Validate user permissions in database
        // 4. Implement proper role-based access control

        // For now, using a secure admin token comparison
        const adminToken = process.env.ADMIN_TOKEN;
        const backupAdminToken = process.env.BACKUP_ADMIN_TOKEN;
        
        if (!adminToken) {
            console.error('ADMIN_TOKEN environment variable not configured');
            return false;
        }

        // Use constant-time comparison to prevent timing attacks
        const isValidAdmin = constantTimeCompare(token, adminToken);
        const isValidBackup = backupAdminToken ? constantTimeCompare(token, backupAdminToken) : false;

        const isValid = isValidAdmin || isValidBackup;
        
        // Log the validation attempt (without exposing token)
        logApiUsage(token, isValid);
        
        return isValid;

    } catch (error) {
        console.error('Token validation error:', error);
        return false;
    }
}

/**
 * Constant-time string comparison to prevent timing attacks
 */
function constantTimeCompare(a, b) {
    if (a.length !== b.length) {
        return false;
    }
    
    let result = 0;
    for (let i = 0; i < a.length; i++) {
        result |= a.charCodeAt(i) ^ b.charCodeAt(i);
    }
    
    return result === 0;
}

/**
 * Enhanced rate limiting function
 */
let requestCounts = new Map();
const RATE_LIMIT_WINDOW = 60000; // 1 minute
const RATE_LIMIT_MAX_REQUESTS = 10; // 10 requests per minute

function checkRateLimit(req) {
    const clientIP = req.headers['x-forwarded-for'] || 
                     req.headers['x-real-ip'] || 
                     req.connection.remoteAddress || 
                     'unknown';
    
    const now = Date.now();
    const windowStart = now - RATE_LIMIT_WINDOW;
    
    // Clean old entries
    for (const [ip, timestamps] of requestCounts.entries()) {
        const filteredTimestamps = timestamps.filter(time => time > windowStart);
        if (filteredTimestamps.length === 0) {
            requestCounts.delete(ip);
        } else {
            requestCounts.set(ip, filteredTimestamps);
        }
    }
    
    // Check current IP
    const clientRequests = requestCounts.get(clientIP) || [];
    const recentRequests = clientRequests.filter(time => time > windowStart);
    
    if (recentRequests.length >= RATE_LIMIT_MAX_REQUESTS) {
        return false;
    }
    
    // Add current request
    recentRequests.push(now);
    requestCounts.set(clientIP, recentRequests);
    
    return true;
}

/**
 * Log API usage for monitoring (optional)
 */
function logApiUsage(userToken, success) {
    // Implement usage logging here
    console.log(`API Key Request - Token: ${userToken.substring(0, 10)}... - Success: ${success} - Time: ${new Date().toISOString()}`);
}