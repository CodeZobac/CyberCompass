'use client';

import { useQuery } from '@tanstack/react-query';
import type { ProfileAnalytics } from '@lib/types';

async function fetchProfileAnalytics(userId: string): Promise<ProfileAnalytics> {
  const response = await fetch(`/api/profile/analytics?userId=${userId}`);
  
  if (!response.ok) {
    throw new Error('Failed to fetch profile analytics');
  }
  
  return response.json();
}

export function useProfileAnalytics(userId: string) {
  return useQuery({
    queryKey: ['profile', 'analytics', userId],
    queryFn: () => fetchProfileAnalytics(userId),
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 3,
    retryDelay: attemptIndex => Math.min(1000 * 2 ** attemptIndex, 30000),
  });
}
