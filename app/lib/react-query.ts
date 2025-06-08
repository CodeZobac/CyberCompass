'use client';

import { QueryClient } from '@tanstack/react-query';
import { createSyncStoragePersister } from '@tanstack/query-sync-storage-persister';
import { get, set, del } from 'idb-keyval';

// Create a custom storage adapter that uses localStorage (simplified for now)
const createPersistentStorage = () => {
  if (typeof window === 'undefined') {
    // Server-side fallback
    return {
      getItem: () => null,
      setItem: () => {},
      removeItem: () => {},
    };
  }

  return {
    getItem: (key: string): string | null => {
      try {
        return localStorage.getItem(key);
      } catch {
        return null;
      }
    },
    setItem: (key: string, value: string): void => {
      try {
        localStorage.setItem(key, value);
      } catch {
        // Silently fail if storage is not available
      }
    },
    removeItem: (key: string): void => {
      try {
        localStorage.removeItem(key);
      } catch {
        // Silently fail if storage is not available
      }
    },
  };
};

// Query client configuration
export const createQueryClient = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 1000 * 60 * 5, // 5 minutes
        gcTime: 1000 * 60 * 60 * 24, // 24 hours (formerly cacheTime)
        retry: (failureCount, error: any) => {
          // Don't retry on 4xx errors
          if (error?.status >= 400 && error?.status < 500) {
            return false;
          }
          return failureCount < 3;
        },
        retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
      },
      mutations: {
        retry: 2,
        retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
      },
    },
  });

  // Set up persistence only on the client side
  if (typeof window !== 'undefined') {
    const persister = createSyncStoragePersister({
      storage: createPersistentStorage(),
      key: 'cybercompass-queries',
    });
    
    // Note: Persistence setup would be handled in the provider
    // This is just the configuration
  }

  return queryClient;
};

// Progress-specific query keys
export const progressQueryKeys = {
  all: ['progress'] as const,
  user: (userId: string) => [...progressQueryKeys.all, 'user', userId] as const,
  anonymous: (sessionId: string) => [...progressQueryKeys.all, 'anonymous', sessionId] as const,
  category: (userId: string, category: string) => 
    [...progressQueryKeys.user(userId), 'category', category] as const,
  challenge: (userId: string, challengeId: string) => 
    [...progressQueryKeys.user(userId), 'challenge', challengeId] as const,
  presence: (userId: string) => [...progressQueryKeys.all, 'presence', userId] as const,
} as const;

// Challenge-specific query keys
export const challengeQueryKeys = {
  all: ['challenges'] as const,
  lists: () => [...challengeQueryKeys.all, 'list'] as const,
  list: (filters: string) => [...challengeQueryKeys.lists(), { filters }] as const,
  details: () => [...challengeQueryKeys.all, 'detail'] as const,
  detail: (id: string) => [...challengeQueryKeys.details(), id] as const,
  category: (slug: string) => [...challengeQueryKeys.all, 'category', slug] as const,
} as const;

// Utility function to generate session ID for anonymous users
export const generateSessionId = (): string => {
  if (typeof window !== 'undefined') {
    let sessionId = localStorage.getItem('cybercompass-session-id');
    if (!sessionId) {
      sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      localStorage.setItem('cybercompass-session-id', sessionId);
    }
    return sessionId;
  }
  return `temp_${Date.now()}`;
};

// Get device ID for tracking
export const getDeviceId = (): string => {
  if (typeof window !== 'undefined') {
    let deviceId = localStorage.getItem('cybercompass-device-id');
    if (!deviceId) {
      deviceId = `device_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      localStorage.setItem('cybercompass-device-id', deviceId);
    }
    return deviceId;
  }
  return `temp_device_${Date.now()}`;
};
