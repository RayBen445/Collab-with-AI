/**
 * Firebase Authentication Service
 * Handles all authentication operations for the Collab-with-AI platform
 */

import { 
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signInWithPopup,
  GoogleAuthProvider,
  signOut,
  onAuthStateChanged,
  updateProfile,
  sendPasswordResetEmail
} from 'firebase/auth';

import { 
  doc,
  setDoc,
  getDoc,
  updateDoc,
  serverTimestamp
} from 'firebase/firestore';

import { auth, db } from './firebase-config.js';

class FirebaseAuthService {
  constructor() {
    this.auth = auth;
    this.db = db;
    this.googleProvider = new GoogleAuthProvider();
    this.currentUser = null;
    this.adminEmail = window.ENV?.ADMIN_EMAIL || null;
    
    // Set up authentication state listener
    this.setupAuthStateListener();
  }

  /**
   * Set up authentication state listener
   */
  setupAuthStateListener() {
    onAuthStateChanged(this.auth, async (user) => {
      if (user) {
        this.currentUser = user;
        await this.updateUserData(user);
        this.onUserSignedIn(user);
      } else {
        this.currentUser = null;
        this.onUserSignedOut();
      }
    });
  }

  /**
   * Sign in with email and password
   */
  async signInWithEmail(email, password) {
    try {
      const userCredential = await signInWithEmailAndPassword(this.auth, email, password);
      const user = userCredential.user;
      
      // Update last login time
      await this.updateUserData(user);
      
      return {
        success: true,
        user: user,
        isAdmin: email === this.adminEmail
      };
    } catch (error) {
      console.error('Email sign-in error:', error);
      return {
        success: false,
        error: this.getErrorMessage(error.code)
      };
    }
  }

  /**
   * Sign up with email and password
   */
  async signUpWithEmail(email, password, displayName = '') {
    try {
      const userCredential = await createUserWithEmailAndPassword(this.auth, email, password);
      const user = userCredential.user;

      // Update user profile
      if (displayName) {
        await updateProfile(user, { displayName });
      }

      // Create user document in Firestore
      await this.createUserDocument(user, { displayName });

      return {
        success: true,
        user: user,
        isAdmin: email === this.adminEmail
      };
    } catch (error) {
      console.error('Email sign-up error:', error);
      return {
        success: false,
        error: this.getErrorMessage(error.code)
      };
    }
  }

  /**
   * Sign in with Google
   */
  async signInWithGoogle() {
    try {
      const result = await signInWithPopup(this.auth, this.googleProvider);
      const user = result.user;

      // Create or update user document
      await this.createUserDocument(user);

      return {
        success: true,
        user: user,
        isAdmin: user.email === this.adminEmail
      };
    } catch (error) {
      console.error('Google sign-in error:', error);
      return {
        success: false,
        error: this.getErrorMessage(error.code)
      };
    }
  }

  /**
   * Sign out current user
   */
  async signOutUser() {
    try {
      await signOut(this.auth);
      return { success: true };
    } catch (error) {
      console.error('Sign-out error:', error);
      return {
        success: false,
        error: 'Failed to sign out'
      };
    }
  }

  /**
   * Send password reset email
   */
  async resetPassword(email) {
    try {
      await sendPasswordResetEmail(this.auth, email);
      return { success: true };
    } catch (error) {
      console.error('Password reset error:', error);
      return {
        success: false,
        error: this.getErrorMessage(error.code)
      };
    }
  }

  /**
   * Create user document in Firestore
   */
  async createUserDocument(user, additionalData = {}) {
    if (!user) return;

    const userRef = doc(this.db, 'users', user.uid);
    const userSnap = await getDoc(userRef);

    if (!userSnap.exists()) {
      const { displayName, email, photoURL } = user;
      const createdAt = serverTimestamp();

      try {
        await setDoc(userRef, {
          displayName: displayName || additionalData.displayName || '',
          email,
          photoURL: photoURL || '',
          role: email === this.adminEmail ? 'admin' : 'user',
          isAdmin: email === this.adminEmail,
          createdAt,
          lastLoginAt: createdAt,
          projects: [],
          tasks: [],
          settings: {
            notifications: true,
            theme: 'light',
            language: 'en'
          },
          ...additionalData
        });
      } catch (error) {
        console.error('Error creating user document:', error);
      }
    }
  }

  /**
   * Update user data on sign in
   */
  async updateUserData(user) {
    if (!user) return;

    const userRef = doc(this.db, 'users', user.uid);
    
    try {
      await updateDoc(userRef, {
        lastLoginAt: serverTimestamp(),
        isOnline: true
      });
    } catch (error) {
      // If document doesn't exist, create it
      await this.createUserDocument(user);
    }
  }

  /**
   * Get current user data from Firestore
   */
  async getCurrentUserData() {
    if (!this.currentUser) return null;

    const userRef = doc(this.db, 'users', this.currentUser.uid);
    const userSnap = await getDoc(userRef);

    if (userSnap.exists()) {
      return userSnap.data();
    }
    return null;
  }

  /**
   * Check if current user is admin
   */
  isCurrentUserAdmin() {
    return this.currentUser && this.currentUser.email === this.adminEmail;
  }

  /**
   * Get user-friendly error messages
   */
  getErrorMessage(errorCode) {
    const errorMessages = {
      'auth/user-not-found': 'No account found with this email address.',
      'auth/wrong-password': 'Incorrect password. Please try again.',
      'auth/email-already-in-use': 'An account with this email already exists.',
      'auth/weak-password': 'Password should be at least 6 characters long.',
      'auth/invalid-email': 'Please enter a valid email address.',
      'auth/user-disabled': 'This account has been disabled.',
      'auth/operation-not-allowed': 'Operation not allowed. Please contact support.',
      'auth/popup-closed-by-user': 'Sign-in popup was closed before completion.',
      'auth/popup-blocked': 'Sign-in popup was blocked by the browser.',
      'auth/network-request-failed': 'Network error. Please check your connection.',
      'auth/too-many-requests': 'Too many failed attempts. Please try again later.'
    };

    return errorMessages[errorCode] || 'An unexpected error occurred. Please try again.';
  }

  /**
   * Called when user signs in
   */
  onUserSignedIn(user) {
    console.log('User signed in:', user.email);
    
    // Dispatch custom event
    window.dispatchEvent(new CustomEvent('userSignedIn', { 
      detail: { 
        user: user,
        isAdmin: user.email === this.adminEmail
      } 
    }));
  }

  /**
   * Called when user signs out
   */
  onUserSignedOut() {
    console.log('User signed out');
    
    // Dispatch custom event
    window.dispatchEvent(new CustomEvent('userSignedOut'));
    
    // Redirect to login page if not already there
    if (!window.location.pathname.includes('login.html') && 
        !window.location.pathname.includes('index.html')) {
      window.location.href = 'login.html';
    }
  }
}

// Export singleton instance
export const authService = new FirebaseAuthService();
export default authService;