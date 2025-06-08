'use client';

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';
import { progressStorage } from '@lib/storage/progress-storage';
import { 
  progressQueryKeys, 
  generateSessionId, 
  getDeviceId 
} from '@lib/react-query';
import { useEffect, useCallback } from 'react';

interface ProgressSubmission {
  challengeId: string;
  optionId: string;
  isCompleted?: boolean;
}

interface ProgressData {
  challengeId: string;
  selectedOptionId?: string;
  isCompleted: boolean;
  completedAt?: string;
  createdAt: string;
  updatedAt: string;
}

// Submit progress for authenticated users
async function submitAuthenticatedProgress(
  challengeId: string, 
  optionId: string
): Promise<any> {
  const response = await fetch('/api/challenges', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      challengeId,
      optionId,
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to submit authenticated progress');
  }

  return response.json();
}

// Submit progress for anonymous users
async function submitAnonymousProgress(
  challengeId: string, 
  optionId: string,
  sessionId: string
): Promise<any> {
  // Save to local storage immediately
  await progressStorage.saveProgress(challengeId, {
    selectedOptionId: optionId,
    isCompleted: true,
    completedAt: new Date().toISOString(),
    sessionId,
  });

  // Try to sync with server (anonymous_progress table)
  try {
    const response = await fetch('/api/progress/anonymous', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        sessionId,
        challengeId,
        optionId,
      }),
    });

    if (!response.ok) {
      // Queue for later sync if server fails
      await progressStorage.queueForSync({
        action: 'submit',
        challengeId,
        selectedOptionId: optionId,
        isCompleted: true,
        sessionId,
      });
    }

    return { isCorrect: true }; // We'll determine this client-side for anonymous users
  } catch (error) {
    // Queue for later sync if network fails
    await progressStorage.queueForSync({
      action: 'submit',
      challengeId,
      selectedOptionId: optionId,
      isCompleted: true,
      sessionId,
    });
    
    return { isCorrect: true };
  }
}

// Get progress for authenticated user
async function getAuthenticatedProgress(userId: string): Promise<ProgressData[]> {
  const response = await fetch(`/api/progress?userId=${userId}`);
  if (!response.ok) {
    throw new Error('Failed to fetch authenticated progress');
  }
  return response.json();
}

// Get progress for anonymous user
async function getAnonymousProgress(sessionId: string): Promise<ProgressData[]> {
  return await progressStorage.getAllProgress(sessionId);
}

export function useProgressPersistence() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();
  const sessionId = generateSessionId();
  const deviceId = getDeviceId();

  // Initialize storage on mount
  useEffect(() => {
    progressStorage.init();
  }, []);

  // Get appropriate user identifier
  const userId = session?.user?.id;
  const userIdentifier = userId || sessionId;

  // Query for fetching progress
  const { data: progress = [], isLoading: isLoadingProgress } = useQuery({
    queryKey: userId 
      ? progressQueryKeys.user(userId)
      : progressQueryKeys.anonymous(sessionId),
    queryFn: () => userId 
      ? getAuthenticatedProgress(userId)
      : getAnonymousProgress(sessionId),
    staleTime: 1000 * 60 * 5, // 5 minutes
    gcTime: 1000 * 60 * 30, // 30 minutes
  });

  // Mutation for submitting progress
  const submitProgress = useMutation({
    mutationFn: async ({ challengeId, optionId, isCompleted = true }: ProgressSubmission) => {
      if (userId) {
        return submitAuthenticatedProgress(challengeId, optionId);
      } else {
        return submitAnonymousProgress(challengeId, optionId, sessionId);
      }
    },
    onMutate: async (variables) => {
      // Cancel any outgoing refetches
      const queryKey = userId 
        ? progressQueryKeys.user(userId)
        : progressQueryKeys.anonymous(sessionId);
        
      await queryClient.cancelQueries({ queryKey });

      // Snapshot the previous value
      const previousProgress = queryClient.getQueryData(queryKey) as ProgressData[] || [];

      // Optimistically update cache
      const optimisticProgress: ProgressData = {
        challengeId: variables.challengeId,
        selectedOptionId: variables.optionId,
        isCompleted: variables.isCompleted || true,
        completedAt: new Date().toISOString(),
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };

      const updatedProgress = [
        ...previousProgress.filter(p => p.challengeId !== variables.challengeId),
        optimisticProgress
      ];

      queryClient.setQueryData(queryKey, updatedProgress);

      return { previousProgress };
    },
    onError: (err, variables, context) => {
      // Rollback on error
      const queryKey = userId 
        ? progressQueryKeys.user(userId)
        : progressQueryKeys.anonymous(sessionId);
        
      if (context?.previousProgress) {
        queryClient.setQueryData(queryKey, context.previousProgress);
      }
    },
    onSuccess: (data, variables) => {
      // Broadcast progress update
      broadcastProgressUpdate(variables.challengeId, data);
      
      // Invalidate related queries
      queryClient.invalidateQueries({ 
        queryKey: progressQueryKeys.all 
      });
    },
  });

  // Get progress for specific challenge
  const getProgressForChallenge = useCallback((challengeId: string): ProgressData | null => {
    return progress.find(p => p.challengeId === challengeId) || null;
  }, [progress]);

  // Check if challenge is completed
  const isChallengeCompleted = useCallback((challengeId: string): boolean => {
    const challengeProgress = getProgressForChallenge(challengeId);
    return challengeProgress?.isCompleted || false;
  }, [getProgressForChallenge]);

  // Get completion percentage for category
  const getCategoryProgress = useCallback((challengeIds: string[]): number => {
    const completedCount = challengeIds.filter(id => isChallengeCompleted(id)).length;
    return challengeIds.length > 0 ? Math.round((completedCount / challengeIds.length) * 100) : 0;
  }, [isChallengeCompleted]);

  return {
    // State
    progress,
    isLoadingProgress,
    sessionId,
    deviceId,
    isAuthenticated: !!userId,
    
    // Actions
    submitProgress,
    
    // Helpers
    getProgressForChallenge,
    isChallengeCompleted,
    getCategoryProgress,
    
    // Mutation state
    isSubmitting: submitProgress.isPending,
    submitError: submitProgress.error,
  };
}

// Broadcast progress updates to other tabs/windows
function broadcastProgressUpdate(challengeId: string, data: any) {
  if (typeof window !== 'undefined' && window.BroadcastChannel) {
    const channel = new BroadcastChannel('cybercompass-progress');
    channel.postMessage({
      type: 'PROGRESS_UPDATE',
      challengeId,
      data,
      timestamp: Date.now(),
    });
  }
}

// Hook to listen for progress updates from other tabs
export function useProgressBroadcast() {
  const queryClient = useQueryClient();

  useEffect(() => {
    if (typeof window !== 'undefined' && window.BroadcastChannel) {
      const channel = new BroadcastChannel('cybercompass-progress');
      
      channel.onmessage = (event) => {
        if (event.data.type === 'PROGRESS_UPDATE') {
          // Invalidate progress queries to refetch data
          queryClient.invalidateQueries({ 
            queryKey: progressQueryKeys.all 
          });
        }
      };

      return () => {
        channel.close();
      };
    }
  }, [queryClient]);
}
