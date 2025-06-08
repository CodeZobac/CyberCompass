'use client';

import { progressStorage } from '@lib/storage/progress-storage';
import { generateSessionId, getDeviceId } from '@lib/react-query';

interface SyncQueueItem {
  id: number;
  action: 'submit' | 'update' | 'delete';
  challengeId: string;
  selectedOptionId?: string;
  isCompleted: boolean;
  timestamp: number;
  retryCount: number;
  sessionId: string;
}

class OfflineSyncService {
  private isOnline: boolean = true;
  private syncInProgress: boolean = false;
  private maxRetries: number = 3;
  private retryDelay: number = 1000; // Start with 1 second
  private syncInterval: NodeJS.Timeout | null = null;

  constructor() {
    if (typeof window !== 'undefined') {
      this.isOnline = navigator.onLine;
      this.setupEventListeners();
      this.startPeriodicSync();
    }
  }

  private setupEventListeners() {
    window.addEventListener('online', () => {
      this.isOnline = true;
      console.log('Network connection restored');
      this.processSyncQueue();
    });

    window.addEventListener('offline', () => {
      this.isOnline = false;
      console.log('Network connection lost');
    });

    // Sync when page becomes visible
    document.addEventListener('visibilitychange', () => {
      if (!document.hidden && this.isOnline) {
        this.processSyncQueue();
      }
    });

    // Sync before page unload
    window.addEventListener('beforeunload', () => {
      if (this.isOnline) {
        // Use sendBeacon for reliable sync during page unload
        this.processSyncQueueBeacon();
      }
    });
  }

  private startPeriodicSync() {
    // Sync every 30 seconds when online
    this.syncInterval = setInterval(() => {
      if (this.isOnline && !this.syncInProgress) {
        this.processSyncQueue();
      }
    }, 30000);
  }

  async queueForSync(item: Omit<SyncQueueItem, 'id' | 'timestamp' | 'retryCount'>) {
    try {
      await progressStorage.queueForSync({
        ...item,
        sessionId: item.sessionId || generateSessionId(),
      });

      // Try immediate sync if online
      if (this.isOnline) {
        setTimeout(() => this.processSyncQueue(), 100);
      }
    } catch (error) {
      console.error('Error queuing for sync:', error);
    }
  }

  async processSyncQueue() {
    if (this.syncInProgress || !this.isOnline) {
      return;
    }

    this.syncInProgress = true;

    try {
      const queueItems = await progressStorage.getPendingSyncItems();
      
      if (queueItems.length === 0) {
        this.syncInProgress = false;
        return;
      }

      console.log(`Processing ${queueItems.length} queued sync items`);

      for (const item of queueItems) {
        try {
          const success = await this.syncItem(item);
          
          if (success) {
            await progressStorage.removeSyncItem(item.id);
            console.log(`Successfully synced item ${item.id}`);
          } else {
            // Increment retry count
            await progressStorage.incrementRetryCount(item.id);
            
            // Remove item if max retries exceeded
            if (item.retryCount >= this.maxRetries) {
              await progressStorage.removeSyncItem(item.id);
              console.warn(`Max retries exceeded for item ${item.id}, removing from queue`);
            }
          }
        } catch (error) {
          console.error(`Error syncing item ${item.id}:`, error);
          await progressStorage.incrementRetryCount(item.id);
        }
      }
    } catch (error) {
      console.error('Error processing sync queue:', error);
    } finally {
      this.syncInProgress = false;
    }
  }

  private async syncItem(item: SyncQueueItem): Promise<boolean> {
    try {
      const payload = {
        sessionId: item.sessionId,
        challengeId: item.challengeId,
        optionId: item.selectedOptionId,
        deviceId: getDeviceId(),
        timestamp: item.timestamp,
      };

      const response = await fetch('/api/progress/anonymous', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      return response.ok;
    } catch (error) {
      console.error('Sync request failed:', error);
      return false;
    }
  }

  private async processSyncQueueBeacon() {
    try {
      const queueItems = await progressStorage.getPendingSyncItems();
      
      if (queueItems.length === 0) return;

      // Use sendBeacon for reliable sync during page unload
      const payload = JSON.stringify({
        type: 'batch_sync',
        items: queueItems.slice(0, 5), // Limit to 5 items for beacon
        deviceId: getDeviceId(),
      });

      if (navigator.sendBeacon) {
        navigator.sendBeacon('/api/progress/sync-beacon', payload);
      }
    } catch (error) {
      console.error('Error with beacon sync:', error);
    }
  }

  // Get sync status
  async getSyncStatus() {
    try {
      const queueItems = await progressStorage.getPendingSyncItems();
      return {
        isOnline: this.isOnline,
        syncInProgress: this.syncInProgress,
        pendingItems: queueItems.length,
        lastSyncAttempt: await progressStorage.getMetadata('last_sync_attempt'),
      };
    } catch (error) {
      console.error('Error getting sync status:', error);
      return {
        isOnline: this.isOnline,
        syncInProgress: this.syncInProgress,
        pendingItems: 0,
        lastSyncAttempt: null,
      };
    }
  }

  // Force sync attempt
  async forcSync() {
    if (this.isOnline) {
      await this.processSyncQueue();
    }
  }

  // Clear sync queue (useful for cleanup)
  async clearSyncQueue() {
    try {
      const queueItems = await progressStorage.getPendingSyncItems();
      for (const item of queueItems) {
        await progressStorage.removeSyncItem(item.id);
      }
      console.log('Sync queue cleared');
    } catch (error) {
      console.error('Error clearing sync queue:', error);
    }
  }

  // Cleanup method
  destroy() {
    if (this.syncInterval) {
      clearInterval(this.syncInterval);
      this.syncInterval = null;
    }
  }
}

// Singleton instance
export const offlineSyncService = new OfflineSyncService();

// React hook for offline sync status
import { useState, useEffect } from 'react';

interface SyncStatus {
  isOnline: boolean;
  syncInProgress: boolean;
  pendingItems: number;
  lastSyncAttempt: any;
}

export function useOfflineSync() {
  const [syncStatus, setSyncStatus] = useState<SyncStatus>({
    isOnline: true,
    syncInProgress: false,
    pendingItems: 0,
    lastSyncAttempt: null,
  });

  useEffect(() => {
    const updateStatus = async () => {
      const status = await offlineSyncService.getSyncStatus();
      setSyncStatus(status);
    };

    // Initial status
    updateStatus();

    // Update status every 5 seconds
    const interval = setInterval(updateStatus, 5000);

    // Listen for online/offline events
    const handleOnline = () => updateStatus();
    const handleOffline = () => updateStatus();

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      clearInterval(interval);
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return {
    ...syncStatus,
    forceSync: () => offlineSyncService.forcSync(),
    clearQueue: () => offlineSyncService.clearSyncQueue(),
  };
}

// Network status hook
export function useNetworkStatus() {
  const [isOnline, setIsOnline] = useState(true);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      setIsOnline(navigator.onLine);

      const handleOnline = () => setIsOnline(true);
      const handleOffline = () => setIsOnline(false);

      window.addEventListener('online', handleOnline);
      window.addEventListener('offline', handleOffline);

      return () => {
        window.removeEventListener('online', handleOnline);
        window.removeEventListener('offline', handleOffline);
      };
    }
  }, []);

  return { isOnline };
}
