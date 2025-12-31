import { NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@lib/auth';
import { createClient } from '@supabase/supabase-js';
import { format, subDays, startOfDay } from 'date-fns';
import type { ProfileAnalytics } from '@lib/types';

export async function GET() {
  try {
    const session = await getServerSession(authOptions);
    
    if (!session?.user?.id) {
      return NextResponse.json(
        { error: 'Authentication required' },
        { status: 401 }
      );
    }

    const supabase = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.SUPABASE_SERVICE_ROLE_KEY!
    );

    const userId = session.user.id;

    // Fetch user progress data
    const { data: progressData, error: progressError } = await supabase
      .from('user_challenge_progress')
      .select(`
        *,
        challenges (
          id,
          title,
          difficulty,
          category_id,
          challenge_categories (
            id,
            name,
            slug
          )
        ),
        challenge_options (
          is_correct
        )
      `)
      .eq('user_id', userId);

    if (progressError) {
      console.error('Error fetching progress:', progressError);
      return NextResponse.json({ error: 'Failed to fetch progress' }, { status: 500 });
    }

    // Fetch all challenges for total count
    const { data: allChallenges, error: challengesError } = await supabase
      .from('challenges')
      .select(`
        id,
        difficulty,
        category_id,
        challenge_categories (
          id,
          name,
          slug
        )
      `);

    if (challengesError) {
      console.error('Error fetching challenges:', challengesError);
      return NextResponse.json({ error: 'Failed to fetch challenges' }, { status: 500 });
    }

    // Fetch user achievements
    const { data: achievements, error: achievementsError } = await supabase
      .from('user_achievements')
      .select('*')
      .eq('user_id', userId)
      .order('earned_at', { ascending: false });

    if (achievementsError) {
      console.error('Error fetching achievements:', achievementsError);
    }

    // Calculate analytics
    const analytics = calculateProfileAnalytics(
      progressData || [],
      allChallenges || [],
      achievements || []
    );

    return NextResponse.json(analytics);
  } catch (error) {
    console.error('Error in profile analytics API:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

function calculateProfileAnalytics(
  progressData: any[],
  allChallenges: any[],
  achievements: any[]
): ProfileAnalytics {
  const completedChallenges = progressData.filter(p => p.is_completed).length;
  const totalChallenges = allChallenges.length;
  const completionRate = totalChallenges > 0 ? (completedChallenges / totalChallenges) * 100 : 0;

  // Calculate category breakdown
  const categoryMap = new Map();
  
  // Initialize categories
  allChallenges.forEach(challenge => {
    const category = challenge.challenge_categories;
    if (category && !categoryMap.has(category.id)) {
      categoryMap.set(category.id, {
        category: category.name,
        categoryId: category.id,
        slug: category.slug,
        completed: 0,
        total: 0,
        correctAnswers: 0,
        totalAnswers: 0,
        totalDifficulty: 0,
      });
    }
  });

  // Count totals per category
  allChallenges.forEach(challenge => {
    const category = challenge.challenge_categories;
    if (category) {
      const cat = categoryMap.get(category.id);
      cat.total += 1;
      cat.totalDifficulty += challenge.difficulty || 1;
    }
  });

  // Count completed and accuracy per category
  progressData.forEach(progress => {
    const challenge = progress.challenges;
    if (challenge?.challenge_categories) {
      const cat = categoryMap.get(challenge.challenge_categories.id);
      if (cat) {
        if (progress.is_completed) {
          cat.completed += 1;
        }
        if (progress.selected_option_id && progress.challenge_options) {
          cat.totalAnswers += 1;
          if (progress.challenge_options.is_correct) {
            cat.correctAnswers += 1;
          }
        }
      }
    }
  });

  const categoryBreakdown = Array.from(categoryMap.values()).map(cat => ({
    category: cat.category,
    categoryId: cat.categoryId,
    completed: cat.completed,
    total: cat.total,
    accuracy: cat.totalAnswers > 0 ? (cat.correctAnswers / cat.totalAnswers) * 100 : 0,
    averageDifficulty: cat.total > 0 ? cat.totalDifficulty / cat.total : 1,
  }));

  // Calculate overall accuracy
  const answeredChallenges = progressData.filter(p => p.selected_option_id && p.challenge_options);
  const correctAnswers = answeredChallenges.filter(p => p.challenge_options?.is_correct).length;
  const averageScore = answeredChallenges.length > 0 ? (correctAnswers / answeredChallenges.length) * 100 : 0;

  // Calculate ethical development score (weighted by difficulty and category performance)
  const ethicalDevelopmentScore = calculateEthicalScore(categoryBreakdown, averageScore, completionRate);

  // Calculate recent activity (last 7 days)
  const recentActivity = calculateRecentActivity(progressData);

  // Identify weak areas
  const weakAreas = categoryBreakdown
    .filter(cat => cat.accuracy < 70 && cat.total > 0)
    .map(cat => ({
      category: cat.category,
      accuracy: cat.accuracy,
      recommendedChallenges: [], // This would be populated by ML recommendations
    }));

  // Calculate streak data
  const streakData = calculateStreakData(progressData);

  // Mock peer comparison (in real app, this would query anonymized data)
  const peerComparison = {
    rank: Math.floor(Math.random() * 100) + 1,
    percentile: Math.round(averageScore + Math.random() * 20 - 10),
    averagePeerScore: 65 + Math.random() * 20,
  };

  return {
    totalChallenges,
    completedChallenges,
    completionRate,
    averageScore,
    ethicalDevelopmentScore,
    categoryBreakdown,
    recentActivity,
    achievements,
    weakAreas,
    streakData,
    peerComparison,
  };
}

function calculateEthicalScore(
  categoryBreakdown: any[],
  averageScore: number,
  completionRate: number
): number {
  const categoryWeight = 0.4;
  const accuracyWeight = 0.4;
  const completionWeight = 0.2;

  // Category balance score (how well-rounded across categories)
  const categoryScores = categoryBreakdown.map(cat => cat.accuracy);
  const categoryBalance = categoryScores.length > 0 
    ? Math.min(...categoryScores) / Math.max(...categoryScores, 1) * 100
    : 0;

  const score = (
    categoryBalance * categoryWeight +
    averageScore * accuracyWeight +
    completionRate * completionWeight
  );

  return Math.round(Math.min(score, 100));
}

function calculateRecentActivity(progressData: any[]) {
  const last7Days = Array.from({ length: 7 }, (_, i) => {
    const date = startOfDay(subDays(new Date(), i));
    return {
      date: format(date, 'yyyy-MM-dd'),
      challengesCompleted: 0,
      score: 0,
    };
  }).reverse();

  progressData.forEach(progress => {
    if (progress.completed_at) {
      const completedDate = format(new Date(progress.completed_at), 'yyyy-MM-dd');
      const dayIndex = last7Days.findIndex(day => day.date === completedDate);
      if (dayIndex !== -1) {
        last7Days[dayIndex].challengesCompleted += 1;
        if (progress.challenge_options?.is_correct) {
          last7Days[dayIndex].score += 1;
        }
      }
    }
  });

  return last7Days.map(day => ({
    ...day,
    score: day.challengesCompleted > 0 ? (day.score / day.challengesCompleted) * 100 : 0,
  }));
}

function calculateStreakData(progressData: any[]) {
  const completedDates = progressData
    .filter(p => p.is_completed && p.completed_at)
    .map(p => format(startOfDay(new Date(p.completed_at)), 'yyyy-MM-dd'))
    .sort();

  const uniqueDates = [...new Set(completedDates)];
  
  let currentStreak = 0;
  let longestStreak = 0;
  let tempStreak = 0;
  
  const today = format(startOfDay(new Date()), 'yyyy-MM-dd');
  const yesterday = format(startOfDay(subDays(new Date(), 1)), 'yyyy-MM-dd');
  
  // Calculate current streak
  let checkDate = new Date();
  while (uniqueDates.includes(format(startOfDay(checkDate), 'yyyy-MM-dd'))) {
    currentStreak++;
    checkDate = subDays(checkDate, 1);
  }
  
  // If no activity today but activity yesterday, current streak is 0
  if (!uniqueDates.includes(today) && !uniqueDates.includes(yesterday)) {
    currentStreak = 0;
  }

  // Calculate longest streak
  for (let i = 0; i < uniqueDates.length; i++) {
    if (i === 0) {
      tempStreak = 1;
    } else {
      const prevDate = new Date(uniqueDates[i - 1]);
      const currDate = new Date(uniqueDates[i]);
      const diffDays = Math.round((currDate.getTime() - prevDate.getTime()) / (1000 * 60 * 60 * 24));
      
      if (diffDays === 1) {
        tempStreak++;
      } else {
        longestStreak = Math.max(longestStreak, tempStreak);
        tempStreak = 1;
      }
    }
  }
  longestStreak = Math.max(longestStreak, tempStreak);

  return {
    currentStreak,
    longestStreak,
    lastActiveDate: uniqueDates.length > 0 ? uniqueDates[uniqueDates.length - 1] : '',
  };
}
