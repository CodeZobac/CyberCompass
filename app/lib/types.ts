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
