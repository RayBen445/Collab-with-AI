/**
 * Firebase Configuration and Initialization
 * This file sets up Firebase services for the Collab-with-AI platform
 */

// Import Firebase modules
import { initializeApp } from 'firebase/app';
import { getAuth, connectAuthEmulator } from 'firebase/auth';
import { getFirestore, connectFirestoreEmulator } from 'firebase/firestore';
import { getFunctions, connectFunctionsEmulator } from 'firebase/functions';
import { getStorage, connectStorageEmulator } from 'firebase/storage';
import { getAnalytics } from 'firebase/analytics';

// Firebase configuration object
// These values are loaded from environment variables for security
// For client-side code, Vercel exposes environment variables prefixed with NEXT_PUBLIC_
// or they can be injected at build time
const firebaseConfig = {
  apiKey: window.ENV?.FIREBASE_API_KEY || "your-api-key-here",
  authDomain: window.ENV?.FIREBASE_AUTH_DOMAIN || "collab-with-ai.firebaseapp.com",
  projectId: window.ENV?.FIREBASE_PROJECT_ID || "collab-with-ai",
  storageBucket: window.ENV?.FIREBASE_STORAGE_BUCKET || "collab-with-ai.appspot.com",
  messagingSenderId: window.ENV?.FIREBASE_MESSAGING_SENDER_ID || "123456789",
  appId: window.ENV?.FIREBASE_APP_ID || "1:123456789:web:abcdefghijklmnop",
  measurementId: window.ENV?.FIREBASE_MEASUREMENT_ID || "G-ABCDEFGHIJ"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase services
const auth = getAuth(app);
const db = getFirestore(app);
const functions = getFunctions(app);
const storage = getStorage(app);

// Initialize Analytics (only in production)
let analytics = null;
if (typeof window !== 'undefined' && window.location.hostname !== 'localhost') {
  analytics = getAnalytics(app);
}

// Connect to emulators in development environment
if (typeof window !== 'undefined' && window.location.hostname === 'localhost') {
  try {
    connectAuthEmulator(auth, 'http://localhost:9099');
    connectFirestoreEmulator(db, 'localhost', 8080);
    connectFunctionsEmulator(functions, 'localhost', 5001);
    connectStorageEmulator(storage, 'localhost', 9199);
    console.log('Connected to Firebase emulators');
  } catch (error) {
    console.log('Firebase emulators already connected or not available');
  }
}

// Export Firebase services
export {
  app,
  auth,
  db,
  functions,
  storage,
  analytics
};

// Export Firebase configuration for reference
export { firebaseConfig };