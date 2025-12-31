/**
 * Analytics API Route
 * Fetches user learning analytics from AI backend
 */

import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { userId, locale } = body;

    // TODO: Replace with actual AI backend call
    const AI_BACKEND_URL = process.env.AI_BACKEND_URL || 'http://localhost:8000';

    const response = await fetch(`${AI_BACKEND_URL}/api/analytics/user`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.AI_BACKEND_API_KEY}`,
      },
      body: JSON.stringify({
        user_id: userId,
        locale,
      }),
    });

    if (!response.ok) {
      throw new Error('AI backend request failed');
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error fetching analytics:', error);
    
    // Return mock analytics for development
    return NextResponse.json({
      competencyScores: [
        { category: 'Deepfake Detection', score: 75, trend: 'up', lastUpdated: new Date().toISOString() },
        { category: 'Disinformation Awareness', score: 82, trend: 'up', lastUpdated: new Date().toISOString() },
        { category: 'Catfish Detection', score: 68, trend: 'stable', lastUpdated: new Date().toISOString() },
        { category: 'Cyberbullying Prevention', score: 90, trend: 'up', lastUpdated: new Date().toISOString() },
      ],
      achievements: [
        {
          id: '1',
          name: 'First Steps',
          description: 'Complete your first challenge',
          icon: '🎯',
          earnedAt: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
          rarity: 'common',
        },
        {
          id: '2',
          name: 'Deepfake Detective',
          description: 'Correctly identify 10 deepfakes',
          icon: '🔍',
          earnedAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
          rarity: 'rare',
        },
        {
          id: '3',
          name: 'Week Warrior',
          description: 'Maintain a 7-day streak',
          icon: '🔥',
          earnedAt: new Date().toISOString(),
          rarity: 'epic',
        },
      ],
      recommendations: [
        {
          category: 'Catfish Detection',
          priority: 'high',
          description: 'Your catfish detection skills need improvement. Focus on identifying inconsistencies in conversations.',
          suggestedChallenges: ['Advanced Catfish Scenarios', 'Red Flag Recognition', 'Profile Analysis'],
        },
        {
          category: 'Deepfake Detection',
          priority: 'medium',
          description: 'Continue practicing with more complex deepfake examples to sharpen your skills.',
          suggestedChallenges: ['Expert Deepfake Analysis', 'Audio Deepfake Detection'],
        },
      ],
      peerComparison: {
        userPercentile: 78,
        averageScore: 72,
        userScore: 79,
      },
      totalChallengesCompleted: 45,
      currentStreak: 7,
      level: 8,
      experiencePoints: 2340,
      nextLevelXP: 3000,
    });
  }
}
