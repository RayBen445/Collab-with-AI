/**
 * Firebase Storage Service
 * Handles all file upload and storage operations for the Collab-with-AI platform
 */

import { 
  ref,
  uploadBytes,
  uploadBytesResumable,
  getDownloadURL,
  deleteObject,
  listAll,
  getMetadata
} from 'firebase/storage';

import { storage } from './firebase-config.js';

class FirebaseStorageService {
  constructor() {
    this.storage = storage;
    this.maxFileSize = 10 * 1024 * 1024; // 10MB
    this.allowedTypes = [
      'image/jpeg',
      'image/png', 
      'image/gif',
      'image/webp',
      'application/pdf',
      'text/plain',
      'text/csv',
      'application/json',
      'application/zip',
      'audio/mpeg',
      'audio/wav',
      'video/mp4',
      'video/webm'
    ];
  }

  /**
   * Validate file before upload
   */
  validateFile(file) {
    const errors = [];

    // Check file size
    if (file.size > this.maxFileSize) {
      errors.push(`File size exceeds ${this.maxFileSize / (1024 * 1024)}MB limit`);
    }

    // Check file type
    if (!this.allowedTypes.includes(file.type)) {
      errors.push(`File type ${file.type} is not allowed`);
    }

    return {
      isValid: errors.length === 0,
      errors: errors
    };
  }

  /**
   * Upload file to user's folder
   */
  async uploadUserFile(userId, file, fileName = null) {
    try {
      // Validate file
      const validation = this.validateFile(file);
      if (!validation.isValid) {
        throw new Error(`File validation failed: ${validation.errors.join(', ')}`);
      }

      // Generate unique filename if not provided
      const finalFileName = fileName || `${Date.now()}_${file.name}`;
      
      // Create storage reference
      const storageRef = ref(this.storage, `users/${userId}/${finalFileName}`);

      // Upload file
      const snapshot = await uploadBytes(storageRef, file);
      
      // Get download URL
      const downloadURL = await getDownloadURL(snapshot.ref);

      return {
        success: true,
        fileName: finalFileName,
        downloadURL: downloadURL,
        size: file.size,
        type: file.type,
        path: snapshot.ref.fullPath
      };

    } catch (error) {
      console.error('Error uploading user file:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Upload file to project folder
   */
  async uploadProjectFile(projectId, file, fileName = null) {
    try {
      // Validate file
      const validation = this.validateFile(file);
      if (!validation.isValid) {
        throw new Error(`File validation failed: ${validation.errors.join(', ')}`);
      }

      // Generate unique filename if not provided
      const finalFileName = fileName || `${Date.now()}_${file.name}`;
      
      // Create storage reference
      const storageRef = ref(this.storage, `projects/${projectId}/${finalFileName}`);

      // Upload file
      const snapshot = await uploadBytes(storageRef, file);
      
      // Get download URL
      const downloadURL = await getDownloadURL(snapshot.ref);

      return {
        success: true,
        fileName: finalFileName,
        downloadURL: downloadURL,
        size: file.size,
        type: file.type,
        path: snapshot.ref.fullPath,
        projectId: projectId
      };

    } catch (error) {
      console.error('Error uploading project file:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Upload file with progress tracking
   */
  uploadFileWithProgress(path, file, onProgress = null) {
    return new Promise((resolve, reject) => {
      try {
        // Validate file
        const validation = this.validateFile(file);
        if (!validation.isValid) {
          reject(new Error(`File validation failed: ${validation.errors.join(', ')}`));
          return;
        }

        // Create storage reference
        const storageRef = ref(this.storage, path);

        // Create upload task
        const uploadTask = uploadBytesResumable(storageRef, file);

        // Listen for state changes, errors, and completion
        uploadTask.on('state_changed',
          (snapshot) => {
            // Progress callback
            const progress = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
            if (onProgress) {
              onProgress({
                progress: progress,
                bytesTransferred: snapshot.bytesTransferred,
                totalBytes: snapshot.totalBytes,
                state: snapshot.state
              });
            }
          },
          (error) => {
            // Error callback
            console.error('Upload error:', error);
            reject(error);
          },
          async () => {
            // Success callback
            try {
              const downloadURL = await getDownloadURL(uploadTask.snapshot.ref);
              resolve({
                success: true,
                fileName: file.name,
                downloadURL: downloadURL,
                size: file.size,
                type: file.type,
                path: uploadTask.snapshot.ref.fullPath
              });
            } catch (error) {
              reject(error);
            }
          }
        );

      } catch (error) {
        reject(error);
      }
    });
  }

  /**
   * Upload multiple files
   */
  async uploadMultipleFiles(basePath, files, onProgress = null) {
    try {
      const uploadPromises = files.map((file, index) => {
        const fileName = `${Date.now()}_${index}_${file.name}`;
        const filePath = `${basePath}/${fileName}`;
        
        return this.uploadFileWithProgress(filePath, file, (progress) => {
          if (onProgress) {
            onProgress({
              fileIndex: index,
              fileName: file.name,
              ...progress
            });
          }
        });
      });

      const results = await Promise.all(uploadPromises);
      
      return {
        success: true,
        files: results,
        totalFiles: files.length
      };

    } catch (error) {
      console.error('Error uploading multiple files:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Get file download URL
   */
  async getFileURL(path) {
    try {
      const storageRef = ref(this.storage, path);
      const downloadURL = await getDownloadURL(storageRef);
      return downloadURL;
    } catch (error) {
      console.error('Error getting file URL:', error);
      throw error;
    }
  }

  /**
   * Delete file
   */
  async deleteFile(path) {
    try {
      const storageRef = ref(this.storage, path);
      await deleteObject(storageRef);
      return {
        success: true,
        message: 'File deleted successfully'
      };
    } catch (error) {
      console.error('Error deleting file:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * List files in a directory
   */
  async listFiles(path) {
    try {
      const storageRef = ref(this.storage, path);
      const result = await listAll(storageRef);
      
      const files = await Promise.all(
        result.items.map(async (itemRef) => {
          try {
            const [downloadURL, metadata] = await Promise.all([
              getDownloadURL(itemRef),
              getMetadata(itemRef)
            ]);
            
            return {
              name: itemRef.name,
              path: itemRef.fullPath,
              downloadURL: downloadURL,
              size: metadata.size,
              contentType: metadata.contentType,
              timeCreated: metadata.timeCreated,
              updated: metadata.updated
            };
          } catch (error) {
            console.error(`Error getting file info for ${itemRef.name}:`, error);
            return {
              name: itemRef.name,
              path: itemRef.fullPath,
              error: 'Failed to get file info'
            };
          }
        })
      );

      return {
        success: true,
        files: files,
        folders: result.prefixes.map(ref => ({
          name: ref.name,
          path: ref.fullPath
        }))
      };

    } catch (error) {
      console.error('Error listing files:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Get user files
   */
  async getUserFiles(userId) {
    return this.listFiles(`users/${userId}`);
  }

  /**
   * Get project files
   */
  async getProjectFiles(projectId) {
    return this.listFiles(`projects/${projectId}`);
  }

  /**
   * Upload user avatar
   */
  async uploadUserAvatar(userId, file) {
    try {
      // Validate that it's an image
      if (!file.type.startsWith('image/')) {
        throw new Error('Avatar must be an image file');
      }

      // Check file size (limit to 2MB for avatars)
      const avatarMaxSize = 2 * 1024 * 1024; // 2MB
      if (file.size > avatarMaxSize) {
        throw new Error('Avatar file size must be less than 2MB');
      }

      const fileName = `avatar_${Date.now()}.${file.type.split('/')[1]}`;
      const result = await this.uploadUserFile(userId, file, fileName);

      if (result.success) {
        return {
          ...result,
          isAvatar: true
        };
      }

      return result;

    } catch (error) {
      console.error('Error uploading avatar:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Create shareable link with expiration
   */
  async createShareableLink(path, expirationTime = 7 * 24 * 60 * 60 * 1000) { // 7 days default
    try {
      // Note: Firebase Storage doesn't directly support expiring URLs
      // This would need to be implemented with Cloud Functions
      const downloadURL = await this.getFileURL(path);
      
      // In a real implementation, you would:
      // 1. Create a Cloud Function that generates temporary tokens
      // 2. Store the token in Firestore with expiration
      // 3. Create a custom URL that goes through your function
      
      return {
        success: true,
        shareableURL: downloadURL,
        expiresAt: new Date(Date.now() + expirationTime).toISOString(),
        message: 'Note: This is a permanent URL. Implement Cloud Functions for expiring links.'
      };

    } catch (error) {
      console.error('Error creating shareable link:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Get file metadata
   */
  async getFileMetadata(path) {
    try {
      const storageRef = ref(this.storage, path);
      const metadata = await getMetadata(storageRef);
      
      return {
        success: true,
        metadata: {
          name: metadata.name,
          bucket: metadata.bucket,
          fullPath: metadata.fullPath,
          size: metadata.size,
          contentType: metadata.contentType,
          timeCreated: metadata.timeCreated,
          updated: metadata.updated,
          md5Hash: metadata.md5Hash,
          customMetadata: metadata.customMetadata
        }
      };

    } catch (error) {
      console.error('Error getting file metadata:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Update file metadata
   */
  async updateFileMetadata(path, customMetadata) {
    try {
      const storageRef = ref(this.storage, path);
      await updateMetadata(storageRef, { customMetadata });
      
      return {
        success: true,
        message: 'Metadata updated successfully'
      };

    } catch (error) {
      console.error('Error updating file metadata:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Utility functions
   */

  // Format file size for display
  formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  // Get file icon based on type
  getFileIcon(contentType) {
    const iconMap = {
      'image/': '🖼️',
      'video/': '🎥',
      'audio/': '🎵',
      'application/pdf': '📄',
      'text/': '📝',
      'application/zip': '📦',
      'application/json': '⚙️'
    };

    for (const [type, icon] of Object.entries(iconMap)) {
      if (contentType.startsWith(type)) {
        return icon;
      }
    }

    return '📁'; // Default file icon
  }

  // Generate unique filename
  generateUniqueFileName(originalName) {
    const timestamp = Date.now();
    const random = Math.random().toString(36).substring(2, 8);
    const extension = originalName.split('.').pop();
    const nameWithoutExt = originalName.replace(`.${extension}`, '');
    
    return `${nameWithoutExt}_${timestamp}_${random}.${extension}`;
  }
}

// Export singleton instance
export const storageService = new FirebaseStorageService();
export default storageService;