// Challenge-related types
export type ChallengeCategory = {
  id: string;
  name: string;
  slug: string;
  description?: string;
  created_at: string;
  updated_at: string;
};

export type Challenge = {
  id: string;
  category_id: string;
  title: string;
  description?: string;
  difficulty: number;
  order_index: number;
  created_at: string;
  updated_at: string;
  options?: ChallengeOption[];
};

export type ChallengeOption = {
  id: string;
  challenge_id: string;
  content: string;
  is_correct: boolean;
  created_at: string;
  updated_at: string;
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