'use client';

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { progressStorage } from '@lib/storage/progress-storage';
import { progressQueryKeys, generateSessionId } from '@lib/react-query';

interface MigrationResult {
  migrated: number;
  conflicts: number;
  failed: number;
  details: Array<{
    challengeId: string;
    status: 'migrated' | 'conflict' | 'failed';
    reason?: string;
  }>;
}

async function migrateAnonymousProgressToUser(
  userId: string,
  sessionId: string
): Promise<MigrationResult> {
  try {
    // Get anonymous progress from local storage
    const anonymousProgress = await progressStorage.getAllProgress(sessionId);
    
    if (anonymousProgress.length === 0) {
      return {
        migrated: 0,
        conflicts: 0,
        failed: 0,
        details: [],
      };
    }

    // Send migration request to server
    const response = await fetch('/api/progress/migrate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        userId,
        sessionId,
        anonymousProgress,
      }),
    });

    if (!response.ok) {
      throw new Error('Migration request failed');
    }

    const result = await response.json();

    // Clear anonymous progress after successful migration
    if (result.migrated > 0) {
      await progressStorage.clearProgress(sessionId);
      
      // Log migration for analytics
      await progressStorage.saveMetadata('last_migration', {
        userId,
        sessionId,
        timestamp: new Date().toISOString(),
        result,
      });
    }

    return result;
  } catch (error) {
    console.error('Migration error:', error);
    throw error;
  }
}

export function useProgressMigration() {
  const queryClient = useQueryClient();

  const migrateProgress = useMutation({
    mutationFn: async (userId: string) => {
      const sessionId = generateSessionId();
      return await migrateAnonymousProgressToUser(userId, sessionId);
    },
    onSuccess: (result, userId) => {
      // Invalidate all progress queries to refetch merged data
      queryClient.invalidateQueries({ 
        queryKey: progressQueryKeys.user(userId) 
      });
      
      // Also invalidate anonymous progress
      queryClient.invalidateQueries({ 
        queryKey: progressQueryKeys.all 
      });

      // Show success notification if any progress was migrated
      if (result.migrated > 0) {
        console.log(`Successfully migrated ${result.migrated} challenge(s)`);
        
        // Broadcast migration success
        if (typeof window !== 'undefined' && window.BroadcastChannel) {
          const channel = new BroadcastChannel('cybercompass-progress');
          channel.postMessage({
            type: 'MIGRATION_SUCCESS',
            result,
            timestamp: Date.now(),
          });
        }
      }
    },
    onError: (error) => {
      console.error('Progress migration failed:', error);
    },
  });

  // Check if there's anonymous progress to migrate
  const checkForMigratableProgress = async (): Promise<boolean> => {
    try {
      const sessionId = generateSessionId();
      const anonymousProgress = await progressStorage.getAllProgress(sessionId);
      return anonymousProgress.length > 0;
    } catch {
      return false;
    }
  };

  // Get anonymous progress count
  const getAnonymousProgressCount = async (): Promise<number> => {
    try {
      const sessionId = generateSessionId();
      const anonymousProgress = await progressStorage.getAllProgress(sessionId);
      return anonymousProgress.length;
    } catch {
      return 0;
    }
  };

  return {
    migrateProgress,
    isMigrating: migrateProgress.isPending,
    migrationError: migrateProgress.error,
    migrationResult: migrateProgress.data,
    checkForMigratableProgress,
    getAnonymousProgressCount,
  };
}

// Hook to automatically trigger migration when user signs in
export function useAutoMigration() {
  const { migrateProgress, checkForMigratableProgress } = useProgressMigration();

  const triggerAutoMigration = async (userId: string) => {
    try {
      const hasMigratableProgress = await checkForMigratableProgress();
      
      if (hasMigratableProgress) {
        // Small delay to ensure user is fully authenticated
        setTimeout(() => {
          migrateProgress.mutate(userId);
        }, 1000);
      }
    } catch (error) {
      console.error('Auto-migration check failed:', error);
    }
  };

  return {
    triggerAutoMigration,
    isMigrating: migrateProgress.isPending,
  };
}
