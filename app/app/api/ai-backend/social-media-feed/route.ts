/**
 * Social Media Feed API Route
 * Generates simulated social media feed with disinformation
 */

import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { userId, locale, postCount } = body;

    // TODO: Replace with actual AI backend call
    const AI_BACKEND_URL = process.env.AI_BACKEND_URL || 'http://localhost:8000';

    const response = await fetch(`${AI_BACKEND_URL}/api/social-media/feed`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.AI_BACKEND_API_KEY}`,
      },
      body: JSON.stringify({
        user_id: userId,
        locale,
        post_count: postCount,
      }),
    });

    if (!response.ok) {
      throw new Error('AI backend request failed');
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error generating social media feed:', error);
    
    // Return mock feed for development
    return NextResponse.json({
      posts: [
        {
          id: '1',
          author: { name: 'Health News Daily', avatar: '👨‍⚕️', verified: false },
          content: 'BREAKING: New study shows miracle cure for all diseases! Doctors hate this one simple trick!',
          timestamp: '2 hours ago',
          likes: 15234,
          shares: 8932,
          comments: 456,
          isDisinformation: true,
          category: 'health',
          redFlags: ['Sensational claims', 'No credible source', 'Too good to be true'],
        },
        {
          id: '2',
          author: { name: 'Science Journal', avatar: '🔬', verified: true },
          content: 'New research published in Nature shows promising results in cancer treatment trials.',
          timestamp: '5 hours ago',
          likes: 3421,
          shares: 892,
          comments: 156,
          isDisinformation: false,
          category: 'authentic',
          redFlags: [],
        },
      ],
    });
  }
}
