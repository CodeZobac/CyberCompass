'use client';

import { openDB, DBSchema, IDBPDatabase } from 'idb';

// Define the database schema
interface ProgressDB extends DBSchema {
  progress: {
    key: string;
    value: {
      challengeId: string;
      selectedOptionId?: string;
      isCompleted: boolean;
      completedAt?: string;
      createdAt: string;
      updatedAt: string;
      sessionId: string;
    };
  };
  syncQueue: {
    key: number;
    value: {
      id?: number;
      action: 'submit' | 'update' | 'delete';
      challengeId: string;
      selectedOptionId?: string;
      isCompleted: boolean;
      timestamp: number;
      retryCount: number;
      sessionId: string;
    };
  };
  metadata: {
    key: string;
    value: any;
  };
}

class ProgressStorage {
  private db: IDBPDatabase<ProgressDB> | null = null;
  private dbName = 'cybercompass-progress';
  private dbVersion = 1;

  async init(): Promise<void> {
    try {
      this.db = await openDB<ProgressDB>(this.dbName, this.dbVersion, {
        upgrade(db) {
          // Create progress store
          if (!db.objectStoreNames.contains('progress')) {
            db.createObjectStore('progress', { keyPath: 'challengeId' });
          }

          // Create sync queue store
          if (!db.objectStoreNames.contains('syncQueue')) {
            db.createObjectStore('syncQueue', { 
              keyPath: 'id', 
              autoIncrement: true 
            });
          }

          // Create metadata store
          if (!db.objectStoreNames.contains('metadata')) {
            db.createObjectStore('metadata', { keyPath: 'key' });
          }
        },
      });
    } catch (error) {
      console.warn('IndexedDB not available, falling back to localStorage:', error);
    }
  }

  // Save progress with IndexedDB + localStorage fallback
  async saveProgress(challengeId: string, progressData: {
    selectedOptionId?: string;
    isCompleted: boolean;
    completedAt?: string;
    sessionId: string;
  }): Promise<void> {
    const progress = {
      challengeId,
      ...progressData,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    try {
      if (this.db) {
        await this.db.put('progress', progress);
      } else {
        throw new Error('IndexedDB not available');
      }
    } catch (error) {
      // Fallback to localStorage
      console.warn('IndexedDB failed, using localStorage:', error);
      localStorage.setItem(
        `progress_${challengeId}`,
        JSON.stringify(progress)
      );
    }
  }

  // Get progress for a specific challenge
  async getProgress(challengeId: string): Promise<any | null> {
    try {
      if (this.db) {
        return await this.db.get('progress', challengeId) || null;
      } else {
        throw new Error('IndexedDB not available');
      }
    } catch (error) {
      // Fallback to localStorage
      const stored = localStorage.getItem(`progress_${challengeId}`);
      return stored ? JSON.parse(stored) : null;
    }
  }

  // Get all progress for current session
  async getAllProgress(sessionId: string): Promise<any[]> {
    try {
      if (this.db) {
        const allProgress = await this.db.getAll('progress');
        return allProgress.filter(p => p.sessionId === sessionId);
      } else {
        throw new Error('IndexedDB not available');
      }
    } catch (error) {
      // Fallback to localStorage
      const progressItems: any[] = [];
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key?.startsWith('progress_')) {
          const stored = localStorage.getItem(key);
          if (stored) {
            const progress = JSON.parse(stored);
            if (progress.sessionId === sessionId) {
              progressItems.push(progress);
            }
          }
        }
      }
      return progressItems;
    }
  }

  // Clear all progress for current session
  async clearProgress(sessionId: string): Promise<void> {
    try {
      if (this.db) {
        const allProgress = await this.db.getAll('progress');
        const sessionProgress = allProgress.filter(p => p.sessionId === sessionId);
        
        for (const progress of sessionProgress) {
          await this.db.delete('progress', progress.challengeId);
        }
      } else {
        throw new Error('IndexedDB not available');
      }
    } catch (error) {
      // Fallback to localStorage
      const keysToRemove: string[] = [];
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key?.startsWith('progress_')) {
          const stored = localStorage.getItem(key);
          if (stored) {
            const progress = JSON.parse(stored);
            if (progress.sessionId === sessionId) {
              keysToRemove.push(key);
            }
          }
        }
      }
      
      keysToRemove.forEach(key => localStorage.removeItem(key));
    }
  }

  // Queue failed mutations for retry
  async queueForSync(mutation: {
    action: 'submit' | 'update' | 'delete';
    challengeId: string;
    selectedOptionId?: string;
    isCompleted: boolean;
    sessionId: string;
  }): Promise<void> {
    const queueItem = {
      ...mutation,
      timestamp: Date.now(),
      retryCount: 0,
    };

    try {
      if (this.db) {
        await this.db.add('syncQueue', queueItem);
      } else {
        throw new Error('IndexedDB not available');
      }
    } catch (error) {
      // Fallback to localStorage queue
      const queueKey = 'sync_queue';
      const existingQueue = localStorage.getItem(queueKey);
      const queue = existingQueue ? JSON.parse(existingQueue) : [];
      queue.push({ ...queueItem, id: Date.now() });
      localStorage.setItem(queueKey, JSON.stringify(queue));
    }
  }

  // Get pending sync items
  async getPendingSyncItems(): Promise<any[]> {
    try {
      if (this.db) {
        return await this.db.getAll('syncQueue');
      } else {
        throw new Error('IndexedDB not available');
      }
    } catch (error) {
      // Fallback to localStorage
      const stored = localStorage.getItem('sync_queue');
      return stored ? JSON.parse(stored) : [];
    }
  }

  // Remove sync item after successful sync
  async removeSyncItem(id: number): Promise<void> {
    try {
      if (this.db) {
        await this.db.delete('syncQueue', id);
      } else {
        throw new Error('IndexedDB not available');
      }
    } catch (error) {
      // Fallback to localStorage
      const stored = localStorage.getItem('sync_queue');
      if (stored) {
        const queue = JSON.parse(stored);
        const filtered = queue.filter((item: any) => item.id !== id);
        localStorage.setItem('sync_queue', JSON.stringify(filtered));
      }
    }
  }

  // Update retry count for failed sync
  async incrementRetryCount(id: number): Promise<void> {
    try {
      if (this.db) {
        const item = await this.db.get('syncQueue', id);
        if (item) {
          item.retryCount += 1;
          await this.db.put('syncQueue', item);
        }
      } else {
        throw new Error('IndexedDB not available');
      }
    } catch (error) {
      // Fallback to localStorage
      const stored = localStorage.getItem('sync_queue');
      if (stored) {
        const queue = JSON.parse(stored);
        const itemIndex = queue.findIndex((item: any) => item.id === id);
        if (itemIndex !== -1) {
          queue[itemIndex].retryCount += 1;
          localStorage.setItem('sync_queue', JSON.stringify(queue));
        }
      }
    }
  }

  // Save metadata
  async saveMetadata(key: string, value: any): Promise<void> {
    try {
      if (this.db) {
        await this.db.put('metadata', { key, value });
      } else {
        throw new Error('IndexedDB not available');
      }
    } catch (error) {
      localStorage.setItem(`metadata_${key}`, JSON.stringify(value));
    }
  }

  // Get metadata
  async getMetadata(key: string): Promise<any | null> {
    try {
      if (this.db) {
        const result = await this.db.get('metadata', key);
        return result?.value || null;
      } else {
        throw new Error('IndexedDB not available');
      }
    } catch (error) {
      const stored = localStorage.getItem(`metadata_${key}`);
      return stored ? JSON.parse(stored) : null;
    }
  }
}

// Singleton instance
export const progressStorage = new ProgressStorage();
