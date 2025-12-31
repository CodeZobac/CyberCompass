'use client';

import React from 'react';
import { useSession } from 'next-auth/react';
import { useProgressPersistence } from '@lib/hooks/useProgressPersistence';
import { useProgressMigration } from '@lib/hooks/useProgressMigration';
import { useOfflineSync, useNetworkStatus } from '@lib/services/offline-sync';
import { 
  StatusIndicator, 
  SyncSpinner, 
  OfflineIndicator,
  ConflictWarning 
} from './ui/progress-indicator';
import { Button } from './ui/button';
import { cn } from '@lib/utils';

interface GlobalSyncStatusProps {
  className?: string;
}

export function GlobalSyncStatus({ className }: GlobalSyncStatusProps) {
  const { data: session } = useSession();
  const { isOnline } = useNetworkStatus();
  const { 
    syncInProgress, 
    pendingItems, 
    forceSync, 
    clearQueue 
  } = useOfflineSync();
  
  const { 
    isSubmitting, 
    isAuthenticated,
    sessionId 
  } = useProgressPersistence();
  
  const { 
    isMigrating, 
    getAnonymousProgressCount 
  } = useProgressMigration();

  const [anonymousCount, setAnonymousCount] = React.useState(0);
  const [showDetails, setShowDetails] = React.useState(false);

  // Check for anonymous progress that can be migrated
  React.useEffect(() => {
    const checkAnonymousProgress = async () => {
      if (!isAuthenticated) {
        const count = await getAnonymousProgressCount();
        setAnonymousCount(count);
      }
    };

    checkAnonymousProgress();
  }, [isAuthenticated, getAnonymousProgressCount]);

  // Don't show if everything is normal
  const shouldShow = !isOnline || syncInProgress || pendingItems > 0 || isMigrating || 
                    isSubmitting || (anonymousCount > 0 && session?.user?.id);

  if (!shouldShow) {
    return null;
  }

  return (
    <div className={cn(
      'fixed bottom-4 right-4 z-50 max-w-sm',
      className
    )}>
      <div className="bg-white border-4 border-black rounded-sm shadow-[8px_8px_0_0_#000] p-4">
        {/* Header */}
        <div className="flex items-center justify-between mb-3">
          <h3 className="font-bold text-sm uppercase tracking-wider">
            Sync Status
          </h3>
          <button
            onClick={() => setShowDetails(!showDetails)}
            className="text-xs font-bold px-2 py-1 border border-black rounded-sm hover:bg-gray-100 transition-colors"
          >
            {showDetails ? 'Hide' : 'Details'}
          </button>
        </div>

        {/* Status Items */}
        <div className="space-y-2">
          {/* Network Status */}
          {!isOnline && (
            <div className="flex items-center gap-2">
              <OfflineIndicator />
              <span className="text-xs">You&apos;re offline. Changes will sync when online.</span>
            </div>
          )}

          {/* Migration Status */}
          {isMigrating && (
            <div className="flex items-center gap-2">
              <SyncSpinner />
              <span className="text-xs">Migrating anonymous progress to your account...</span>
            </div>
          )}

          {/* Submission Status */}
          {isSubmitting && (
            <div className="flex items-center gap-2">
              <SyncSpinner />
              <span className="text-xs">Submitting challenge response...</span>
            </div>
          )}

          {/* Sync Queue Status */}
          {syncInProgress && (
            <div className="flex items-center gap-2">
              <SyncSpinner />
              <span className="text-xs">Syncing {pendingItems} pending item(s)...</span>
            </div>
          )}

          {/* Pending Items */}
          {pendingItems > 0 && !syncInProgress && (
            <div className="flex items-center gap-2">
              <ConflictWarning />
              <span className="text-xs">{pendingItems} items waiting to sync</span>
            </div>
          )}

          {/* Anonymous Progress Alert */}
          {anonymousCount > 0 && session?.user?.id && (
            <div className="p-3 bg-blue-50 border-2 border-blue-500 rounded-sm">
              <div className="text-xs font-bold text-blue-800 mb-2">
                Found {anonymousCount} challenge(s) from before you signed in!
              </div>
              <div className="text-xs text-blue-600 mb-2">
                These will be automatically added to your account.
              </div>
            </div>
          )}
        </div>

        {/* Detailed Status */}
        {showDetails && (
          <div className="mt-4 pt-3 border-t-2 border-gray-200">
            <div className="space-y-2 text-xs">
              <div className="flex justify-between">
                <span>Connection:</span>
                <StatusIndicator 
                  status={isOnline ? 'online' : 'offline'} 
                  showText 
                />
              </div>
              
              <div className="flex justify-between">
                <span>Auth Status:</span>
                <span className="font-bold">
                  {isAuthenticated ? 'Signed In' : 'Anonymous'}
                </span>
              </div>
              
              {!isAuthenticated && (
                <div className="flex justify-between">
                  <span>Session ID:</span>
                  <span className="font-mono text-[10px]">
                    {sessionId.slice(-8)}
                  </span>
                </div>
              )}
              
              {pendingItems > 0 && (
                <div className="flex justify-between">
                  <span>Pending Sync:</span>
                  <span className="font-bold text-orange-600">
                    {pendingItems} items
                  </span>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Action Buttons */}
        {(pendingItems > 0 || !isOnline) && (
          <div className="mt-4 pt-3 border-t-2 border-gray-200 flex gap-2">
            {isOnline && pendingItems > 0 && (
              <Button
                variant="brutal"
                size="sm"
                onClick={forceSync}
                disabled={syncInProgress}
                className="text-xs"
              >
                {syncInProgress ? 'Syncing...' : 'Force Sync'}
              </Button>
            )}
            
            {pendingItems > 0 && (
              <Button
                variant="outline"
                size="sm"
                onClick={clearQueue}
                className="text-xs"
              >
                Clear Queue
              </Button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

// Compact version for header/navbar
export function CompactSyncStatus({ className }: GlobalSyncStatusProps) {
  const { isOnline } = useNetworkStatus();
  const { syncInProgress, pendingItems } = useOfflineSync();
  const { isSubmitting } = useProgressPersistence();

  if (isOnline && !syncInProgress && pendingItems === 0 && !isSubmitting) {
    return null;
  }

  return (
    <div className={cn('flex items-center gap-2', className)}>
      {!isOnline && <OfflineIndicator />}
      {(syncInProgress || isSubmitting) && <SyncSpinner />}
      {pendingItems > 0 && !syncInProgress && (
        <div className="text-xs font-bold text-orange-600">
          {pendingItems} pending
        </div>
      )}
    </div>
  );
}
