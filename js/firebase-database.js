/**
 * Firebase Database Service
 * Handles all Firestore database operations for the Collab-with-AI platform
 */

import { 
  collection,
  doc,
  addDoc,
  getDoc,
  getDocs,
  setDoc,
  updateDoc,
  deleteDoc,
  query,
  where,
  orderBy,
  limit,
  onSnapshot,
  serverTimestamp,
  arrayUnion,
  arrayRemove,
  increment
} from 'firebase/firestore';

import { db } from './firebase-config.js';

class FirebaseDatabaseService {
  constructor() {
    this.db = db;
    this.listeners = new Map(); // Store active listeners for cleanup
  }

  /**
   * User Management
   */

  // Get user data
  async getUser(userId) {
    try {
      const userRef = doc(this.db, 'users', userId);
      const userSnap = await getDoc(userRef);
      
      if (userSnap.exists()) {
        return { id: userSnap.id, ...userSnap.data() };
      }
      return null;
    } catch (error) {
      console.error('Error getting user:', error);
      throw error;
    }
  }

  // Update user data
  async updateUser(userId, data) {
    try {
      const userRef = doc(this.db, 'users', userId);
      await updateDoc(userRef, {
        ...data,
        updatedAt: serverTimestamp()
      });
      return true;
    } catch (error) {
      console.error('Error updating user:', error);
      throw error;
    }
  }

  // Get all users (admin only)
  async getAllUsers() {
    try {
      const usersRef = collection(this.db, 'users');
      const snapshot = await getDocs(usersRef);
      
      return snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }));
    } catch (error) {
      console.error('Error getting all users:', error);
      throw error;
    }
  }

  /**
   * Project Management
   */

  // Create new project
  async createProject(projectData, userId) {
    try {
      const projectRef = await addDoc(collection(this.db, 'projects'), {
        ...projectData,
        owner: userId,
        collaborators: projectData.collaborators || [],
        createdAt: serverTimestamp(),
        updatedAt: serverTimestamp(),
        status: 'active'
      });

      return projectRef.id;
    } catch (error) {
      console.error('Error creating project:', error);
      throw error;
    }
  }

  // Get project by ID
  async getProject(projectId) {
    try {
      const projectRef = doc(this.db, 'projects', projectId);
      const projectSnap = await getDoc(projectRef);
      
      if (projectSnap.exists()) {
        return { id: projectSnap.id, ...projectSnap.data() };
      }
      return null;
    } catch (error) {
      console.error('Error getting project:', error);
      throw error;
    }
  }

  // Get user's projects
  async getUserProjects(userId) {
    try {
      const projectsRef = collection(this.db, 'projects');
      const ownerQuery = query(
        projectsRef,
        where('owner', '==', userId),
        orderBy('createdAt', 'desc')
      );
      
      const collaboratorQuery = query(
        projectsRef,
        where('collaborators', 'array-contains', userId),
        orderBy('createdAt', 'desc')
      );

      const [ownerSnap, collaboratorSnap] = await Promise.all([
        getDocs(ownerQuery),
        getDocs(collaboratorQuery)
      ]);

      const projects = new Map();
      
      // Add owned projects
      ownerSnap.docs.forEach(doc => {
        projects.set(doc.id, { id: doc.id, ...doc.data(), role: 'owner' });
      });

      // Add collaborative projects (avoid duplicates)
      collaboratorSnap.docs.forEach(doc => {
        if (!projects.has(doc.id)) {
          projects.set(doc.id, { id: doc.id, ...doc.data(), role: 'collaborator' });
        }
      });

      return Array.from(projects.values());
    } catch (error) {
      console.error('Error getting user projects:', error);
      throw error;
    }
  }

  // Update project
  async updateProject(projectId, data) {
    try {
      const projectRef = doc(this.db, 'projects', projectId);
      await updateDoc(projectRef, {
        ...data,
        updatedAt: serverTimestamp()
      });
      return true;
    } catch (error) {
      console.error('Error updating project:', error);
      throw error;
    }
  }

  // Add collaborator to project
  async addCollaborator(projectId, userId) {
    try {
      const projectRef = doc(this.db, 'projects', projectId);
      await updateDoc(projectRef, {
        collaborators: arrayUnion(userId),
        updatedAt: serverTimestamp()
      });
      return true;
    } catch (error) {
      console.error('Error adding collaborator:', error);
      throw error;
    }
  }

  // Remove collaborator from project
  async removeCollaborator(projectId, userId) {
    try {
      const projectRef = doc(this.db, 'projects', projectId);
      await updateDoc(projectRef, {
        collaborators: arrayRemove(userId),
        updatedAt: serverTimestamp()
      });
      return true;
    } catch (error) {
      console.error('Error removing collaborator:', error);
      throw error;
    }
  }

  /**
   * Task Management
   */

  // Create new task
  async createTask(taskData, userId) {
    try {
      const taskRef = await addDoc(collection(this.db, 'tasks'), {
        ...taskData,
        creator: userId,
        createdAt: serverTimestamp(),
        updatedAt: serverTimestamp(),
        status: taskData.status || 'todo'
      });

      return taskRef.id;
    } catch (error) {
      console.error('Error creating task:', error);
      throw error;
    }
  }

  // Get project tasks
  async getProjectTasks(projectId) {
    try {
      const tasksRef = collection(this.db, 'tasks');
      const q = query(
        tasksRef,
        where('projectId', '==', projectId),
        orderBy('createdAt', 'desc')
      );
      
      const snapshot = await getDocs(q);
      return snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }));
    } catch (error) {
      console.error('Error getting project tasks:', error);
      throw error;
    }
  }

  // Update task
  async updateTask(taskId, data) {
    try {
      const taskRef = doc(this.db, 'tasks', taskId);
      await updateDoc(taskRef, {
        ...data,
        updatedAt: serverTimestamp()
      });
      return true;
    } catch (error) {
      console.error('Error updating task:', error);
      throw error;
    }
  }

  // Delete task
  async deleteTask(taskId) {
    try {
      const taskRef = doc(this.db, 'tasks', taskId);
      await deleteDoc(taskRef);
      return true;
    } catch (error) {
      console.error('Error deleting task:', error);
      throw error;
    }
  }

  /**
   * Chat and Communication
   */

  // Add message to chat
  async addMessage(chatId, messageData, userId) {
    try {
      const messagesRef = collection(this.db, 'chats', chatId, 'messages');
      const messageRef = await addDoc(messagesRef, {
        ...messageData,
        sender: userId,
        timestamp: serverTimestamp(),
        edited: false
      });

      return messageRef.id;
    } catch (error) {
      console.error('Error adding message:', error);
      throw error;
    }
  }

  // Listen to chat messages
  listenToMessages(chatId, callback) {
    try {
      const messagesRef = collection(this.db, 'chats', chatId, 'messages');
      const q = query(messagesRef, orderBy('timestamp', 'asc'));
      
      const unsubscribe = onSnapshot(q, (snapshot) => {
        const messages = snapshot.docs.map(doc => ({
          id: doc.id,
          ...doc.data()
        }));
        callback(messages);
      });

      // Store listener for cleanup
      this.listeners.set(`chat_${chatId}`, unsubscribe);
      
      return unsubscribe;
    } catch (error) {
      console.error('Error listening to messages:', error);
      throw error;
    }
  }

  /**
   * Analytics and Monitoring
   */

  // Update user activity
  async updateUserActivity(userId, activity) {
    try {
      const userRef = doc(this.db, 'users', userId);
      await updateDoc(userRef, {
        lastActivity: serverTimestamp(),
        isOnline: true
      });

      // Log activity
      const activityRef = collection(this.db, 'user_activities');
      await addDoc(activityRef, {
        userId: userId,
        activity: activity,
        timestamp: serverTimestamp()
      });

      return true;
    } catch (error) {
      console.error('Error updating user activity:', error);
      throw error;
    }
  }

  // Get analytics data
  async getAnalytics(projectId = null) {
    try {
      if (projectId) {
        // Get project-specific analytics
        const analyticsRef = doc(this.db, 'analytics', projectId);
        const analyticsSnap = await getDoc(analyticsRef);
        
        if (analyticsSnap.exists()) {
          return { id: analyticsSnap.id, ...analyticsSnap.data() };
        }
        return null;
      } else {
        // Get platform-wide analytics
        const analyticsRef = collection(this.db, 'analytics');
        const snapshot = await getDocs(analyticsRef);
        
        return snapshot.docs.map(doc => ({
          id: doc.id,
          ...doc.data()
        }));
      }
    } catch (error) {
      console.error('Error getting analytics:', error);
      throw error;
    }
  }

  /**
   * Real-time Listeners
   */

  // Listen to project updates
  listenToProject(projectId, callback) {
    try {
      const projectRef = doc(this.db, 'projects', projectId);
      
      const unsubscribe = onSnapshot(projectRef, (doc) => {
        if (doc.exists()) {
          callback({ id: doc.id, ...doc.data() });
        } else {
          callback(null);
        }
      });

      this.listeners.set(`project_${projectId}`, unsubscribe);
      return unsubscribe;
    } catch (error) {
      console.error('Error listening to project:', error);
      throw error;
    }
  }

  // Listen to user's projects
  listenToUserProjects(userId, callback) {
    try {
      const projectsRef = collection(this.db, 'projects');
      const q = query(
        projectsRef,
        where('owner', '==', userId),
        orderBy('updatedAt', 'desc')
      );
      
      const unsubscribe = onSnapshot(q, (snapshot) => {
        const projects = snapshot.docs.map(doc => ({
          id: doc.id,
          ...doc.data()
        }));
        callback(projects);
      });

      this.listeners.set(`user_projects_${userId}`, unsubscribe);
      return unsubscribe;
    } catch (error) {
      console.error('Error listening to user projects:', error);
      throw error;
    }
  }

  /**
   * Utility Functions
   */

  // Clean up all active listeners
  cleanupListeners() {
    this.listeners.forEach((unsubscribe, key) => {
      try {
        unsubscribe();
        console.log(`Cleaned up listener: ${key}`);
      } catch (error) {
        console.error(`Error cleaning up listener ${key}:`, error);
      }
    });
    this.listeners.clear();
  }

  // Search projects
  async searchProjects(searchTerm, userId) {
    try {
      // Note: Firestore doesn't have full-text search built-in
      // This is a simple implementation using array-contains
      // For production, consider using Algolia or Elasticsearch
      
      const projectsRef = collection(this.db, 'projects');
      const q = query(
        projectsRef,
        where('collaborators', 'array-contains', userId),
        orderBy('updatedAt', 'desc'),
        limit(20)
      );
      
      const snapshot = await getDocs(q);
      const projects = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }));

      // Client-side filtering (not ideal for large datasets)
      if (searchTerm) {
        return projects.filter(project => 
          project.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
          project.description?.toLowerCase().includes(searchTerm.toLowerCase())
        );
      }

      return projects;
    } catch (error) {
      console.error('Error searching projects:', error);
      throw error;
    }
  }

  // Batch operations
  async batchUpdate(operations) {
    try {
      const batch = writeBatch(this.db);
      
      operations.forEach(operation => {
        const { type, ref, data } = operation;
        
        switch (type) {
          case 'set':
            batch.set(ref, data);
            break;
          case 'update':
            batch.update(ref, data);
            break;
          case 'delete':
            batch.delete(ref);
            break;
        }
      });

      await batch.commit();
      return true;
    } catch (error) {
      console.error('Error performing batch update:', error);
      throw error;
    }
  }
}

// Export singleton instance
export const dbService = new FirebaseDatabaseService();
export default dbService;