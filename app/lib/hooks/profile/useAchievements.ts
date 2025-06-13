'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import type { UserAchievement } from '@lib/types';

async function fetchAchievements(userId: string): Promise<UserAchievement[]> {
  const response = await fetch(`/api/profile/achievements?userId=${userId}`);
  
  if (!response.ok) {
    throw new Error('Failed to fetch achievements');
  }
  
  return response.json();
}

async function createAchievement(achievement: {
  achievement_type: string;
  achievement_name: string;
  achievement_description?: string;
  metadata?: Record<string, any>;
}): Promise<UserAchievement> {
  const response = await fetch('/api/profile/achievements', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(achievement),
  });
  
  if (!response.ok) {
    throw new Error('Failed to create achievement');
  }
  
  return response.json();
}

export function useAchievements(userId: string) {
  return useQuery({
    queryKey: ['profile', 'achievements', userId],
    queryFn: () => fetchAchievements(userId),
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
}

export function useCreateAchievement() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: createAchievement,
    onSuccess: () => {
      // Invalidate achievements and analytics queries
      queryClient.invalidateQueries({ queryKey: ['profile', 'achievements'] });
      queryClient.invalidateQueries({ queryKey: ['profile', 'analytics'] });
    },
  });
}

// Predefined achievement templates
export const ACHIEVEMENT_TEMPLATES = {
  FIRST_CHALLENGE: {
    achievement_type: 'milestone',
    achievement_name: 'First Steps',
    achievement_description: 'Completed your first cybersecurity challenge',
  },
  PERFECT_CATEGORY: {
    achievement_type: 'category_master',
    achievement_name: 'Category Master',
    achievement_description: 'Achieved 100% accuracy in a category',
  },
  STREAK_7: {
    achievement_type: 'streak',
    achievement_name: 'Week Warrior',
    achievement_description: 'Maintained a 7-day learning streak',
  },
  STREAK_30: {
    achievement_type: 'streak',
    achievement_name: 'Monthly Master',
    achievement_description: 'Maintained a 30-day learning streak',
  },
  SPEED_DEMON: {
    achievement_type: 'speed_demon',
    achievement_name: 'Speed Demon',
    achievement_description: 'Completed 10 challenges in one day',
  },
  COMPLETION_25: {
    achievement_type: 'milestone',
    achievement_name: 'Quarter Champion',
    achievement_description: 'Completed 25% of all challenges',
  },
  COMPLETION_50: {
    achievement_type: 'milestone',
    achievement_name: 'Halfway Hero',
    achievement_description: 'Completed 50% of all challenges',
  },
  COMPLETION_75: {
    achievement_type: 'milestone',
    achievement_name: 'Three Quarter Titan',
    achievement_description: 'Completed 75% of all challenges',
  },
  COMPLETION_100: {
    achievement_type: 'milestone',
    achievement_name: 'Cyber Guardian',
    achievement_description: 'Completed all available challenges',
  },
  CONSISTENCY: {
    achievement_type: 'consistency',
    achievement_name: 'Steady Learner',
    achievement_description: 'Completed challenges 5 days in a row',
  },
} as const;
