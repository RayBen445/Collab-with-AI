/**
 * Firebase Cloud Functions for Collab-with-AI Platform
 * 
 * This file contains all serverless functions for the platform including:
 * - Secure Gemini API proxy
 * - User management functions
 * - Real-time data processing
 * - Email notifications
 */

const functions = require('firebase-functions');
const admin = require('firebase-admin');
const cors = require('cors');
const express = require('express');

// Initialize Firebase Admin
admin.initializeApp();

// Get admin email from environment variable
const ADMIN_EMAIL = functions.config().admin?.email || process.env.ADMIN_EMAIL;

// Initialize Express app with CORS
const app = express();
app.use(cors({ origin: true }));

/**
 * Secure Gemini API Proxy Function
 * Handles all Gemini API calls securely on the server side
 */
exports.geminiApiProxy = functions.https.onRequest(async (req, res) => {
  // Enable CORS
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  // Handle preflight requests
  if (req.method === 'OPTIONS') {
    res.status(204).send('');
    return;
  }

  // Only allow POST requests
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Method not allowed' });
    return;
  }

  try {
    // Verify user authentication
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      res.status(401).json({ error: 'Unauthorized: Missing or invalid token' });
      return;
    }

    const idToken = authHeader.substring(7); // Remove 'Bearer ' prefix
    const decodedToken = await admin.auth().verifyIdToken(idToken);
    const userId = decodedToken.uid;

    // Get the Gemini API key from environment variables
    const geminiApiKey = functions.config().gemini?.api_key || process.env.GEMINI_API_KEY;
    
    if (!geminiApiKey) {
      res.status(500).json({ error: 'Gemini API key not configured' });
      return;
    }

    // Extract request parameters
    const { prompt, model = 'gemini-1.5-flash-latest', features = [] } = req.body;

    if (!prompt) {
      res.status(400).json({ error: 'Prompt is required' });
      return;
    }

    // Make request to Gemini API
    const geminiResponse = await makeGeminiRequest(geminiApiKey, prompt, model, features);

    // Log the API usage
    await logApiUsage(userId, decodedToken.email, 'gemini_api', true);

    // Return the response
    res.status(200).json({
      success: true,
      data: geminiResponse,
      timestamp: new Date().toISOString(),
      model: model
    });

  } catch (error) {
    console.error('Gemini API proxy error:', error);
    
    // Log the failed attempt
    try {
      const authHeader = req.headers.authorization;
      if (authHeader) {
        const idToken = authHeader.substring(7);
        const decodedToken = await admin.auth().verifyIdToken(idToken);
        await logApiUsage(decodedToken.uid, decodedToken.email, 'gemini_api', false, error.message);
      }
    } catch (logError) {
      console.error('Error logging failed API usage:', logError);
    }

    res.status(500).json({ 
      error: 'Failed to process Gemini API request',
      timestamp: new Date().toISOString()
    });
  }
});

/**
 * Make request to Gemini API
 */
async function makeGeminiRequest(apiKey, prompt, model, features) {
  const fetch = (await import('node-fetch')).default;
  
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;
  
  const requestBody = {
    contents: [{
      parts: [{
        text: prompt
      }]
    }],
    generationConfig: {
      temperature: 0.7,
      topK: 40,
      topP: 0.95,
      maxOutputTokens: 2048
    }
  };

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestBody)
  });

  if (!response.ok) {
    throw new Error(`Gemini API error: ${response.status} ${response.statusText}`);
  }

  const data = await response.json();
  return data;
}

/**
 * User Management Functions
 */

// Create user profile on signup
exports.createUserProfile = functions.auth.user().onCreate(async (user) => {
  try {
    const userRef = admin.firestore().collection('users').doc(user.uid);
    
    await userRef.set({
      displayName: user.displayName || '',
      email: user.email,
      photoURL: user.photoURL || '',
      role: user.email === ADMIN_EMAIL ? 'admin' : 'user',
      isAdmin: user.email === ADMIN_EMAIL,
      createdAt: admin.firestore.FieldValue.serverTimestamp(),
      lastLoginAt: admin.firestore.FieldValue.serverTimestamp(),
      isOnline: true,
      projects: [],
      tasks: [],
      settings: {
        notifications: true,
        theme: 'light',
        language: 'en'
      },
      apiUsage: {
        totalRequests: 0,
        lastRequestAt: null
      }
    });

    console.log('User profile created for:', user.email);
  } catch (error) {
    console.error('Error creating user profile:', error);
  }
});

// Clean up user data on deletion
exports.deleteUserData = functions.auth.user().onDelete(async (user) => {
  try {
    const batch = admin.firestore().batch();
    
    // Delete user document
    const userRef = admin.firestore().collection('users').doc(user.uid);
    batch.delete(userRef);
    
    // Delete user's projects (if owner)
    const projectsSnapshot = await admin.firestore()
      .collection('projects')
      .where('owner', '==', user.uid)
      .get();
    
    projectsSnapshot.forEach(doc => {
      batch.delete(doc.ref);
    });
    
    // Delete user's tasks
    const tasksSnapshot = await admin.firestore()
      .collection('tasks')
      .where('assignee', '==', user.uid)
      .get();
    
    tasksSnapshot.forEach(doc => {
      batch.delete(doc.ref);
    });
    
    await batch.commit();
    console.log('User data cleaned up for:', user.email);
  } catch (error) {
    console.error('Error cleaning up user data:', error);
  }
});

/**
 * Real-time Data Processing Functions
 */

// Process new project creation
exports.processNewProject = functions.firestore
  .document('projects/{projectId}')
  .onCreate(async (snap, context) => {
    const projectData = snap.data();
    const projectId = context.params.projectId;

    try {
      // Update user's project list
      const userRef = admin.firestore().collection('users').doc(projectData.owner);
      await userRef.update({
        projects: admin.firestore.FieldValue.arrayUnion(projectId)
      });

      // Create initial analytics entry
      await admin.firestore().collection('analytics').doc(projectId).set({
        projectId: projectId,
        createdAt: admin.firestore.FieldValue.serverTimestamp(),
        totalTasks: 0,
        completedTasks: 0,
        totalCollaborators: (projectData.collaborators || []).length + 1,
        lastActivity: admin.firestore.FieldValue.serverTimestamp()
      });

      console.log('New project processed:', projectId);
    } catch (error) {
      console.error('Error processing new project:', error);
    }
  });

// Process task updates
exports.processTaskUpdate = functions.firestore
  .document('tasks/{taskId}')
  .onWrite(async (change, context) => {
    const taskId = context.params.taskId;

    try {
      if (!change.after.exists) {
        // Task was deleted
        return;
      }

      const taskData = change.after.data();
      const projectId = taskData.projectId;

      if (!projectId) return;

      // Update project analytics
      const analyticsRef = admin.firestore().collection('analytics').doc(projectId);
      
      await analyticsRef.update({
        lastActivity: admin.firestore.FieldValue.serverTimestamp()
      });

      // If task was just completed, increment completed tasks
      if (!change.before.exists || 
          (change.before.data().status !== 'completed' && taskData.status === 'completed')) {
        await analyticsRef.update({
          completedTasks: admin.firestore.FieldValue.increment(1)
        });
      }

      console.log('Task update processed:', taskId);
    } catch (error) {
      console.error('Error processing task update:', error);
    }
  });

/**
 * Notification Functions
 */

// Send welcome email to new users
exports.sendWelcomeEmail = functions.auth.user().onCreate(async (user) => {
  try {
    // In a real implementation, you would integrate with an email service
    // like SendGrid, Mailgun, or use Firebase's email extension
    
    console.log(`Welcome email should be sent to: ${user.email}`);
    
    // Placeholder for email sending logic
    // await sendEmail({
    //   to: user.email,
    //   subject: 'Welcome to Collab-with-AI!',
    //   template: 'welcome',
    //   data: {
    //     displayName: user.displayName || 'User',
    //     email: user.email
    //   }
    // });
    
  } catch (error) {
    console.error('Error sending welcome email:', error);
  }
});

/**
 * Utility Functions
 */

// Log API usage for monitoring and analytics
async function logApiUsage(userId, email, apiType, success, errorMessage = null) {
  try {
    const logEntry = {
      userId: userId,
      email: email,
      apiType: apiType,
      success: success,
      timestamp: admin.firestore.FieldValue.serverTimestamp(),
      errorMessage: errorMessage
    };

    await admin.firestore().collection('api_logs').add(logEntry);

    // Update user's API usage counter
    const userRef = admin.firestore().collection('users').doc(userId);
    await userRef.update({
      'apiUsage.totalRequests': admin.firestore.FieldValue.increment(1),
      'apiUsage.lastRequestAt': admin.firestore.FieldValue.serverTimestamp()
    });

  } catch (error) {
    console.error('Error logging API usage:', error);
  }
}

/**
 * Admin Functions
 */

// Get platform analytics (admin only)
exports.getPlatformAnalytics = functions.https.onCall(async (data, context) => {
  // Check if user is authenticated and is admin
  if (!context.auth) {
    throw new functions.https.HttpsError('unauthenticated', 'User must be authenticated');
  }

  const userEmail = context.auth.token.email;
  if (userEmail !== ADMIN_EMAIL) {
    throw new functions.https.HttpsError('permission-denied', 'Admin access required');
  }

  try {
    // Get platform statistics
    const usersSnapshot = await admin.firestore().collection('users').get();
    const projectsSnapshot = await admin.firestore().collection('projects').get();
    const tasksSnapshot = await admin.firestore().collection('tasks').get();

    const analytics = {
      totalUsers: usersSnapshot.size,
      totalProjects: projectsSnapshot.size,
      totalTasks: tasksSnapshot.size,
      adminUser: userEmail,
      timestamp: new Date().toISOString()
    };

    return analytics;
  } catch (error) {
    console.error('Error getting platform analytics:', error);
    throw new functions.https.HttpsError('internal', 'Failed to get analytics');
  }
});