import { supabase } from './supabase';
import { Challenge, ChallengeCategory, UserChallengeProgress } from './types';

/**
 * Get all challenge categories
 */
export async function getAllChallengeCategories(): Promise<ChallengeCategory[]> {
  const { data, error } = await supabase
    .from('challenge_categories')
    .select('*')
    .order('name');

  if (error) {
    console.error('Error fetching challenge categories:', error);
    return [];
  }

  return data || [];
}

/**
 * Get a specific challenge category by slug
 */
export async function getChallengeCategory(slug: string): Promise<ChallengeCategory | null> {
  const { data, error } = await supabase
    .from('challenge_categories')
    .select('*')
    .eq('slug', slug)
    .single();

  if (error) {
    console.error(`Error fetching challenge category with slug ${slug}:`, error);
    return null;
  }

  return data;
}

/**
 * Get all challenges for a specific category slug
 * Includes challenge options with translations
 */
export async function getChallengesByCategorySlug(slug: string, locale: string = 'en'): Promise<Challenge[]> {
  // First, get the category ID from the slug
  const category = await getChallengeCategory(slug);
  
  if (!category) {
    return [];
  }

  // Now get all challenges for this category ID with translations
  const { data: challenges, error: challengesError } = await supabase
    .from('challenges')
    .select(`
      *,
      challenges_i18n!inner (
        title,
        description,
        locale
      )
    `)
    .eq('category_id', category.id)
    .eq('challenges_i18n.locale', locale)
    .order('order_index');

  if (challengesError) {
    console.error(`Error fetching challenges for category ${slug}:`, challengesError);
    return [];
  }

  // For each challenge, fetch its options with translations
  const challengesWithOptions = await Promise.all(
    challenges.map(async (challenge) => {
      const { data: options, error: optionsError } = await supabase
        .from('challenge_options')
        .select(`
          *,
          challenge_options_i18n!inner (
            content,
            locale
          )
        `)
        .eq('challenge_id', challenge.id)
        .eq('challenge_options_i18n.locale', locale);

      if (optionsError) {
        console.error(`Error fetching options for challenge ${challenge.id}:`, optionsError);
        return { ...challenge, options: [] };
      }

      // Transform the data to match our types
      const transformedChallenge: Challenge = {
        ...challenge,
        title: challenge.challenges_i18n[0]?.title || challenge.title,
        description: challenge.challenges_i18n[0]?.description || challenge.description,
        i18n: {
          [locale]: {
            title: challenge.challenges_i18n[0]?.title || challenge.title,
            description: challenge.challenges_i18n[0]?.description || challenge.description
          }
        }
      };

      const transformedOptions = options?.map(option => ({
        ...option,
        content: option.challenge_options_i18n[0]?.content || option.content,
        i18n: {
          [locale]: {
            content: option.challenge_options_i18n[0]?.content || option.content
          }
        }
      }));

      return { ...transformedChallenge, options: transformedOptions || [] };
    })
  );

  return challengesWithOptions;
}

/**
 * Get a specific challenge by ID
 * Includes challenge options with translations
 */
export async function getChallenge(id: string, locale: string = 'en'): Promise<Challenge | null> {
  const { data: challenge, error: challengeError } = await supabase
    .from('challenges')
    .select(`
      *,
      challenges_i18n!inner (
        title,
        description,
        locale
      )
    `)
    .eq('id', id)
    .eq('challenges_i18n.locale', locale)
    .single();

  if (challengeError) {
    console.error(`Error fetching challenge with ID ${id}:`, challengeError);
    return null;
  }

  // Get challenge options with translations
  const { data: options, error: optionsError } = await supabase
    .from('challenge_options')
    .select(`
      *,
      challenge_options_i18n!inner (
        content,
        locale
      )
    `)
    .eq('challenge_id', id)
    .eq('challenge_options_i18n.locale', locale);

  if (optionsError) {
    console.error(`Error fetching options for challenge ${id}:`, optionsError);
    return challenge;
  }

  // Transform the data to match our types
  const transformedChallenge: Challenge = {
    ...challenge,
    title: challenge.challenges_i18n[0]?.title || challenge.title,
    description: challenge.challenges_i18n[0]?.description || challenge.description,
    i18n: {
      [locale]: {
        title: challenge.challenges_i18n[0]?.title || challenge.title,
        description: challenge.challenges_i18n[0]?.description || challenge.description
      }
    }
  };

  const transformedOptions = options?.map(option => ({
    ...option,
    content: option.challenge_options_i18n[0]?.content || option.content,
    i18n: {
      [locale]: {
        content: option.challenge_options_i18n[0]?.content || option.content
      }
    }
  }));

  return { ...transformedChallenge, options: transformedOptions };
}

/**
 * Record a user's progress on a challenge
 */
export async function recordChallengeProgress(
  userId: string,
  challengeId: string,
  selectedOptionId: string
): Promise<{ isCorrect: boolean; correctOptionId?: string }> {
  try {
    // Check if the selected option is correct
    const { data: selectedOption, error: optionError } = await supabase
      .from('challenge_options')
      .select('is_correct')
      .eq('id', selectedOptionId)
      .eq('challenge_id', challengeId)
      .single();

    if (optionError) {
      console.error('Error checking selected option:', optionError);
      throw new Error('Failed to check selected option');
    }

    const isCorrect = selectedOption.is_correct;

    // Get the correct option ID if the selected one is wrong
    let correctOptionId: string | undefined = undefined;
    
    if (!isCorrect) {
      const { data: correctOption, error: correctOptionError } = await supabase
        .from('challenge_options')
        .select('id')
        .eq('challenge_id', challengeId)
        .eq('is_correct', true)
        .single();

      if (correctOptionError) {
        console.error('Error fetching correct option:', correctOptionError);
      } else {
        correctOptionId = correctOption.id;
      }
    }

    // Only record progress in the database for authenticated users (not anonymous)
    if (userId !== 'anonymous') {
      // Check if user has already answered this challenge
      const { data: existingProgress, error: progressError } = await supabase
        .from('user_challenge_progress')
        .select('id')
        .eq('user_id', userId)
        .eq('challenge_id', challengeId);

      if (progressError) {
        console.error('Error checking existing progress:', progressError);
        throw new Error('Failed to check existing progress');
      }

      // Insert or update the user's progress
      if (existingProgress && existingProgress.length > 0) {
        // Update existing record
        const { error: updateError } = await supabase
          .from('user_challenge_progress')
          .update({
            selected_option_id: selectedOptionId,
            is_completed: true,
            completed_at: new Date().toISOString(),
            updated_at: new Date().toISOString()
          })
          .eq('id', existingProgress[0].id);

        if (updateError) {
          console.error('Error updating challenge progress:', updateError);
          throw new Error('Failed to update challenge progress');
        }
      } else {
        // Create new record
        const { error: insertError } = await supabase
          .from('user_challenge_progress')
          .insert({
            user_id: userId,
            challenge_id: challengeId,
            selected_option_id: selectedOptionId,
            is_completed: true,
            completed_at: new Date().toISOString()
          });

        if (insertError) {
          console.error('Error inserting challenge progress:', insertError);
          throw new Error('Failed to record challenge progress');
        }
      }
    } else {
      console.log('Anonymous user completed challenge - progress not saved to database');
    }

    return { isCorrect, correctOptionId };
  } catch (error) {
    console.error('Error recording challenge progress:', error);
    throw error;
  }
}

/**
 * Get a user's progress across all challenges
 */
export async function getUserChallengeProgress(userId: string): Promise<UserChallengeProgress[]> {
  const { data, error } = await supabase
    .from('user_challenge_progress')
    .select('*')
    .eq('user_id', userId);

  if (error) {
    console.error('Error fetching user challenge progress:', error);
    return [];
  }

  return data || [];
}

/**
 * Get a user's progress for a specific challenge
 */
export async function getUserProgressForChallenge(
  userId: string,
  challengeId: string
): Promise<UserChallengeProgress | null> {
  const { data, error } = await supabase
    .from('user_challenge_progress')
    .select('*')
    .eq('user_id', userId)
    .eq('challenge_id', challengeId)
    .single();

  if (error) {
    if (error.code === 'PGRST116') {
      // No results found, which is not really an error in this context
      return null;
    }
    console.error('Error fetching user challenge progress:', error);
    return null;
  }

  return data;
}
