/**
 * Social Media Feedback API Route
 * Analyzes user's social media simulation performance
 */

import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  let posts: any[] = [];
  let interactions: any[] = [];
  
  try {
    const body = await request.json();
    const { userId, locale } = body;
    posts = body.posts || [];
    interactions = body.interactions || [];

    // TODO: Replace with actual AI backend call
    const AI_BACKEND_URL = process.env.AI_BACKEND_URL || 'http://localhost:8000';

    const response = await fetch(`${AI_BACKEND_URL}/api/social-media/feedback`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.AI_BACKEND_API_KEY}`,
      },
      body: JSON.stringify({
        user_id: userId,
        posts,
        interactions,
        locale,
      }),
    });

    if (!response.ok) {
      throw new Error('AI backend request failed');
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error getting social media feedback:', error);
    
    // Calculate basic feedback from interactions
    const correctReports = interactions.filter(
      (i: any) => i.action === 'report' && posts.find((p: any) => p.id === i.postId)?.isDisinformation
    ).length;
    
    const missedDisinfo = posts.filter(
      (p: any) => p.isDisinformation && !interactions.find((i: any) => i.postId === p.id && i.action === 'report')
    ).length;
    
    const falseReports = interactions.filter(
      (i: any) => i.action === 'report' && !posts.find((p: any) => p.id === i.postId)?.isDisinformation
    ).length;

    return NextResponse.json({
      correctIdentifications: correctReports,
      missedDisinformation: missedDisinfo,
      falsePositives: falseReports,
      engagementImpact: 'Your engagement patterns show room for improvement. Be more cautious about sharing unverified content.',
      recommendations: [
        'Always verify sources before sharing',
        'Look for verification badges on accounts',
        'Be skeptical of sensational headlines',
        'Check multiple sources for important news',
      ],
    });
  }
}
