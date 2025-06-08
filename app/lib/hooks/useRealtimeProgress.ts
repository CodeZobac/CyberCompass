'use client';

import { useEffect, useCallback } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';
import { createClient } from '@supabase/supabase-js';
import { progressQueryKeys } from '@lib/react-query';

// Initialize Supabase client
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

interface ProgressUpdate {
  id: string;
  user_id: string;
  challenge_id: string;
  is_completed: boolean;
  selected_option_id?: string;
  completed_at?: string;
  sync_status: string;
  eventType: 'INSERT' | 'UPDATE' | 'DELETE';
}

interface PresenceUpdate {
  user_id: string;
  challenge_id: string;
  last_seen: string;
  device_info?: any;
}

export function useRealtimeProgress() {
  const queryClient = useQueryClient();
  const { data: session } = useSession();
  const userId = session?.user?.id;

  // Handle progress updates
  const handleProgressUpdate = useCallback((payload: any) => {
    const update: ProgressUpdate = {
      ...payload.new,
      eventType: payload.eventType,
    };

    // Invalidate affected queries
    if (update.user_id) {
      queryClient.invalidateQueries({ 
        queryKey: progressQueryKeys.user(update.user_id) 
      });
      
      // Invalidate specific challenge progress
      queryClient.invalidateQueries({ 
        queryKey: progressQueryKeys.challenge(update.user_id, update.challenge_id) 
      });
    }

    // Show real-time notification
    showProgressNotification(update);

    // Broadcast to other tabs
    if (typeof window !== 'undefined' && window.BroadcastChannel) {
      const channel = new BroadcastChannel('cybercompass-realtime');
      channel.postMessage({
        type: 'PROGRESS_UPDATE',
        payload: update,
        timestamp: Date.now(),
      });
    }
  }, [queryClient]);

  // Handle presence updates
  const handlePresenceUpdate = useCallback((payload: any) => {
    const update: PresenceUpdate = payload.new;

    // Update presence queries
    if (update.user_id) {
      queryClient.invalidateQueries({ 
        queryKey: progressQueryKeys.presence(update.user_id) 
      });
    }

    // Show presence notification
    showPresenceNotification(update);
  }, [queryClient]);

  // Set up real-time subscriptions
  useEffect(() => {
    if (!userId) return;

    // Subscribe to user's own progress changes
    const progressChannel = supabase
      .channel(`user_progress:${userId}`)
      .on('postgres_changes', {
        event: '*',
        schema: 'public',
        table: 'user_challenge_progress',
        filter: `user_id=eq.${userId}`,
      }, handleProgressUpdate)
      .subscribe();

    // Subscribe to presence updates for collaborative features
    const presenceChannel = supabase
      .channel(`user_presence:${userId}`)
      .on('postgres_changes', {
        event: '*',
        schema: 'public',
        table: 'user_presence',
        filter: `user_id=eq.${userId}`,
      }, handlePresenceUpdate)
      .subscribe();

    // Update user presence
    updateUserPresence(userId);

    // Set up presence heartbeat
    const presenceInterval = setInterval(() => {
      updateUserPresence(userId);
    }, 30000); // Update every 30 seconds

    return () => {
      supabase.removeChannel(progressChannel);
      supabase.removeChannel(presenceChannel);
      clearInterval(presenceInterval);
    };
  }, [userId, handleProgressUpdate, handlePresenceUpdate]);

  return {
    isConnected: supabase.realtime.isConnected(),
  };
}

// Update user presence
async function updateUserPresence(userId: string) {
  try {
    const deviceInfo = {
      userAgent: typeof window !== 'undefined' ? navigator.userAgent : '',
      timestamp: Date.now(),
      url: typeof window !== 'undefined' ? window.location.href : '',
    };

    await supabase
      .from('user_presence')
      .upsert({
        user_id: userId,
        last_seen: new Date().toISOString(),
        device_info: deviceInfo,
      }, {
        onConflict: 'user_id',
      });
  } catch (error) {
    console.error('Error updating presence:', error);
  }
}

// Show progress notification
function showProgressNotification(update: ProgressUpdate) {
  // Only show notifications for other users or cross-device updates
  if (typeof window !== 'undefined' && update.eventType === 'UPDATE') {
    console.log('Progress updated:', {
      challengeId: update.challenge_id,
      completed: update.is_completed,
      syncStatus: update.sync_status,
    });

    // Could integrate with a toast notification system here
    // toast.success(`Challenge progress synced from another device`);
  }
}

// Show presence notification
function showPresenceNotification(update: PresenceUpdate) {
  console.log('User presence updated:', {
    userId: update.user_id,
    challengeId: update.challenge_id,
    lastSeen: update.last_seen,
  });
}

// Hook for collaborative progress features
export function useCollaborativeProgress(challengeId?: string) {
  const queryClient = useQueryClient();

  // Get active users for a challenge
  const getActiveUsers = useCallback(async (challenge_id: string) => {
    try {
      const fiveMinutesAgo = new Date(Date.now() - 5 * 60 * 1000).toISOString();
      
      const { data, error } = await supabase
        .from('user_presence')
        .select(`
          user_id,
          last_seen,
          device_info,
          users (
            name,
            email,
            image
          )
        `)
        .eq('challenge_id', challenge_id)
        .gte('last_seen', fiveMinutesAgo);

      if (error) throw error;
      return data || [];
    } catch (error) {
      console.error('Error fetching active users:', error);
      return [];
    }
  }, []);

  // Track user activity on challenge
  const trackChallengeActivity = useCallback(async (challenge_id: string) => {
    const { data: session } = await supabase.auth.getSession();
    if (!session?.session?.user?.id) return;

    try {
      await supabase
        .from('user_presence')
        .upsert({
          user_id: session.session.user.id,
          challenge_id: challenge_id,
          last_seen: new Date().toISOString(),
          device_info: {
            userAgent: navigator.userAgent,
            timestamp: Date.now(),
          },
        }, {
          onConflict: 'user_id,challenge_id',
        });
    } catch (error) {
      console.error('Error tracking challenge activity:', error);
    }
  }, []);

  // Set up challenge-specific real-time subscriptions
  useEffect(() => {
    if (!challengeId) return;

    const channel = supabase
      .channel(`challenge_activity:${challengeId}`)
      .on('postgres_changes', {
        event: '*',
        schema: 'public',
        table: 'user_presence',
        filter: `challenge_id=eq.${challengeId}`,
      }, (payload) => {
        // Invalidate active users query
        queryClient.invalidateQueries({ 
          queryKey: ['active_users', challengeId] 
        });
      })
      .subscribe();

    // Track initial activity
    trackChallengeActivity(challengeId);

    return () => {
      supabase.removeChannel(channel);
    };
  }, [challengeId, queryClient, trackChallengeActivity]);

  return {
    getActiveUsers,
    trackChallengeActivity,
  };
}

// Hook for listening to cross-tab real-time updates
export function useRealtimeBroadcast() {
  const queryClient = useQueryClient();

  useEffect(() => {
    if (typeof window !== 'undefined' && window.BroadcastChannel) {
      const channel = new BroadcastChannel('cybercompass-realtime');
      
      channel.onmessage = (event) => {
        const { type, payload } = event.data;
        
        switch (type) {
          case 'PROGRESS_UPDATE':
            // Invalidate relevant queries
            queryClient.invalidateQueries({ 
              queryKey: progressQueryKeys.all 
            });
            break;
          
          case 'SYNC_STATUS_CHANGE':
            // Handle sync status changes
            console.log('Sync status changed:', payload);
            break;
        }
      };

      return () => {
        channel.close();
      };
    }
  }, [queryClient]);
}
