// Challenge-related types
export type ChallengeCategory = {
  id: string;
  name: string;
  slug: string;
  description?: string;
  created_at: string;
  updated_at: string;
};

export type ChallengeI18n = {
  id: string;
  challenge_id: string;
  locale: string;
  title: string;
  description?: string;
  created_at: string;
  updated_at: string;
};

export type ChallengeOptionI18n = {
  id: string;
  option_id: string;
  locale: string;
  content: string;
  created_at: string;
  updated_at: string;
};

export type Challenge = {
  id: string;
  category_id: string;
  title: string; // Default English title
  description?: string; // Default English description
  difficulty: number;
  order_index: number;
  created_at: string;
  updated_at: string;
  options?: ChallengeOption[];
  i18n?: {
    [key: string]: {
      title: string;
      description?: string;
    };
  };
};

export type ChallengeOption = {
  id: string;
  challenge_id: string;
  content: string; // Default English content
  is_correct: boolean;
  created_at: string;
  updated_at: string;
  i18n?: {
    [key: string]: {
      content: string;
    };
  };
};

export type UserChallengeProgress = {
  id: string;
  user_id: string;
  challenge_id: string;
  is_completed: boolean;
  selected_option_id?: string;
  completed_at?: string;
  created_at: string;
  updated_at: string;
};

// Profile Dashboard Types
export type UserAchievement = {
  id: string;
  user_id: string;
  achievement_type: 'streak' | 'category_master' | 'perfect_score' | 'speed_demon' | 'consistency' | 'milestone';
  achievement_name: string;
  achievement_description?: string;
  earned_at: string;
  metadata: Record<string, any>;
  created_at: string;
};

export type UserLearningPath = {
  id: string;
  user_id: string;
  category_id: string;
  recommended_challenges: string[];
  weakness_areas: Record<string, any>;
  improvement_score: number;
  created_at: string;
  updated_at: string;
};

export type ProgressSnapshot = {
  id: string;
  user_id: string;
  snapshot_date: string;
  total_score: number;
  category_scores: Record<string, number>;
  completion_rate: number;
  correct_answers: number;
  total_answers: number;
  streak_days: number;
  created_at: string;
};

export type ProfileAnalytics = {
  totalChallenges: number;
  completedChallenges: number;
  completionRate: number;
  averageScore: number;
  ethicalDevelopmentScore: number;
  categoryBreakdown: Array<{
    category: string;
    categoryId: string;
    completed: number;
    total: number;
    accuracy: number;
    averageDifficulty: number;
  }>;
  recentActivity: Array<{
    date: string;
    challengesCompleted: number;
    score: number;
  }>;
  achievements: UserAchievement[];
  weakAreas: Array<{
    category: string;
    accuracy: number;
    recommendedChallenges: string[];
  }>;
  streakData: {
    currentStreak: number;
    longestStreak: number;
    lastActiveDate: string;
  };
  peerComparison: {
    rank: number;
    percentile: number;
    averagePeerScore: number;
  };
};

export type ChartDataPoint = {
  name: string;
  value: number;
  date?: string;
  category?: string;
  label?: string;
};

export type ExportData = {
  userInfo: {
    name?: string;
    email?: string;
    joinDate: string;
  };
  analytics: ProfileAnalytics;
  generatedAt: string;
};
